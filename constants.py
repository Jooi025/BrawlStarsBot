class Constants:
    #! Change the speed and range for the brawler you are using
    # go to https://pixelcrux.com/Brawl_Stars/Brawlers/
    # to find brawler's speed and attack range
    # eg. eve's speed (2.4) and attack_range (9.33)
    speed = 2.4 # units: (tiles per second)
    attack_range = 9.33 # units: (tiles per second)
    # use hsf_finder.py to get the brawler's height scale factor
    heightScaleFactor = 0.154
    
    #! Change this to suit the current map
    # map's characteristic
    # if map have a lot of walls make sharpCorner True otherwise False
    sharpCorner = True
    # if brawler spawn in the middle of the map make centerOrder False other True
    centerOrder = True
    
    #! Change this to True if you have Nvidia graphics card and TensorRT installed
    gpu = True
    #! Do not change these
    # Main contants
    DEBUG = 1
    # Windowcapture contants
    window_name = "Bluestacks App Player"
    # Detector constants
    classes = ["Player","Bush","Enemy","Cubebox"]
    """
    Threshold's index correspond with classes's index.
    e.g. First element of classes is player so the first
    element of threshold is threshold for player.
    """
    threshold = [0.43,0.5,0.65,0.65]
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
    midpoint_offset = 12
