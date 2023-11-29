
import cv2
import random
import numpy as np
from imutils.video import WebcamVideoStream
import imutils
import smtplib
import ssl
from email.message import EmailMessage
import time

# EYE sequence password that can be modified
password = 'LRBB'  # Password: 'L' for left eye closed, 'R' for right eye closed, 'B' for both eyes closed.

# Haar cascades for eye detection
l_eye_cascade = cv2.CascadeClassifier('haarcascades/haarcascade_lefteye_2splits.xml')
r_eye_cascade = cv2.CascadeClassifier('haarcascades/haarcascade_righteye_2splits.xml')
eye_cascade = cv2.CascadeClassifier('haarcascades/haarcascade_eye.xml')

# Parameters for eye detection
scale = 1.2
left_eye_found = False
right_eye_found = False

l_eye_x = 0
l_eye_y = 0

r_eye_x = 0
r_eye_y = 0

frame_x = 0
frame_y = 0

l_eye_blink_state = 'closed'  # Possible states: 'notfound', 'open', or 'closed'
r_eye_blink_state = 'closed'  # Possible states: 'notfound', 'open', or 'closed'

frameForDrawing = ''
# Initialize the webcam thread that updates frames in the background
cap = WebcamVideoStream(src=0).start()

# Counters and states for eye blink detection
counter = 0
eyeStateSequence = ''  # 'L' for left eye closed, 'R' for right eye closed, 'B' for both closed, 'O' for both open
eyeStateCounter = 0
eyeStateCountConfirmed = 2
lastState = ''
eyesNotFoundCounter = 0
eyeStateQueue = ''

# Functions for capturing an image and sending an email alert
def take_picture():
    cap = cv2.VideoCapture(0)
    
    cap.set(cv2.CAP_PROP_FRAME_WIDTH, 1280)
    cap.set(cv2.CAP_PROP_FRAME_HEIGHT, 720)
    
    ret,frame = cap.read()
    
    cv2.imwrite("captured_image.jpg", frame)
    cap.release()

def email_alert(subject, body, to, attachment_path=None):
    Otp = random.randint(000000,999999)
    ebody = 'OTP for validation is :'+str(Otp) + body
    
    msg = EmailMessage()
    msg.set_content(ebody)
    msg['Subject'] = subject
    msg['To'] = to

    user = "revatest88@gmail.com"
    msg['From'] = user
    password = "gswqnfyucomqyvlm"

    if attachment_path:
        with open(attachment_path, "rb") as attachment:
            msg.add_attachment(attachment.read(), maintype="image", subtype="jpg", filename="captured_image.jpg")

    context = ssl.create_default_context()
    with smtplib.SMTP_SSL("smtp.gmail.com", 465, context=context) as smtp:
        smtp.login(user, password)
        smtp.send_message(msg)

    print("Otp sent to mail id...")
    return Otp

# Functions for detecting left and right eyes
def detect_left_and_right_eyes(frame_for_detection):
    global left_eye_found, right_eye_found, l_eye_x, l_eye_y, r_eye_x, r_eye_y, r_eye_y, l_eye_blink_state, r_eye_blink_state, scale, frameForDrawing

    l_eyes_rects = l_eye_cascade.detectMultiScale(frame_for_detection, scaleFactor=scale, minNeighbors=5)

    left_most_eye = ()
    left_eye_found = False
    counter = 0
    biggestArea = 0

    for (x, y, w, h) in l_eyes_rects:
        left_eye_found = True
        tempArea = w * h

        if counter == 0:
            left_most_eye = (x, y, w, h)
            biggestArea = tempArea

        elif x > left_most_eye[0]:
            left_most_eye = (x, y, w, h)
            biggestArea = tempArea

        counter = counter + 1

    if left_eye_found == True:
        x, y, w, h = left_most_eye

        l_eye_x = x
        l_eye_y = y

    r_eyes_rects = r_eye_cascade.detectMultiScale(frame_for_detection, scaleFactor=scale, minNeighbors=5)

    right_most_eye = ()
    right_eye_found = False
    counter = 0
    biggestArea = 0

    for (x, y, w, h) in r_eyes_rects:
        right_eye_found = True
        tempArea = w * h

        if counter == 0:
            right_most_eye = (x, y, w, h)
            biggestArea = tempArea

        elif x < right_most_eye[0]:
            right_most_eye = (x, y, w, h)
            biggestArea = tempArea

        counter = counter + 1

    if right_eye_found == True:
        x, y, w, h = right_most_eye
       
        cv2.rectangle(frameForDrawing, (x, y), (x + w, y + h), (0, 255, 0), 10)

        r_eye_x = x
        r_eye_y = y

    return None

