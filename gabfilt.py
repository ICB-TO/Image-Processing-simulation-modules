import cv2
import PySimpleGUI as sg
from PIL import Image, ImageOps
import numpy as np
import webbrowser
from math import pi

thresh=255
gotImg=False
gotTImg=False
url = "https://homepages.inf.ed.ac.uk/rbf/CVonline/LOCAL_COPIES/TRAPP1/filter.html"

sg.theme('GreenTan')
photoO=[[sg.Image('',k='orig')]]
photoU=[[sg.Image('',background_color='black',k='updated')]]

def win1():
    layout1=[[sg.Input(size=80,key='fileB',enable_events=True),sg.FileBrowse(button_text='Browse All')],
        [sg.Frame('Original',photoO,size=(640,360),element_justification='center'),
            sg.Frame('Updated',photoU,size=(640,360),element_justification='center')],
        [sg.vbottom(sg.Text("Kernel Size:")),sg.Slider(range=(1,10),orientation='h',default_value=1,enable_events=True,resolution=1,k='ksize')],
                              #Kernel Size:
         [sg.vbottom(sg.Text("Sigma        ")),sg.Slider(range=(0.4,2.5),orientation='h',default_value=0.4,enable_events=True,resolution=0.1,k='sigma')],

         [sg.vbottom(sg.Text("Theta         ")),sg.Slider(range=(0,pi),orientation='h',default_value=0,enable_events=True,resolution=pi/16,k='theta')],

         [sg.vbottom(sg.Text("Lambda     ")),sg.Slider(range=(1,5),orientation='h',default_value=1,enable_events=True,resolution=1,k='hl3')],

         [sg.vbottom(sg.Text("Gamma     ")),sg.Slider(range=(0.2,1),orientation='h',default_value=0.2,enable_events=True,resolution=0.1,k='hulk')],

         [sg.vbottom(sg.Text("Psi          ")),sg.Slider(range=(-pi,pi),orientation='h',default_value=0,enable_events=True,resolution=pi/8,k='spy')],
        [sg.Save()]]
    return sg.Window('Image Processing - Gabor Filter',layout1,relative_location=(0,-100),finalize=True)


def win2():
    layout2 = [[sg.Text(f'''General Instructions
1. If the image output does not get updated recheck the selected checkbox to update output

2.Input Image from your local directory, It can only read Image Files, any other file type will lead to error.

3. Image can be of any dimensions, the implementation here will automatically modify the dimensions to (Width=640px,
Length= 360px) 

4. The slider Values here represents the threshold for the five primary properties: Kernel Size,Sigma, Theta ,
lambda,gamma and psi

5.The Output Image can be saved by clicking on the save button, The default format is .png 

6. To access additional theory you require Internet access

7. If you select the save  option and close without specifying the save directory the module fails 

***************************************************************************
Implementation by:

Viswadruth Akkaraju, Atanu Wadhwa and K Priya 

Machine Perception and Cognition class 

SRM Institute of Science and Technology
***************************************************************************''', font='Lucida', size=(50, 33))],
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
        img=cv2.imread(values['fileB'])
        img = rez(img)
        window['orig'].update(data=cv2.imencode('.ppm', img)[1].tobytes())
        window['updated'].update(data=cv2.imencode('.ppm', img)[1].tobytes())
        gotImg=True
        fPath=values['fileB'].rsplit('/',1)[0]

    if gotImg:
        temp = int(values['ksize'])
        kernel = (temp, temp)
        kern = cv2.getGaborKernel(ksize=kernel, sigma=float(values['sigma']), theta=float(values['theta']),
                                  lambd=int(values['hl3']), gamma=float(values['hulk']), psi=float(values['spy']),
                                  ktype=cv2.CV_32F)
        kern /= 1.5 * kern.sum()
        img_f = cv2.filter2D(img, cv2.CV_8UC3, kern)
        img_f = np.maximum(np.zeros_like(img), img_f, np.zeros_like(img))
        window['updated'].update(data=cv2.imencode('.png', img_f)[1].tobytes())
        gotTImg=True

    if event == 'Save' and gotTImg:
        saveFile= sg.popup_get_file('',save_as=True,no_window=True,
                        initial_folder=fPath,default_extension='.png')
        cv2.imwrite(saveFile,img_f)

    if event in (sg.WIN_CLOSED, 'Exit'):
        sg.popup('Close all windows')
        break

    if event == '-LINK-':
        sg.popup('Redirect to website')
        webbrowser.open(url)

window.close()