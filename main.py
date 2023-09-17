from time import sleep

import cv2
import numpy
import win32api
import win32con
import win32gui
import win32ui
import ctypes

from window import Window

window = Window()
window.find_window_pid("Notepad")
width, height = window.get_window_size()
crop_x, crop_y = 8, 30
width = width - (crop_x * 2)
height = height - (crop_x + crop_y)

needle = cv2.imread("exit.png")
h_y = needle.shape[0]
w_x = needle.shape[1]


# run realtime window capture
while True:
    WDC = win32gui.GetWindowDC(window.window_pid)
    DCUI = win32ui.CreateDCFromHandle(WDC)
    CB = win32ui.CreateBitmap()
    CB.CreateCompatibleBitmap(DCUI, width, height)

    save_screen = DCUI.CreateCompatibleDC()
    save_screen.SelectObject(CB)

    save_screen.BitBlt(
        (0, 0), (width, height), DCUI, (crop_x, crop_y), win32con.SRCCOPY
    )

    bitmap_array = CB.GetBitmapBits(True)
    img = numpy.frombuffer(bitmap_array, dtype="uint8")
    img.shape = (height, width, 4)
    img = img[..., :3]
    img = numpy.ascontiguousarray(img)

    # match template with needle and draw green rectangle around it in img
    result = cv2.matchTemplate(img, needle, cv2.TM_CCOEFF_NORMED)
    yloc, xloc = numpy.where(result >= 0.8)
    for x, y in zip(xloc, yloc):
        cv2.rectangle(img, (x, y), (x + w_x, y + h_y), (0, 255, 0), 1)

    cv2.imshow("window", img)
    sleep(0.5)

    if cv2.waitKey(1) == ord("q"):
        cv2.destroyAllWindows()
        break
