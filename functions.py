from setup import *
import setup

import cv2
import numpy as np
import pyautogui as pg
import time
import keyboard
from mss import mss


def img_detection(frame, img):
    threshold = .80
    result = cv2.matchTemplate(frame, img, cv2.TM_CCOEFF_NORMED)
    minVal, maxVal, minLoc, maxLoc = cv2.minMaxLoc(result)
    if maxVal >= threshold:
        return True
    else:
        return False


def img_detection_rectangle(frame, img):
    threshold = .80
    height, width, dump = img.shape
    result = cv2.matchTemplate(frame, img, cv2.TM_CCOEFF_NORMED)
    # minVal, maxVal, minLoc, maxLoc = cv2.minMaxLoc(result)
    yLoc, xLoc = np.where(result >= threshold)

    ## group rectangles
    rectangles = []
    for (x, y) in zip(xLoc, yLoc):
        rectangles.append([int(x), int(y), int(width), int(height)])
        rectangles.append([int(x), int(y), int(width), int(height)])

    rectangles, weights = cv2.groupRectangles(rectangles, 1, 0.2)
    return rectangles


def phase_detection(p_frame, p_img):
    phase_threshold = .95

    for i in range(0, 4):
        #print(i)
        #print(p_img[i])
        p_result = cv2.matchTemplate(p_frame, p_img[i], cv2.TM_CCOEFF_NORMED)
        minVal, maxVal, minLoc, maxLoc = cv2.minMaxLoc(p_result)
        if maxVal >= phase_threshold:
            return int(i+1)


def left_click_mouse(frame_top, frame_left, frame_width, frame_height, sleep=0.05):
    if not keyboard.is_pressed("p"):
        pg.mouseDown(frame_left + frame_width/2, frame_top + frame_height/2)
        time.sleep(sleep)
        pg.mouseUp()


def use_card(skill_frame_top, skill_frame_left, rectangles):
    if not keyboard.is_pressed("p"):
        for (x, y, w, h) in rectangles:
            pg.mouseDown(skill_frame_left + x + w / 2, skill_frame_top + y + h / 2)
            time.sleep(0.05)
            pg.mouseUp()


def move_card(skill_frame_top, skill_frame_left, rectangles):
    if not keyboard.is_pressed("p"):
        count = 0
        for (x, y, w, h) in rectangles:
            if count == 0:
                pg.mouseDown(skill_frame_left + x + w / 2, skill_frame_top + y + h / 2)
                time.sleep(0.5)
                count = count + 1
            else:
                pg.moveTo(skill_frame_left + x + w / 2, skill_frame_top + y + h / 2)
                pg.mouseUp(skill_frame_left + x + w / 2, skill_frame_top + y + h / 2)
                time.sleep(0.5)


def skill_detection():
    ## compare skill_frame with skill images
    for p in Skills:
        p.result = cv2.matchTemplate(setup.skill_frame, p.img, cv2.TM_CCOEFF_NORMED)

    ## (get values and locations of comparison)
    # for p in Skills:
    #     minVal, p.maxVal, minLoc, p.maxLoc = cv2.minMaxLoc(p.result)  # minVal and minLoc neglected

    ## filter locations
    for p in Skills:
        p.yLoc, p.xLoc = np.where(p.result >= p.threshold)

    ## group and draw rectangles
    for p in Skills:
        rectangles = []
        for (x, y) in zip(p.xLoc, p.yLoc):
            rectangles.append([int(x), int(y), int(p.width), int(p.height)])
            rectangles.append([int(x), int(y), int(p.width), int(p.height)])
        p.rectangles, weights = cv2.groupRectangles(rectangles, 1, 0.2)
        for (x, y, w, h) in p.rectangles:
            cv2.rectangle(setup.skill_frame, (x, y), (x + w, y + h), p.color, p.thickness)
            p.count = int(p.rectangles.size / 4)


