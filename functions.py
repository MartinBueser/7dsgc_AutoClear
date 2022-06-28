from setup import *
import setup
from bird_functions import *

import cv2
import numpy as np
import pyautogui as pg
import time


def img_detection(frame, img, threshold=0.8):
    result = cv2.matchTemplate(frame, img, cv2.TM_CCOEFF_NORMED)
    minVal, maxVal, minLoc, maxLoc = cv2.minMaxLoc(result)
    if maxVal >= threshold:
        return True
    else:
        return False


def img_detection_rectangle(frame, img, threshold=0.8):
    height, width, dump = img.shape
    result = cv2.matchTemplate(frame, img, cv2.TM_CCOEFF_NORMED)
    minVal, maxVal, minLoc, maxLoc = cv2.minMaxLoc(result)
    if maxVal >= threshold:
        img_detected = True
    else:
        img_detected = False

    yLoc, xLoc = np.where(result >= threshold)

    ## group rectangles
    rectangles = []
    for (x, y) in zip(xLoc, yLoc):
        rectangles.append([int(x), int(y), int(width), int(height)])
        rectangles.append([int(x), int(y), int(width), int(height)])

    rectangles, weights = cv2.groupRectangles(rectangles, 1, 0.2)

    count = 0
    for (x, y, w, h) in rectangles:
        count = int(rectangles.size / 4)

    return rectangles, img_detected, count


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
    if setup.MOUSE_ACTIVE:
        pg.mouseDown(frame_left + frame_width/2, frame_top + frame_height/2)
        time.sleep(sleep)
        pg.mouseUp()


def right_click_mouse(frame_top, frame_left, frame_width, frame_height, sleep=0.05):
    if setup.MOUSE_ACTIVE:
        pg.mouseDown(frame_left + frame_width/2, frame_top + frame_height/2, button='right')
        time.sleep(sleep)
        pg.mouseUp(button='right')


def use_card(skill_frame_top, skill_frame_left, rectangles):
    if setup.MOUSE_ACTIVE:
        for (x, y, w, h) in rectangles:
            pg.mouseDown(skill_frame_left + x + w / 2, skill_frame_top + y + h / 2)
            time.sleep(0.05)
            pg.mouseUp()


def move_card(skill_frame_top, skill_frame_left, rectangles):
    if setup.MOUSE_ACTIVE:
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


def isbright(image):
    # Convert color space to HSV format and receive max V
    H, S, V = cv2.split(cv2.cvtColor(image, cv2.COLOR_BGR2HSV))
    V = np.max(V)
    # Return True if Card is usable
    return V > 200


def skill_detection():
    ## compare skill_frame with skill images
    for p in Skills:
        p.result = cv2.matchTemplate(setup.skill_frame, p.img, cv2.TM_CCOEFF_NORMED)

    ## filter locations
        p.yLoc, p.xLoc = np.where(p.result >= p.threshold)

    ## group and draw rectangles
        rectangles = []
        for (x, y) in zip(p.xLoc, p.yLoc):
            rectangles.append([int(x), int(y), int(p.width), int(p.height)])
            rectangles.append([int(x), int(y), int(p.width), int(p.height)])
        p.rectangles, weights = cv2.groupRectangles(rectangles, 1, 0.2)
        for (x, y, w, h) in p.rectangles:
            temp_img = setup.skill_frame[y:y+h, x:x+w]
            if isbright(temp_img) or p.name == "gow1" or p.name == "mel2" or p.name == "mat1" or p.name == "mat2" or p.name == "brun_ult" or p.name == "mel_ult" or p.name == "mat_ult" or p.name == "gow_ult" or (p.name == "gow2" and setup.STAGE_3 and setup.phase == 4):
                cv2.rectangle(setup.skill_frame, (x, y), (x + w, y + h), p.color, p.thickness)
                p.count = int(p.rectangles.size / 4)