# Function for detecting both eyes
def detect_eyes(frame_for_detection):
    global l_eye_found, r_eye_found, l_eye_x, l_eye_y, r_eye_x, r_eye_y, l_eye_blink_state, r_eye_blink_state, scale, frameForDrawing

    l_eye_blink_state = 'closed'
    r_eye_blink_state = 'closed'

    eyes_rects = eye_cascade.detectMultiScale(frame_for_detection, scaleFactor=scale, minNeighbors=40)

    counter = 0
    for (x, y, w, h) in eyes_rects:
        if counter >= 2:
            break
        # if isRaspberryPi==False:
        cv2.rectangle(frameForDrawing, (x, y), (x + w, y + h), (255, 255, 255), 3)

        if abs(l_eye_x - x) < frame_x * 0.05 and abs(l_eye_y - y) < frame_y * 0.05 and left_eye_found == True:
            l_eye_blink_state = 'open'
        elif abs(r_eye_x - x) < frame_x * 0.05 and abs(r_eye_y - y) < frame_y * 0.05 and right_eye_found == True:
            r_eye_blink_state = 'open'
        counter = counter + 1

    return None

# Main script
lcdstate = ''  # State: 'found', 'not'
while True:
    tempState = ''

    frameForDetection = cap.read()
    frameForDetection = cv2.resize(frameForDetection, (320, 240))

    frameForDrawing = frameForDetection.copy()

    if counter == 0:
        frame_y = frameForDetection.shape[1]
        frame_x = frameForDetection.shape[0]

    # FRAME DRAWING AND VARIABLE FETCHING
    detect_left_and_right_eyes(frameForDetection)

    detect_eyes(frameForDetection)
    cv2.imshow('EYE WINDOW', frameForDrawing)

    # EYE BLINK LOGIC
    if left_eye_found == True and right_eye_found == True:
        eyesNotFoundCounter = 0

        if l_eye_blink_state == 'open' and r_eye_blink_state == 'open':
            tempState = 'O'
        elif l_eye_blink_state == 'closed' and r_eye_blink_state == 'open':
            tempState = 'L'
        elif l_eye_blink_state == 'open' and r_eye_blink_state == 'closed':
            tempState = 'R'
        elif l_eye_blink_state == 'closed' and r_eye_blink_state == 'closed':
            tempState = 'B'

        if lastState == tempState and eyeStateCounter < eyeStateCountConfirmed:
            eyeStateCounter = eyeStateCounter + 1
        elif lastState == tempState and eyeStateCounter >= eyeStateCountConfirmed:
            if eyeStateQueue == '' and tempState != 'O':
                eyeStateQueue = tempState
                eyeStateCounter = 0
            elif eyeStateQueue != '' and tempState == 'O':
                eyeStateSequence = eyeStateSequence + eyeStateQueue
                eyeStateCounter = 0
                eyeStateQueue = ''
                print("Current eye state sequence: " + str(eyeStateSequence))

        elif lastState != tempState:
            eyeStateCounter = 0

        lastState = tempState

        if eyeStateSequence == password:
            print("EYE SEQUENCE PASSWORD MATCHED!")
            
            cap.stop()
            take_picture()
            #Email otp 
            OTP = email_alert("OTP for acess", "\nIf not you, here's the captured image of the person trying", "revanthjanjanam0@gmail.com", attachment_path="captured_image.jpg")
            
            lock = ''
            for i in range(0,3):
                In_Otp = input("Enter the Otp:")
                if In_Otp == str(OTP):
                    print('Otp matched!\n .....$$ System  Opened $$...')
                    lock = 'open'
                    break
                print('Invalid Otp !! \nRemaining chances :',2-i)
            if lock != 'open' :
                print('!!Error!!\n...System is locked...')
            break
               

    else:
        if counter % 100 == 0:
            print("Left and/or Right eye not detected. Please face the camera directly around 1 ft away from the camera.")

        if eyesNotFoundCounter > eyeStateCountConfirmed + 5:
            if eyeStateSequence != '':
                print("Resetting eye blink sequence. Try password again.")
                eyesNotFoundCounter = 0
                eyeStateSequence = ''
                lastState = ''

        eyesNotFoundCounter = eyesNotFoundCounter + 1

    print("Left/Right Eye State: " + str(l_eye_blink_state) + "/" + str(r_eye_blink_state) + "   Current eye state sequence: " + str(eyeStateSequence))

    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

    counter = counter + 1
time.sleep(2)
cv2.destroyAllWindows()
