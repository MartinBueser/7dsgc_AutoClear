from setup import *
import setup
from functions import *
from bird_functions import *
from tkinter_gui import *

import cv2
import numpy as np
import pyautogui as pg
import time
import keyboard
from mss import mss


setup.init()
setup_frame()
setup_death_match()
# setup_daily_menu()
# setup_daily_states()
setup_demonic_beast_battle_menu()
setup_cards()
GUI()


## screenshot of display
setup.sct = mss()


while setup.RUN_LOOP:
    setup.current_time = time.time()

    setup.skill_frame = cv2.cvtColor(np.array(setup.sct.grab(setup.skill_frame_box)), cv2.COLOR_BGRA2BGR)

    ### demonic beast battle
    if setup.BIRD_AUTO or setup.DEER_AUTO:
        ## capture different areas on screen
        demonic_beast_battle_frames()


        ## ready detection
        ready_rectangle, READY, ready_count = img_detection_rectangle(setup.ready_frame, setup.ready_img)
        #print("READY: " + str(READY))
        #print(ready_count)

        ## determine how many team members are alive
        FOUR = True
        THREE = False
        TWO = False
        ONE = False
        for (x, y, w, h) in ready_rectangle:
            # 4: 13 85 156 228     39
            # 3: 49 120 192    39
            # 2: 85 156    39
            # 1: 120    39
            if x == 228:
                FOUR = True
                THREE = False
                TWO = False
                ONE = False
            elif x == 192:
                FOUR = False
                THREE = True
                TWO = False
                ONE = False
            elif x == 156:
                FOUR = False
                THREE = False
                TWO = True
                ONE = False
            elif x == 120:
                FOUR = False
                THREE = False
                TWO = False
                ONE = True

        ## phase detection
        setup.phase = phase_detection(setup.phase_frame, [setup.phase1_img, setup.phase2_img, setup.phase3_img, setup.phase4_img])
        #print("phase: " + str(phase))

        if setup.phase == 1 and (setup.STAGE_2 or setup.STAGE_3) and (ONE or TWO or THREE):  # don't waste time if team member gets oneshotted in first phase
            ## forfeit battle
            FORFEIT_BATTLE = img_detection(setup.forfeit_battle_frame, setup.forfeit_battle_img)
            CONFIRM_FORFEIT = img_detection(setup.confirm_reset_frame, setup.confirm_reset_img)
            if FORFEIT_BATTLE:
                #print("forfeit battle")
                left_click_mouse(setup.forfeit_battle_frame_top, setup.forfeit_battle_frame_left, setup.forfeit_battle_frame_width, setup.forfeit_battle_frame_height)
            elif CONFIRM_FORFEIT:
                #print("confirm forfeit")
                if setup.STAGE_1 and not setup.BIRD_FAILURE_COUNTER_SET:
                    setup.bird_failure_counter1 = setup.bird_failure_counter1 + 1
                    setup.BIRD_FAILURE_COUNTER_SET = True
                if setup.STAGE_2 and not setup.BIRD_FAILURE_COUNTER_SET:
                    setup.bird_failure_counter2 = setup.bird_failure_counter2 + 1
                    setup.BIRD_FAILURE_COUNTER_SET = True
                if setup.STAGE_3 and not setup.BIRD_FAILURE_COUNTER_SET:
                    setup.bird_failure_counter3 = setup.bird_failure_counter3 + 1
                    setup.BIRD_FAILURE_COUNTER_SET = True
                left_click_mouse(setup.confirm_reset_frame_top, setup.confirm_reset_frame_left, setup.confirm_reset_frame_width, setup.confirm_reset_frame_height)
            else:
                #print("right click")
                right_click_mouse(setup.forfeit_battle_frame_top, setup.forfeit_battle_frame_left, setup.forfeit_battle_frame_width, setup.forfeit_battle_frame_height)
        elif READY:  # cards can be used
            ## skill detection
            skill_detection()


            ## reset stage2_phase3 functions
            if setup.phase == 4:
                setup.RUSH_STAGE2_PHASE3 = False


            ## detect buffs (attack, evasion, reflect) and focus on removing them
            if (FOUR and ready_count == 4) or (THREE and ready_count == 3) or (TWO and ready_count == 2) or (ONE and ready_count == 1):  # TODO: know how many team members are still alive
                setup.ATTACK = img_detection(setup.beast_status_bar_frame, setup.attack_buff_img)
                setup.EVASION = img_detection(setup.beast_status_bar_frame, setup.evasion_buff_img)
                setup.REFLECT = img_detection(setup.beast_status_bar_frame, setup.reflect_buff_img)
                #print("attack buff: " + str(setup.ATTACK))
                #print("evasion buff: " + str(setup.EVASION))
                #print("reflect buff: " + str(setup.REFLECT))

            if setup.ATTACK or setup.EVASION or setup.REFLECT:
                setup.buff_remove_forward = 30

            if setup.STAGE_3 and setup.phase == 3:
                setup.STAGE3_PHASE3_HP_MIN = img_detection(setup.boss_hp_frame, setup.stage3_phase3_hp_min_img)


            ## queue skills
            if setup.BIRD_AUTO:
                if setup.STAGE_1:
                    if setup.phase != 4:
                        stage1_phase123_bird()
                    elif setup.phase == 4:
                        stage1_phase4_bird()
                elif setup.STAGE_2:
                    if setup.phase == 1 or setup.phase == 2:
                        stage2_phase12_bird()
                    elif setup.phase == 3:
                        stage2_phase3_bird(ready_count)
                    elif setup.phase == 4:
                        stage2_phase4_bird()
                elif setup.STAGE_3:
                    if setup.phase == 1 or setup.phase == 2:
                        stage3_phase12_bird()
                    elif setup.phase == 3:
                        stage3_phase3_bird()
                    elif setup.phase == 4:
                        stage3_phase4_bird()
            elif setup.DEER_AUTO:
                if setup.phase == 1:
                    phase1_deer()
                elif setup.phase == 2:
                    phase2_deer()
                elif setup.phase == 3:
                    phase3_deer()
                elif setup.phase == 4:
                    phase4_deer()


            ## queue special skills
            if setup.BIRD_AUTO and not setup.RUSH_STAGE2_PHASE3:
                if not (setup.STAGE_2 and setup.phase == 3):
                    gow_bird()
                    mat_bird()
                if setup.STAGE_1:
                    brun_bird()
                    mel_bird()


            ## process queue and reset
            process_queue()

            while not setup.skillQueue.empty():  # empty queue
                flush = setup.skillQueue.get()

            for p in Skills:  # reset skill count
                # print(p.name)
                p.count = 0
        else:
            ## menu navigation
            demonic_beast_battle_menu()



    ### Death Matches
    if setup.DEATH_MATCH:
        full_frame()  # TODO: death_match_frames()
        death_match()

    # ### daily missions
    # if setup.DAILY:
    #     full_frame()  # TODO: daily_mission_frames()
    #     daily_menu()




    ### show different frames
    # demonic_beast_battle_frames()

    # cv2.imshow("phase", setup.phase_frame)
    # cv2.imshow("ready", setup.ready_frame)
    # cv2.imshow("skill", setup.skill_frame)
    # #cv2.setWindowProperty("skill", cv2.WND_PROP_TOPMOST, 1)
    # cv2.imshow("ok", setup.ok_reset_frame)
    # cv2.imshow("select stage 1", setup.select_stage_1_frame)
    # cv2.imshow("select stage 2", setup.select_stage_2_frame)
    # cv2.imshow("select stage 3", setup.select_stage_3_frame)
    # cv2.imshow("confirm reset", setup.confirm_reset_frame)
    # cv2.imshow("save team", setup.save_team_frame)
    # cv2.imshow("confirm team", setup.confirm_team_frame)
    # cv2.imshow("use stamina portion", setup.use_stamina_potion_frame)
    # cv2.imshow("team", setup.team_frame)
    # cv2.imshow("matrona health", setup.matrona_health_frame)
    # cv2.imshow("beast status bar", setup.beast_status_bar_frame)
    # cv2.imshow("boss hp", setup.boss_hp_frame)
    # cv2.imshow("forfeit_battle", setup.forfeit_battle_frame)

    # cv2.imshow("frame", setup.frame)
    # cv2.imshow("free stage mission", setup.free_stage_mission_frame)
    # cv2.imshow("menu bar", setup.menu_bar_frame)


    ### GUI
    createGUI()


    ### hotkeys
    if keyboard.is_pressed("p") and setup.MOUSE_ACTIVE:
        start_stop_mouse()
    if keyboard.is_pressed("r") and not setup.MOUSE_ACTIVE:
        start_stop_mouse()
    if keyboard.is_pressed("s"):
        stop_auto()
    if keyboard.is_pressed("q"):
        quitGUI()
