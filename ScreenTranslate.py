import keyboard
import mouse
from PIL import ImageGrab
import pyautogui
import time

# TODO On CTRL+F6 track mouse location, on click save location and keep tracking while user moves to another location
# TODO When user moves to another location and presses CTRL+F7 the new location is saved and then subtract values to get height and width.

while True:
    try:
        if keyboard.is_pressed('ctrl+F6'):
            startPointCoordinates = [mouse.get_position()[0], mouse.get_position()[1]]

            while True:
                if mouse.is_pressed():
                    endPointCoordinates = [mouse.get_position()[0], mouse.get_position()[1]]
                    break
                time.sleep(0.002)

            if(endPointCoordinates[0] < startPointCoordinates[0]):
                startPointCoordinates[0], endPointCoordinates[0] = endPointCoordinates[0], startPointCoordinates[0]
            if(endPointCoordinates[1] < startPointCoordinates[1]):
                startPointCoordinates[1], endPointCoordinates[1] = endPointCoordinates[1], startPointCoordinates[1]

            image = ImageGrab.grab(bbox=(
                startPointCoordinates[0], startPointCoordinates[1], endPointCoordinates[0], endPointCoordinates[1]))
            image.save('sc.png')

        time.sleep(0.002)
    except Exception as e:
        print(e)
        break
