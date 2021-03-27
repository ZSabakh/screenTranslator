import keyboard
import mouse
from PIL import ImageGrab, Image
import pyautogui
import time
import pytesseract

pytesseract.pytesseract.tesseract_cmd = r'C:\Program Files\Tesseract-OCR\tesseract.exe'

# TODO On CTRL+F6 track mouse location, on click save location and keep tracking while user moves to another location
# TODO When user moves to another location and presses CTRL+F7 the new location is saved and then subtract values to get height and width.

while True:
    try:
        if keyboard.is_pressed('ctrl+F6'):
            start_point_coordinates = [mouse.get_position()[0], mouse.get_position()[1]]


            while True:
                if mouse.is_pressed():
                    end_point_coordinates = [mouse.get_position()[0], mouse.get_position()[1]]
                    break
                time.sleep(0.002)
            if (end_point_coordinates[0] < start_point_coordinates[0]):
                start_point_coordinates[0], end_point_coordinates[0] = end_point_coordinates[0], start_point_coordinates[0]
            if (end_point_coordinates[1] < start_point_coordinates[1]):
                start_point_coordinates[1], end_point_coordinates[1] = end_point_coordinates[1], start_point_coordinates[1]

            while True:
                image = ImageGrab.grab(bbox=(
                    start_point_coordinates[0], start_point_coordinates[1], end_point_coordinates[0], end_point_coordinates[1]))
                image.save('sc.png')
                print(pytesseract.image_to_string(Image.open('sc.png')))
                time.sleep(0.1)
        time.sleep(0.002)

    except Exception as e:
        print(e)
        break
