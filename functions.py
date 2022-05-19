import cv2
import pyautogui as pg
import time
import setup
import keyboard
import numpy as np


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


def menu(boss_name, ok_reset_frame, confirm_reset_frame, select_stage_frame, save_team_frame, confirm_team_frame, use_stamina_potion_frame):
    OK = img_detection(ok_reset_frame, setup.ok_img)
    STAGE_OPEN = img_detection(select_stage_frame, setup.stage_open_img)
    STAGE_CLEARED = img_detection(select_stage_frame, setup.stage_cleared_img)
    RESET = img_detection(ok_reset_frame, setup.reset_img)
    CONFIRM_RESET = img_detection(confirm_reset_frame, setup.confirm_reset_img)
    SET_PARTY = img_detection(ok_reset_frame, setup.set_party_img)
    SAVE_TEAM = img_detection(save_team_frame, setup.save_team_img)
    CONFIRM_TEAM = img_detection(confirm_team_frame, setup.confirm_team_img)
    WEEKLY_RESET_OK = img_detection(confirm_team_frame, setup.weekly_reset_ok_img)
    START_STAGE = img_detection(ok_reset_frame, setup.start_img)
    USE_STAMINA_POTION = img_detection(use_stamina_potion_frame, setup.use_stamina_potion_img)
    RECONNECT = img_detection(confirm_reset_frame, setup.reconnect_img)
    FAILED_OK = img_detection(ok_reset_frame, setup.failed_ok_img)

    if OK:
        print("ok")
        left_click_mouse(setup.ok_reset_frame_top, setup.ok_reset_frame_left, setup.ok_reset_frame_width, setup.ok_reset_frame_height)
        if not setup.COMPLETION_COUNTER_SET:
            setup.completion_counter = setup.completion_counter + 1
            setup.COMPLETION_COUNTER_SET = True
    if CONFIRM_RESET:
        print("confirm reset")
        left_click_mouse(setup.confirm_reset_frame_top, setup.confirm_reset_frame_left, setup.confirm_reset_frame_width, setup.confirm_reset_frame_height)
    elif STAGE_CLEARED and RESET:
        print("stage cleared")
        print("reset")
        left_click_mouse(setup.ok_reset_frame_top, setup.ok_reset_frame_left, setup.ok_reset_frame_width, setup.ok_reset_frame_height)
    if STAGE_OPEN and SET_PARTY:
        print("stage open")
        print("set party")
        left_click_mouse(setup.ok_reset_frame_top, setup.ok_reset_frame_left, setup.ok_reset_frame_width, setup.ok_reset_frame_height)
    if CONFIRM_TEAM:
        print("confirm team")
        left_click_mouse(setup.confirm_team_frame_top, setup.confirm_team_frame_left, setup.confirm_team_frame_width, setup.confirm_team_frame_height)
    elif SAVE_TEAM:
        print("save team")
        left_click_mouse(setup.save_team_frame_top, setup.save_team_frame_left, setup.save_team_frame_width, setup.save_team_frame_height)
    if STAGE_OPEN and RESET:
        print("stage open")
        left_click_mouse(setup.select_stage_frame_top, setup.select_stage_frame_left, setup.select_stage_frame_width, setup.select_stage_frame_height)
    if USE_STAMINA_POTION:
        print("use stamina potion")
        left_click_mouse(setup.use_stamina_potion_frame_top, setup.use_stamina_potion_frame_left, setup.use_stamina_potion_frame_width, setup.use_stamina_potion_frame_height)
    elif WEEKLY_RESET_OK:
        print("weekly reset ok")
        left_click_mouse(setup.confirm_team_frame_top, setup.confirm_team_frame_left, setup.confirm_team_frame_width, setup.confirm_team_frame_height)
    elif START_STAGE:
        print("start stage")
        left_click_mouse(setup.ok_reset_frame_top, setup.ok_reset_frame_left, setup.ok_reset_frame_width, setup.ok_reset_frame_height)
        setup.COMPLETION_COUNTER_SET = False
        setup.FAILURE_COUNTER_SET = False
        if boss_name == "bird":
            setup.mat2_delay_counter = 0
        elif boss_name == "deer":
            setup.red_card_delay_phase2 = 0
            setup.green_card_delay_phase2 = 100
            setup.blue_card_delay_phase2 = 100
            setup.red_card_delay_phase4 = 100
            setup.green_card_delay_phase4 = 100
            setup.blue_card_delay_phase4 = 0
    if RECONNECT:
        print("reconnect")
        left_click_mouse(setup.confirm_reset_frame_top, setup.confirm_reset_frame_left, setup.confirm_reset_frame_width, setup.confirm_reset_frame_height)
    if FAILED_OK:
        print("failed ok")
        left_click_mouse(setup.ok_reset_frame_top, setup.ok_reset_frame_left, setup.ok_reset_frame_width, setup.ok_reset_frame_height)
        if not setup.FAILURE_COUNTER_SET:
            setup.failure_counter = setup.failure_counter + 1
            setup.FAILURE_COUNTER_SET = True

    time.sleep(1)
    # print("Completions: " + str(setup.completion_counter))
    # print("Failures: " + str(setup.failure_counter))


def phase123_bird(p):
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
            # if p.count > 1 and p.level == 1:
            #     setup.skillQueue.put((16, p, "move"))
            # elif p.count >= 3:                                # see main.py
            #     if p.level == 1:
            #         setup.skillQueue.put((80, p, "use"))
            #     elif p.level == 2:
            #         setup.skillQueue.put((100, p, "use"))
            #     elif p.level == 3:
            #         setup.skillQueue.put((120, p, "use"))
        case "brun_ult":
            setup.skillQueue.put((28, p, "use"))
        # case "mag1":
        #     setup.skillQueue.put((40 + p.level, p, "use"))
        # case "mag2":
        #     print(35 + p.level + setup.mag2_delay)
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
            # elif p.level == 1:
            #     setup.skillQueue.put((70, p, "use"))
            # elif p.count >= 2 and p.level == 2:
            #     setup.skillQueue.put((80, p, "use"))
            # elif p.count >= 3 and p.level == 3:
            #     setup.skillQueue.put((100, p, "use"))
        case "mel2":
            if p.level == 1:
                setup.skillQueue.put((30, p, "use"))
            elif p.level == 2:
                setup.skillQueue.put((40, p, "use"))
            elif p.level == 3:
                setup.skillQueue.put((50, p, "use"))
        case "mel_ult":
            setup.skillQueue.put((27, p, "use"))


def phase4_bird(p):
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
                else:
                    pass  # setup.skillQueue.put((29, p, "use"))
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


def phase1_deer(p):
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


def phase2_deer(p):
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
            if p.count > 1:
                setup.skillQueue.put((50, p, "move"))
            if p.level == 1:
                setup.skillQueue.put((102, p, "use"))
            elif p.level == 2:
                setup.skillQueue.put((101, p, "use"))
            elif p.level == 3:
                setup.skillQueue.put((100, p, "use"))
        case "mel2":
            if p.count > 1:
                setup.skillQueue.put((51, p, "move"))
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


def phase3_deer(p):
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
                setup.skillQueue.put((50, p, "move"))
            if p.level == 1:
                setup.skillQueue.put((51, p, "use"))
            elif p.level == 2:
                setup.skillQueue.put((52, p, "use"))
            elif p.level == 3:
                setup.skillQueue.put((53, p, "use"))
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


def phase4_deer(p):
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
