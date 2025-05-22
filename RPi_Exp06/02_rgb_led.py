import RPi.GPIO as GPIO   #导入RPi.GPIO，并起别名GPIO

import time    #导入时间库，提供延时、时钟和其它时间函数

GPIO.setmode(GPIO.BOARD)   #设置引脚编号模式为板载模式

GPIO.setwarnings(False)   #去除GPIO口警告

pinR=11    #物理位置编号，红色针脚为11号

pinG=12    #物理位置编号，绿色针脚为12号

GPIO.setup(pinR,GPIO.OUT)  #设置针脚模式为输出

GPIO.setup(pinG,GPIO.OUT)  #设置针脚模式为输出

GPIO.output(pinR,GPIO.LOW)  #设置针脚为低电平，关掉LED灯

GPIO.output(pinG,GPIO.LOW)  #设置针脚为低电平，关掉LED灯

i=0

while i<5:

    GPIO.output(pinR,GPIO.HIGH)  #设置红灯对应的针脚为高电平，打开LED灯

    time.sleep(1)  #程序等待1秒

    GPIO.output(pinR,GPIO.LOW)  #设置红灯对应的针脚为低电平，关闭LED灯

    time.sleep(1)  #程序等待1秒

    i=i+1  #循环变量增1

GPIO.cleanup()  #释放资源

