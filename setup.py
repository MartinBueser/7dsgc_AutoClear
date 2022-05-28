import cv2
import queue
import numpy as np
from tkinter import *


class IterRegistry(type):
    def __iter__(cls):
        return iter(cls._registry)


class Skills(metaclass=IterRegistry):
    _registry = []

    def __init__(self, name, level, path, img, width, height, color, thickness):
        self.name = name
        self.level = level
        self.path = path
        self.img = img
        self.width = width
        self.height = height
        self.color = color
        self.thickness = thickness
        self._registry.append(self)
    threshold = .90
    result = None
    maxVal = None
    maxLoc = None
    xLoc = None
    yLoc = None
    rectangles = None
    count = 0


def init():#boss_name):
    global skillQueue
    skillQueue = queue.PriorityQueue()

    global BIRD_COMPLETION_COUNTER_SET
    BIRD_COMPLETION_COUNTER_SET = False
    global BIRD_FAILURE_COUNTER_SET
    BIRD_FAILURE_COUNTER_SET = False
    global bird_completion_counter
    bird_completion_counter = 0
    global bird_failure_counter
    bird_failure_counter = 0

    global DEER_COMPLETION_COUNTER_SET
    DEER_COMPLETION_COUNTER_SET = False
    global DEER_FAILURE_COUNTER_SET
    DEER_FAILURE_COUNTER_SET = False
    global deer_completion_counter
    deer_completion_counter = 0
    global deer_failure_counter
    deer_failure_counter = 0

    # if boss_name == "bird":
    global mag2_delay
    mag2_delay = int()
    global mat2_delay
    mat2_delay = int()
    global mat2_delay_counter
    mat2_delay_counter = 0
    # elif boss_name == "deer":
    global red_card_delay_phase2
    red_card_delay_phase2 = 0
    global green_card_delay_phase2
    green_card_delay_phase2 = 100
    global blue_card_delay_phase2
    blue_card_delay_phase2 = 100

    global red_card_delay_phase4
    red_card_delay_phase4 = 100
    global green_card_delay_phase4
    green_card_delay_phase4 = 100
    global blue_card_delay_phase4
    blue_card_delay_phase4 = 0


def setup_frame():
    ## ready frame
    global ready_frame_top
    global ready_frame_left
    global ready_frame_width
    global ready_frame_height
    global ready_frame_box
    ready_frame_top = 715
    ready_frame_left = 840
    ready_frame_width = 260
    ready_frame_height = 100
    ready_frame_box = {"top": ready_frame_top, "left": ready_frame_left, "width": ready_frame_width, "height": ready_frame_height}

    ## phase frame (top left)
    global phase_frame_top
    global phase_frame_left
    global phase_frame_width
    global phase_frame_height
    global phase_frame_box
    phase_frame_top = 130
    phase_frame_left = 70
    phase_frame_width = 110
    phase_frame_height = 50
    phase_frame_box = {"top": phase_frame_top, "left": phase_frame_left, "width": phase_frame_width, "height": phase_frame_height}

    ## skill frame (bottom right)
    global skill_frame_top
    global skill_frame_left
    global skill_frame_width
    global skill_frame_height
    global skill_frame_box
    skill_frame_top = 830
    skill_frame_left = 1150
    skill_frame_width = 700
    skill_frame_height = 200
    skill_frame_box = {"top": skill_frame_top, "left": skill_frame_left, "width": skill_frame_width, "height": skill_frame_height}

    ## ok reset frame (+set party //+start // (+skip))
    global ok_reset_frame_top
    global ok_reset_frame_left
    global ok_reset_frame_width
    global ok_reset_frame_height
    global ok_reset_frame_box
    ok_reset_frame_top = 950
    ok_reset_frame_left = 870
    ok_reset_frame_width = 180
    ok_reset_frame_height = 80
    ok_reset_frame_box = {"top": ok_reset_frame_top, "left": ok_reset_frame_left, "width": ok_reset_frame_width, "height": ok_reset_frame_height}

    ## select stage
    global select_stage_frame_top
    global select_stage_frame_left
    global select_stage_frame_width
    global select_stage_frame_height
    global select_stage_frame_box
    select_stage_frame_top = 700
    select_stage_frame_left = 890
    select_stage_frame_width = 100
    select_stage_frame_height = 100
    select_stage_frame_box = {"top": select_stage_frame_top, "left": select_stage_frame_left, "width": select_stage_frame_width, "height": select_stage_frame_height}

    ## confirm reset
    global confirm_reset_frame_top
    global confirm_reset_frame_left
    global confirm_reset_frame_width
    global confirm_reset_frame_height
    global confirm_reset_frame_box
    confirm_reset_frame_top = 590
    confirm_reset_frame_left = 970
    confirm_reset_frame_width = 160
    confirm_reset_frame_height = 60
    confirm_reset_frame_box = {"top": confirm_reset_frame_top, "left": confirm_reset_frame_left, "width": confirm_reset_frame_width, "height": confirm_reset_frame_height}

    ## save team
    global save_team_frame_top
    global save_team_frame_left
    global save_team_frame_width
    global save_team_frame_height
    global save_team_frame_box
    save_team_frame_top = 845
    save_team_frame_left = 870
    save_team_frame_width = 180
    save_team_frame_height = 80
    save_team_frame_box = {"top": save_team_frame_top, "left": save_team_frame_left, "width": save_team_frame_width, "height": save_team_frame_height}

    ## confirm team
    global confirm_team_frame_top
    global confirm_team_frame_left
    global confirm_team_frame_width
    global confirm_team_frame_height
    global confirm_team_frame_box
    confirm_team_frame_top = 650
    confirm_team_frame_left = 970
    confirm_team_frame_width = 160
    confirm_team_frame_height = 60
    confirm_team_frame_box = {"top": confirm_team_frame_top, "left": confirm_team_frame_left, "width": confirm_team_frame_width, "height": confirm_team_frame_height}

    ## use stamina potion
    global use_stamina_potion_frame_top
    global use_stamina_potion_frame_left
    global use_stamina_potion_frame_width
    global use_stamina_potion_frame_height
    global use_stamina_potion_frame_box
    use_stamina_potion_frame_top = 770
    use_stamina_potion_frame_left = 920
    use_stamina_potion_frame_width = 80
    use_stamina_potion_frame_height = 70
    use_stamina_potion_frame_box = {"top": use_stamina_potion_frame_top, "left": use_stamina_potion_frame_left, "width": use_stamina_potion_frame_width, "height": use_stamina_potion_frame_height}


