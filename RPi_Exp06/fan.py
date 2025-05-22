import RPi.GPIO as GPIO

import time

# 设置风扇管脚PIN

Makerobo_MotorPin1 = 17


def Makerobo_setup():
    # 将GPIO模式设置为BCM编号

    GPIO.setmode(GPIO.BCM)

    GPIO.setwarnings(False)  # 忽略警告

    GPIO.setup(Makerobo_MotorPin1, GPIO.OUT)  # 风扇设置为输出模式


# 风扇电机控制函数

def Makerobo_motor(direction):
    # 开启风扇

    if direction == 1:
        GPIO.output(Makerobo_MotorPin1, GPIO.HIGH)

        print("Makerobo Open")

    # 关闭风扇

    if direction == 0:
        # 关闭风扇

        GPIO.output(Makerobo_MotorPin1, GPIO.LOW)

        print("Stop")


def Makerobo_main():
    fs_directions = {'Open': 1, 'STOP': 0}  # 定义开和关


while True:
    # 风扇开

    Makerobo_motor(fs_directions['Open'])

    time.sleep(5)

    # 风扇关

    Makerobo_motor(fs_directions['STOP'])

    time.sleep(5)


# 释放资源

def destroy():
    # 关闭风扇

    GPIO.output(Makerobo_MotorPin1, GPIO.LOW)

    # 释放资源

    GPIO.cleanup()


# 程序入口

if __name__ == '__main__':

    Makerobo_setup()

    try:

        Makerobo_main()

    except KeyboardInterrupt:  # 当按下Ctrl+C时，将执行destroy()子程序。

        destroy()  # 释放资源

