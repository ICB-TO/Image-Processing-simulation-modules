import cv2
import PySimpleGUI as sg
from PIL import Image, ImageOps
import numpy as np
import webbrowser
import colour
from colour.plotting import *

thresh = 255
gotImg = False
gotTImg = False
url = "https://www.geeksforgeeks.org/difference-between-rgb-cmyk-hsv-and-yiq-color-models/"

sg.theme('GreenTan')
photoO = [[sg.Image('', k='orig')]]
photoU = [[sg.Image('', background_color='black', k='updated')]]


def win1():
    layout1 = [[sg.Input(size=80, key='fileB', enable_events=True), sg.FileBrowse(button_text='Browse All')],
               [sg.Frame('Original', photoO, size=(640, 360), element_justification='center'),
                sg.Frame('Updated', photoU, size=(640, 360), element_justification='center')],
               [sg.Radio('HSV', 'bgc', enable_events=True, default=True, k='w'),
                sg.Radio('HSL', 'bgc', enable_events=True, k='b'), sg.Radio('LAB', 'bgc', enable_events=True, k='l'),
                sg.Radio('YcrCb', 'bgc', enable_events=True, k='y'),
                sg.Radio('YUV', 'bgc', enable_events=True, k='v'),
                sg.Radio('R-Channel', 'bgc', enable_events=True, k='r')
                   , sg.Radio('G-Channel', 'bgc', enable_events=True, k='g'),
                sg.Radio('B-Channel', 'bgc', enable_events=True, k='B'),
                sg.Radio('Gray', 'bgc', enable_events=True, k='gre'),
                sg.Radio('LUV', 'bgc', enable_events=True, k='LV'),
                sg.Radio('CIE XYZ', 'bgc', enable_events=True, k='CIE'),
                sg.Radio('Binarize', 'bgc', enable_events=True, k='bin')],
               [sg.Save()]]
    return sg.Window('Image Processing-Color Modules', layout1, relative_location=(0, -100), finalize=True)


def win2():
    layout2 = [[sg.Text(f'''General Instructions
1. If the image output does not get updated recheck the selected checkbox to update output

2.Input Image from your local directory, It can only read Image Files, any other file type will lead to error.

3. Image can be of any dimensions, the implementation here will automatically modify the dimensions to (Width=640px,
Length= 360px) 

4. The output image is based on standard image parameters as defined in opencv

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


def chrome(image):
    nd = np.asarray(image)
    RGB = colour.models.eotf_inverse_sRGB(np.array(nd / 255))
    colour.plotting.plot_RGB_chromaticities_in_chromaticity_diagram_CIE1931(RGB)


while True:
    window, event, values = sg.read_all_windows()
    if event == 'fileB':
        img = cv2.imread(values['fileB'])
        img = rez(img)
        window['orig'].update(data=cv2.imencode('.ppm', img)[1].tobytes())
        window['updated'].update(data=cv2.imencode('.ppm', img)[1].tobytes())
        gotImg = True
        fPath = values['fileB'].rsplit('/', 1)[0]

    if gotImg:
        B, G, R = cv2.split(img)
        if values['w']:
            img_f = cv2.cvtColor(img, cv2.COLOR_BGR2HSV)
        if values['b']:
            img_f = cv2.cvtColor(img, cv2.COLOR_BGR2HLS)
        if values['l']:
            img_f = cv2.cvtColor(img, cv2.COLOR_BGR2LAB)
        if values['y']:
            img_f = cv2.cvtColor(img, cv2.COLOR_BGR2YCrCb)
        if values['v']:
            img_f = cv2.cvtColor(img, cv2.COLOR_BGR2YUV)
        if values['r']:
            img_f = R
        if values['g']:
            img_f = img.copy()
            img_f = G
        if values['B']:
            img_f = B
        if values['gre']:
            img_f = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
        if values['LV']:
            img_f = cv2.cvtColor(img, cv2.COLOR_BGR2Luv)
        if values['CIE']:
            img_f = cv2.cvtColor(img, cv2.COLOR_BGR2XYZ)
            chrome(img)
        if values['bin']:
            im_gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
            th, img_f = cv2.threshold(im_gray, 128, 192, cv2.THRESH_OTSU)

        window['updated'].update(data=cv2.imencode('.png', img_f)[1].tobytes())
        gotTImg = True

    if event == 'Save' and gotTImg:
        saveFile = sg.popup_get_file('', save_as=True, no_window=True,
                                     initial_folder=fPath, default_extension='.png')
        cv2.imwrite(saveFile, img_f)

    if event in (sg.WIN_CLOSED, 'Exit'):
        sg.popup('Close all windows')
        break

    if event == '-LINK-':
        sg.popup('Redirect to website')
        webbrowser.open(url)

window.close()