def frames():
    setup.ready_frame = cv2.cvtColor(np.array(setup.sct.grab(setup.ready_frame_box)), cv2.COLOR_BGRA2BGR)
    setup.phase_frame = cv2.cvtColor(np.array(setup.sct.grab(setup.phase_frame_box)), cv2.COLOR_BGRA2BGR)
    setup.ok_reset_frame = cv2.cvtColor(np.array(setup.sct.grab(setup.ok_reset_frame_box)), cv2.COLOR_BGRA2BGR)
    setup.select_stage_frame = cv2.cvtColor(np.array(setup.sct.grab(setup.select_stage_frame_box)), cv2.COLOR_BGRA2BGR)
    setup.confirm_reset_frame = cv2.cvtColor(np.array(setup.sct.grab(setup.confirm_reset_frame_box)), cv2.COLOR_BGRA2BGR)
    setup.save_team_frame = cv2.cvtColor(np.array(setup.sct.grab(setup.save_team_frame_box)), cv2.COLOR_BGRA2BGR)
    setup.confirm_team_frame = cv2.cvtColor(np.array(setup.sct.grab(setup.confirm_team_frame_box)), cv2.COLOR_BGRA2BGR)
    setup.use_stamina_potion_frame = cv2.cvtColor(np.array(setup.sct.grab(setup.use_stamina_potion_frame_box)), cv2.COLOR_BGRA2BGR)


def process_queue(READY, phase):
    if setup.skillQueue.qsize() == 0 and READY:  # skip turn
        use_card(setup.ready_frame_top, setup.ready_frame_left, img_detection_rectangle(ready_frame, setup.ready_img))

    if setup.skillQueue.qsize() >= 1 and not keyboard.is_pressed("p"):
        queue_priority, skill_object, skill_option = setup.skillQueue.get()
        #print(str(queue_priority) + " " + str(skill_object.name) + " " + str(skill_option))

        if skill_option == "use":
            use_card(setup.skill_frame_top, setup.skill_frame_left, skill_object.rectangles)
        elif skill_option == "move":
            move_card(setup.skill_frame_top, setup.skill_frame_left, skill_object.rectangles)

        ## special activation rules
        if setup.BIRD_AUTO:
            bird_rules(phase, skill_object.name)
        elif setup.DEER_AUTO:
            deer_rules(phase, skill_object.name, skill_option)

        if setup.BIRD_AUTO:  # delay
            time.sleep(0.5)
        elif setup.DEER_AUTO:
            time.sleep(1.5)
        else:
            time.sleep(1.5)


