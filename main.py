from setup import *
import setup
from functions import *
from tkinter_gui import *

import cv2
import numpy as np
import pyautogui as pg
import time
import keyboard
from mss import mss


setup.init()
setup_frame()
setup_menu()
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
        frames()


        ## ready detection
        READY = img_detection(setup.ready_frame, setup.ready_img)
        #print("READY: " + str(READY))


        ## phase detection
        if READY:
            phase = phase_detection(setup.phase_frame, [setup.phase1_img, setup.phase2_img, setup.phase3_img, setup.phase4_img])
            #print("phase: " + str(phase))


        ## skill detection
        if READY:
            skill_detection()


        ## queue special skills
        if READY and setup.BIRD_AUTO:
            gow_bird()
            brun_bird(phase)
            mel_bird(phase)
            #mag_bird()
            mat_bird()


        ## queue skills
        if READY:
            if setup.BIRD_AUTO:
                if phase != 4:
                    phase123_bird()
                elif phase == 4:
                    phase4_bird()
            elif setup.DEER_AUTO:
                if phase == 1:
                    phase1_deer()
                elif phase == 2:
                    phase2_deer()
                elif phase == 3:
                    phase3_deer()
                elif phase == 4:
                    phase4_deer()


        ## process queue
        if READY and setup.MOUSE_ACTIVE:
            if (setup.BIRD_AUTO or setup.DEER_AUTO) and (setup.current_time - setup.skill_delay_time >= 2.5):  # delay card usage
                process_queue(READY, phase)
                setup.skill_delay_time = setup.current_time

        while not setup.skillQueue.empty():  # empty queue
            flush = setup.skillQueue.get()


        ## reset skill count
        for p in Skills:
            # print(p.name)
            p.count = 0


        ## menu navigation
        if setup.MOUSE_ACTIVE and (setup.current_time - setup.menu_delay_time >= 1):
            menu()
            setup.menu_delay_time = setup.current_time


    ### show different frames
    # cv2.imshow("phase", setup.phase_frame)
    # cv2.imshow("ready", setup.ready_frame)
    #cv2.imshow("skill", setup.skill_frame)
    #cv2.setWindowProperty("skill", cv2.WND_PROP_TOPMOST, 1)
    # cv2.imshow("ok", setup.ok_reset_frame)
    # cv2.imshow("select stage", setup.select_stage_frame)
    # cv2.imshow("confirm reset", setup.confirm_reset_frame)
    # cv2.imshow("save team", setup.save_team_frame)
    # cv2.imshow("confirm team", setup.confirm_team_frame)
    # cv2.imshow("use stamina portion", setup.use_stamina_potion_frame)


    ### GUI
    createGUI()


    ### hotkeys
    if keyboard.is_pressed("p") and (setup.current_time - setup.p_delay_time >= 0.5):
        start_stop_mouse()
        setup.p_delay_time = setup.current_time
    if keyboard.is_pressed("s"):
        stop_auto()
    if keyboard.is_pressed("q"):
        quitGUI()
