#实验三：无源蜂鸣器演奏生日快乐歌

import RPi.GPIO as GPIO
import time

BUZZER_PIN = 11
NOTE_FREQS = [
    262, 262, 294, 262, 349, 330,
    262, 262, 294, 262, 392, 349,
    262, 262, 523, 440, 349, 330, 294,
    466, 466, 440, 349, 392, 349
]
NOTE_DURATIONS = [
    4, 4, 8, 4, 4, 8,
    4, 4, 4, 4, 4, 4,
    4, 4, 4, 4, 4, 4, 4,
    4, 4, 4, 4, 4, 4
]
BASE_DURATION = 0.1
DELAY = 0.1


def setup():
    """初始化GPIO设置"""
    GPIO.setmode(GPIO.BOARD)
    GPIO.setwarnings(False)
    GPIO.setup(BUZZER_PIN, GPIO.OUT)


def play_buzzer(freq, duration):
    """播放指定频率和持续时间的音符"""
    if freq == 0:  # 0表示休止符
        time.sleep(duration)
        return

    # 创建PWM实例并播放音符
    buzzer = GPIO.PWM(BUZZER_PIN, freq)
    buzzer.start(50)
    time.sleep(duration)
    buzzer.stop()
    time.sleep(DELAY)


def play_happy_birthday():
    """播放《生日快乐》歌曲"""
    print('\n' + '*' * 40)
    print('*         祝你生日快乐！         *')
    print('*' * 40 + '\n')

    # 遍历所有音符并播放
    for freq, duration in zip(NOTE_FREQS, NOTE_DURATIONS):
        play_buzzer(freq, BASE_DURATION / duration * 4)


def destroy():
    """清理GPIO资源"""
    GPIO.output(BUZZER_PIN, GPIO.LOW)  # 关闭蜂鸣器
    GPIO.cleanup()  # 释放所有GPIO资源


def main():
    """主程序"""
    setup()
    try:
        print("程序运行中... 按下Ctrl+C退出")
        play_happy_birthday()  # 程序启动后自动播放音乐
        while True:  # 保持程序运行
            time.sleep(1)
    except KeyboardInterrupt:
        destroy()


if __name__ == '__main__':
    main()