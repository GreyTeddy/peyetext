
from PIL import ImageGrab
import easyocr
import cv2
import numpy as np
import keyboard

import itertools
import pyperclip
import pyautogui

# put text to clipboard
def imageFromClipboard():
    print("Grabbing image from clipboard")
    # get an image from the clipboard
    im = ImageGrab.grabclipboard()
    if not im:
        return None
    return im


def cv2FromPillowImage(image):
    return cv2.cvtColor(np.array(image), cv2.COLOR_RGB2BGR)


def processCv2Image(cv2_image): 
    cv2.imwrite('hello.png',cv2_image)
    cv2_image = cv2.cvtColor(cv2_image, cv2.COLOR_BGR2GRAY)
    return cv2_image


def cv2ImageToString(cv2_image):
    reader = easyocr.Reader(['en'])
    result_string_list = reader.readtext(cv2_image)
    grouped_by_y_string =  [list(g) for m, g in itertools.groupby(result_string_list, key=lambda x: x[0][0][1]//10)]

    for y in range(len(grouped_by_y_string)):
        for x in range(len(grouped_by_y_string[y])):
            grouped_by_y_string[y][x] = grouped_by_y_string[y][x][1]

    stripped_grouped_by_y_string = [' '.join(y) for y in grouped_by_y_string]
    joined_string = "\n".join(stripped_grouped_by_y_string)
    return joined_string

def copyPasteFromClipboard(result_string):
    pyperclip.copy(result_string)
    pyautogui.hotkey('ctrl', 'v')

def main():
    print("Clipboard to text Started")
    # wait for keypress combination globally
    while True:
        keyboard.wait("ctrl+alt+v")
        image = imageFromClipboard()
        if not image:
            print("No image on clipboard")
            continue
        cv2_image = cv2FromPillowImage(image)
        cv2.imwrite('hello.png',cv2_image)
        cv2_image = processCv2Image(cv2_image)
        result_string = cv2ImageToString(cv2_image)
        copyPasteFromClipboard(result_string)
        print(result_string)

if __name__ == "__main__":
    main()

