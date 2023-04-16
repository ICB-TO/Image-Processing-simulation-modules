import cv2
import PySimpleGUI as sg
from PIL import Image, ImageOps
import numpy as np
import webbrowser

url = "https://en.wikipedia.org/wiki/Canny_edge_detector"
sg.theme('GreenTan')
cap = cv2.VideoCapture(0)

layout = [
      [sg.Text('Image processing - Real time basic image Operations', size=(60, 1), justification='center')],
      [sg.Image(filename='', key='-IMAGE-')],
      [sg.Radio('None', 'Radio', True, size=(10, 1))],
      [sg.Radio('Binarize', 'Radio', size=(10, 1), key='-THRESH-'),
       sg.Slider((0, 255), 128, 1, orientation='h', size=(40, 15), key='-THRESH SLIDER-')],
      [sg.Radio('canny', 'Radio', size=(10, 1), key='-CANNY-'),
       sg.Slider((0, 255), 128, 1, orientation='h', size=(20, 15), key='-CANNY SLIDER A-'),
       sg.Slider((0, 255), 128, 1, orientation='h', size=(20, 15), key='-CANNY SLIDER B-')],
      [sg.Radio('blur', 'Radio', size=(10, 1), key='-BLUR-'),
       sg.Slider((1, 11), 1, 1, orientation='h', size=(40, 15), key='-BLUR SLIDER-')],
      [sg.Radio('hue', 'Radio', size=(10, 1), key='-HUE-'),
       sg.Slider((0, 225), 0, 1, orientation='h', size=(40, 15), key='-HUE SLIDER-')],
      [sg.Radio('enhance', 'Radio', size=(10, 1), key='-ENHANCE-'),
       sg.Slider((1, 255), 128, 1, orientation='h', size=(40, 15), key='-ENHANCE SLIDER-')]
      , [sg.Button('Exit')]]

window = sg.Window('Basic ops', layout, location=(800, 400))

txt=f'''General Instructions
1. The video stream is realtime at 24 fps

2.These are representation of the basic core operators in image processing real time

3. The video stream is created with the help of opencv

4. The output for edge is implemented by using a canny edge detector and for Contour is based on chain approximation

5.We can differentiate both along the x and y axis to better represent how the algo works

6. To access additional theory you require Internet access

7. If you select the save  option and close without specifying the save directory the module fails 

******************************************************
Implementation by:

Viswadruth Akkaraju, Atanu Wadhwa and K Priya 

Machine Perception and Cognition class 

SRM Institute of Science and Technology
****************************************************'''

while True:
    event, values = window.read(timeout=20)

    if event in ('Exit', sg.WIN_CLOSED):
        ch = sg.popup_yes_no("Yes to Access Theory and No to close application", title="YesNo")
        if ch == 'No':
            break
        ch = sg.popup_ok_cancel(txt,"Press Ok to access theory", "Press cancel to stop", title="OkCancel")
        if ch == "OK":
            webbrowser.open(url)
        if ch == "Cancel" or ch=='No':
            break
    ret, frame = cap.read()

    if values['-THRESH-']:
        frame = cv2.cvtColor(frame, cv2.COLOR_BGR2LAB)[:, :, 0]
        frame = cv2.threshold(frame, values['-THRESH SLIDER-'], 255, cv2.THRESH_BINARY)[1]
    elif values['-CANNY-']:
        frame = cv2.Canny(frame, values['-CANNY SLIDER A-'], values['-CANNY SLIDER B-'])
    elif values['-BLUR-']:
        frame = cv2.GaussianBlur(frame, (21, 21), values['-BLUR SLIDER-'])
    elif values['-HUE-']:
        frame = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)
        frame[:, :, 0] += int(values['-HUE SLIDER-'])
        frame = cv2.cvtColor(frame, cv2.COLOR_HSV2BGR)
    elif values['-ENHANCE-']:
        enh_val = values['-ENHANCE SLIDER-'] / 40
        clahe = cv2.createCLAHE(clipLimit=enh_val, tileGridSize=(8, 8))
        lab = cv2.cvtColor(frame, cv2.COLOR_BGR2LAB)
        lab[:, :, 0] = clahe.apply(lab[:, :, 0])
        frame = cv2.cvtColor(lab, cv2.COLOR_LAB2BGR)

    imgbytes = cv2.imencode('.png', frame)[1].tobytes()
    window['-IMAGE-'].update(data=imgbytes)

window.close()