def demonic_beast_battle_frames():
    setup.ready_frame = cv2.cvtColor(np.array(setup.sct.grab(setup.ready_frame_box)), cv2.COLOR_BGRA2BGR)
    setup.phase_frame = cv2.cvtColor(np.array(setup.sct.grab(setup.phase_frame_box)), cv2.COLOR_BGRA2BGR)
    setup.ok_reset_frame = cv2.cvtColor(np.array(setup.sct.grab(setup.ok_reset_frame_box)), cv2.COLOR_BGRA2BGR)
    setup.select_stage_1_frame = cv2.cvtColor(np.array(setup.sct.grab(setup.select_stage_1_frame_box)), cv2.COLOR_BGRA2BGR)
    setup.select_stage_2_frame = cv2.cvtColor(np.array(setup.sct.grab(setup.select_stage_2_frame_box)), cv2.COLOR_BGRA2BGR)
    setup.select_stage_3_frame = cv2.cvtColor(np.array(setup.sct.grab(setup.select_stage_3_frame_box)), cv2.COLOR_BGRA2BGR)
    setup.confirm_reset_frame = cv2.cvtColor(np.array(setup.sct.grab(setup.confirm_reset_frame_box)), cv2.COLOR_BGRA2BGR)
    setup.save_team_frame = cv2.cvtColor(np.array(setup.sct.grab(setup.save_team_frame_box)), cv2.COLOR_BGRA2BGR)
    setup.confirm_team_frame = cv2.cvtColor(np.array(setup.sct.grab(setup.confirm_team_frame_box)), cv2.COLOR_BGRA2BGR)
    setup.use_stamina_potion_frame = cv2.cvtColor(np.array(setup.sct.grab(setup.use_stamina_potion_frame_box)), cv2.COLOR_BGRA2BGR)
    setup.team_frame = cv2.cvtColor(np.array(setup.sct.grab(setup.team_frame_box)), cv2.COLOR_BGRA2BGR)
    setup.matrona_health_frame = cv2.cvtColor(np.array(setup.sct.grab(setup.matrona_health_frame_box)), cv2.COLOR_BGRA2BGR)
    setup.beast_status_bar_frame = cv2.cvtColor(np.array(setup.sct.grab(setup.beast_status_bar_frame_box)), cv2.COLOR_BGRA2BGR)
    setup.boss_hp_frame = cv2.cvtColor(np.array(setup.sct.grab(setup.boss_hp_frame_box)), cv2.COLOR_BGRA2BGR)
    setup.forfeit_battle_frame = cv2.cvtColor(np.array(setup.sct.grab(setup.forfeit_battle_frame_box)), cv2.COLOR_BGRA2BGR)


def full_frame():
    if setup.current_time - setup.skill_delay_time >= setup.skill_delay and setup.current_time - setup.menu_delay_time >= setup.menu_delay:
        setup.frame = cv2.cvtColor(np.array(setup.sct.grab(setup.frame_box)), cv2.COLOR_BGRA2BGR)


def process_queue():
    if setup.current_time - setup.skill_delay_time >= setup.skill_delay:  # delay card usage
        setup.skill_delay_time = setup.current_time

        if setup.skillQueue.qsize() == 0:  # skip turn
            temp_rectangle, temp_bool, dump = img_detection_rectangle(setup.ready_frame, setup.ready_img)
            use_card(setup.ready_frame_top, setup.ready_frame_left, temp_rectangle)

        if setup.skillQueue.qsize() >= 1:
            queue_priority, skill_object, skill_option = setup.skillQueue.get()
            print(str(queue_priority) + " " + str(skill_object.name) + " " + str(skill_option))

            if skill_option == "use":
                use_card(setup.skill_frame_top, setup.skill_frame_left, skill_object.rectangles)
            elif skill_option == "move":
                move_card(setup.skill_frame_top, setup.skill_frame_left, skill_object.rectangles)

            if skill_object.name == "mat1" or skill_object.name == "mel_ult":
                setup.ATTACK = False
                setup.EVASION = False
                setup.REFLECT = False
                setup.buff_remove_forward = 0

            ## special activation rules
            if setup.BIRD_AUTO:
                bird_rules(skill_object.name)
            elif setup.DEER_AUTO:
                deer_rules(skill_object.name, skill_option)