def setup_menu():#boss_name):
    ## image pathes
    ready_path = "images/ready.png"
    phase1_path = "images/phase1.png"
    phase2_path = "images/phase2.png"
    phase3_path = "images/phase3.png"
    phase4_path = "images/phase4.png"
    ok_path = "images/ok.png"
    reset_path = "images/reset.png"
    set_party_path = "images/set_party.png"
    start_path = "images/start.png"
    confirm_reset_path = "images/confirm_reset.png"
    save_team_path = "images/save.png"
    confirm_team_path = "images/confirm_ok.png"
    weekly_reset_ok_path = "images/weekly_reset_ok.png"
    use_stamina_potion_path = "images/use_stamina_potion.png"
    reconnect_path = "images/reconnect.png"
    failed_ok_path = "images/failed_ok.png"

    # if boss_name == "bird":
    stage_open_bird_path = "images/stage_open_bird.png"
    stage_cleared_bird_path = "images/stage_cleared_bird.png"
    # elif boss_name == "deer":
    stage_open_deer_path = "images/stage_open_deer.png"
    stage_cleared_deer_path = "images/stage_cleared_deer.png"

    ## images
    global ready_img
    ready_img = cv2.imread(ready_path)
    global phase1_img
    phase1_img = cv2.imread(phase1_path)
    global phase2_img
    phase2_img = cv2.imread(phase2_path)
    global phase3_img
    phase3_img = cv2.imread(phase3_path)
    global phase4_img
    phase4_img = cv2.imread(phase4_path)
    global ok_img
    ok_img = cv2.imread(ok_path)
    global reset_img
    reset_img = cv2.imread(reset_path)
    global set_party_img
    set_party_img = cv2.imread(set_party_path)
    global start_img
    start_img = cv2.imread(start_path)
    global confirm_reset_img
    confirm_reset_img = cv2.imread(confirm_reset_path)
    global save_team_img
    save_team_img = cv2.imread(save_team_path)
    global confirm_team_img
    confirm_team_img = cv2.imread(confirm_team_path)
    global weekly_reset_ok_img
    weekly_reset_ok_img = cv2.imread(weekly_reset_ok_path)
    global use_stamina_potion_img
    use_stamina_potion_img = cv2.imread(use_stamina_potion_path)
    global reconnect_img
    reconnect_img = cv2.imread(reconnect_path)
    global failed_ok_img
    failed_ok_img = cv2.imread(failed_ok_path)

    global stage_open_bird_img
    stage_open_bird_img = cv2.imread(stage_open_bird_path)
    global stage_cleared_bird_img
    stage_cleared_bird_img = cv2.imread(stage_cleared_bird_path)
    global stage_open_deer_img
    stage_open_deer_img = cv2.imread(stage_open_deer_path)
    global stage_cleared_deer_img
    stage_cleared_deer_img = cv2.imread(stage_cleared_deer_path)


