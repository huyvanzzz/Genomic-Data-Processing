import torch
import torchxrayvision as xrv
from PIL import Image
import torchvision.transforms as T
import numpy as np
import pandas as pd

def load_disease_severity(csv_path="../data/disease_severity.csv"):
    """Load disease severity mapping from CSV file"""
    df = pd.read_csv(csv_path)
    
    # Tạo mapping dictionary: disease -> severity info
    severity_mapping = {}
    for _, row in df.iterrows():
        severity_mapping[row['Disease']] = {
            'level': int(row['Severity_Level']),
            'name': row['Severity_Name'],
            'description': row['Description']
        }
    
    return severity_mapping


def predict_chest_xray(image_path, threshold=0.7, severity_csv="../data/disease_severity.csv"):
    """
    Dự đoán bệnh từ ảnh X-quang ngực
    Args:
        image_path: đường dẫn đến ảnh
        threshold: ngưỡng xác suất tối thiểu (mặc định 0.7)
        severity_csv: đường dẫn đến file disease_severity.csv
    """
    # 1. Load disease severity mapping
    severity_data = load_disease_severity(severity_csv)
    
    # 2. Load pretrained model trained on NIH ChestX-ray14
    model = xrv.models.DenseNet(weights="densenet121-res224-nih")
    model.eval()

    # 3. Load ảnh
    img = Image.open(image_path).convert("L")
    img = img.resize((224, 224))

    # 4. Convert to numpy float32
    img = np.array(img).astype(np.float32)

    # 5. Normalize theo chuẩn TorchXRayVision
    img = xrv.utils.normalize(img, 255, 0)   # chuẩn hóa ảnh PNG sang [0 - 1]
    img = img[np.newaxis, :, :]              # (1, 224, 224)

    # 6. Convert thành tensor
    x = torch.from_numpy(img).unsqueeze(0)   # (1, 1, 224, 224)

    # 7. Chạy model
    with torch.no_grad():
        logits = model(x)
        probs = torch.sigmoid(logits)[0]

    # 8. Lọc kết quả >= threshold và có tên
    results = []
    for name, p in zip(model.pathologies, probs):
        if name and float(p) >= threshold:
            # Lấy thông tin severity từ CSV
            severity_info = severity_data.get(name, {'level': 0, 'name': 'Không xác định', 'description': ''})
            severity_level = severity_info['level']
            severity_name = severity_info['name']
            description = severity_info['description']
            
            results.append({
                'disease': name,
                'probability': float(p),
                'severity_level': severity_level,
                'severity_name': severity_name,
                'description': description
            })
    
    # 9. Sắp xếp theo mức độ nguy hiểm (cao -> thấp), sau đó theo xác suất
    results.sort(key=lambda x: (-x['severity_level'], -x['probability']))
    
    return results


# Test với ảnh mẫu
if __name__ == "__main__":
    image_path = "../data/images/00000011_004.png"
    results = predict_chest_xray(image_path, threshold=0.65)
    print(results)