def demonic_beast_battle_menu():  # ok_reset_frame, confirm_reset_frame, select_stage_frame, save_team_frame, confirm_team_frame, use_stamina_potion_frame
    if setup.current_time - setup.menu_delay_time >= setup.menu_delay:
        setup.menu_delay_time = setup.current_time

        OK = img_detection(setup.ok_reset_frame, setup.ok_img)
        BIRD_STAGE_OPEN_1 = img_detection(setup.select_stage_1_frame, setup.stage_open_bird_1_img)
        BIRD_STAGE_OPEN_2 = img_detection(setup.select_stage_2_frame, setup.stage_open_bird_2_img)
        BIRD_STAGE_OPEN_3 = img_detection(setup.select_stage_3_frame, setup.stage_open_bird_3_img)
        #BIRD_STAGE_CLEARED = img_detection(setup.select_stage_frame, setup.stage_cleared_bird_img)
        DEER_STAGE_OPEN = img_detection(setup.select_stage_1_frame, setup.stage_open_deer_img)
        DEER_STAGE_CLEARED = img_detection(setup.select_stage_1_frame, setup.stage_cleared_deer_img)
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
        TEAM = img_detection(setup.team_frame, setup.team_bird_img, 0.9)
        MATRONA_HEALTH_MIN2 = img_detection(setup.matrona_health_frame, setup.matrona_health_min2_img)
        MATRONA_HEALTH_MIN3 = img_detection(setup.matrona_health_frame, setup.matrona_health_min3_img)

        if setup.BIRD_AUTO:
            #print("BIRD AUTO")
            #print(setup.STAGE_1)
            #print(setup.STAGE_2)
            #print(setup.STAGE_3)
            if OK:
                #print("ok")
                if setup.STAGE_1 and not setup.BIRD_COMPLETION_COUNTER_SET:
                    setup.bird_completion_counter1 = setup.bird_completion_counter1 + 1
                    setup.BIRD_COMPLETION_COUNTER_SET = True
                if setup.STAGE_2 and not setup.BIRD_COMPLETION_COUNTER_SET:
                    setup.bird_completion_counter2 = setup.bird_completion_counter2 + 1
                    setup.BIRD_COMPLETION_COUNTER_SET = True
                if setup.STAGE_3 and not setup.BIRD_COMPLETION_COUNTER_SET:
                    setup.bird_completion_counter3 = setup.bird_completion_counter3 + 1
                    setup.BIRD_COMPLETION_COUNTER_SET = True
                left_click_mouse(setup.ok_reset_frame_top, setup.ok_reset_frame_left, setup.ok_reset_frame_width, setup.ok_reset_frame_height)
            if RESET and not CONFIRM_RESET:
                if not TEAM or (setup.STAGE_1 and not MATRONA_HEALTH_MIN2) or (setup.STAGE_2 and not MATRONA_HEALTH_MIN3):
                    #print("reset")
                    left_click_mouse(setup.ok_reset_frame_top, setup.ok_reset_frame_left, setup.ok_reset_frame_width, setup.ok_reset_frame_height)
            if CONFIRM_RESET:
                #print("confirm reset")
                left_click_mouse(setup.confirm_reset_frame_top, setup.confirm_reset_frame_left, setup.confirm_reset_frame_width, setup.confirm_reset_frame_height)
            if TEAM:
                if BIRD_STAGE_OPEN_3 and MATRONA_HEALTH_MIN3:
                    #print("stage 3")
                    setup.STAGE_1 = False
                    setup.STAGE_2 = False
                    setup.STAGE_3 = True
                    left_click_mouse(setup.select_stage_3_frame_top, setup.select_stage_3_frame_left, setup.select_stage_3_frame_width, setup.select_stage_3_frame_height)
                if BIRD_STAGE_OPEN_2 and MATRONA_HEALTH_MIN2:
                    #print("stage 2")
                    setup.STAGE_1 = False
                    setup.STAGE_2 = True
                    setup.STAGE_3 = False
                    left_click_mouse(setup.select_stage_2_frame_top, setup.select_stage_2_frame_left, setup.select_stage_2_frame_width, setup.select_stage_2_frame_height)
                elif BIRD_STAGE_OPEN_1:
                    #print("stage 1")
                    setup.STAGE_1 = True
                    setup.STAGE_2 = False
                    setup.STAGE_3 = False
                    left_click_mouse(setup.select_stage_1_frame_top, setup.select_stage_1_frame_left, setup.select_stage_1_frame_width, setup.select_stage_1_frame_height)
            if BIRD_STAGE_OPEN_1 and SET_PARTY:
                #print("set party")
                left_click_mouse(setup.ok_reset_frame_top, setup.ok_reset_frame_left, setup.ok_reset_frame_width, setup.ok_reset_frame_height)
            if CONFIRM_TEAM:
                #print("confirm team")
                left_click_mouse(setup.confirm_team_frame_top, setup.confirm_team_frame_left, setup.confirm_team_frame_width, setup.confirm_team_frame_height)
            elif SAVE_TEAM:
                #print("save team")
                left_click_mouse(setup.save_team_frame_top, setup.save_team_frame_left, setup.save_team_frame_width, setup.save_team_frame_height)
            if USE_STAMINA_POTION:
                #print("use stamina potion")
                left_click_mouse(setup.use_stamina_potion_frame_top, setup.use_stamina_potion_frame_left, setup.use_stamina_potion_frame_width, setup.use_stamina_potion_frame_height)
            elif WEEKLY_RESET_OK:
                #print("weekly reset ok")
                left_click_mouse(setup.confirm_team_frame_top, setup.confirm_team_frame_left, setup.confirm_team_frame_width, setup.confirm_team_frame_height)
            elif START_STAGE:
                #print("start stage")
                setup.BIRD_COMPLETION_COUNTER_SET = False
                setup.BIRD_FAILURE_COUNTER_SET = False
                setup.mat2_delay_counter = 0
                left_click_mouse(setup.ok_reset_frame_top, setup.ok_reset_frame_left, setup.ok_reset_frame_width, setup.ok_reset_frame_height)
            if RECONNECT:
                #print("reconnect")
                left_click_mouse(setup.confirm_reset_frame_top, setup.confirm_reset_frame_left, setup.confirm_reset_frame_width, setup.confirm_reset_frame_height)
            if FAILED_OK:
                #print("failed ok")
                if setup.STAGE_1 and not setup.BIRD_FAILURE_COUNTER_SET:
                    setup.bird_failure_counter1 = setup.bird_failure_counter1 + 1
                    setup.BIRD_FAILURE_COUNTER_SET = True
                if setup.STAGE_2 and not setup.BIRD_FAILURE_COUNTER_SET:
                    setup.bird_failure_counter2 = setup.bird_failure_counter2 + 1
                    setup.BIRD_FAILURE_COUNTER_SET = True
                if setup.STAGE_3 and not setup.BIRD_FAILURE_COUNTER_SET:
                    setup.bird_failure_counter3 = setup.bird_failure_counter3 + 1
                    setup.BIRD_FAILURE_COUNTER_SET = True
                left_click_mouse(setup.ok_reset_frame_top, setup.ok_reset_frame_left, setup.ok_reset_frame_width, setup.ok_reset_frame_height)

        if setup.DEER_AUTO:
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