def menu():  # ok_reset_frame, confirm_reset_frame, select_stage_frame, save_team_frame, confirm_team_frame, use_stamina_potion_frame
    OK = img_detection(setup.ok_reset_frame, setup.ok_img)
    BIRD_STAGE_OPEN = img_detection(setup.select_stage_frame, setup.stage_open_bird_img)
    BIRD_STAGE_CLEARED = img_detection(setup.select_stage_frame, setup.stage_cleared_bird_img)
    DEER_STAGE_OPEN = img_detection(setup.select_stage_frame, setup.stage_open_deer_img)
    DEER_STAGE_CLEARED = img_detection(setup.select_stage_frame, setup.stage_cleared_deer_img)
    RESET = img_detection(setup.ok_reset_frame, setup.reset_img)
    CONFIRM_RESET = img_detection(setup.confirm_reset_frame, setup.confirm_reset_img)
    SET_PARTY = img_detection(setup.ok_reset_frame, setup.set_party_img)
    SAVE_TEAM = img_detection(setup.save_team_frame, setup.save_team_img)
    CONFIRM_TEAM = img_detection(setup.confirm_team_frame, setup.confirm_team_img)
    WEEKLY_RESET_OK = img_detection(setup.confirm_team_frame, setup.weekly_reset_ok_img)
    START_STAGE = img_detection(setup.ok_reset_frame, setup.start_img)
    USE_STAMINA_POTION = img_detection(setup.use_stamina_potion_frame, setup.use_stamina_potion_img)
    RECONNECT = img_detection(setup.confirm_reset_frame, setup.reconnect_img)
    FAILED_OK = img_detection(setup.ok_reset_frame, setup.failed_ok_img)

    if OK:
        #print("ok")
        left_click_mouse(setup.ok_reset_frame_top, setup.ok_reset_frame_left, setup.ok_reset_frame_width, setup.ok_reset_frame_height)
        if setup.BIRD_AUTO and not setup.BIRD_COMPLETION_COUNTER_SET:
            setup.bird_completion_counter = setup.bird_completion_counter + 1
            setup.BIRD_COMPLETION_COUNTER_SET = True
        elif setup.DEER_AUTO and not setup.DEER_COMPLETION_COUNTER_SET:
            setup.deer_completion_counter = setup.deer_completion_counter + 1
            setup.DEER_COMPLETION_COUNTER_SET = True
    if CONFIRM_RESET:
        #print("confirm reset")
        left_click_mouse(setup.confirm_reset_frame_top, setup.confirm_reset_frame_left, setup.confirm_reset_frame_width, setup.confirm_reset_frame_height)
    elif (BIRD_STAGE_CLEARED or DEER_STAGE_CLEARED) and RESET:
        #print("stage cleared")
        #print("reset")
        left_click_mouse(setup.ok_reset_frame_top, setup.ok_reset_frame_left, setup.ok_reset_frame_width, setup.ok_reset_frame_height)
    if (BIRD_STAGE_OPEN or DEER_STAGE_OPEN) and SET_PARTY:
        #print("stage open")
        #print("set party")
        left_click_mouse(setup.ok_reset_frame_top, setup.ok_reset_frame_left, setup.ok_reset_frame_width, setup.ok_reset_frame_height)
    if CONFIRM_TEAM:
        #print("confirm team")
        left_click_mouse(setup.confirm_team_frame_top, setup.confirm_team_frame_left, setup.confirm_team_frame_width, setup.confirm_team_frame_height)
    elif SAVE_TEAM:
        #print("save team")
        left_click_mouse(setup.save_team_frame_top, setup.save_team_frame_left, setup.save_team_frame_width, setup.save_team_frame_height)
    if (BIRD_STAGE_OPEN or DEER_STAGE_OPEN) and RESET:
        #print("stage open")
        left_click_mouse(setup.select_stage_frame_top, setup.select_stage_frame_left, setup.select_stage_frame_width, setup.select_stage_frame_height)
    if USE_STAMINA_POTION:
        #print("use stamina potion")
        left_click_mouse(setup.use_stamina_potion_frame_top, setup.use_stamina_potion_frame_left, setup.use_stamina_potion_frame_width, setup.use_stamina_potion_frame_height)
    elif WEEKLY_RESET_OK:
        #print("weekly reset ok")
        left_click_mouse(setup.confirm_team_frame_top, setup.confirm_team_frame_left, setup.confirm_team_frame_width, setup.confirm_team_frame_height)
    elif START_STAGE:
        #print("start stage")
        left_click_mouse(setup.ok_reset_frame_top, setup.ok_reset_frame_left, setup.ok_reset_frame_width, setup.ok_reset_frame_height)
        setup.BIRD_COMPLETION_COUNTER_SET = False
        setup.BIRD_FAILURE_COUNTER_SET = False
        setup.DEER_COMPLETION_COUNTER_SET = False
        setup.DEER_FAILURE_COUNTER_SET = False
        if setup.BIRD_AUTO:
            setup.mat2_delay_counter = 0
        elif setup.DEER_AUTO:
            setup.red_card_delay_phase2 = 0
            setup.green_card_delay_phase2 = 100
            setup.blue_card_delay_phase2 = 100
            setup.red_card_delay_phase4 = 100
            setup.green_card_delay_phase4 = 100
            setup.blue_card_delay_phase4 = 0
    if RECONNECT:
        #print("reconnect")
        left_click_mouse(setup.confirm_reset_frame_top, setup.confirm_reset_frame_left, setup.confirm_reset_frame_width, setup.confirm_reset_frame_height)
    if FAILED_OK:
        #print("failed ok")
        left_click_mouse(setup.ok_reset_frame_top, setup.ok_reset_frame_left, setup.ok_reset_frame_width, setup.ok_reset_frame_height)
        if setup.BIRD_AUTO and not setup.BIRD_FAILURE_COUNTER_SET:
            setup.bird_failure_counter = setup.bird_failure_counter + 1
            setup.BIRD_FAILURE_COUNTER_SET = True
        elif setup.DEER_AUTO and not setup.DEER_FAILURE_COUNTER_SET:
            setup.deer_failure_counter = setup.deer_failure_counter + 1
            setup.DEER_FAILURE_COUNTER_SET = True

    time.sleep(1)
    #print("Completions: " + str(setup.completion_counter))
    #print("Failures: " + str(setup.failure_counter))


