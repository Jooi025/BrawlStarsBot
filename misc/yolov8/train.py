from ultralytics import YOLO

if __name__ == '__main__':
    model = YOLO("yolov5n.pt")
    data_path = "C:\\Users\\josep\\Desktop\\yolov8\\dataset\\train_data\\data.yaml"
    model.train(data=data_path, epochs=240, device=0)