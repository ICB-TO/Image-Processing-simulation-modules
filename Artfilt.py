import PySimpleGUI as sg
import cv2

def main():
    sg.theme('Black')

    layout = [
      [sg.Text('Basic Operators', size=(60, 1), justification='center')],
      [sg.Image(filename='', key='-IMAGE-')],
      [sg.Radio('None', 'Radio', True, size=(10, 1))],
        [sg.Radio('stylization ', 'Radio', size=(10, 1), key='-STY-'),
         sg.Slider((0, 200), 0, 1, orientation='h', size=(20, 15), key='-sigma_s-'),
         sg.Slider((0, 1), 0.1, 0.1, orientation='h', size=(20, 15), key='-sigma_r-')],
        [sg.Radio('Pencil', 'Radio', size=(10, 1), key='-PEN-'),
         sg.Slider((0, 200), 0, 1, orientation='h', size=(20, 15), key='-sigma_s-'),
         sg.Slider((0, 1), 0.1, 0.1, orientation='h', size=(20, 15), key='-sigma_r-')],
        [sg.Radio('Cel', 'Radio', size=(10, 1), key='-CEL-'),
         sg.Slider((0, 200), 0, 1, orientation='h', size=(20, 15), key='-sigma_s-'),
         sg.Slider((0, 1), 0.1, 0.1, orientation='h', size=(20, 15), key='-sigma_r-')],
        [sg.Button('Exit', size=(10, 1))]
    ]

    window = sg.Window('OpenCV Integration', layout, location=(800, 400))

    cap = cv2.VideoCapture(0)

    while True:
        event, values = window.read(timeout=20)
        if event == 'Exit' or event == sg.WIN_CLOSED:
            break

        ret, frame = cap.read()

        if values['-STY-']:
            frame = cv2.stylization(frame, values['-sigma_s-'], values['-sigma_r-'])

        elif values['-PEN-']:
            sk_gray, frame = cv2.pencilSketch(frame, values['-sigma_s-'], values['-sigma_r-'], shade_factor=0.05)

        elif values['-CEL-']:
            frame = cv2.edgePreservingFilter(frame , flags=1, sigma_s=values['-sigma_s-'], sigma_r=values['-sigma_r-'])

        imgbytes = cv2.imencode('.png', frame)[1].tobytes()
        window['-IMAGE-'].update(data=imgbytes)

    window.close()


main()