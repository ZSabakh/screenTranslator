import keyboard
import mouse
from PIL import ImageGrab
import time
import pytesseract
import tkinter as tk
import cv2
from google_trans_new import google_translator
import numpy as np

translator = google_translator()

pytesseract.pytesseract.tesseract_cmd = r'C:\Program Files\Tesseract-OCR\tesseract.exe'
root = tk.Tk()
root.overrideredirect(False)
root.wm_attributes()
root.wm_attributes("-topmost", True)

crossStart = tk.Tk()
crossStart.overrideredirect(True)
crossStart.wm_attributes("-topmost", True)
crossStart.wm_attributes("-transparentcolor", 'grey')

crossEnd = tk.Tk()
crossEnd.overrideredirect(True)
crossEnd.wm_attributes("-topmost", True)
crossEnd.wm_attributes("-transparentcolor", 'grey')

def change_label(label):
    def scanImage():
        image = ImageGrab.grab(bbox=(
            start_point_coordinates[0], start_point_coordinates[1], end_point_coordinates[0], end_point_coordinates[1]))
        processed_image = np.array(image.getdata(), dtype='uint8').reshape((image.size[1], image.size[0], 3))
        processed_image = cv2.cvtColor(processed_image, cv2.COLOR_BGR2RGB)
        gray = cv2.cvtColor(processed_image, cv2.COLOR_BGR2GRAY)
        thresh = cv2.threshold(gray, 0, 255, cv2.THRESH_BINARY_INV + cv2.THRESH_OTSU)[1]
        thresh = cv2.GaussianBlur(thresh, (3, 3), 0)
        cv2.imshow("thresh", thresh)
        scanned_text = pytesseract.image_to_string(thresh, lang='ita', config='--psm 6').replace("", "").replace("\n", " ")
        translated_text = ""
        try:
            translated_text = translator.translate(scanned_text, lang_src='it', lang_tgt='ru')
        except Exception as e:
            print(e)
        print(scanned_text)
        label.config(text=f"Original: {scanned_text}\nTranslated: {translated_text}")
        root.after(1000, scanImage)

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

            crossStart.geometry(f"+{start_point_coordinates[0]}+{start_point_coordinates[1]}")
            crossEnd.geometry(f"+{end_point_coordinates[0]}+{end_point_coordinates[1]}")

            crossLabelStart = tk.Label(crossStart, font=('Times New Roman', '20'), fg='red', bg='gray')
            crossLabelStart.config(text="+")
            crossLabelStart.pack(expand=True)

            crossLabelEnd = tk.Label(crossStart, font=('Times New Roman', '20'), fg='red', bg='gray')
            crossLabelEnd.config(text="+")
            crossLabelEnd.pack(expand=True)

            while True:

                label = tk.Label(root, font=('Times New Roman', '20'), fg='black', bg='white')
                label.pack(expand=True)
                change_label(label)
                crossStart.mainloop()
                crossEnd.mainloop()
                root.mainloop()

        time.sleep(0.002)

    except Exception as e:
        print(e)
        break
