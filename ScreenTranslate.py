import keyboard
import mouse
from PIL import ImageGrab, Image
import pyautogui
import time
import pytesseract
import tkinter as tk
import cv2
import imutils

pytesseract.pytesseract.tesseract_cmd = r'C:\Program Files\Tesseract-OCR\tesseract.exe'
root = tk.Tk()
root.overrideredirect(True)
root.wm_attributes("-topmost", True)
root.wm_attributes("-disabled", True)


# TODO On CTRL+F6 track mouse location, on click save location and keep tracking while user moves to another location
# TODO When user moves to another location and presses CTRL+F7 the new location is saved and then subtract values to get height and width.
def change_label(label):
    def scanImage():
        image = ImageGrab.grab(bbox=(
            start_point_coordinates[0], start_point_coordinates[1], end_point_coordinates[0], end_point_coordinates[1]))
        image.save('sc.png')

        processed_image = cv2.imread('sc.png')
        processed_image = imutils.resize(processed_image, width=700)
        gray = cv2.cvtColor(processed_image, cv2.COLOR_BGR2GRAY)
        thresh = cv2.threshold(gray, 0, 255, cv2.THRESH_BINARY_INV + cv2.THRESH_OTSU)[1]
        thresh = cv2.GaussianBlur(thresh, (3, 3), 0)

        scanned_text = pytesseract.image_to_string(thresh, lang='eng', config='--psm 6').replace("", "").replace("\n", "")
        print(scanned_text)
        label.config(text=scanned_text)
        root.after(500, scanImage)

    scanImage()


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
                start_point_coordinates[0], end_point_coordinates[0] = end_point_coordinates[0], \
                                                                       start_point_coordinates[0]
            if (end_point_coordinates[1] < start_point_coordinates[1]):
                start_point_coordinates[1], end_point_coordinates[1] = end_point_coordinates[1], \
                                                                       start_point_coordinates[1]
            root.geometry(f"+{250}+{250}")

            while True:
                label = tk.Label(root, font=('Times New Roman', '40'), fg='black', bg='white')
                label.pack(expand=True)
                change_label(label)
                root.mainloop()

        time.sleep(0.002)

    except Exception as e:
        print(e)
        break
