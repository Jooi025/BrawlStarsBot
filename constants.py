class Constants:
    #! Change the speed and range for the brawler you are using
    """
    go to https://pixelcrux.com/Brawl_Stars/Brawlers/
    to find brawler's speed and attack range
    and use hsf_finder.py to get the brawler's height scale factor
    eg. eve's speed (2.4), attack_range (9.33) and 
    height scale factor (0.158)
    """
    speed = 2.4 # units: (tiles per second)
    attack_range = 9.33 # units: (tiles per second)
    heightScaleFactor = 0.158
    
    #! Change this to suit the current map
    # map's characteristic
    # if map have a lot of walls make sharpCorner True otherwise False
    sharpCorner = False
    # if brawler spawn in the middle of the map make centerOrder False other True
    centerOrder = True
    """
    If you have multiple instance of bluestacks or you got 
    "Bluestacks App Player not found". Please change the window 
    name to name located on the top left corner of your bluestacks
    eg. Bluestacks App Player 1, Bluestacks App Player 2, etc
    """
    window_name = "Bluestacks App Player"

    #! Change this to True if you have Nvidia graphics card and TensorRT installed
    gpu = False
    #! Do not change these
    # Main contants
    DEBUG = False
    # Detector constants
    classes = ["Player","Bush","Enemy","Cubebox"]
    """
    Threshold's index correspond with classes's index.
    e.g. First element of classes is player so the first
    element of threshold is threshold for player.
    """
    threshold = [0.4,0.5,0.65,0.65]
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
