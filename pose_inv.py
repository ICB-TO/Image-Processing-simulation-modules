import PySimpleGUI as sg
import cv2
import mediapipe as mp
import webbrowser

url = "https://learnopencv.com/building-a-body-posture-analysis-system-using-mediapipe/"

txt=f'''General Instructions
1. The video stream is realtime at 24 fps

2.These are representation of the basic core operators in image processing real time

3. The video stream is created with the help of mediapipe 

4. The output is implementation of pose detection using tensorflow light

5. Uses Tensorflow Lite

6. To access additional theory you require Internet access

7. If you select the save  option and close without specifying the save directory the module fails 

******************************************************
Implementation by:

Viswadruth Akkaraju, Atanu Wadhwa and K Priya 

Machine Perception and Cognition class 

SRM Institute of Science and Technology
****************************************************'''

sg.theme('Black')

mpPose = mp.solutions.pose
pose = mpPose.Pose()
mpDraw= mp.solutions.drawing_utils

def main():
    layout = [[sg.Text('Basic Operators', size=(60, 1), justification='center')],
              [sg.Image(filename='', key='-IMAGE-')], [sg.Button('Exit', size=(10, 1))]]

    window = sg.Window('OpenCV Integration', layout, location=(800, 400))

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
        imgRGB = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        results = pose.process(imgRGB)
        if results.pose_landmarks:
                mpDraw.draw_landmarks(frame, results.pose_landmarks,mpPose.POSE_CONNECTIONS)
                for id, lm in enumerate(results.pose_landmarks.landmark):
                    ih, iw, ic = frame.shape
                    x, y = int(lm.x * iw), int(lm.y * ih)
                    cv2.circle(frame, (x,y),5,(255,0,0), cv2.FILLED)

        window['-IMAGE-'].update(data=cv2.imencode('.ppm', frame)[1].tobytes())

    window.close()


main()