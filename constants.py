class Constants:
    #! Change the speed and range for the brawler you are using
    # go to https://pixelcrux.com/Brawl_Stars/Brawlers/ to find brawler's speed 
    speed = 2.4 # units: (tiles per second)
    range = 1 # 0 for short, 1 for medium and 2 for long range
    
    #! Do not change these
    # Windowcapture contants
    window_name = 'Bluestacks App Player'
    
    # Detector contants
    model_file_path = "model/best.onnx"
    threshold = 0.5
    classes = ["Player","Bush","Enemy"]
    heightScaleFactor = 0.154 