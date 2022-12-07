import os
os.environ['PYGAME_HIDE_SUPPORT_PROMPT'] = "hide"
import pygame as py
import win32api
import win32con
import win32gui
import pyscreenshot as ImageGrab
import cv2
import numpy as np
import time
import screeninfo
import sys
py.init()
screen = screeninfo.get_monitors()[0]
width, height = screen.width, screen.height
window_screen = py.display.set_mode((width, height),py.NOFRAME)
win32gui.SetWindowPos(py.display.get_wm_info()['window'], win32con.HWND_TOPMOST, 0,0,0,0, win32con.SWP_NOMOVE | win32con.SWP_NOSIZE)
hwnd = py.display.get_wm_info()["window"]
win32gui.SetWindowLong(hwnd, win32con.GWL_EXSTYLE, win32gui.GetWindowLong(hwnd, win32con.GWL_EXSTYLE) | win32con.WS_EX_LAYERED)
win32gui.SetLayeredWindowAttributes(hwnd, win32api.RGB(255, 0, 128), 0, win32con.LWA_COLORKEY)

cascade_face_front = cv2.CascadeClassifier("./cascades/haarcascade_frontalface_default.xml")
cascade_face_profile = cv2.CascadeClassifier("./cascades/haarcascade_profileface.xml")

def rect(x1, y1, x2, y2):
    color = (0,255,0)
    py.draw.rect(window_screen, color, py.Rect((x1, y1), (x2,y2)),2)
    py.display.flip()

def detectface():
    image = np.array(ImageGrab.grab())
    gray=cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    faces = []
    faces.extend(cascade_face_front.detectMultiScale(gray, 1.1, 5,minSize=(30, 30),flags = cv2.CASCADE_SCALE_IMAGE))
    faces.extend(cascade_face_profile.detectMultiScale(gray, 1.1, 5,minSize=(30, 30),flags = cv2.CASCADE_SCALE_IMAGE))
    for (x, y, w, h) in faces:
        rect(x,y,w,h)
        
exitStatus = False
while not exitStatus:
    for event in py.event.get():
        if event.type == py.QUIT:
            exitStatus = True
        if event.type == py.KEYDOWN:
            if event.key == py.K_ESCAPE:
                exitStatus = True
    window_screen.fill((255,0,128))
    py.display.update()
    detectface()
    time.sleep(0.2)
    py.display.update()
py.quit()
sys.exit()	