def death_match():
    if setup.current_time - setup.menu_delay_time >= setup.menu_delay:
        setup.menu_delay_time = setup.current_time

        battle_rectangle, BATTLE, dump = img_detection_rectangle(setup.frame, setup.battle_img)
        boss_battle_rectangle, BOSS_BATTLE, dump = img_detection_rectangle(setup.frame, setup.boss_battle_img)
        death_match_chance_0_rectangle, DEATH_MATCH_CHANCE_0, dump = img_detection_rectangle(setup.frame, setup.death_match_chance_0_img)
        boss_battle_extreme_rectangle, BOSS_BATTLE_EXTREME, dump = img_detection_rectangle(setup.frame, setup.boss_battle_extreme_img)
        auto_clear_rectangle, AUTO_CLEAR, dump = img_detection_rectangle(setup.frame, setup.auto_clear_img)
        start_auto_clear_rectangle, START_AUTO_CLEAR, dump = img_detection_rectangle(setup.frame, setup.start_auto_clear_img)
        use_stamina_potion_rectangle, USE_STAMINA_POTION, dump = img_detection_rectangle(setup.frame, setup.use_stamina_potion_img)
        ok_rectangle, OK, dump = img_detection_rectangle(setup.frame, setup.ok_img)
        death_match_ok_rectangle, DEATH_MATCH_OK, dump = img_detection_rectangle(setup.frame, setup.death_match_ok_img)
        death_match_hell_rectangle, DEATH_MATCH_HELL, dump = img_detection_rectangle(setup.frame, setup.death_match_hell_img)
        ai_rectangle, AI, dump = img_detection_rectangle(setup.frame, setup.ai_img)
        invite_ai_rectangle, INVITE_AI, dump = img_detection_rectangle(setup.frame, setup.invite_ai_img)
        preparation_complete_rectangle, PREPARATION_COMPLETE, dump = img_detection_rectangle(setup.frame, setup.preparation_complete_img)
        death_match_start_rectangle, DEATH_MATCH_START, dump = img_detection_rectangle(setup.frame, setup.death_match_start_img)
        auto_rectangle, AUTO, dump = img_detection_rectangle(setup.frame, setup.auto_img)
        death_match_success_ok_rectangle, DEATH_MATCH_SUCCESS_OK, dump = img_detection_rectangle(setup.frame, setup.death_match_success_ok_img)

        if BATTLE:
            use_card(setup.frame_top, setup.frame_left, battle_rectangle)
        elif BOSS_BATTLE:
            use_card(setup.frame_top, setup.frame_left, boss_battle_rectangle)
        elif DEATH_MATCH_CHANCE_0:
            use_card(setup.frame_top-20, setup.frame_left, death_match_chance_0_rectangle)
        elif BOSS_BATTLE_EXTREME and not DEATH_MATCH_HELL:
            use_card(setup.frame_top, setup.frame_left, boss_battle_extreme_rectangle)
        elif AUTO_CLEAR and not START_AUTO_CLEAR and not OK and not USE_STAMINA_POTION:
            use_card(setup.frame_top, setup.frame_left, auto_clear_rectangle)
        elif START_AUTO_CLEAR:
            use_card(setup.frame_top, setup.frame_left, start_auto_clear_rectangle)
        elif USE_STAMINA_POTION:
            use_card(setup.frame_top, setup.frame_left, use_stamina_potion_rectangle)
        elif OK and not DEATH_MATCH_OK:
            use_card(setup.frame_top, setup.frame_left, ok_rectangle)
        elif DEATH_MATCH_OK:
            use_card(setup.frame_top, setup.frame_left, death_match_ok_rectangle)
        elif DEATH_MATCH_HELL:
            use_card(setup.frame_top, setup.frame_left, death_match_hell_rectangle)
        elif AI:
            use_card(setup.frame_top, setup.frame_left, ai_rectangle)
        elif INVITE_AI:
            use_card(setup.frame_top, setup.frame_left, invite_ai_rectangle)
        elif PREPARATION_COMPLETE and not AI:
            use_card(setup.frame_top, setup.frame_left, preparation_complete_rectangle)
        elif DEATH_MATCH_START:
            use_card(setup.frame_top, setup.frame_left, death_match_start_rectangle)
        elif AUTO:
            use_card(setup.frame_top, setup.frame_left, auto_rectangle)
        elif DEATH_MATCH_SUCCESS_OK:
            use_card(setup.frame_top, setup.frame_left, death_match_success_ok_rectangle)
            #print("success")


