import cv2
import numpy as np
from mss import mss
import pyautogui as pg
import time
from functions import *
import keyboard
from setup import *
import setup

from tkinter import *
from PIL import Image, ImageTk

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
setup.init()#boss_name)
setup_frame()
setup_menu()#boss_name)
setup_cards()#char_names)
MOUSE_ACTIVE = True
BIRD_AUTO = False
DEER_AUTO = False

## screenshot of display
sct = mss()


## tkinter(GUI) stuff
tkinter_width = str(800)
tkinter_height = str(500)

root = Tk()
root.title("Auto 7dsgc")
root.geometry(tkinter_width+"x"+tkinter_height)
root.attributes("-topmost", True)

skill_label_frame = Label(root, bg="black")
skill_label_frame.grid(row=0, column=1, rowspan=4, columnspan=14, padx=50, pady=50)


def quitGUi():
    global run_loop
    run_loop = False
    cv2.destroyAllWindows()
    root.destroy()


exit_button = Button(root, text="Exit", command=quitGUi, width=10)
exit_button.grid(row=8, column=14)


def start_stop_mouse():
    global MOUSE_ACTIVE
    MOUSE_ACTIVE = not MOUSE_ACTIVE
    if MOUSE_ACTIVE:
        mouse_text.set("Stop Mouse")
    else:
        mouse_text.set("Start Mouse")


mouse_text = StringVar()
mouse_text.set("Stop Mouse")
mouse_button = Button(root, textvariable=mouse_text, command=start_stop_mouse, width=10)
mouse_button.grid(row=6, column=14)


def stop_auto():
    global BIRD_AUTO
    BIRD_AUTO = False
    global DEER_AUTO
    DEER_AUTO = False


stop_button = Button(root, text="Stop", command=stop_auto, width=10)
stop_button.grid(row=7, column=14)


def bird_auto():
    global DEER_AUTO
    DEER_AUTO = False
    global BIRD_AUTO
    BIRD_AUTO = True


bird_button = Button(root, text="Bird", command=bird_auto, width=10)
bird_button.grid(row=4, column=1)

bird_completions_text = StringVar()
# bird_completions_text.set("Completions: " + str(0))
bird_completions_label = Label(root, textvariable=bird_completions_text, font=("Arial", 10))
bird_completions_label.grid(row=5, column=1)

bird_failures_text = StringVar()
# bird_failures_text.set("Failures: " + str(0))
bird_failures_label = Label(root, textvariable=bird_failures_text, font=("Arial", 10))
bird_failures_label.grid(row=6, column=1)


def deer_auto():
    global BIRD_AUTO
    BIRD_AUTO = False
    global DEER_AUTO
    DEER_AUTO = True


deer_button = Button(root, text="Deer", command=deer_auto, width=10)
deer_button.grid(row=4, column=2)

deer_completions_text = StringVar()
# deer_completions_text.set("Completions: " + str(0))
deer_completions_label = Label(root, textvariable=deer_completions_text, font=("Arial", 10))
deer_completions_label.grid(row=5, column=2)

deer_failures_text = StringVar()
# deer_failures_text.set("Failures: " + str(0))
deer_failures_label = Label(root, textvariable=deer_failures_text, font=("Arial", 10))
deer_failures_label.grid(row=6, column=2)


run_loop = True
while run_loop:
    skill_frame = cv2.cvtColor(np.array(sct.grab(setup.skill_frame_box)), cv2.COLOR_BGRA2BGR)
    if BIRD_AUTO or DEER_AUTO:
        ## capture area on screen
        ready_frame = cv2.cvtColor(np.array(sct.grab(setup.ready_frame_box)), cv2.COLOR_BGRA2BGR)
        phase_frame = cv2.cvtColor(np.array(sct.grab(setup.phase_frame_box)), cv2.COLOR_BGRA2BGR)
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
        if BIRD_AUTO:
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

        if BIRD_AUTO:
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

        if BIRD_AUTO:
            mel1_lvl1_counter = 0
            mel1_lvl2_counter = 0
            mel1_lvl3_counter = 0
            if READY and phase != 4:
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

        ## mag buff activation
        if BIRD_AUTO:
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
        if BIRD_AUTO:
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
            if BIRD_AUTO:
                if phase != 4:
                    for p in Skills:
                        if p.count > 0:
                            phase123_bird(p)
                elif phase == 4:
                    for p in Skills:
                        if p.count > 0:
                            phase4_bird(p)
            elif DEER_AUTO:
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
        if MOUSE_ACTIVE:
            if setup.skillQueue.qsize() == 0 and READY:# and keyboard.is_pressed("o"):
                use_card(setup.ready_frame_top, setup.ready_frame_left, img_detection_rectangle(ready_frame, setup.ready_img))  # skip turn

            if setup.skillQueue.qsize() >= 1 and not keyboard.is_pressed("p"):# and keyboard.is_pressed("o"):
                queue_priority, skill_object, skill_option = setup.skillQueue.get()
                print(str(queue_priority) + " " + str(skill_object.name) + " " + str(skill_option))

                if skill_option == "use":
                    use_card(setup.skill_frame_top, setup.skill_frame_left, skill_object.rectangles)
                elif skill_option == "move":
                    move_card(setup.skill_frame_top, setup.skill_frame_left, skill_object.rectangles)

                if BIRD_AUTO:
                    time.sleep(0.5)
                elif DEER_AUTO:
                    time.sleep(1.5)
                else:
                    time.sleep(1.5)

                ## bird special counters
                if BIRD_AUTO:
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

                elif DEER_AUTO:
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
        if MOUSE_ACTIVE:
            menu(BIRD_AUTO, DEER_AUTO, ok_reset_frame, confirm_reset_frame, select_stage_frame, save_team_frame, confirm_team_frame, use_stamina_potion_frame)


    ### completion and failure counter
        #cv2.putText(skill_frame, f"Completions: {setup.completion_counter}   Failures: {setup.failure_counter}", (5, 20), cv2.FONT_HERSHEY_SIMPLEX, 0.6, (0, 255, 0), 2, cv2.LINE_AA)


    ### show
        # cv2.imshow("phase", phase_frame)
        # cv2.imshow("ready", ready_frame)
        #cv2.imshow("skill", skill_frame)
        #cv2.setWindowProperty("skill", cv2.WND_PROP_TOPMOST, 1)
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

    skill_img = cv2.cvtColor(skill_frame, cv2.COLOR_BGR2RGB)
    skill_img = ImageTk.PhotoImage(Image.fromarray(skill_img))
    skill_label_frame['image'] = skill_img

    bird_completions_text.set("Completions: " + str(setup.bird_completion_counter))
    bird_failures_text.set("Failures: " + str(setup.bird_failure_counter))
    deer_completions_text.set("Completions: " + str(setup.deer_completion_counter))
    deer_failures_text.set("Failures: " + str(setup.deer_failure_counter))

    root.update()


        ## quit by pressing q
        # if (cv2.waitKey(1) & 0xFF) == ord("q"):
        #     print("Completions: " + str(setup.completion_counter))
        #     print("Failures: " + str(setup.failure_counter))
        #     break
# cv2.destroyAllWindows()
