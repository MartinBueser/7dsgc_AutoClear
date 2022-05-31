# 7dsgc_AutoClear
This program is able to clear floor 1 of bird and deer Demonic Boss Battle in auto clear mode. <br>
It works by capturing your main screen every few second, analyzing it and executing specific mouse movements to auto clear the battle.
<br>

### Useful hotkeys
Press "q" to quit <br>
Press "p" to pause/resume mouse movements <br>
Press "s" to stop auto clear
<br>

### Project Structure
4 files (main.py, setup.py, functions.py, tkinter_gui.py) <br>
1 folder (images) including all pictures needed to run the code<br>
1 executable file (main.exe) to run the program without installing anything
<br><br>


## Quick Guide
1. Click on "Code" and select "Download ZIP"
2. Extract the folder
3. Navigate to "main.exe"
4. Open 7dsgc Desktop app
5. Resize the window to 1920x1080
6. Navigate to any demonic beast battle
7. Execute "main.exe" as administrator (Windows will probably warn you a few times)
8. Start by clicking on "Bird" or "Deer"

You can adjust "Set Skill Delay" and "Set Menu Delay" to fit you game/computer speed (my computer is fine with 2.5 skill delay; my laptop needs 3.5 skill delay) (the program may use an older picture of your screen if your computer is slow (->clicks on a wrong skill)) (this can be seen pretty good in phase 2 of deer)<br><br>
The GUI is half transparent because I want to see the damage numbers :P
<br><br>


## Setup
The program was created on Windows 10 with PyCharm Community Edition (2022.1) in Python. <br>
My main screen is 1920x1080 and I am running the 7dsgc desktop app on fullscreen. <br>

You should be able to run the program immediately by executing main.exe (run as administrator to allow the program to click).

If you want to edit the code, follow these steps (you may have to restart pycharm/your computer a few times):
1. Tutorial for python and PyCharm installation https://www.youtube.com/watch?v=WJynvGY-2wk
2. Open 7dsgc_AutoClear-main with PyCharm (Pay attention to the folder structure)
3. Add the needed libraries to your project ("File->Settings...->Project: [Name]->Python Interpreter->+" (opencv-python, numpy, mss, pyautogui, time, keyboard, tkinter, PIL)
4. Execute the program by right clicking main.py in the left window and press "Run 'main'"
5. The program will start doing something as soon as it sees the demonic beast battle stages
<br><br>


## Screen adjustments
If you are running the program on a 1920x1080 display with the desktop app on fullscreen, you probably wont need to read this part. <br><br>
Due to the screen capture working principle it may be possible that the program isn't working for you (e.g. different screen size, ...). You can adjust the screen capture boxes in setup.py (setup_frame()). (Display the frames in main.py bottom under ###show) <br><br>
It is also possible that you cannot detect areas/skills because they are just some screenshots of my setup. You can replace every image in the images folder with your own setup (take care that it is still .png/.PNG). (Try to keep the same image area) <br><br>
In addition, you can change the threshold values of each skill card (how similar the reference image has to be to the screen image) in the bottom of setup.py
<br><br>


## Teams
You can see my teams below. The boss battle can be switched freely in the gui.<br>
You can use your own teams but you have to code them yourself. <br><br>
E.g. if you want to use red Tarmiel instead of Skadi, you could replace every skadi image with a tarmiel one and keep the name (pretty dirty)<br>
Otherwise, you have to add his cards to "setup_cards(boss_name)" in setup.py and replace every skadi call (in main.py and functions.py) with them <br><br>
If you want to do a completely different clear technique, you will have to adjust the phase functions in functions.py and the call of them in main.py (thats a lot of work)
<br>
#### Bird Team (>90% success rate):
![](/readme_images/bird_team.PNG)
#### Bird Artifact:
![](/readme_images/bird_artifact.PNG)

#### Deer Team (>95% success rate):
![](/readme_images/deer_team.PNG)
#### Deer Artifact:
![](/readme_images/deer_artifact.PNG)
