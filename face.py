import cv2
import PySimpleGUI as sg
from PIL import Image, ImageOps
import numpy as np
import webbrowser
import mediapipe as mp

url = "https://google.github.io/mediapipe/solutions/face_detection.html"

sg.theme('Black')
pTime = 0
NUM_FACE = 2

mpDraw = mp.solutions.drawing_utils
mpFaceMesh = mp.solutions.face_mesh
faceMesh = mpFaceMesh.FaceMesh(max_num_faces=NUM_FACE)
drawSpec = mpDraw.DrawingSpec(thickness=1, circle_radius=1)

cap = cv2.VideoCapture(0)

layout = [[sg.Text('Basic Operators', size=(60, 1), justification='center')],
              [sg.Image(filename='', key='-IMAGE-')], [sg.Button('Exit', size=(10, 1))]]


window = sg.Window('Face Invariant', layout, location=(800, 400))

cap = cv2.VideoCapture(0)

txt=f'''General Instructions
1. The video stream is realtime at 24 fps

2.These are representation of the basic core operators in image processing real time

3. The video stream is created with the help of mediapipe 

4. The output is implementation of 468 landmarks face algorithm

5. Uses Tensorflow Lite

6. To access additional theory you require Internet access

7. If you select the save  option and close without specifying the save directory the module fails 

******************************************************
Implementation by:

Viswadruth Akkaraju, Atanu Wadhwa and K Priya 

Machine Perception and Cognition class 

SRM Institute of Science and Technology
****************************************************'''

while True:

    event, values = window.read(timeout=0)
    if event in ('Exit', sg.WIN_CLOSED):
        ch = sg.popup_yes_no("Yes to Access Theory and No to close application", title="YesNo")
        if ch == 'No':
            break
        ch = sg.popup_ok_cancel(txt, "Press Ok to access theory", "Press cancel to stop", title="OkCancel")
        if ch == "OK":
            webbrowser.open(url)
        if ch == "Cancel" or ch == 'No':
            break
    ret, frame = cap.read()
    imgRGB = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
    results = faceMesh.process(imgRGB)
    if results.multi_face_landmarks:
        for faceLms in results.multi_face_landmarks:
            mpDraw.draw_landmarks(frame, faceLms, mpFaceMesh.FACEMESH_CONTOURS, drawSpec, drawSpec)

            for id, lm in enumerate(faceLms.landmark):
                ih, iw, ic = frame.shape
                x, y = int(lm.x * iw), int(lm.y * ih)
                print(id, x, y)

    window['-IMAGE-'].update(data=cv2.imencode('.ppm', frame)[1].tobytes())

window.close()