class Constants:
    #! Change the speed and range for the brawler you are using
    # go to https://pixelcrux.com/Brawl_Stars/Brawlers/ to find brawler's speed 
    speed = 2.4 # units: (tiles per second)
    range = 1 # 0 for short, 1 for medium and 2 for long range
    
    #! Change this to True if you have Nvidia graphics card and TensorRT installed
    gpu = False

    #! Do not change these
    # Windowcapture contants
    window_name = "Bluestacks App Player"
    # Detector constants
    player_threshold = 0.35
    bush_threshold = 0.35
    player_threshold = 0.35
    enemy_threshold = 0.6
    cubebox_threshold = 0.55
    classes = ["Player","Bush","Enemy","Cubebox"]
    heightScaleFactor = 0.154 
    
    if gpu is None:
        # load pytorch interface
        model_file_path = "new_model/best.pt"

    elif gpu:
        # load TensorRT interface
        model_file_path = "new_model/best.engine"
    else:
        # load ONNX interface
        model_file_path = "new_model/best.onnx"
    