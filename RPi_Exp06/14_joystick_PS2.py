import PCF8591 as ADC

import time


# 初始化

def makerobo_setup():
    ADC.setup(0x48)  # 设置PCF8591模块地址


global makerobo_state  # 状态变量


# 方向判断函数

def makerobo_direction():
    state = ['home', 'up', 'down', 'left', 'right', 'pressed']  # 方向状态信息

    i = 0

    if ADC.read(0) <= 30:
        i = 1  # up方向

    if ADC.read(0) >= 225:
        i = 2  # down方向

    if ADC.read(1) >= 225:
        i = 4  # left方向

    if ADC.read(1) <= 30:
        i = 3  # right方向


    if ADC.read(2) == 0 and ADC.read(1) == 128:
        i = 5  # Button按下

        # home位置

    if ADC.read(0) - 125 < 15 and ADC.read(0) - 125 > -15 and ADC.read(1) - 125 < 15 and ADC.read(
            1) - 125 > -15 and ADC.read(2) == 255:
        i = 0

    return state[i]  # 返回状态


# 循环函数

def makerobo_loop():
    makerobo_status = ''  # 状态值赋空值

    while True:

        makerobo_tmp = makerobo_direction()  # 调用方向判断函数

        if makerobo_tmp != None and makerobo_tmp != makerobo_status:  # 判断状态是否发生改变

            print(makerobo_tmp)  # 打印出方向位

            makerobo_status = makerobo_tmp  # 把当前状态赋给状态值，以防止同一状态多次打印


# 异常处理函数

def destroy():
    pass


# 程序入口

if __name__ == '__main__':

    makerobo_setup()  # 初始化

    try:

        makerobo_loop()  # 调用循环函数

    except KeyboardInterrupt:  # 当按下Ctrl+C时，将执行destroy()子程序。

        destroy()  # 调用释放函数