def gow_bird():  # rank up
    gow2_lvl1_counter = 0
    gow2_lvl2_counter = 0
    gow2_lvl3_counter = 0
    for p in Skills:
        if p.name == "gow2" and p.count > 0:
            if p.level == 1:
                gow2_lvl1_counter = p.count
            elif p.level == 2:
                gow2_lvl2_counter = p.count
            elif p.level == 3:
                gow2_lvl3_counter = p.count

    gow2_counter = gow2_lvl1_counter + gow2_lvl2_counter + gow2_lvl3_counter
    if (gow2_lvl2_counter >= 1 or gow2_lvl3_counter >= 1) and (gow2_counter >= 2):
        for p in Skills:
            if p.name == "gow2" and p.count > 0:
                if p.level == 2:
                    setup.skillQueue.put((5, p, "use"))
                    break
                elif p.level == 3:
                    setup.skillQueue.put((4, p, "use"))
                    break


def brun_bird(phase):  # power strike
    brun2_lvl1_counter = 0
    brun2_lvl2_counter = 0
    brun2_lvl3_counter = 0
    if phase != 4:
        for p in Skills:
            if p.name == "brun2" and p.count > 0:
                if p.level == 1:
                    brun2_lvl1_counter = p.count
                elif p.level == 2:
                    brun2_lvl2_counter = p.count
                elif p.level == 3:
                    brun2_lvl3_counter = p.count

        brun2_counter = brun2_lvl1_counter + brun2_lvl2_counter + brun2_lvl3_counter
        if brun2_counter >= 4:
            for p in Skills:
                if p.name == "brun2" and p.count > 0:
                    if p.level == 1:
                        setup.skillQueue.put((90, p, "use"))
                        break
                    elif p.level == 2:
                        setup.skillQueue.put((110, p, "use"))
                        break
                    elif p.level == 3:
                        setup.skillQueue.put((120, p, "use"))
                        break


def mel_bird(phase):  # amplify
    mel1_lvl1_counter = 0
    mel1_lvl2_counter = 0
    mel1_lvl3_counter = 0
    if phase != 4:
        for p in Skills:
            if p.name == "mel1" and p.count > 0:
                if p.level == 1:
                    mel1_lvl1_counter = p.count
                elif p.level == 2:
                    mel1_lvl2_counter = p.count
                elif p.level == 3:
                    mel1_lvl3_counter = p.count

        mel1_counter = mel1_lvl1_counter + mel1_lvl2_counter + mel1_lvl3_counter
        if mel1_counter >= 2:
            for p in Skills:
                if p.name == "mel1" and p.count > 0:
                    if p.level == 1:
                        setup.skillQueue.put((70, p, "use"))
                        break
                    elif p.level == 2:
                        setup.skillQueue.put((80, p, "use"))
                        break
                    elif p.level == 3:
                        setup.skillQueue.put((100, p, "use"))
                        break


def mag_bird():  # buff
    mag2_counter = 0
    for p in Skills:
        if p.name == "mag2" and p.count > 0:
            mag2_counter = mag2_counter + 1

    if mag2_counter >= 3:
        for p in Skills:
            if p.name == "mag2" and p.count > 0 and p.level < 3:
                setup.mag2_delay = 0


def mat_bird():  # taunt
    mat2_counter = 0
    for p in Skills:
        if p.name == "mat2" and p.count > 0:
            mat2_counter = mat2_counter + 1

    if mat2_counter >= 3:
        for p in Skills:
            if p.name == "mat2" and p.count > 0 and p.level < 3:
                setup.mat2_delay = 0


