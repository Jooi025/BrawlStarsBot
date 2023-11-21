class Constants:
    #! Change the speed and range for the brawler you are using
    # go to https://pixelcrux.com/Brawl_Stars/Brawlers/ to find brawler's speed 
    speed = 2.4 # units: (tiles per second)
    range = 1 # 0 for short, 1 for medium and 2 for long range
    
    #! Change this to suit the current map
    # map's characteristic
    # if map have a lot of walls make sharpCorner True otherwise False
    sharpCorner = False
    # if brawler spawn in the middle of the map make centerOrder False other True
    centerOrder = True
    
    #! Change this to True if you have Nvidia graphics card and TensorRT installed
    gpu = False
    #! Do not change these
    # Main contants
    DEBUG = False
    # Windowcapture contants
    window_name = "Bluestacks App Player"
    # Detector constants
    classes = ["Player","Bush","Enemy","Cubebox"]
    """
    Threshold's index correspond with classes's index.
    e.g. First element of classes is player so the first
    element of threshold is threshold for player.
    """
    threshold = [0.45,0.5,0.65,0.65]
    heightScaleFactor = 0.154
    # interface
    if gpu is None:
        # load pytorch interface
        model_file_path = "yolov8_model/yolov8.pt"
        half = False
        imgsz = (384,640)
    elif gpu:
        # load TensorRT interface
        model_file_path = "yolov8_model/yolov8.engine"
        half = False
        imgsz = 640
    else:
        # load ONNX interface
        model_file_path = "yolov8_model/yolov8_openvino_model"
        half = True
        imgsz = (384,640)
    #bot constant
    movement_key = "middle"
