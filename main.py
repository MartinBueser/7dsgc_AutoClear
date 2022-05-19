import cv2
import numpy as np
from mss import mss
import pyautogui as pg
import time
from functions import *
import keyboard
from setup import *
import setup

# +++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
boss_name = "bird"  # bird, deer
# char_names = ["brun", "mat", "jor", "mel"]  # brun, mag, mat, gow, mel, jor, skadi, one
if boss_name == "bird":
    char_names = ["brun", "mel", "mat", "gow"]
elif boss_name == "deer":
    char_names = ["skadi", "jor", "mel", "one"]
# +++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++

print(boss_name)
print(char_names)
setup.init(boss_name)
setup_frame()
setup_menu(boss_name)
setup_cards(char_names)

## screenshot of display
sct = mss()


while True:
    ## capture area on screen
    ready_frame = cv2.cvtColor(np.array(sct.grab(setup.ready_frame_box)), cv2.COLOR_BGRA2BGR)
    phase_frame = cv2.cvtColor(np.array(sct.grab(setup.phase_frame_box)), cv2.COLOR_BGRA2BGR)
    skill_frame = cv2.cvtColor(np.array(sct.grab(setup.skill_frame_box)), cv2.COLOR_BGRA2BGR)
    ok_reset_frame = cv2.cvtColor(np.array(sct.grab(setup.ok_reset_frame_box)), cv2.COLOR_BGRA2BGR)
    select_stage_frame = cv2.cvtColor(np.array(sct.grab(setup.select_stage_frame_box)), cv2.COLOR_BGRA2BGR)
    confirm_reset_frame = cv2.cvtColor(np.array(sct.grab(setup.confirm_reset_frame_box)), cv2.COLOR_BGRA2BGR)
    save_team_frame = cv2.cvtColor(np.array(sct.grab(setup.save_team_frame_box)), cv2.COLOR_BGRA2BGR)
    confirm_team_frame = cv2.cvtColor(np.array(sct.grab(setup.confirm_team_frame_box)), cv2.COLOR_BGRA2BGR)
    use_stamina_potion_frame = cv2.cvtColor(np.array(sct.grab(setup.use_stamina_potion_frame_box)), cv2.COLOR_BGRA2BGR)


### ready detection
    READY = img_detection(ready_frame, setup.ready_img)
    #print("READY: " + str(READY))


### phase detection
    if READY:
        phase = phase_detection(phase_frame, [setup.phase1_img, setup.phase2_img, setup.phase3_img, setup.phase4_img])
        print("phase: " + str(phase))


### skill detection
    if READY:
        ## compare skill_frame with skill images
        for p in Skills:
            p.result = cv2.matchTemplate(skill_frame, p.img, cv2.TM_CCOEFF_NORMED)

        ## (get values and locations of comparison)
        for p in Skills:
            minVal, p.maxVal, minLoc, p.maxLoc = cv2.minMaxLoc(p.result)  # minVal and minLoc neglected

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
                cv2.rectangle(skill_frame, (x, y), (x + w, y + h), p.color, p.thickness)
                p.count = int(p.rectangles.size / 4)


### queue special skills
    ## gow rank up activation
    if "gow" in char_names:
        gow2_lvl1_counter = 0
        gow2_lvl2_counter = 0
        gow2_lvl3_counter = 0
        if READY:
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

    if "brun" in char_names:
        brun2_lvl1_counter = 0
        brun2_lvl2_counter = 0
        brun2_lvl3_counter = 0
        if READY and phase != 4:
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

    if "mel" in char_names and boss_name == "bird":
        mel2_lvl1_counter = 0
        mel2_lvl2_counter = 0
        mel2_lvl3_counter = 0
        if READY and phase != 4:
            for p in Skills:
                if p.name == "mel2" and p.count > 0:
                    if p.level == 1:
                        mel2_lvl1_counter = p.count
                    elif p.level == 2:
                        mel2_lvl2_counter = p.count
                    elif p.level == 3:
                        mel2_lvl3_counter = p.count

            mel2_counter = mel2_lvl1_counter + mel2_lvl2_counter + mel2_lvl3_counter
            if mel2_counter >= 2:
                for p in Skills:
                    if p.name == "mel2" and p.count > 0:
                        if p.level == 1:
                            setup.skillQueue.put((70, p, "use"))
                            break
                        elif p.level == 2:
                            setup.skillQueue.put((80, p, "use"))
                            break
                        elif p.level == 3:
                            setup.skillQueue.put((100, p, "use"))
                            break

    ## mag buff activation
    if "mag" in char_names:
        mag2_counter = 0
        if READY:
            for p in Skills:
                if p.name == "mag2" and p.count > 0:
                    mag2_counter = mag2_counter + 1

            if mag2_counter >= 3:
                for p in Skills:
                    if p.name == "mag2" and p.count > 0 and p.level < 3:
                        setup.mag2_delay = 0

    ## mat taunt activation
    if "mat" in char_names:
        mat2_counter = 0
        if READY:
            for p in Skills:
                if p.name == "mat2" and p.count > 0:
                    mat2_counter = mat2_counter + 1

            if mat2_counter >= 3:
                for p in Skills:
                    if p.name == "mat2" and p.count > 0 and p.level < 3:
                        setup.mat2_delay = 0

