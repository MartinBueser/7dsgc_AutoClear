# 7dsgc_AutoClear
This program is able to clear floor 1 of bird and deer Demonic Boss Battle in auto clear mode. <br>
It works by capturing your main screen every few second, analyzing it and executing specific mouse movements to auto clear the battle.

### Useful hotkeys
Press "q" inside the skill window to quit <br>
Hold "p" to pause mouse movements

### Project Structure
3 files (main.py, setup.py, functions.py) <br>
1 folder (images) including all pictures needed to run the code 

## Setup
The program was written on Windows 10 with PyCharm Community Edition (2022.1) in Python. <br>
My main screen is 1920x1080 and I am running the 7dsgc desktop app on fullscreen.

It may be possible that you are able to instantly run the code by executing main.py. <br>
If not follow this tutorial: https://www.youtube.com/watch?v=WJynvGY-2wk <br>
Once everything is setup, create the project in PyCharm. (Pay attention to the folder structure). <br>
You can add different libraries by following this path "File->Settings...->Project: [Name]->Python Interpreter->+" (Just search for the ones that are underlined in red). <br>
After installing all packages you can execute the program by right clicking main.py in the left window and pressing "Run 'main'". <br>
The program will start doing something as soon as it sees the demonic beast battle stages.

## Screen adjustments
Due to the screen capture working principle it may be possible that the program isn't working for you (e.g. different screen size, ...). You can adjust the screen capture boxes in setup.py (setup_frame()). (Display the frames in main.py bottom under ###show) <br>
It is also possible that you cannot detect areas/skills because they are just some screenshots of my setup. You can replace every image in the images folder with your own setup (take care that it is still .png/.PNG). (Try to keep the same image area) <br>
In addition, you can change the threshold values of each skill card (how similar the reference image has to be to the screen image) in the bottom of setup.py


## Teams
Team and boss battle is set at the top of main.py
You can use your own teams but you have to code them yourself. <br>
E.g. if you want to use red Tarmiel instead of Skadi (I don't have red Tarmiel) you have to add his cards to setup_cards(boss_name) in setup.py (dirty way would be to take screenshots of his cards and name them skadi) <br>
If you want to do a completely different clear technique, you will have to adjust the phase functions in functions.py and the call of them in main.py (thats a lot of work)

#### Bird Team:
![](/readme_images/bird_team.PNG)
#### Bird Artifact:
![](/readme_images/bird_artifact.PNG)

#### Deer Team:
![](/readme_images/deer_team.PNG)
#### Deer Artifact:
![](/readme_images/deer_artifact.PNG)
