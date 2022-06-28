from setup import *
import setup

from tkinter import Button, Label, Entry
from PIL import Image, ImageTk
import cv2


def bird_auto():
    stop_auto()
    setup.skill_delay = 2.0
    setup.menu_delay = 1.0
    setup.BIRD_AUTO = True


def deer_auto():
    stop_auto()
    setup.DEER_AUTO = True


def death_match_button_function():
    stop_auto()
    setup.DEATH_MATCH = True


# def daily_missions():
#     stop_auto()
#     setup.DAILY = True


def start_stop_mouse():
    setup.MOUSE_ACTIVE = not setup.MOUSE_ACTIVE
    if setup.MOUSE_ACTIVE:
        setup.mouse_text.set("Pause")
    else:
        setup.mouse_text.set("Resume")


def stop_auto():
    setup.BIRD_AUTO = False
    setup.DEER_AUTO = False
    setup.DEATH_MATCH = False
    setup.DAILY = False


def set_skill_delay():
    try:
        setup.skill_delay = float(setup.skill_delay_text.get())
    except ValueError:
        pass#print("Input is not a number")


def set_menu_delay():
    try:
        setup.menu_delay = float(setup.menu_delay_text.get())
    except ValueError:
        pass#print("Input is not a number")


def quitGUI():
    setup.RUN_LOOP = False
    setup.root.destroy()
    cv2.destroyAllWindows()


def GUI():
    tkinter_width = str(800)
    tkinter_height = str(500)
    button_width = 12

    setup.root.title("Auto 7dsgc")
    setup.root.geometry(tkinter_width+"x"+tkinter_height + "+1111+0")
    setup.root.attributes("-topmost", True)
    # setup.root.attributes("-alpha", 0.5)

    setup.skill_label_frame = Label(setup.root, bg="black")
    setup.skill_label_frame.grid(row=0, column=1, rowspan=4, columnspan=14, padx=50, pady=50)


    # bird
    bird_button = Button(setup.root, text="Bird", command=bird_auto, width=button_width)
    bird_button.grid(row=4, column=1)

    bird_completions_label = Label(setup.root, textvariable=setup.bird_completions_text, font=("Arial", 10))
    bird_completions_label.grid(row=5, column=1)

    bird_failures_label = Label(setup.root, textvariable=setup.bird_failures_text, font=("Arial", 10))
    bird_failures_label.grid(row=6, column=1)


    # deer
    deer_button = Button(setup.root, text="Deer", command=deer_auto, width=button_width)
    deer_button.grid(row=4, column=2)

    deer_completions_label = Label(setup.root, textvariable=setup.deer_completions_text, font=("Arial", 10))
    deer_completions_label.grid(row=5, column=2)

    deer_failures_label = Label(setup.root, textvariable=setup.deer_failures_text, font=("Arial", 10))
    deer_failures_label.grid(row=6, column=2)


    # death match
    death_match_button = Button(setup.root, text="Death Match", command=death_match_button_function, width=button_width)
    death_match_button.grid(row=4, column=13)


    # # daily missions
    # daily_button = Button(setup.root, text="Daily Missions", command=daily_missions, width=button_width)
    # daily_button.grid(row=4, column=14)


    # mouse
    setup.mouse_text.set("Pause")
    mouse_button = Button(setup.root, textvariable=setup.mouse_text, command=start_stop_mouse, width=button_width)
    mouse_button.grid(row=6, column=14)


    # stop
    stop_button = Button(setup.root, text="Stop Auto", command=stop_auto, width=button_width)
    stop_button.grid(row=7, column=14)


    # skill delay
    set_skill_delay_button = Button(setup.root, text="Set Skill Delay", command=set_skill_delay, width=button_width)
    set_skill_delay_button.grid(row=9, column=1)

    e_skill_delay = Entry(setup.root, textvariable=setup.skill_delay_text, width=10)
    e_skill_delay.grid(row=10, column=1, pady=5)

    # menu delay
    set_menu_delay_button = Button(setup.root, text="Set Menu Delay", command=set_menu_delay, width=button_width)
    set_menu_delay_button.grid(row=9, column=2)

    e_menu_delay = Entry(setup.root, textvariable=setup.menu_delay_text, width=10)
    e_menu_delay.grid(row=10, column=2, pady=5)


    # quit
    quit_button = Button(setup.root, text="Quit", command=quitGUI, width=button_width)
    quit_button.grid(row=11, column=14)


def createGUI():
    skill_img = cv2.cvtColor(setup.skill_frame, cv2.COLOR_BGR2RGB)
    skill_img = ImageTk.PhotoImage(Image.fromarray(skill_img))
    setup.skill_label_frame['image'] = skill_img

    setup.bird_completions_text.set("S1:" + str(setup.bird_completion_counter1) + "  S2:" + str(setup.bird_completion_counter2) + "  S3:" + str(setup.bird_completion_counter3))
    setup.bird_failures_text.set("F1:" + str(setup.bird_failure_counter1) + "  F2:" + str(setup.bird_failure_counter2) + "  F3:" + str(setup.bird_failure_counter3))
    setup.deer_completions_text.set("Completions: " + str(setup.deer_completion_counter))
    setup.deer_failures_text.set("Failures: " + str(setup.deer_failure_counter))

    setup.skill_delay_text.set(setup.skill_delay)
    setup.menu_delay_text.set(setup.menu_delay)

    setup.root.update()
