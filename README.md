# 7dsgc_AutoClear
This program is able to clear floor 1 of bird and deer Demonic Boss Battle in auto clear mode. <br>
It works by capturing your main screen every few second, analyzing it and executing specific mouse movements to auto clear the battle.
<br>

### Useful hotkeys
Press "q" inside the skill window to quit <br>
Hold "p" to pause mouse movements
<br>

### Project Structure
3 files (main.py, setup.py, functions.py) <br>
1 folder (images) including all pictures needed to run the code 
<br><br>


## Setup
The program was created on Windows 10 with PyCharm Community Edition (2022.1) in Python. <br>
My main screen is 1920x1080 and I am running the 7dsgc desktop app on fullscreen. <br>

It may be possible that you are able to instantly run the code by executing main.py. <br>
If not follow these steps:
1. Tutorial for python and PyCharm installation https://www.youtube.com/watch?v=WJynvGY-2wk
2. Open 7dsgc_AutoClear-main with PyCharm (Pay attention to the folder structure)
3. Add the needed libraries to your project ("File->Settings...->Project: [Name]->Python Interpreter->+" (opencv-python, numpy, mss, pyautogui, time, keyboard)
4. Execute the program by right clicking main.py in the left window and press "Run 'main'"
5. The program will start doing something as soon as it sees the demonic beast battle stages. (Run PyCharm as administrator if mouse clicks are not working)
<br><br>


## Screen adjustments
If you are running the program on a 1920x1080 display with the desktop app on fullscreen, you probably wont need to read this part. <br><br>
Due to the screen capture working principle it may be possible that the program isn't working for you (e.g. different screen size, ...). You can adjust the screen capture boxes in setup.py (setup_frame()). (Display the frames in main.py bottom under ###show) <br><br>
It is also possible that you cannot detect areas/skills because they are just some screenshots of my setup. You can replace every image in the images folder with your own setup (take care that it is still .png/.PNG). (Try to keep the same image area) <br><br>
In addition, you can change the threshold values of each skill card (how similar the reference image has to be to the screen image) in the bottom of setup.py
<br><br>


## Teams
Team and boss battle is set at the top of main.py
You can use your own teams but you have to code them yourself. <br><br>
E.g. if you want to use red Tarmiel instead of Skadi, you could replace every skadi image with a tarmiel one and keep the name (pretty dirty)<br>
Otherwise, you have to add his cards to "setup_cards(boss_name)" in setup.py and replace every skadi call (in main.py and functions.py) with them <br><br>
If you want to do a completely different clear technique, you will have to adjust the phase functions in functions.py and the call of them in main.py (thats a lot of work)
<br>
#### Bird Team (19/20 runs are successful):
![](/readme_images/bird_team.PNG)
#### Bird Artifact:
![](/readme_images/bird_artifact.PNG)

#### Deer Team (20/20 runs are successful):
![](/readme_images/deer_team.PNG)
#### Deer Artifact:
![](/readme_images/deer_artifact.PNG)
