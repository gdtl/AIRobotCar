
# coding: utf-8

# In[4]:

from keras.models import *
print('keras imported')

import picamera
import time

import os
import numpy as np

from tqdm import tqdm
from scipy.misc import imread

import RPi.GPIO as GPIO
from time import sleep

from shutil import copy2
from shutil import rmtree
 
GPIO.setmode(GPIO.BOARD)

print('imports finished')

# In[7]:


class Motor:
 
    def __init__(self, pinForward, pinBackward, pinControl):
        """ Initialize the motor with its control pins and start pulse-width
             modulation """
 
        self.pinForward = pinForward
        self.pinBackward = pinBackward
        self.pinControl = pinControl
        GPIO.setup(self.pinForward, GPIO.OUT)
        GPIO.setup(self.pinBackward, GPIO.OUT)
        GPIO.setup(self.pinControl, GPIO.OUT)
        self.pwm_forward = GPIO.PWM(self.pinForward, 100)
        self.pwm_backward = GPIO.PWM(self.pinBackward, 100)
        self.pwm_forward.start(0)
        self.pwm_backward.start(0)
        GPIO.output(self.pinControl,GPIO.HIGH) 
 
    def forward(self, speed):
        """ pinForward is the forward Pin, so we change its duty
             cycle according to speed. """
        self.pwm_backward.ChangeDutyCycle(0)
        self.pwm_forward.ChangeDutyCycle(speed)    
 
    def backward(self, speed):
        """ pinBackward is the forward Pin, so we change its duty
             cycle according to speed. """
 
        self.pwm_forward.ChangeDutyCycle(0)
        self.pwm_backward.ChangeDutyCycle(speed)
 
    def stop(self):
        """ Set the duty cycle of both control pins to zero to stop the motor. """
 
        self.pwm_forward.ChangeDutyCycle(0)
        self.pwm_backward.ChangeDutyCycle(0)
        
motor1 = Motor(16, 18, 8)
motor2 = Motor(11, 15, 7)


# In[2]:


#Load the model
model = load_model('my_model.h5')


# In[ ]:
# Deletes all pictures already in storage
f = os.listdir('./CurrentPic')
for fil in f:
	os.remove('./CurrentPic/'+fil)

# General loop

# take the pictures -> save them in a specific folder
# apply the model
# transform the prediction into an engine command
# delete the picture in the folder

#Repeat


# In[9]:


def race(maxPictures = 1000, resolution = (250, 190), FdSpeed = 5, TurnSpeed = 4):
    
    with picamera.PiCamera() as camera:
        
        camera.resolution = resolution
        time.sleep(1) # Camera warm-up time

        for i, filename in enumerate(camera.capture_continuous('./CurrentPic/image{counter:02d}.jpg')):

            print('Captured %s' % filename)
            # Capture one image a minute
            time.sleep(0.01)
            
            file=os.listdir('CurrentPic')[0]

            RacePic = selectedTest('CurrentPic') #collect the picture, ready to find its label

            predi = model.predict(RacePic) # predict the angle
            newAngle = np.argmax(predi[0])

            mot1Speed, mot2Speed = Speeds(newAngle, FdSpeed, TurnSpeed)

            motor1.forward(mot1Speed-5) #compense le déséquilibre des moteurs
            motor2.forward(mot2Speed)
            
            print('vitesse moteur 1 :'+ str(mot1Speed))
            print('vitesse moteur 2 :'+ str(mot2Speed))
            print('angle prédit'+ str(newAngle))
        
            if i == maxPictures:
                break
            
            copy2('./CurrentPic/'+file, './pictures')
            
            os.remove('./CurrentPic/'+file)


# In[3]:


# convert the pictures in the folder 'pat' to be ready for the prediction with model
def selectedTest(pat):
    
    if isinstance(pat, str):
        paths = [pat]
    
    images = []

    for path in paths:
        
        for image_file in tqdm(os.listdir(path)):
            
            if '.jpg' not in image_file: continue
            try:
                img = imread(os.path.join(path, image_file))
                
                if img is not None:
                    images.append(img[:, :])
                    
            except Exception as e:
                pass

    images = np.array(images)
    
    return images.astype('float32') / 255.

# Speeds

def Speeds(Angle, FdSpeed, TurnSpeed):

    FdSpeed, TurnSpeed = FdSpeed*20, TurnSpeed*20
    
    if Angle == 0:
        return (TurnSpeed, max(TurnSpeed - 40, 20))
    
    if Angle == 1:
        return (TurnSpeed, max(TurnSpeed - 20, 20))

    if Angle == 2:
        return (FdSpeed, FdSpeed)

    if Angle == 3:
        return (max(TurnSpeed - 20, 20), TurnSpeed)

    if Angle == 4:
        return (max(TurnSpeed - 40, 20), TurnSpeed)
    
# In[ ]:

print('race started')
race(maxPictures = 1000, resolution = (250, 190), FdSpeed = 3, TurnSpeed = 3)