def phase123_bird():
    for p in Skills:
        if p.count > 0:
            match p.name:
                case "brun1":
                    if p.level == 1:
                        setup.skillQueue.put((31, p, "use"))
                    elif p.level == 2:
                        setup.skillQueue.put((41, p, "use"))
                    elif p.level == 3:
                        setup.skillQueue.put((51, p, "use"))
                case "brun2":
                    pass
                case "brun_ult":
                    setup.skillQueue.put((28, p, "use"))
                # case "mag1":
                #     setup.skillQueue.put((40 + p.level, p, "use"))
                # case "mag2":
                #     if p.level == 3:
                #         if p.count >= 2:
                #             setup.skillQueue.put((6, p, "use"))
                #         else:
                #             pass
                #     else:
                #         setup.skillQueue.put((35 + p.level + setup.mag2_delay, p, "use"))
                # case "mag_ult":
                #     setup.skillQueue.put((50, p, "use"))
                case "mat1":
                    if p.level == 1:
                        setup.skillQueue.put((23, p, "use"))
                    elif p.level == 2:
                        setup.skillQueue.put((21, p, "use"))
                    elif p.level == 3:
                        setup.skillQueue.put((22, p, "use"))
                case "mat2":
                    if p.level == 3:
                        if p.count >= 2:
                            setup.skillQueue.put((7, p, "use"))
                        else:
                            pass
                    else:
                        setup.skillQueue.put((11 + p.level + setup.mat2_delay, p, "use"))
                case "mat_ult":
                    setup.skillQueue.put((29, p, "use"))
                case "gow1":
                    if p.level == 1:
                        setup.skillQueue.put((26, p, "use"))
                    elif p.level == 2:
                        setup.skillQueue.put((24, p, "use"))
                    elif p.level == 3:
                        setup.skillQueue.put((25, p, "use"))
                case "gow2":
                    if p.count == 1 or p.level >= 2:
                        pass
                    elif p.count > 1 and p.level == 1:
                        setup.skillQueue.put((10, p, "move"))
                case "gow_ult":
                    setup.skillQueue.put((19, p, "use"))
                case "mel1":
                    if p.count >= 2 and p.level == 1:
                        setup.skillQueue.put((17, p, "move"))
                case "mel2":
                    if p.level == 1:
                        setup.skillQueue.put((30, p, "use"))
                    elif p.level == 2:
                        setup.skillQueue.put((40, p, "use"))
                    elif p.level == 3:
                        setup.skillQueue.put((50, p, "use"))
                case "mel_ult":
                    setup.skillQueue.put((27, p, "use"))


def phase4_bird():
    for p in Skills:
        if p.count > 0:
            match p.name:
                case "brun1":
                    if p.level == 1:
                        setup.skillQueue.put((25, p, "use"))
                    elif p.level == 2:
                        setup.skillQueue.put((24, p, "use"))
                    elif p.level == 3:
                        setup.skillQueue.put((23, p, "use"))
                case "brun2":
                    if p.level == 1:
                        setup.skillQueue.put((22, p, "use"))
                    elif p.level == 2:
                        setup.skillQueue.put((21, p, "use"))
                    elif p.level == 3:
                        setup.skillQueue.put((20, p, "use"))
                case "brun_ult":
                    setup.skillQueue.put((35, p, "use"))
                # case "mag1":
                #     setup.skillQueue.put((35 - p.level, p, "use"))
                # case "mag2":
                #     if p.level == 3:
                #         if p.count >= 2:
                #             setup.skillQueue.put((6, p, "use"))
                #         else:
                #             pass
                #     else:
                #         setup.skillQueue.put((25 - p.level + setup.mag2_delay, p, "use"))
                # case "mag_ult":
                #     setup.skillQueue.put((20, p, "use"))
                case "mat1":
                    if p.level == 1:
                        setup.skillQueue.put((47, p, "use"))
                    elif p.level == 2:
                        setup.skillQueue.put((46, p, "use"))
                    elif p.level == 3:
                        setup.skillQueue.put((45, p, "use"))
                case "mat2":
                    if p.level == 3:
                        if p.count >= 2:
                            setup.skillQueue.put((7, p, "use"))
                        else:
                            pass
                    else:
                        setup.skillQueue.put((11 + p.level + setup.mat2_delay, p, "use"))
                case "mat_ult":
                    setup.skillQueue.put((36, p, "use"))
                case "gow1":
                    if p.level == 1:
                        setup.skillQueue.put((59, p, "use"))
                    elif p.level == 2:
                        setup.skillQueue.put((49, p, "use"))
                    elif p.level == 3:
                        setup.skillQueue.put((48, p, "use"))
                case "gow2":
                    if p.count == 1 or p.level >= 2:
                        pass
                    elif p.count > 1 and p.level == 1:
                        setup.skillQueue.put((10, p, "move"))
                case "gow_ult":
                    setup.skillQueue.put((37, p, "use"))
                case "mel1":
                    if p.level == 1:
                        if p.count >= 2:
                            setup.skillQueue.put((17, p, "move"))
                    elif p.level == 2:
                        setup.skillQueue.put((28, p, "use"))
                    elif p.level == 3:
                        setup.skillQueue.put((27, p, "use"))
                case "mel2":
                    if p.level == 1:
                        setup.skillQueue.put((32, p, "use"))
                    elif p.level == 2:
                        setup.skillQueue.put((31, p, "use"))
                    elif p.level == 3:
                        setup.skillQueue.put((30, p, "use"))
                case "mel_ult":
                    setup.skillQueue.put((26, p, "use"))