def setup_cards():#char_names):
    ## image pathes
    # if "brun" in char_names:
    brun1_lvl1_path = "images/brun1_lvl1.png"
    brun2_lvl1_path = "images/brun2_lvl1.png"
    brun1_lvl2_path = "images/brun1_lvl2.png"
    brun2_lvl2_path = "images/brun2_lvl2.png"
    brun1_lvl3_path = "images/brun1_lvl3.png"
    brun2_lvl3_path = "images/brun2_lvl3.png"
    brun_ult_path = "images/brun_ult.png"
    # if "mag" in char_names:
    mag1_lvl1_path = "images/mag1_lvl1.png"
    mag2_lvl1_path = "images/mag2_lvl1.png"
    mag1_lvl2_path = "images/mag1_lvl2.png"
    mag2_lvl2_path = "images/mag2_lvl2.png"
    mag1_lvl3_path = "images/mag1_lvl3.png"
    mag2_lvl3_path = "images/mag2_lvl3.png"
    mag_ult_path = "images/mag_ult.png"
    # if "mat" in char_names:
    mat1_lvl1_path = "images/mat1_lvl1.png"
    mat2_lvl1_path = "images/mat2_lvl1.png"
    mat1_lvl2_path = "images/mat1_lvl2.png"
    mat2_lvl2_path = "images/mat2_lvl2.png"
    mat1_lvl3_path = "images/mat1_lvl3.png"
    mat2_lvl3_path = "images/mat2_lvl3.png"
    mat_ult_path = "images/mat_ult.png"
    # if "gow" in char_names:
    gow1_lvl1_path = "images/gow1_lvl1.png"
    gow2_lvl1_path = "images/gow2_lvl1.png"
    gow1_lvl2_path = "images/gow1_lvl2.png"
    gow2_lvl2_path = "images/gow2_lvl2.png"
    gow1_lvl3_path = "images/gow1_lvl3.png"
    gow2_lvl3_path = "images/gow2_lvl3.png"
    gow_ult_path = "images/gow_ult.png"
    # if "mel" in char_names:
    mel1_lvl1_path = "images/mel1_lvl1.png"
    mel2_lvl1_path = "images/mel2_lvl1.png"
    mel1_lvl2_path = "images/mel1_lvl2.png"
    mel2_lvl2_path = "images/mel2_lvl2.png"
    mel1_lvl3_path = "images/mel1_lvl3.png"
    mel2_lvl3_path = "images/mel2_lvl3.png"
    mel_ult_path = "images/mel_ult.png"
    # if "jor" in char_names:
    jor1_lvl1_path = "images/jor1_lvl1.png"
    jor2_lvl1_path = "images/jor2_lvl1.png"
    jor1_lvl2_path = "images/jor1_lvl2.png"
    jor2_lvl2_path = "images/jor2_lvl2.png"
    jor1_lvl3_path = "images/jor1_lvl3.png"
    jor2_lvl3_path = "images/jor2_lvl3.png"
    jor_ult_path = "images/jor_ult.png"
    # if "skadi" in char_names:
    skadi1_lvl1_path = "images/skadi1_lvl1.png"
    skadi2_lvl1_path = "images/skadi2_lvl1.png"
    skadi1_lvl2_path = "images/skadi1_lvl2.png"
    skadi2_lvl2_path = "images/skadi2_lvl2.png"
    skadi1_lvl3_path = "images/skadi1_lvl3.png"
    skadi2_lvl3_path = "images/skadi2_lvl3.png"
    skadi_ult_path = "images/skadi_ult.png"
    # if "one" in char_names:
    one1_lvl1_path = "images/one1_lvl1.png"
    one2_lvl1_path = "images/one2_lvl1.png"
    one1_lvl2_path = "images/one1_lvl2.png"
    one2_lvl2_path = "images/one2_lvl2.png"
    one1_lvl3_path = "images/one1_lvl3.png"
    one2_lvl3_path = "images/one2_lvl3.png"
    one_ult_path = "images/one_ult.png"

    ## images
    # if "brun" in char_names:
    brun1_lvl1_img = cv2.imread(brun1_lvl1_path)
    brun2_lvl1_img = cv2.imread(brun2_lvl1_path)
    brun1_lvl2_img = cv2.imread(brun1_lvl2_path)
    brun2_lvl2_img = cv2.imread(brun2_lvl2_path)
    brun1_lvl3_img = cv2.imread(brun1_lvl3_path)
    brun2_lvl3_img = cv2.imread(brun2_lvl3_path)
    brun_ult_img = cv2.imread(brun_ult_path)
    # if "mag" in char_names:
    mag1_lvl1_img = cv2.imread(mag1_lvl1_path)
    mag2_lvl1_img = cv2.imread(mag2_lvl1_path)
    mag1_lvl2_img = cv2.imread(mag1_lvl2_path)
    mag2_lvl2_img = cv2.imread(mag2_lvl2_path)
    mag1_lvl3_img = cv2.imread(mag1_lvl3_path)
    mag2_lvl3_img = cv2.imread(mag2_lvl3_path)
    mag_ult_img = cv2.imread(mag_ult_path)
    # if "mat" in char_names:
    mat1_lvl1_img = cv2.imread(mat1_lvl1_path)
    mat2_lvl1_img = cv2.imread(mat2_lvl1_path)
    mat1_lvl2_img = cv2.imread(mat1_lvl2_path)
    mat2_lvl2_img = cv2.imread(mat2_lvl2_path)
    mat1_lvl3_img = cv2.imread(mat1_lvl3_path)
    mat2_lvl3_img = cv2.imread(mat2_lvl3_path)
    mat_ult_img = cv2.imread(mat_ult_path)
    # if "gow" in char_names:
    gow1_lvl1_img = cv2.imread(gow1_lvl1_path)
    gow2_lvl1_img = cv2.imread(gow2_lvl1_path)
    gow1_lvl2_img = cv2.imread(gow1_lvl2_path)
    gow2_lvl2_img = cv2.imread(gow2_lvl2_path)
    gow1_lvl3_img = cv2.imread(gow1_lvl3_path)
    gow2_lvl3_img = cv2.imread(gow2_lvl3_path)
    gow_ult_img = cv2.imread(gow_ult_path)
    # if "mel" in char_names:
    mel1_lvl1_img = cv2.imread(mel1_lvl1_path)
    mel2_lvl1_img = cv2.imread(mel2_lvl1_path)
    mel1_lvl2_img = cv2.imread(mel1_lvl2_path)
    mel2_lvl2_img = cv2.imread(mel2_lvl2_path)
    mel1_lvl3_img = cv2.imread(mel1_lvl3_path)
    mel2_lvl3_img = cv2.imread(mel2_lvl3_path)
    mel_ult_img = cv2.imread(mel_ult_path)
    # if "jor" in char_names:
    jor1_lvl1_img = cv2.imread(jor1_lvl1_path)
    jor2_lvl1_img = cv2.imread(jor2_lvl1_path)
    jor1_lvl2_img = cv2.imread(jor1_lvl2_path)
    jor2_lvl2_img = cv2.imread(jor2_lvl2_path)
    jor1_lvl3_img = cv2.imread(jor1_lvl3_path)
    jor2_lvl3_img = cv2.imread(jor2_lvl3_path)
    jor_ult_img = cv2.imread(jor_ult_path)
    # if "skadi" in char_names:
    skadi1_lvl1_img = cv2.imread(skadi1_lvl1_path)
    skadi2_lvl1_img = cv2.imread(skadi2_lvl1_path)
    skadi1_lvl2_img = cv2.imread(skadi1_lvl2_path)
    skadi2_lvl2_img = cv2.imread(skadi2_lvl2_path)
    skadi1_lvl3_img = cv2.imread(skadi1_lvl3_path)
    skadi2_lvl3_img = cv2.imread(skadi2_lvl3_path)
    skadi_ult_img = cv2.imread(skadi_ult_path)
    # if "one" in char_names:
    one1_lvl1_img = cv2.imread(one1_lvl1_path)
    one2_lvl1_img = cv2.imread(one2_lvl1_path)
    one1_lvl2_img = cv2.imread(one1_lvl2_path)
    one2_lvl2_img = cv2.imread(one2_lvl2_path)
    one1_lvl3_img = cv2.imread(one1_lvl3_path)
    one2_lvl3_img = cv2.imread(one2_lvl3_path)
    one_ult_img = cv2.imread(one_ult_path)

    ## skill images width and height
    # if "brun" in char_names:
    brun1_lvl1_width  = brun1_lvl1_img.shape[1]
    brun1_lvl1_height = brun1_lvl1_img.shape[0]
    brun2_lvl1_width  = brun2_lvl1_img.shape[1]
    brun2_lvl1_height = brun2_lvl1_img.shape[0]
    brun1_lvl2_width  = brun1_lvl2_img.shape[1]
    brun1_lvl2_height = brun1_lvl2_img.shape[0]
    brun2_lvl2_width  = brun2_lvl2_img.shape[1]
    brun2_lvl2_height = brun2_lvl2_img.shape[0]
    brun1_lvl3_width  = brun1_lvl3_img.shape[1]
    brun1_lvl3_height = brun1_lvl3_img.shape[0]
    brun2_lvl3_width  = brun2_lvl3_img.shape[1]
    brun2_lvl3_height = brun2_lvl3_img.shape[0]
    brun_ult_width = brun_ult_img.shape[1]
    brun_ult_height = brun_ult_img.shape[0]
    # if "mag" in char_names:
    mag1_lvl1_width  = mag1_lvl1_img.shape[1]
    mag1_lvl1_height = mag1_lvl1_img.shape[0]
    mag2_lvl1_width  = mag2_lvl1_img.shape[1]
    mag2_lvl1_height = mag2_lvl1_img.shape[0]
    mag1_lvl2_width  = mag1_lvl2_img.shape[1]
    mag1_lvl2_height = mag1_lvl2_img.shape[0]
    mag2_lvl2_width  = mag2_lvl2_img.shape[1]
    mag2_lvl2_height = mag2_lvl2_img.shape[0]
    mag1_lvl3_width  = mag1_lvl3_img.shape[1]
    mag1_lvl3_height = mag1_lvl3_img.shape[0]
    mag2_lvl3_width  = mag2_lvl3_img.shape[1]
    mag2_lvl3_height = mag2_lvl3_img.shape[0]
    mag_ult_width = mag_ult_img.shape[1]
    mag_ult_height = mag_ult_img.shape[0]
    # if "mat" in char_names:
    mat1_lvl1_width  = mat1_lvl1_img.shape[1]
    mat1_lvl1_height = mat1_lvl1_img.shape[0]
    mat2_lvl1_width  = mat2_lvl1_img.shape[1]
    mat2_lvl1_height = mat2_lvl1_img.shape[0]
    mat1_lvl2_width  = mat1_lvl2_img.shape[1]
    mat1_lvl2_height = mat1_lvl2_img.shape[0]
    mat2_lvl2_width  = mat2_lvl2_img.shape[1]
    mat2_lvl2_height = mat2_lvl2_img.shape[0]
    mat1_lvl3_width  = mat1_lvl3_img.shape[1]
    mat1_lvl3_height = mat1_lvl3_img.shape[0]
    mat2_lvl3_width  = mat2_lvl3_img.shape[1]
    mat2_lvl3_height = mat2_lvl3_img.shape[0]
    mat_ult_width = mat_ult_img.shape[1]
    mat_ult_height = mat_ult_img.shape[0]
    # if "gow" in char_names:
    gow1_lvl1_width  = gow1_lvl1_img.shape[1]
    gow1_lvl1_height = gow1_lvl1_img.shape[0]
    gow2_lvl1_width  = gow2_lvl1_img.shape[1]
    gow2_lvl1_height = gow2_lvl1_img.shape[0]
    gow1_lvl2_width  = gow1_lvl2_img.shape[1]
    gow1_lvl2_height = gow1_lvl2_img.shape[0]
    gow2_lvl2_width  = gow2_lvl2_img.shape[1]
    gow2_lvl2_height = gow2_lvl2_img.shape[0]
    gow1_lvl3_width  = gow1_lvl3_img.shape[1]
    gow1_lvl3_height = gow1_lvl3_img.shape[0]
    gow2_lvl3_width  = gow2_lvl3_img.shape[1]
    gow2_lvl3_height = gow2_lvl3_img.shape[0]
    gow_ult_width = gow_ult_img.shape[1]
    gow_ult_height = gow_ult_img.shape[0]
    # if "mel" in char_names:
    mel1_lvl1_width  = mel1_lvl1_img.shape[1]
    mel1_lvl1_height = mel1_lvl1_img.shape[0]
    mel2_lvl1_width  = mel2_lvl1_img.shape[1]
    mel2_lvl1_height = mel2_lvl1_img.shape[0]
    mel1_lvl2_width  = mel1_lvl2_img.shape[1]
    mel1_lvl2_height = mel1_lvl2_img.shape[0]
    mel2_lvl2_width  = mel2_lvl2_img.shape[1]
    mel2_lvl2_height = mel2_lvl2_img.shape[0]
    mel1_lvl3_width  = mel1_lvl3_img.shape[1]
    mel1_lvl3_height = mel1_lvl3_img.shape[0]
    mel2_lvl3_width  = mel2_lvl3_img.shape[1]
    mel2_lvl3_height = mel2_lvl3_img.shape[0]
    mel_ult_width = mel_ult_img.shape[1]
    mel_ult_height = mel_ult_img.shape[0]
    # if "jor" in char_names:
    jor1_lvl1_width = jor1_lvl1_img.shape[1]
    jor1_lvl1_height = jor1_lvl1_img.shape[0]
    jor2_lvl1_width = jor2_lvl1_img.shape[1]
    jor2_lvl1_height = jor2_lvl1_img.shape[0]
    jor1_lvl2_width = jor1_lvl2_img.shape[1]
    jor1_lvl2_height = jor1_lvl2_img.shape[0]
    jor2_lvl2_width = jor2_lvl2_img.shape[1]
    jor2_lvl2_height = jor2_lvl2_img.shape[0]
    jor1_lvl3_width = jor1_lvl3_img.shape[1]
    jor1_lvl3_height = jor1_lvl3_img.shape[0]
    jor2_lvl3_width = jor2_lvl3_img.shape[1]
    jor2_lvl3_height = jor2_lvl3_img.shape[0]
    jor_ult_width = jor_ult_img.shape[1]
    jor_ult_height = jor_ult_img.shape[0]
    # if "skadi" in char_names:
    skadi1_lvl1_width = skadi1_lvl1_img.shape[1]
    skadi1_lvl1_height = skadi1_lvl1_img.shape[0]
    skadi2_lvl1_width = skadi2_lvl1_img.shape[1]
    skadi2_lvl1_height = skadi2_lvl1_img.shape[0]
    skadi1_lvl2_width = skadi1_lvl2_img.shape[1]
    skadi1_lvl2_height = skadi1_lvl2_img.shape[0]
    skadi2_lvl2_width = skadi2_lvl2_img.shape[1]
    skadi2_lvl2_height = skadi2_lvl2_img.shape[0]
    skadi1_lvl3_width = skadi1_lvl3_img.shape[1]
    skadi1_lvl3_height = skadi1_lvl3_img.shape[0]
    skadi2_lvl3_width = skadi2_lvl3_img.shape[1]
    skadi2_lvl3_height = skadi2_lvl3_img.shape[0]
    skadi_ult_width = skadi_ult_img.shape[1]
    skadi_ult_height = skadi_ult_img.shape[0]
    # if "one" in char_names:
    one1_lvl1_width = one1_lvl1_img.shape[1]
    one1_lvl1_height = one1_lvl1_img.shape[0]
    one2_lvl1_width = one2_lvl1_img.shape[1]
    one2_lvl1_height = one2_lvl1_img.shape[0]
    one1_lvl2_width = one1_lvl2_img.shape[1]
    one1_lvl2_height = one1_lvl2_img.shape[0]
    one2_lvl2_width = one2_lvl2_img.shape[1]
    one2_lvl2_height = one2_lvl2_img.shape[0]
    one1_lvl3_width = one1_lvl3_img.shape[1]
    one1_lvl3_height = one1_lvl3_img.shape[0]
    one2_lvl3_width = one2_lvl3_img.shape[1]
    one2_lvl3_height = one2_lvl3_img.shape[0]
    one_ult_width = one_ult_img.shape[1]
    one_ult_height = one_ult_img.shape[0]

    ## skill rectangle colors
    # if "brun" in char_names:
    brun1_lvl1_color = (0, 128, 255)  # same as one
    brun2_lvl1_color = (0, 255, 255)
    brun1_lvl2_color = (0, 128, 255)
    brun2_lvl2_color = (0, 255, 255)
    brun1_lvl3_color = (0, 128, 255)
    brun2_lvl3_color = (0, 255, 255)
    brun_ult_color = (0, 0, 255)
    # if "mag" in char_names:
    mag1_lvl1_color = (255, 128, 0)  # same as mel
    mag2_lvl1_color = (255, 255, 0)
    mag1_lvl2_color = (255, 128, 0)
    mag2_lvl2_color = (255, 255, 0)
    mag1_lvl3_color = (255, 128, 0)
    mag2_lvl3_color = (255, 255, 0)
    mag_ult_color = (255, 0, 0)
    # if "mat" in char_names:
    mat1_lvl1_color = (128, 255, 128)  # same as skadi
    mat2_lvl1_color = (255, 255, 255)
    mat1_lvl2_color = (128, 255, 128)
    mat2_lvl2_color = (255, 255, 255)
    mat1_lvl3_color = (128, 255, 128)
    mat2_lvl3_color = (255, 255, 255)
    mat_ult_color = (0, 255, 0)
    # if "gow" in char_names:
    gow1_lvl1_color = (128, 0, 255)  # same as jor
    gow2_lvl1_color = (255, 0, 255)
    gow1_lvl2_color = (128, 0, 255)
    gow2_lvl2_color = (255, 0, 255)
    gow1_lvl3_color = (128, 0, 255)
    gow2_lvl3_color = (255, 0, 255)
    gow_ult_color = (0, 0, 0)
    # if "mel" in char_names:
    mel1_lvl1_color = (255, 128, 0)  # same as mag
    mel2_lvl1_color = (255, 255, 0)
    mel1_lvl2_color = (255, 128, 0)
    mel2_lvl2_color = (255, 255, 0)
    mel1_lvl3_color = (255, 128, 0)
    mel2_lvl3_color = (255, 255, 0)
    mel_ult_color = (255, 0, 0)
    # if "jor" in char_names:
    jor1_lvl1_color = (128, 0, 255)  # same as gow
    jor2_lvl1_color = (255, 0, 255)
    jor1_lvl2_color = (128, 0, 255)
    jor2_lvl2_color = (255, 0, 255)
    jor1_lvl3_color = (128, 0, 255)
    jor2_lvl3_color = (255, 0, 255)
    jor_ult_color = (0, 0, 0)
    # if "skadi" in char_names:
    skadi1_lvl1_color = (128, 255, 128)  # same as mat
    skadi2_lvl1_color = (255, 255, 255)
    skadi1_lvl2_color = (128, 255, 128)
    skadi2_lvl2_color = (255, 255, 255)
    skadi1_lvl3_color = (128, 255, 128)
    skadi2_lvl3_color = (255, 255, 255)
    skadi_ult_color = (0, 255, 0)
    # if "one" in char_names:
    one1_lvl1_color = (0, 128, 255)  # same as brun
    one2_lvl1_color = (0, 255, 255)
    one1_lvl2_color = (0, 128, 255)
    one2_lvl2_color = (0, 255, 255)
    one1_lvl3_color = (0, 128, 255)
    one2_lvl3_color = (0, 255, 255)
    one_ult_color = (0, 0, 255)

    ## skill rectangle thickness
    # if "brun" in char_names:
    brun1_lvl1_thickness = 1
    brun2_lvl1_thickness = 1
    brun1_lvl2_thickness = 5
    brun2_lvl2_thickness = 5
    brun1_lvl3_thickness = 10
    brun2_lvl3_thickness = 10
    brun_ult_thickness = 10
    # if "mag" in char_names:
    mag1_lvl1_thickness = 1
    mag2_lvl1_thickness = 1
    mag1_lvl2_thickness = 5
    mag2_lvl2_thickness = 5
    mag1_lvl3_thickness = 10
    mag2_lvl3_thickness = 10
    mag_ult_thickness = 10
    # if "mat" in char_names:
    mat1_lvl1_thickness = 1
    mat2_lvl1_thickness = 1
    mat1_lvl2_thickness = 5
    mat2_lvl2_thickness = 5
    mat1_lvl3_thickness = 10
    mat2_lvl3_thickness = 10
    mat_ult_thickness = 10
    # if "gow" in char_names:
    gow1_lvl1_thickness = 1
    gow2_lvl1_thickness = 1
    gow1_lvl2_thickness = 5
    gow2_lvl2_thickness = 5
    gow1_lvl3_thickness = 10
    gow2_lvl3_thickness = 10
    gow_ult_thickness = 10
    # if "mel" in char_names:
    mel1_lvl1_thickness = 1
    mel2_lvl1_thickness = 1
    mel1_lvl2_thickness = 5
    mel2_lvl2_thickness = 5
    mel1_lvl3_thickness = 10
    mel2_lvl3_thickness = 10
    mel_ult_thickness = 10
    # if "jor" in char_names:
    jor1_lvl1_thickness = 1
    jor2_lvl1_thickness = 1
    jor1_lvl2_thickness = 5
    jor2_lvl2_thickness = 5
    jor1_lvl3_thickness = 10
    jor2_lvl3_thickness = 10
    jor_ult_thickness = 10
    # if "skadi" in char_names:
    skadi1_lvl1_thickness = 1
    skadi2_lvl1_thickness = 1
    skadi1_lvl2_thickness = 5
    skadi2_lvl2_thickness = 5
    skadi1_lvl3_thickness = 10
    skadi2_lvl3_thickness = 10
    skadi_ult_thickness = 10
    # if "one" in char_names:
    one1_lvl1_thickness = 1
    one2_lvl1_thickness = 1
    one1_lvl2_thickness = 5
    one2_lvl2_thickness = 5
    one1_lvl3_thickness = 10
    one2_lvl3_thickness = 10
    one_ult_thickness = 10

    ## initialize skill objects
    # if "brun" in char_names:
    brun1_lvl1_Skill = Skills("brun1", 1, brun1_lvl1_path, brun1_lvl1_img, brun1_lvl1_width, brun1_lvl1_height, brun1_lvl1_color, brun1_lvl1_thickness)
    brun2_lvl1_Skill = Skills("brun2", 1, brun2_lvl1_path, brun2_lvl1_img, brun2_lvl1_width, brun2_lvl1_height, brun2_lvl1_color, brun2_lvl1_thickness)
    brun1_lvl2_Skill = Skills("brun1", 2, brun1_lvl2_path, brun1_lvl2_img, brun1_lvl2_width, brun1_lvl2_height, brun1_lvl2_color, brun1_lvl2_thickness)
    brun2_lvl2_Skill = Skills("brun2", 2, brun2_lvl2_path, brun2_lvl2_img, brun2_lvl2_width, brun2_lvl2_height, brun2_lvl2_color, brun2_lvl2_thickness)
    brun1_lvl3_Skill = Skills("brun1", 3, brun1_lvl3_path, brun1_lvl3_img, brun1_lvl3_width, brun1_lvl3_height, brun1_lvl3_color, brun1_lvl3_thickness)
    brun2_lvl3_Skill = Skills("brun2", 3, brun2_lvl3_path, brun2_lvl3_img, brun2_lvl3_width, brun2_lvl3_height, brun2_lvl3_color, brun2_lvl3_thickness)
    brun_ult_Skill = Skills("brun_ult", 3, brun_ult_path, brun_ult_img, brun_ult_width, brun_ult_height, brun_ult_color, brun_ult_thickness)
    # if "mag" in char_names:
    mag1_lvl1_Skill = Skills("mag1", 1, mag1_lvl1_path, mag1_lvl1_img, mag1_lvl1_width, mag1_lvl1_height, mag1_lvl1_color, mag1_lvl1_thickness)
    mag2_lvl1_Skill = Skills("mag2", 1, mag2_lvl1_path, mag2_lvl1_img, mag2_lvl1_width, mag2_lvl1_height, mag2_lvl1_color, mag2_lvl1_thickness)
    mag1_lvl2_Skill = Skills("mag1", 2, mag1_lvl2_path, mag1_lvl2_img, mag1_lvl2_width, mag1_lvl2_height, mag1_lvl2_color, mag1_lvl2_thickness)
    mag2_lvl2_Skill = Skills("mag2", 2, mag2_lvl2_path, mag2_lvl2_img, mag2_lvl2_width, mag2_lvl2_height, mag2_lvl2_color, mag2_lvl2_thickness)
    mag1_lvl3_Skill = Skills("mag1", 3, mag1_lvl3_path, mag1_lvl3_img, mag1_lvl3_width, mag1_lvl3_height, mag1_lvl3_color, mag1_lvl3_thickness)
    mag2_lvl3_Skill = Skills("mag2", 3, mag2_lvl3_path, mag2_lvl3_img, mag2_lvl3_width, mag2_lvl3_height, mag2_lvl3_color, mag2_lvl3_thickness)
    mag_ult_Skill = Skills("mag_ult", 3, mag_ult_path, mag_ult_img, mag_ult_width, mag_ult_height, mag_ult_color, mag_ult_thickness)
    # if "mat" in char_names:
    mat1_lvl1_Skill = Skills("mat1", 1, mat1_lvl1_path, mat1_lvl1_img, mat1_lvl1_width, mat1_lvl1_height, mat1_lvl1_color, mat1_lvl1_thickness)
    mat2_lvl1_Skill = Skills("mat2", 1, mat2_lvl1_path, mat2_lvl1_img, mat2_lvl1_width, mat2_lvl1_height, mat2_lvl1_color, mat2_lvl1_thickness)
    mat1_lvl2_Skill = Skills("mat1", 2, mat1_lvl2_path, mat1_lvl2_img, mat1_lvl2_width, mat1_lvl2_height, mat1_lvl2_color, mat1_lvl2_thickness)
    mat2_lvl2_Skill = Skills("mat2", 2, mat2_lvl2_path, mat2_lvl2_img, mat2_lvl2_width, mat2_lvl2_height, mat2_lvl2_color, mat2_lvl2_thickness)
    mat1_lvl3_Skill = Skills("mat1", 3, mat1_lvl3_path, mat1_lvl3_img, mat1_lvl3_width, mat1_lvl3_height, mat1_lvl3_color, mat1_lvl3_thickness)
    mat2_lvl3_Skill = Skills("mat2", 3, mat2_lvl3_path, mat2_lvl3_img, mat2_lvl3_width, mat2_lvl3_height, mat2_lvl3_color, mat2_lvl3_thickness)
    mat_ult_Skill = Skills("mat_ult", 3, mat_ult_path, mat_ult_img, mat_ult_width, mat_ult_height, mat_ult_color, mat_ult_thickness)
    # if "gow" in char_names:
    gow1_lvl1_Skill = Skills("gow1", 1, gow1_lvl1_path, gow1_lvl1_img, gow1_lvl1_width, gow1_lvl1_height, gow1_lvl1_color, gow1_lvl1_thickness)
    gow2_lvl1_Skill = Skills("gow2", 1, gow2_lvl1_path, gow2_lvl1_img, gow2_lvl1_width, gow2_lvl1_height, gow2_lvl1_color, gow2_lvl1_thickness)
    gow1_lvl2_Skill = Skills("gow1", 2, gow1_lvl2_path, gow1_lvl2_img, gow1_lvl2_width, gow1_lvl2_height, gow1_lvl2_color, gow1_lvl2_thickness)
    gow2_lvl2_Skill = Skills("gow2", 2, gow2_lvl2_path, gow2_lvl2_img, gow2_lvl2_width, gow2_lvl2_height, gow2_lvl2_color, gow2_lvl2_thickness)
    gow1_lvl3_Skill = Skills("gow1", 3, gow1_lvl3_path, gow1_lvl3_img, gow1_lvl3_width, gow1_lvl3_height, gow1_lvl3_color, gow1_lvl3_thickness)
    gow2_lvl3_Skill = Skills("gow2", 3, gow2_lvl3_path, gow2_lvl3_img, gow2_lvl3_width, gow2_lvl3_height, gow2_lvl3_color, gow2_lvl3_thickness)
    gow_ult_Skill = Skills("gow_ult", 3, gow_ult_path, gow_ult_img, gow_ult_width, gow_ult_height, gow_ult_color, gow_ult_thickness)
    # if "mel" in char_names:
    mel1_lvl1_Skill = Skills("mel1", 1, mel1_lvl1_path, mel1_lvl1_img, mel1_lvl1_width, mel1_lvl1_height, mel1_lvl1_color, mel1_lvl1_thickness)
    mel2_lvl1_Skill = Skills("mel2", 1, mel2_lvl1_path, mel2_lvl1_img, mel2_lvl1_width, mel2_lvl1_height, mel2_lvl1_color, mel2_lvl1_thickness)
    mel1_lvl2_Skill = Skills("mel1", 2, mel1_lvl2_path, mel1_lvl2_img, mel1_lvl2_width, mel1_lvl2_height, mel1_lvl2_color, mel1_lvl2_thickness)
    mel2_lvl2_Skill = Skills("mel2", 2, mel2_lvl2_path, mel2_lvl2_img, mel2_lvl2_width, mel2_lvl2_height, mel2_lvl2_color, mel2_lvl2_thickness)
    mel1_lvl3_Skill = Skills("mel1", 3, mel1_lvl3_path, mel1_lvl3_img, mel1_lvl3_width, mel1_lvl3_height, mel1_lvl3_color, mel1_lvl3_thickness)
    mel2_lvl3_Skill = Skills("mel2", 3, mel2_lvl3_path, mel2_lvl3_img, mel2_lvl3_width, mel2_lvl3_height, mel2_lvl3_color, mel2_lvl3_thickness)
    mel_ult_Skill = Skills("mel_ult", 3, mel_ult_path, mel_ult_img, mel_ult_width, mel_ult_height, mel_ult_color, mel_ult_thickness)
    # if "jor" in char_names:
    jor1_lvl1_Skill = Skills("jor1", 1, jor1_lvl1_path, jor1_lvl1_img, jor1_lvl1_width, jor1_lvl1_height, jor1_lvl1_color, jor1_lvl1_thickness)
    jor2_lvl1_Skill = Skills("jor2", 1, jor2_lvl1_path, jor2_lvl1_img, jor2_lvl1_width, jor2_lvl1_height, jor2_lvl1_color, jor2_lvl1_thickness)
    jor1_lvl2_Skill = Skills("jor1", 2, jor1_lvl2_path, jor1_lvl2_img, jor1_lvl2_width, jor1_lvl2_height, jor1_lvl2_color, jor1_lvl2_thickness)
    jor2_lvl2_Skill = Skills("jor2", 2, jor2_lvl2_path, jor2_lvl2_img, jor2_lvl2_width, jor2_lvl2_height, jor2_lvl2_color, jor2_lvl2_thickness)
    jor1_lvl3_Skill = Skills("jor1", 3, jor1_lvl3_path, jor1_lvl3_img, jor1_lvl3_width, jor1_lvl3_height, jor1_lvl3_color, jor1_lvl3_thickness)
    jor2_lvl3_Skill = Skills("jor2", 3, jor2_lvl3_path, jor2_lvl3_img, jor2_lvl3_width, jor2_lvl3_height, jor2_lvl3_color, jor2_lvl3_thickness)
    jor_ult_Skill = Skills("jor_ult", 3, jor_ult_path, jor_ult_img, jor_ult_width, jor_ult_height, jor_ult_color, jor_ult_thickness)
    # if "skadi" in char_names:
    skadi1_lvl1_Skill = Skills("skadi1", 1, skadi1_lvl1_path, skadi1_lvl1_img, skadi1_lvl1_width, skadi1_lvl1_height, skadi1_lvl1_color, skadi1_lvl1_thickness)
    skadi2_lvl1_Skill = Skills("skadi2", 1, skadi2_lvl1_path, skadi2_lvl1_img, skadi2_lvl1_width, skadi2_lvl1_height, skadi2_lvl1_color, skadi2_lvl1_thickness)
    skadi1_lvl2_Skill = Skills("skadi1", 2, skadi1_lvl2_path, skadi1_lvl2_img, skadi1_lvl2_width, skadi1_lvl2_height, skadi1_lvl2_color, skadi1_lvl2_thickness)
    skadi2_lvl2_Skill = Skills("skadi2", 2, skadi2_lvl2_path, skadi2_lvl2_img, skadi2_lvl2_width, skadi2_lvl2_height, skadi2_lvl2_color, skadi2_lvl2_thickness)
    skadi1_lvl3_Skill = Skills("skadi1", 3, skadi1_lvl3_path, skadi1_lvl3_img, skadi1_lvl3_width, skadi1_lvl3_height, skadi1_lvl3_color, skadi1_lvl3_thickness)
    skadi2_lvl3_Skill = Skills("skadi2", 3, skadi2_lvl3_path, skadi2_lvl3_img, skadi2_lvl3_width, skadi2_lvl3_height, skadi2_lvl3_color, skadi2_lvl3_thickness)
    skadi_ult_Skill = Skills("skadi_ult", 3, skadi_ult_path, skadi_ult_img, skadi_ult_width, skadi_ult_height, skadi_ult_color, skadi_ult_thickness)
    # if "one" in char_names:
    one1_lvl1_Skill = Skills("one1", 1, one1_lvl1_path, one1_lvl1_img, one1_lvl1_width, one1_lvl1_height, one1_lvl1_color, one1_lvl1_thickness)
    one2_lvl1_Skill = Skills("one2", 1, one2_lvl1_path, one2_lvl1_img, one2_lvl1_width, one2_lvl1_height, one2_lvl1_color, one2_lvl1_thickness)
    one1_lvl2_Skill = Skills("one1", 2, one1_lvl2_path, one1_lvl2_img, one1_lvl2_width, one1_lvl2_height, one1_lvl2_color, one1_lvl2_thickness)
    one2_lvl2_Skill = Skills("one2", 2, one2_lvl2_path, one2_lvl2_img, one2_lvl2_width, one2_lvl2_height, one2_lvl2_color, one2_lvl2_thickness)
    one1_lvl3_Skill = Skills("one1", 3, one1_lvl3_path, one1_lvl3_img, one1_lvl3_width, one1_lvl3_height, one1_lvl3_color, one1_lvl3_thickness)
    one2_lvl3_Skill = Skills("one2", 3, one2_lvl3_path, one2_lvl3_img, one2_lvl3_width, one2_lvl3_height, one2_lvl3_color, one2_lvl3_thickness)
    one_ult_Skill = Skills("one_ult", 3, one_ult_path, one_ult_img, one_ult_width, one_ult_height, one_ult_color, one_ult_thickness)

    for p in Skills:
        if p.name == "brun1":
            p.threshold = 0.9
        elif p.name == "brun2":
            p.threshold = 0.9
        elif p.name == "brun_ult":
            p.threshold = 0.9
        elif p.name == "mag1":
            p.threshold = 0.9
        elif p.name == "mag2":
            p.threshold = 0.9
        elif p.name == "mag_ult":
            p.threshold = 0.9
        elif p.name == "mat1":
            p.threshold = 0.85
        elif p.name == "mat2":
            p.threshold = 0.8
        elif p.name == "mat_ult":
            p.threshold = 0.9
        elif p.name == "gow1":
            p.threshold = 0.9
        elif p.name == "gow2":
            p.threshold = 0.85
        elif p.name == "gow_ult":
            p.threshold = 0.9
        elif p.name == "mel1":
            p.threshold = 0.93
        elif p.name == "mel2":
            p.threshold = 0.9
        elif p.name == "mel_ult":
            p.threshold = 0.9
        elif p.name == "jor1":
            p.threshold = 0.93
        elif p.name == "jor2":
            p.threshold = 0.9
        elif p.name == "jor_ult":
            p.threshold = 0.85
        elif p.name == "skadi1":
            p.threshold = 0.93
        elif p.name == "skadi2":
            p.threshold = 0.9
        elif p.name == "skadi_ult":
            p.threshold = 0.9
        elif p.name == "one1":
            p.threshold = 0.9
        elif p.name == "one2":
            p.threshold = 0.9
        elif p.name == "one_ult":
            p.threshold = 0.9
