import cv2
from PIL import Image, ImageOps
import webbrowser
import numpy as np
import PySimpleGUI as sg

thresh = 255
gotImg = False
gotTImg = False
url = "https://en.wikipedia.org/wiki/Foreground_detection"

sg.theme('GreenTan')
photoO = [[sg.Image('', k='orig')]]
photoU = [[sg.Image('', background_color='black', k='updated')]]


def win1():
    layout1 = [[sg.Input(size=80, key='fileB', enable_events=True), sg.FileBrowse(button_text='Browse All')],
               [sg.Frame('Original', photoO, size=(640, 360), element_justification='center'),
                sg.Frame('Updated', photoU, size=(640, 360), element_justification='center')],
               [sg.Radio('Remove White Background', 'bgc', enable_events=True, default=True, k='w'),
                sg.Radio('Remove Black Background', 'bgc', enable_events=True, k='b'),
                sg.Slider(range=(0, 255), orientation='h', default_value=255, enable_events=True, resolution=5,
                          k='sw')],
               [sg.Save()]]
    return sg.Window('Image Processing Module- Background Seperator (Black and White)', layout1, relative_location=(0, -100),
                     finalize=True)


def win2():
    layout2 = [[sg.Text(f'''General Instructions
1. If the image output does not get updated recheck the selected checkbox to update output

2.Input Image from your local directory, It can only read Image Files, any other file type will lead to error.

3. Image can be of any dimensions, the implementation here will automatically modify the dimensions to (Width=640px,
Length= 360px) 

4. The slider Values here represents the threshold for separation ranged (0-255)

5.The Output Image can be saved by clicking on the save button, The default format is .png 

6. To access additional theory you require Internet access

7. If you select the save  option and close without specifying the save directory the module fails 

***************************************************************************
Implementation by:

Viswadruth Akkaraju, Atanu Wadhwa and K Priya 

Machine Perception and Cognition class 

SRM Institute of Science and Technology
***************************************************************************''', font='Lucida', size=(50, 31))],
               [sg.Button('Hyperlink to theory', font='Lucida', enable_events=True, key="-LINK-")]]

    return sg.Window('Help', layout2, finalize=True)


window1, window2 = win1(), win2()


def rez(image):
    color_converted = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
    pil_image = Image.fromarray(color_converted)
    x = ImageOps.pad(pil_image, (640, 360), color=None, centering=(0.5, 0.5))
    np_img = np.array(x)
    opencv_image = cv2.cvtColor(np_img, cv2.COLOR_RGB2BGR)
    return opencv_image


while True:
    window, event, values = sg.read_all_windows()
    if event == 'fileB':
        img = cv2.imread(values['fileB'])
        img = rez(img)
        window['orig'].update(data=cv2.imencode('.ppm', img)[1].tobytes())
        window['updated'].update(data=cv2.imencode('.ppm', img)[1].tobytes())
        gotImg = True
        fPath = values['fileB'].rsplit('/', 1)[0]

    if event == 'sw' and gotImg:
        thresh = int(values['sw'])
        if values['w']:
            alpha = ~np.all(img > thresh, axis=2) * 255
            imgBGRA = np.dstack((img, alpha)).astype(np.uint8)
        if values['b']:
            alpha = ~np.all(img < thresh, axis=2) * 255
            imgBGRA = np.dstack((img, alpha)).astype(np.uint8)
        window['updated'].update(data=cv2.imencode('.png', imgBGRA)[1].tobytes())
        gotTImg = True

    if event == 'Save' and gotTImg:
        saveFile = sg.popup_get_file('', save_as=True, no_window=True,
                                     initial_folder=fPath, default_extension='.png')
        cv2.imwrite(saveFile, imgBGRA)

    if event == 'w':
        window['sw'].update(value=255)
        window['updated'].Widget.config(background='black')

    if event == 'b':
        window['sw'].update(value=0)
        window['updated'].Widget.config(background='white')

    if event in (sg.WIN_CLOSED, 'Exit'):
        sg.popup('Close all windows')
        break

    if event == '-LINK-':
        sg.popup('Redirect to website')
        webbrowser.open(url)

window.close()