# def daily_menu():
#     if setup.current_time - setup.menu_delay_time >= setup.menu_delay:
#         setup.menu_delay_time = setup.current_time
#
#         tavern_rectangle, TAVERN, dump = img_detection_rectangle(setup.frame, setup.tavern_img)
#         quests_rectangle, QUESTS, dump = img_detection_rectangle(setup.frame, setup.quests_img)
#         heroes_rectangle, HEROES, dump = img_detection_rectangle(setup.frame, setup.heroes_img)
#         draw_rectangle, DRAW, dump = img_detection_rectangle(setup.frame, setup.draw_img)
#         shop_rectangle, SHOP, dump = img_detection_rectangle(setup.frame, setup.shop_img)
#
#         menu_rectangle, MENU, dump = img_detection_rectangle(setup.frame, setup.menu_img)
#         friends_rectangle, FRIENDS, dump = img_detection_rectangle(setup.frame, setup.friends_img)
#         send_all_rectangle, SEND_ALL, dump = img_detection_rectangle(setup.frame, setup.send_all_img)
#
#         mail_rectangle, MAIL, dump = img_detection_rectangle(setup.frame, setup.mail_img)
#         friendship_rectangle, FRIENDSHIP, dump = img_detection_rectangle(setup.frame, setup.friendship_img)
#         claim_all_rectangle, CLAIM_ALL, dump = img_detection_rectangle(setup.frame, setup.claim_all_img, threshold=0.95)
#         claim_all_gray_rectangle, CLAIM_ALL_GRAY, dump = img_detection_rectangle(setup.frame, setup.claim_all_gray_img, threshold=0.95)
#
#         if setup.FRIENDS_STATE:
#             if MENU and not FRIENDS and not SEND_ALL:
#                 use_card(setup.frame_top, setup.frame_left, menu_rectangle)
#             elif FRIENDS:
#                 use_card(setup.frame_top, setup.frame_left, friends_rectangle)
#             elif SEND_ALL:
#                 use_card(setup.frame_top, setup.frame_left, send_all_rectangle)
#                 setup.FRIENDS_STATE = False
#                 setup.MAIL_STATE = True
#                 return
#
#         if setup.MAIL_STATE:
#             if MAIL:
#                 use_card(setup.frame_top, setup.frame_left, mail_rectangle)
#             elif FRIENDSHIP:
#                 use_card(setup.frame_top, setup.frame_left, friendship_rectangle)
#             elif CLAIM_ALL:
#                 use_card(setup.frame_top, setup.frame_left, claim_all_rectangle)
#             elif CLAIM_ALL_GRAY:
#                 right_click_mouse(setup.frame_top, setup.frame_left, setup.frame_width, setup.frame_height)
#                 setup.MAIL_STATE = False
#                 setup.SHOP_STATE = True
#                 setup.EQUIPMENT_DRAW_STATE = True
#                 return
#
#         if setup.SHOP_STATE:
#             if not SHOP:
#                 right_click_mouse(setup.frame_top, setup.frame_left, setup.frame_width, setup.frame_height)
#             elif setup.EQUIPMENT_DRAW_STATE:
#                 pass  # TODO
#             elif setup.COIN_SHOP_STATE:
#                 pass
#             elif SHOP:
#                 use_card(setup.frame_top, setup.frame_left, shop_rectangle)


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


def deer_rules(skill_name, skill_option):
    if setup.phase == 2:
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
    elif setup.phase == 4:
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
