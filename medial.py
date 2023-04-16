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
url = "https://homepages.inf.ed.ac.uk/rbf/HIPR2/skeleton.htm"

sg.theme('GreenTan')
photoO=[[sg.Image('',k='orig')]]
photoU=[[sg.Image('',background_color='black',k='updated')]]

def win1():
        layout1=[[sg.Input(size=80,key='fileB',enable_events=True),sg.FileBrowse(button_text='Browse All')],
        [sg.Frame('Original', photoO, size=(640, 360), element_justification='center'),
         sg.Frame('Updated', photoU, size=(640, 360), element_justification='center')],
        [sg.Radio('THINNING_GUOHALL', 'bgc', enable_events=True, default=True, k='w'),
         sg.Radio('THINNING_ZHANGSUEN', 'bgc', enable_events=True, k='b')],
            [[sg.Save()]]]
        return sg.Window('Image Processing - Medial Axis theorem', layout1, relative_location=(0, -100), finalize=True)


def win2():
    layout2 = [[sg.Text(f'''General Instructions
1. If the image output does not get updated recheck the selected checkbox to update output

2.Input Image from your local directory, It can only read Image Files, any other file type will lead to error.

3. Image can be of any dimensions, the implementation here will automatically modify the dimensions to (Width=640px,
Length= 360px) 

4.The Output Image can be saved by clicking on the save button, The default format is .png 

5. To access additional theory you require Internet access

6. If you select the save  option and close without specifying the save directory the module fails 



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
        window1['updated'].update(data=cv2.imencode('.ppm', img)[1].tobytes())
        gotImgB = True
        fPath = values['fileB'].rsplit('/', 1)[0]

    if gotImgB:
        if values['w']:
            img_f = cv2.ximgproc.thinning(cv2.cvtColor(img, cv2.COLOR_RGB2GRAY),
                                          thinningType=cv2.ximgproc.THINNING_GUOHALL)
        if values['b']:
            img_f = cv2.ximgproc.thinning(cv2.cvtColor(img, cv2.COLOR_RGB2GRAY))

        window1['updated'].update(data=cv2.imencode('.png', img_f)[1].tobytes())
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

