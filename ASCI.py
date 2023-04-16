import cv2
import PySimpleGUI as sg
from PIL import Image, ImageOps
import numpy as np
import webbrowser

chars = np.asarray(list(' .,:;irsXA253hMHGS#9B&@'))
SC, GCF, WCF = .1, 1, 7 / 4
url = "https://homepages.inf.ed.ac.uk/rbf/HIPR2/skeleton.htm"

sg.theme('Black')
font_size = 6
NUM_LINES = 48

cap = cv2.VideoCapture(0)

layout = [[[sg.Text(i, font=('Courier', font_size), pad=(0, 0), key=('-OUT-', i))] for i in range(NUM_LINES)],
          [sg.Text('GCF', s=9, justification='r'),
           sg.Slider((0.1, 20), resolution=.05, default_value=1, orientation='h', key='-SPIN-GCF-', size=(15, 15))],
          [sg.Text('Font Size', s=9, justification='r'),
           sg.Slider((4, 20), resolution=1, default_value=font_size, orientation='h', key='-FONT SIZE-', size=(15, 15)),
           sg.Push(), sg.Button('Exit')]]

window = sg.Window('Image Processing- ASCII Output', layout, font='Any 18', resizable=True)

txt=f'''General Instructions
1. The video stream is realtime at 24 fps

2.This represents both Binarizing the video stream and a basic implementation of connectedness 

3. The video stream is displayed through opencv

4. The output is implementation of ASCII Binarizing

5. To access additional theory you require Internet access

6. If you select the save  option and close without specifying the save directory the module fails 

******************************************************
Implementation by:

Viswadruth Akkaraju, Atanu Wadhwa and K Priya 

Machine Perception and Cognition class 

SRM Institute of Science and Technology
****************************************************'''


cap = cv2.VideoCapture(0)

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

    img = Image.fromarray(frame)  # create PIL image from frame
    GCF = float(values['-SPIN-GCF-'])
    WCF = 1.75
    # More magic that coverts the image to ascii
    S = (round(img.size[0] * SC * WCF), round(img.size[1] * SC))
    img = np.sum(np.asarray(img.resize(S)), axis=2)
    img -= img.min()
    img = (1.0 - img / img.max()) ** GCF * (chars.size - 1)

    # "Draw" the image in the window, one line of text at a time!
    font_size = int(values['-FONT SIZE-'])
    for i, r in enumerate(chars[img.astype(int)]):
        window[('-OUT-', i)].update("".join(r), font=('Courier', font_size))

window.close()