import cv2
import imutils
import PySimpleGUI as sg
from skimage.metrics import structural_similarity as compare_ssim
from PIL import Image, ImageOps
import numpy as np
import webbrowser

thresh = 255
gotImgB = False
gotImgA = False
gotTImg = False
url = "http://www.cns.nyu.edu/pub/lcv/wang03-reprint.pdf"

sg.theme('GreenTan')
photoO = [[sg.Image('', k='orig')]]
photoU = [[sg.Image('', background_color='black', k='updated')]]
photoD = [[sg.Image('', background_color='black', k='diff')]]


def win1():
    layout1 = [[sg.Input('Image 1', size=80, key='fileB', enable_events=True), sg.FileBrowse(button_text='Browse All')],
               [sg.Input('Image 2', size=80, key='fileA', enable_events=True), sg.FileBrowse(button_text='Browse All')],
               [sg.Frame('Original', photoO, size=(640, 360), element_justification='center'),
                sg.Frame('Updated', photoU, size=(640, 360), element_justification='center')],
               [sg.Frame('Delta', photoD, size=(640, 360), element_justification='center')],
               [[sg.Save()]]]
    return sg.Window('Image Processing module-Image Difference', layout1, relative_location=(0, -100), finalize=True)

def win2():
    layout2 = [[sg.Text(f'''General Instructions
1. If the image output does not get updated recheck the selected checkbox to update output

2.Input Image from your local directory, It can only read Image Files, any other file type will lead to error.

3. Image can be of any dimensions, the implementation here will automatically modify the dimensions to (Width=640px,
Length= 360px) 

4. The output image is a heatmap representing the difference between the images where the darker points denote greater
difference

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

def rez(image):
    color_converted = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
    pil_image = Image.fromarray(color_converted)
    x = ImageOps.pad(pil_image, (640, 360), color=None, centering=(0.5, 0.5))
    np_img = np.array(x)
    opencv_image = cv2.cvtColor(np_img, cv2.COLOR_RGB2BGR)
    return opencv_image


window1, window2 = win1(), win2()

while True:
    window, event, values = sg.read_all_windows()

    if event == 'fileB':
        img = cv2.imread(values['fileB'])
        img = rez(img)
        window1['orig'].update(data=cv2.imencode('.ppm', img)[1].tobytes())
        gotImgB = True
        fPath = values['fileB'].rsplit('/', 1)[0]

    if event == 'fileA':
        img2 = cv2.imread(values['fileA'])
        img2 = rez(img2)
        window1['updated'].update(data=cv2.imencode('.ppm', img2)[1].tobytes())
        gotImgA = True
        fPath = values['fileA'].rsplit('/', 1)[0]

    if gotImgA and gotImgB:
        grayA = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
        grayB = cv2.cvtColor(img2, cv2.COLOR_BGR2GRAY)
        (score, diff) = compare_ssim(grayA, grayB, full=True)
        diff = (diff * 255).astype("uint8")
        thresh = cv2.threshold(diff, 0, 255,
                               cv2.THRESH_BINARY_INV | cv2.THRESH_OTSU)[1]
        cnts = cv2.findContours(thresh.copy(), cv2.RETR_EXTERNAL,
                                cv2.CHAIN_APPROX_SIMPLE)
        cnts = imutils.grab_contours(cnts)

        for c in cnts:
            (x, y, w, h) = cv2.boundingRect(c)
            cv2.rectangle(img, (x, y), (x + w, y + h), (0, 0, 255), 2)
            cv2.rectangle(img2, (x, y), (x + w, y + h), (0, 0, 255), 2)
        window1['diff'].update(data=cv2.imencode('.png', diff)[1].tobytes())
        gotTImg = True

    if event == 'Save' and gotTImg:
        saveFile = sg.popup_get_file('', save_as=True, no_window=True,
                                     initial_folder=fPath, default_extension='.png')
        cv2.imwrite(saveFile, diff)

    if event in (sg.WIN_CLOSED, 'Exit'):
        sg.popup('Close all windows')
        break

    if event == '-LINK-':
        sg.popup('Redirect to website')
        webbrowser.open(url)

window.close()