def bird_rules(phase, skill_name):
    if phase == 3 and setup.mat2_delay_counter > 3:
        setup.mat2_delay_counter = 3

    if setup.mat2_delay_counter == 0:
        setup.mat2_delay = 0
    else:
        setup.mat2_delay_counter = setup.mat2_delay_counter - 1

    if skill_name == "mat2":
        setup.mat2_delay = 30
        if phase != 3:
            setup.mat2_delay_counter = 11
        else:
            setup.mat2_delay_counter = 3


def phase1_deer():
    for p in Skills:
        if p.count > 0:
            match p.name:
                case "skadi1":
                    if p.level == 1:
                        setup.skillQueue.put((20, p, "use"))
                case "jor2":
                    if p.level == 1:
                        setup.skillQueue.put((25, p, "use"))
                case "mel2":
                    if p.level == 1:
                        setup.skillQueue.put((35, p, "use"))
                case "one2":
                    if p.level == 1:
                        setup.skillQueue.put((30, p, "use"))


def phase2_deer():
    for p in Skills:
        if p.count > 0:
            match p.name:
                case "skadi1":
                    if p.level == 1:
                        setup.skillQueue.put((34 + setup.red_card_delay_phase2, p, "use"))
                    elif p.level == 2:
                        setup.skillQueue.put((32 + setup.red_card_delay_phase2, p, "use"))
                    elif p.level == 3:
                        setup.skillQueue.put((30 + setup.red_card_delay_phase2, p, "use"))
                    if p.count >= 2:
                        setup.skillQueue.put((52, p, "move"))
                case "skadi2":
                    if p.level == 1:
                        setup.skillQueue.put((35 + setup.red_card_delay_phase2, p, "use"))
                    elif p.level == 2:
                        setup.skillQueue.put((33 + setup.red_card_delay_phase2, p, "use"))
                    elif p.level == 3:
                        setup.skillQueue.put((31 + setup.red_card_delay_phase2, p, "use"))
                    if p.count >= 2:
                        setup.skillQueue.put((53, p, "move"))
                # case "skadi_ult":
                #     setup.skillQueue.put((29 + setup.red_card_delay_phase2, p, "use"))
                case "jor1":
                    if p.level == 1:
                        setup.skillQueue.put((24 + setup.green_card_delay_phase2, p, "use"))
                    elif p.level == 2:
                        setup.skillQueue.put((22 + setup.green_card_delay_phase2, p, "use"))
                    elif p.level == 3:
                        setup.skillQueue.put((20 + setup.green_card_delay_phase2, p, "use"))
                    if p.count >= 2:
                        setup.skillQueue.put((54, p, "move"))
                case "jor2":
                    if p.level == 1:
                        setup.skillQueue.put((25 + setup.green_card_delay_phase2, p, "use"))
                    elif p.level == 2:
                        setup.skillQueue.put((23 + setup.green_card_delay_phase2, p, "use"))
                    elif p.level == 3:
                        setup.skillQueue.put((21 + setup.green_card_delay_phase2, p, "use"))
                    if p.count >= 2:
                        setup.skillQueue.put((55, p, "move"))
                # case "jor_ult":
                #     setup.skillQueue.put((19 + setup.green_card_delay_phase2, p, "use"))
                case "mel1":
                    if p.count >= 2:
                        if p.level == 1:
                            setup.skillQueue.put((60, p, "move"))
                        elif p.level == 2:
                            setup.skillQueue.put((61, p, "move"))
                        elif p.level == 3:
                            setup.skillQueue.put((62, p, "move"))
                    if p.level == 1:
                        setup.skillQueue.put((102, p, "use"))
                    elif p.level == 2:
                        setup.skillQueue.put((101, p, "use"))
                    elif p.level == 3:
                        setup.skillQueue.put((100, p, "use"))
                case "mel2":
                    if p.count > 1:
                        setup.skillQueue.put((63, p, "move"))
                # case "mel_ult":
                #     setup.skillQueue.put((103, p, "use"))
                case "one1":
                    if p.level == 1:
                        setup.skillQueue.put((15 + setup.blue_card_delay_phase2, p, "use"))
                    elif p.level == 2:
                        setup.skillQueue.put((13 + setup.blue_card_delay_phase2, p, "use"))
                    elif p.level == 3:
                        setup.skillQueue.put((11 + setup.blue_card_delay_phase2, p, "use"))
                    if p.count >= 2:
                        setup.skillQueue.put((56, p, "move"))
                case "one2":
                    if p.level == 1:
                        setup.skillQueue.put((14 + setup.blue_card_delay_phase2, p, "use"))
                    elif p.level == 2:
                        setup.skillQueue.put((12 + setup.blue_card_delay_phase2, p, "use"))
                    elif p.level == 3:
                        setup.skillQueue.put((10 + setup.blue_card_delay_phase2, p, "use"))
                    if p.count >= 2:
                        setup.skillQueue.put((57, p, "move"))
                # case "one_ult":
                #     setup.skillQueue.put((9 + setup.blue_card_delay_phase2, p, "use"))


