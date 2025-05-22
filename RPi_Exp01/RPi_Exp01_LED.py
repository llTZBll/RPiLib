import RPi.GPIO as GPIO
import time

PIN_RED = 11
PIN_GREEN = 12
PWM_FREQ = 2000
COLORS = [0x00FF00,  # 绿色
          0xFF0000,  # 红色
          0x777777,  # 白色(中等亮度)
          0x000000]  # 关闭


def setup_gpio():
    """初始化GPIO设置"""
    GPIO.setmode(GPIO.BOARD)
    GPIO.setwarnings(False)
    GPIO.setup(PIN_RED, GPIO.OUT)
    GPIO.setup(PIN_GREEN, GPIO.OUT)
    GPIO.output(PIN_RED, GPIO.LOW)
    GPIO.output(PIN_GREEN, GPIO.LOW)


def main():
    """主控制函数"""
    # 初始化PWM实例
    pwm_red = GPIO.PWM(PIN_RED, PWM_FREQ)
    pwm_green = GPIO.PWM(PIN_GREEN, PWM_FREQ)

    # 启动PWM，初始占空比为0%
    pwm_red.start(0)
    pwm_green.start(0)

    try:
        while True:
            for color in COLORS:
                # 从24位颜色值中提取红色和绿色分量
                # 格式: 0xRRGGBB (这里我们忽略蓝色分量)
                red_val = (color >> 16) & 0xFF  # 提取红色分量
                green_val = (color >> 8) & 0xFF  # 提取绿色分量

                # 将8位颜色值(0-255)转换为占空比百分比(0-100)
                red_duty = 100 * red_val / 255
                green_duty = 100 * green_val / 255

                # 更新PWM占空比
                pwm_red.ChangeDutyCycle(red_duty)
                pwm_green.ChangeDutyCycle(green_duty)

                time.sleep(1)  # 每种颜色显示1秒

    except KeyboardInterrupt:
        # 捕获Ctrl+C中断信号，优雅地退出程序
        pwm_red.stop()
        pwm_green.stop()
        GPIO.output(PIN_RED, GPIO.LOW)
        GPIO.output(PIN_GREEN, GPIO.LOW)
        GPIO.cleanup()  # 清理GPIO设置
        print("\n程序已安全退出")


if __name__ == "__main__":
    setup_gpio()
    main()