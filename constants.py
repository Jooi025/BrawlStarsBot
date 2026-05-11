import json
import re
from pathlib import Path
from modules.print import bcolors

REPO_ROOT = Path(__file__).resolve().parent
with open(REPO_ROOT / "brawler_stats.json", encoding="utf-8") as stats_file:
    brawler_stats_dict = json.load(stats_file)


def normalize_brawler_name(name):
    """
    Normalize user-provided brawler names for robust lookup.
    e.g. "Mr. P", "MrP", "mr p" -> "mrp"
    """
    return re.sub(r"[^a-z0-9]+", "", name.lower().strip())

class Constants:
    #! Brawler's stats
    """
    change the brawler_name to the one you are using, if its not found,
    please manually change the speed,attack_range and heightScaleFactor below
    """
    brawler_name = "SAMPLE_NAME"
    
    """
    go to https://pixelcrux.com/Brawl_Stars/Brawlers/ to find your
    brawler's speed and attack range and use hsf_finder.py
    to get the brawler's height scale factor
    
    eg. eve's speed (2.4), attack_range (9.33) and heightScaleFactor (0.158)
    """
    speed = 2.4 # units: (tiles per second)
    attack_range = 9.33 # units: (tiles)
    heightScaleFactor = 0.158
    
    #! Map's characteristics
    """
    Change this to suit the current map
    If the map have a lots of walls make sharpCorner True otherwise make it False
    If the brawler spawn in the middle of the map make centerOrder False otherwise make it True
    """
    sharpCorner = True
    centerOrder = True

    #! Gameplay mode profile
    """
    Supported:
    - solo_showdown
    - team_3v3
    - team_5v5
    """
    game_mode = "solo_showdown"
    game_mode_profiles = {
        "solo_showdown": {
            "hide_in_bush": True,
            "centerOrder": True,
            "aggression": 1.0,
            "prediction_seconds": 0.35,
        },
        "team_3v3": {
            "hide_in_bush": False,
            "centerOrder": False,
            "aggression": 1.15,
            "prediction_seconds": 0.35,
        },
        "team_5v5": {
            "hide_in_bush": False,
            "centerOrder": False,
            "aggression": 1.2,
            "prediction_seconds": 0.4,
        },
    }

    #! Rank pushing context (manual)
    """
    This is used for rank push context/output.
    Current and target rank are intentionally manual values.
    """
    rank_push_enabled = False
    current_rank = None
    target_rank = None
    
    #! Window Capture
    """
    If you have multiple instance of bluestacks or you got
    "Bluestacks App Player not found". Please change the window
    name to name located on the top left corner of your bluestacks
    eg. Bluestacks App Player 1, Bluestacks App Player 2, etc
    """
    window_name = "Bluestacks App Player"
    # Make this False if detection_test is outputting a blank screen, otherwise True.
    focused_window = False

    #! Change this to True if you have Nvidia graphics card and CUDA installed
    nvidia_gpu = False

    # Main contants
    """
    Generate a second window with detection annotated
    """
    DEBUG = False

    #! Do not change these
    # Detector constants
    classes = ["Player","Bush","Enemy","Cubebox"]
    class_threshold = {
        "Player": 0.37,
        "Bush": 0.47,
        "Enemy": 0.57,
        "Cubebox": 0.65,
        "Teammate": 0.57,
    }
    threshold = [class_threshold.get(class_name, 0.5) for class_name in classes]

    game_mode = game_mode.lower().strip()
    if game_mode not in game_mode_profiles:
        print(bcolors.WARNING + f"Unknown game_mode '{game_mode}', defaulting to solo_showdown." + bcolors.ENDC)
        game_mode = "solo_showdown"
    selected_game_mode = game_mode_profiles[game_mode]
    centerOrder = selected_game_mode["centerOrder"]

    try:
        brawler_stats = brawler_stats_dict[normalize_brawler_name(brawler_name)]
        display_str = f"Using {brawler_name.upper()}'s stats if your selected brawler is not {brawler_name.upper()},\nplease manually modify at constants.py."
        standard_hsf = 0.15
        if len(brawler_stats) == 2:
            brawler_stats.append(standard_hsf)
        elif len(brawler_stats) > 3:
            display_str = f"{brawler_name} in brawler_stats.json has more then 3 element, using stats at constants.py"
            brawler_stats = 3*[None]
    except KeyError:
        brawler_stats = 3*[None]
        display_str = f"{brawler_name.upper()}'s stats are not found in the JSON. \nUsing speed, attack_range and heightScaleFactor in constants.py.\nPlease manually modify at constants.py if you have not."
    print("")
    print(bcolors.BOLD + bcolors.OKGREEN + "Original Creator: https://github.com/Jooi025/BrawlStarsBot" + bcolors.ENDC)
    print("")
    print(bcolors.WARNING + display_str + bcolors.ENDC)
    speed = brawler_stats[0] or speed # units: (tiles per second)
    attack_range = brawler_stats[1] or attack_range # units: (tiles per second)
    heightScaleFactor = brawler_stats[2] or heightScaleFactor
    print("")
    print(bcolors.OKBLUE + f"speed: {speed} tiles/second \nattack_range: {attack_range} tiles\nHeightScaleFactor: {heightScaleFactor}" + bcolors.ENDC)

    # interface
    if nvidia_gpu is None:
        # load TensorRT interface
        model_file_path = "yolov8_model/yolov8.engine"
        half = False
        imgsz = 640
    elif nvidia_gpu:
        # load pytorch interface
        model_file_path = "yolov8_model/yolov8.pt"
        half = False
        imgsz = (384,640)
    else:
        # load openvino interface
        model_file_path = "yolov8_model/yolov8_openvino_model"
        half = True
        imgsz = (384,640)
    #bot constant
    movement_key = "middle"
    midpoint_offset = 12
    
    float_int_dict = {
        "speed":speed,
        "attack_range":attack_range,
        "heightScaleFactor": heightScaleFactor
    }

    bool_dict = {
        "sharpCorner": sharpCorner,
        "centerOrder": centerOrder,
    }

    for key in float_int_dict:
        assert type(float_int_dict[key]) == float or type(float_int_dict[key]) == int, f"{key.upper()} should be a integer or a float"

    for key in bool_dict:
        assert type(bool_dict[key]) == bool,f"{key.upper()} should be True or False"

if __name__ == "__main__":
    pass
