from ultralytics import YOLO

# Load custom model
model_file_path = "yolov8_model\\yolov8.pt"
model = YOLO(model_file_path)

data = "misc\\dataset\\ready.yaml"
# Export the model
model.export(format='openvino',data=data,int8=True,dynamic=True)