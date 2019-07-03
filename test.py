import RPi.GPIO as GPIO
from time import sleep
 
GPIO.setmode(GPIO.BOARD)
 
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

def race():
    
    print('z: forward, s: backward, q: turn left, d: turn right, 0: stop, 1: slow speed, 2: normal speed, 3:fast speed, 4: very fast, 5: unstoppable, stop: end the program')
    speeds = [100, 100] #speedmot1, speedmot2
    direct = 0 #forwardmot1= 1, backwardmot1 = -1, same for mot2 
    
    while(True):
        a = input()
        if a == '1' or a == '2' or a == '3' or a == '4' or a == '5':
            
            diff = speeds[0]-speeds[1]
            
            s = 20*int(a)
            speeds = [max(min(s, s+diff),0) , max(0,min(s, s-diff))]
           
            if direct > -1:
            
                motor1.forward(s)
                motor2.forward(s)
                direct = 1
            else: 
                motor1.backward(s)
                motor2.backward(s)
        elif a == '0':
            motor1.stop()
            motor2.stop()
            direct = 0
        elif a == 'z':
             motor1.forward(max(speeds[0],speeds[1]))
             motor2.forward(max(speeds[0],speeds[1]))
             direct = 1
        elif a == 's':
             motor1.backward(speeds[0])
             motor2.backward(speeds[1])
             direct = -1
        elif a == 'q': #turn left
            if speeds[0]<speeds[1]:
                speeds[0] = speeds[1]
            if direct == 0:
                speeds[1] = max(speeds[1]-10,0)
            elif direct == 1:
                motor1.forward(speeds[0])
                motor2.forward(max(speeds[1]-10,0))
                speeds[1] = max(speeds[1]-10,0)
            elif direct == -1:
                motor1.backward(speeds[0])
                motor2.backward(max(speeds[1]-10,0))
                speeds[1] = max(speeds[1]-10,0)
                
        elif a == 'd': #turn right
            if speeds[0]>speeds[1]:
                speeds[1] = speeds[0]
            if direct == 0:
                speeds[0] = max(speeds[0]-10,0)
            elif direct == 1:
                motor2.forward(speeds[1])
                motor1.forward(max(speeds[0]-10,0))
                speeds[0] = max(speeds[0]-10,0)
            elif direct == -1:
                motor2.backward(speeds[1])
                motor1.backward(max(speeds[0]-10,0))
                speeds[0] = max(speeds[0]-10,0)
        elif a == 'stop':
            motor1.stop()
            motor2.stop()
            break
        sleep(0.2)
        print(speeds)
race()
print('race ended')
