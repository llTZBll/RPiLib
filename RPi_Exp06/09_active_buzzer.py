import RPi.GPIO as GPIO

import time

makerobo_Buzzer = 11  # 有源蜂鸣器管脚定义


# GPIO设置函数

def makerobo_setup(pin):
    global makerobo_BuzzerPin

    makerobo_BuzzerPin = pin

    GPIO.setmode(GPIO.BOARD)  # 采用实际的物理管脚给GPIO口

    GPIO.setwarnings(False)  # 关闭GPIO警告提示

    GPIO.setup(makerobo_BuzzerPin, GPIO.OUT)  # 设置蜂鸣器管脚为输出模式

    GPIO.output(makerobo_BuzzerPin, GPIO.HIGH)  # 关闭蜂鸟器


#  打开蜂鸣器

def makerobo_buzzer_on():
    GPIO.output(makerobo_BuzzerPin, GPIO.LOW)  # 蜂鸣器为低电平触发


# 关闭蜂鸣器

def makerobo_buzzer_off():
    GPIO.output(makerobo_BuzzerPin, GPIO.HIGH)


# 控制蜂鸣器鸣叫

def makerobo_beep(x):
    makerobo_buzzer_on()  # 打开蜂鸣器控制

    time.sleep(x)  # 延时时间

    makerobo_buzzer_off()  # 关闭蜂鸣器控制

    time.sleep(x)  # 延时时间


# 循环函数

def loop():
    while True:
        makerobo_beep(0.5)  # 控制蜂鸣器鸣叫，延时时间为500ms


def destroy():
    GPIO.output(makerobo_BuzzerPin, GPIO.HIGH)  # 关闭蜂鸣器鸣叫

    GPIO.cleanup()  # 释放资源


# 程序入口

if __name__ == '__main__':

    makerobo_setup(makerobo_Buzzer)  # 设置GPIO管脚

    try:  # 检测异常

        loop()  # 调用循环函数

    except KeyboardInterrupt:  # 当按下Ctrl+C时，将执行destroy()子程序。

        destroy()  # 释放资源