### queue skills
    if READY:
        if boss_name == "bird":
            if phase != 4:
                for p in Skills:
                    if p.count > 0:
                        phase123_bird(p)
            elif phase == 4:
                for p in Skills:
                    if p.count > 0:
                        phase4_bird(p)
        elif boss_name == "deer":
            if phase == 1:
                for p in Skills:
                    if p.count > 0:
                        phase1_deer(p)
            elif phase == 2:
                for p in Skills:
                    if p.count > 0:
                        phase2_deer(p)
            elif phase == 3:
                for p in Skills:
                    if p.count > 0:
                        phase3_deer(p)
            elif phase == 4:
                for p in Skills:
                    if p.count > 0:
                        phase4_deer(p)


### process queue
    if setup.skillQueue.qsize() == 0 and READY:
        use_card(setup.ready_frame_top, setup.ready_frame_left, img_detection_rectangle(ready_frame, setup.ready_img))  # skip turn

    if setup.skillQueue.qsize() >= 1 and not keyboard.is_pressed("p"):# and keyboard.is_pressed("o"):
        queue_priority, skill_object, skill_option = setup.skillQueue.get()
        print(str(queue_priority) + " " + str(skill_object.name) + " " + str(skill_option))

        if skill_option == "use":
            use_card(setup.skill_frame_top, setup.skill_frame_left, skill_object.rectangles)
        elif skill_option == "move":
            move_card(setup.skill_frame_top, setup.skill_frame_left, skill_object.rectangles)

        if boss_name == "bird":
            time.sleep(0.5)
        else:
            time.sleep(1.5)

        ## bird special counters
        if boss_name == "bird":
            # print(setup.mat2_delay_counter)
            # print(str(setup.mat2_delay) + " " + str(skill_object.level))

            # if mag2_delay_counter == 0:
            #     setup.mag2_delay = 0
            # else:
            #     mag2_delay_counter = mag2_delay_counter - 1

            # if skill_object.name == "mag2":
            #     setup.mag2_delay = 10
            #     mag2_counter = 6

            if phase == 3 and setup.mat2_delay_counter > 3:
                setup.mat2_delay_counter = 3

            if setup.mat2_delay_counter == 0:
                setup.mat2_delay = 0
            else:
                setup.mat2_delay_counter = setup.mat2_delay_counter - 1

            if skill_object.name == "mat2":
                setup.mat2_delay = 30
                if phase != 3:
                    setup.mat2_delay_counter = 11
                else:
                    setup.mat2_delay_counter = 3

        elif boss_name == "deer":
            if phase == 2:
                if skill_option == "use":
                    if skill_object.name == "skadi1" or skill_object.name == "skadi2" or skill_object.name == "skadi_ult":
                        setup.red_card_delay_phase2 = 100
                        setup.green_card_delay_phase2 = 0
                        setup.blue_card_delay_phase2 = 100
                    if skill_object.name == "jor1" or skill_object.name == "jor2" or skill_object.name == "jor_ult":
                        setup.red_card_delay_phase2 = 100
                        setup.green_card_delay_phase2 = 100
                        setup.blue_card_delay_phase2 = 0
                    if skill_object.name == "one1" or skill_object.name == "one2" or skill_object.name == "one_ult":
                        setup.red_card_delay_phase2 = 0
                        setup.green_card_delay_phase2 = 100
                        setup.blue_card_delay_phase2 = 100
            elif phase == 4:
                if skill_option == "use":
                    if skill_object.name == "skadi1" or skill_object.name == "skadi2" or skill_object.name == "skadi_ult":
                        setup.red_card_delay_phase4 = 100
                        setup.green_card_delay_phase4 = 0
                        setup.blue_card_delay_phase4 = 100
                    if skill_object.name == "jor1" or skill_object.name == "jor2" or skill_object.name == "jor_ult":
                        setup.red_card_delay_phase4 = 100
                        setup.green_card_delay_phase4 = 100
                        setup.blue_card_delay_phase4 = 0
                    if skill_object.name == "one1" or skill_object.name == "one2" or skill_object.name == "one_ult":
                        setup.red_card_delay_phase4 = 0
                        setup.green_card_delay_phase4 = 100
                        setup.blue_card_delay_phase4 = 100

    while not setup.skillQueue.empty():
        flush = setup.skillQueue.get()

### menu navigation
    menu(boss_name, ok_reset_frame, confirm_reset_frame, select_stage_frame, save_team_frame, confirm_team_frame, use_stamina_potion_frame)


### completion and failure counter
    cv2.putText(skill_frame, f"Completions: {setup.completion_counter}   Failures: {setup.failure_counter}", (5, 20), cv2.FONT_HERSHEY_SIMPLEX, 0.6, (0, 255, 0), 2, cv2.LINE_AA)


### show
    # cv2.imshow("phase", phase_frame)
    # cv2.imshow("ready", ready_frame)
    cv2.imshow("skill", skill_frame)
    # cv2.imshow("ok", ok_reset_frame)
    # cv2.imshow("select stage", select_stage_frame)
    # cv2.imshow("confirm reset", confirm_reset_frame)
    # cv2.imshow("save team", save_team_frame)
    # cv2.imshow("confirm team", confirm_team_frame)
    # cv2.imshow("use stamina portion", use_stamina_potion_frame)


### end
    ## reset skill count
    for p in Skills:
        # print(p.name)
        p.count = 0

    ## take a break
    # time.sleep(1.5)

    ## quit by pressing q
    if (cv2.waitKey(1) & 0xFF) == ord("q"):
        print("Completions: " + str(setup.completion_counter))
        print("Failures: " + str(setup.failure_counter))
        break
cv2.destroyAllWindows()