def phase3_deer():
    for p in Skills:
        if p.count > 0:
            match p.name:
                case "skadi1":
                    if p.level == 1:
                        setup.skillQueue.put((10, p, "use"))
                    elif p.level == 2:
                        setup.skillQueue.put((20, p, "use"))
                    elif p.level == 3:
                        setup.skillQueue.put((30, p, "use"))
                case "skadi2":
                    if p.level == 1:
                        setup.skillQueue.put((11, p, "use"))
                    elif p.level == 2:
                        setup.skillQueue.put((21, p, "use"))
                    elif p.level == 3:
                        setup.skillQueue.put((31, p, "use"))
                case "jor1":
                    if p.level == 1:
                        setup.skillQueue.put((12, p, "use"))
                    elif p.level == 2:
                        setup.skillQueue.put((22, p, "use"))
                    elif p.level == 3:
                        setup.skillQueue.put((32, p, "use"))
                case "jor2":
                    if p.level == 1:
                        setup.skillQueue.put((13, p, "use"))
                    elif p.level == 2:
                        setup.skillQueue.put((23, p, "use"))
                    elif p.level == 3:
                        setup.skillQueue.put((33, p, "use"))
                case "mel1":
                    if p.count >= 2:
                        if p.level == 1:
                            setup.skillQueue.put((50, p, "move"))
                        elif p.level == 2:
                            setup.skillQueue.put((51, p, "move"))
                        elif p.level == 3:
                            setup.skillQueue.put((52, p, "move"))
                    if p.level == 1:
                        setup.skillQueue.put((53, p, "use"))
                    elif p.level == 2:
                        setup.skillQueue.put((54, p, "use"))
                    elif p.level == 3:
                        setup.skillQueue.put((55, p, "use"))
                case "mel2":
                    if p.level == 1:
                        setup.skillQueue.put((16, p, "use"))
                    elif p.level == 2:
                        setup.skillQueue.put((26, p, "use"))
                    elif p.level == 3:
                        setup.skillQueue.put((36, p, "use"))
                case "one1":
                    if p.level == 1:
                        setup.skillQueue.put((15, p, "use"))
                    elif p.level == 2:
                        setup.skillQueue.put((25, p, "use"))
                    elif p.level == 3:
                        setup.skillQueue.put((35, p, "use"))
                case "one2":
                    if p.level == 1:
                        setup.skillQueue.put((14, p, "use"))
                    elif p.level == 2:
                        setup.skillQueue.put((24, p, "use"))
                    elif p.level == 3:
                        setup.skillQueue.put((25, p, "use"))


