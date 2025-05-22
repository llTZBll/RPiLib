import RPi.GPIO as GPIO
import time
makerobo_Buzzer=13
makerobo_TRIG = 11
makerobo_ECHO = 12
def makerobo_setup():
    GPIO.setmode(GPIO.BOARD)
    GPIO.setwarnings(False)
    GPIO.setup(makerobo_TRIG, GPIO.OUT)
    GPIO.setup(makerobo_ECHO, GPIO.IN)
    GPIO.setup(makerobo_Buzzer,GPIO.OUT)
    global makerobo_Buzz
    makerobo_Buzz=GPIO.PWM(makerobo_Buzzer,440)
    makerobo_Buzz.start(50)
def ur_disMeasure():
    GPIO.output(makerobo_TRIG, 0)
    time.sleep(0.000002)
    GPIO.output(makerobo_TRIG, 1)
    time.sleep(0.00001)
    GPIO.output(makerobo_TRIG, 0)
    while GPIO.input(makerobo_ECHO) == 0:
        us_a = 0
    us_time1 = time.time()
    while GPIO.input(makerobo_ECHO) == 1:
        us_a = 1
    us_time2 = time.time()
    us_during = us_time2 - us_time1
    return us_during * 340 / 2 * 100
def makerobo_loop():
    while True:
        us_dis = ur_disMeasure()
        print (us_dis, 'cm')
        print ('')
        if us_dis <10:
            makerobo_Buzz.ChangeFrequency(100)
        if us_dis<20:
            makerobo_Buzz.ChangeFrequency(300)
        else:
            makerobo_Buzz.ChangeFrequency(800)
        time.sleep(0.3)
def destroy():
    makerobo_Buzz.stop()
    GPIO.output(makerobo_Buzzer,1)
    GPIO.cleanup()
if __name__ == "__main__":
    makerobo_setup()
    try:
        makerobo_loop()
    except KeyboardInterrupt:
        destroy()