from setup import *
import setup

from tkinter import Button, Label
from PIL import Image, ImageTk
import cv2


def bird_auto():
    setup.DEER_AUTO = False
    setup.BIRD_AUTO = True


def deer_auto():
    setup.BIRD_AUTO = False
    setup.DEER_AUTO = True


def start_stop_mouse(*unused):
    setup.MOUSE_ACTIVE = not setup.MOUSE_ACTIVE
    if setup.MOUSE_ACTIVE:
        setup.mouse_text.set("Stop Mouse")
    else:
        setup.mouse_text.set("Start Mouse")


def stop_auto(*unused):
    setup.BIRD_AUTO = False
    setup.DEER_AUTO = False


def quitGUI(*unused):
    setup.RUN_LOOP = False
    setup.root.destroy()
    cv2.destroyAllWindows()


def GUI():
    tkinter_width = str(800)
    tkinter_height = str(500)

    setup.root.title("Auto 7dsgc")
    setup.root.geometry(tkinter_width+"x"+tkinter_height + "+1111+0")
    setup.root.attributes("-topmost", True)
    setup.root.attributes("-alpha", 0.5)

    setup.skill_label_frame = Label(setup.root, bg="black")
    setup.skill_label_frame.grid(row=0, column=1, rowspan=4, columnspan=14, padx=50, pady=50)

    # bird
    bird_button = Button(setup.root, text="Bird", command=bird_auto, width=10)
    bird_button.grid(row=4, column=1)

    bird_completions_label = Label(setup.root, textvariable=setup.bird_completions_text, font=("Arial", 10))
    bird_completions_label.grid(row=5, column=1)

    bird_failures_label = Label(setup.root, textvariable=setup.bird_failures_text, font=("Arial", 10))
    bird_failures_label.grid(row=6, column=1)

    # deer
    deer_button = Button(setup.root, text="Deer", command=deer_auto, width=10)
    deer_button.grid(row=4, column=2)

    deer_completions_label = Label(setup.root, textvariable=setup.deer_completions_text, font=("Arial", 10))
    deer_completions_label.grid(row=5, column=2)

    deer_failures_label = Label(setup.root, textvariable=setup.deer_failures_text, font=("Arial", 10))
    deer_failures_label.grid(row=6, column=2)

    # mouse
    setup.mouse_text.set("Stop Mouse")
    mouse_button = Button(setup.root, textvariable=setup.mouse_text, command=start_stop_mouse, width=10)
    #setup.root.bind("<p>", start_stop_mouse)
    mouse_button.grid(row=6, column=14)

    # stop
    stop_button = Button(setup.root, text="Stop Auto", command=stop_auto, width=10)
    #setup.root.bind("<s>", stop_auto)
    stop_button.grid(row=7, column=14)

    # quit
    quit_button = Button(setup.root, text="Quit", command=quitGUI, width=10)
    #setup.root.bind("<q>", quitGUI)
    quit_button.grid(row=8, column=14)


def createGUI():
    skill_img = cv2.cvtColor(setup.skill_frame, cv2.COLOR_BGR2RGB)
    skill_img = ImageTk.PhotoImage(Image.fromarray(skill_img))
    setup.skill_label_frame['image'] = skill_img

    setup.bird_completions_text.set("Completions: " + str(setup.bird_completion_counter))
    setup.bird_failures_text.set("Failures: " + str(setup.bird_failure_counter))
    setup.deer_completions_text.set("Completions: " + str(setup.deer_completion_counter))
    setup.deer_failures_text.set("Failures: " + str(setup.deer_failure_counter))

    setup.root.update()