def phase4_deer():
    for p in Skills:
        if p.count > 0:
            match p.name:
                case "skadi1":
                    if p.level == 1:
                        setup.skillQueue.put((46 + setup.red_card_delay_phase4, p, "use"))
                    elif p.level == 2:
                        setup.skillQueue.put((44 + setup.red_card_delay_phase4, p, "use"))
                    elif p.level == 3:
                        setup.skillQueue.put((42 + setup.red_card_delay_phase4, p, "use"))
                case "skadi2":
                    if p.level == 1:
                        setup.skillQueue.put((45 + setup.red_card_delay_phase4, p, "use"))
                    elif p.level == 2:
                        setup.skillQueue.put((43 + setup.red_card_delay_phase4, p, "use"))
                    elif p.level == 3:
                        setup.skillQueue.put((41 + setup.red_card_delay_phase4, p, "use"))
                case "skadi_ult":
                    setup.skillQueue.put((40 + setup.red_card_delay_phase4, p, "use"))
                case "jor1":
                    if p.level == 1:
                        setup.skillQueue.put((36 + setup.green_card_delay_phase4, p, "use"))
                    elif p.level == 2:
                        setup.skillQueue.put((34 + setup.green_card_delay_phase4, p, "use"))
                    elif p.level == 3:
                        setup.skillQueue.put((32 + setup.green_card_delay_phase4, p, "use"))
                case "jor2":
                    if p.level == 1:
                        setup.skillQueue.put((35 + setup.green_card_delay_phase4, p, "use"))
                    elif p.level == 2:
                        setup.skillQueue.put((33 + setup.green_card_delay_phase4, p, "use"))
                    elif p.level == 3:
                        setup.skillQueue.put((31 + setup.green_card_delay_phase4, p, "use"))
                case "jor_ult":
                    setup.skillQueue.put((30 + setup.green_card_delay_phase4, p, "use"))
                case "mel1":
                    if p.level == 1:
                        setup.skillQueue.put((13, p, "use"))
                    elif p.level == 2:
                        setup.skillQueue.put((12, p, "use"))
                    elif p.level == 3:
                        setup.skillQueue.put((11, p, "use"))
                case "mel2":
                    if p.level == 1:
                        setup.skillQueue.put((16, p, "use"))
                    elif p.level == 2:
                        setup.skillQueue.put((15, p, "use"))
                    elif p.level == 3:
                        setup.skillQueue.put((14, p, "use"))
                case "mel_ult":
                    setup.skillQueue.put((10, p, "use"))
                case "one1":
                    if p.level == 1:
                        setup.skillQueue.put((25 + setup.blue_card_delay_phase4, p, "use"))
                    elif p.level == 2:
                        setup.skillQueue.put((23 + setup.blue_card_delay_phase4, p, "use"))
                    elif p.level == 3:
                        setup.skillQueue.put((21 + setup.blue_card_delay_phase4, p, "use"))
                case "one2":
                    if p.level == 1:
                        setup.skillQueue.put((26 + setup.blue_card_delay_phase4, p, "use"))
                    elif p.level == 2:
                        setup.skillQueue.put((24 + setup.blue_card_delay_phase4, p, "use"))
                    elif p.level == 3:
                        setup.skillQueue.put((22 + setup.blue_card_delay_phase4, p, "use"))
                case "one_ult":
                    setup.skillQueue.put((20 + setup.blue_card_delay_phase4, p, "use"))


def deer_rules(phase, skill_name, skill_option):
    if phase == 2:
        if skill_option == "use":
            if skill_name == "skadi1" or skill_name == "skadi2" or skill_name == "skadi_ult":
                setup.red_card_delay_phase2 = 100
                setup.green_card_delay_phase2 = 0
                setup.blue_card_delay_phase2 = 100
            if skill_name == "jor1" or skill_name == "jor2" or skill_name == "jor_ult":
                setup.red_card_delay_phase2 = 100
                setup.green_card_delay_phase2 = 100
                setup.blue_card_delay_phase2 = 0
            if skill_name == "one1" or skill_name == "one2" or skill_name == "one_ult":
                setup.red_card_delay_phase2 = 0
                setup.green_card_delay_phase2 = 100
                setup.blue_card_delay_phase2 = 100
    elif phase == 4:
        if skill_option == "use":
            if skill_name == "skadi1" or skill_name == "skadi2" or skill_name == "skadi_ult":
                setup.red_card_delay_phase4 = 100
                setup.green_card_delay_phase4 = 0
                setup.blue_card_delay_phase4 = 100
            if skill_name == "jor1" or skill_name == "jor2" or skill_name == "jor_ult":
                setup.red_card_delay_phase4 = 100
                setup.green_card_delay_phase4 = 100
                setup.blue_card_delay_phase4 = 0
            if skill_name == "one1" or skill_name == "one2" or skill_name == "one_ult":
                setup.red_card_delay_phase4 = 0
                setup.green_card_delay_phase4 = 100
                setup.blue_card_delay_phase4 = 100
