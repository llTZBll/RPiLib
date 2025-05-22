"""
树莓派环境监控系统
功能：
1. 通过DS18B20温度传感器监测环境温度
2. 使用PS2摇杆调整温度阈值上下限
3. RGB LED显示不同温度状态（蓝/绿/红）
4. 温度超限时蜂鸣器报警
5. 直流电机模拟风扇控制
6. 紧急停止按钮功能
"""

import RPi.GPIO as GPIO
import importlib
import time
import sys

# --------------------------
# 硬件引脚配置（BOARD编号模式）
# --------------------------
LED_R_PIN = 11  # RGB LED红色引脚
LED_G_PIN = 12  # RGB LED绿色引脚
LED_B_PIN = 13  # RGB LED蓝色引脚
BUZZER_PIN = 15  # 有源蜂鸣器引脚
MOTOR_PIN = 16  # 直流电机控制引脚
BUTTON_PIN = 32  # 紧急停止按钮引脚

# --------------------------
# 模块初始化
# --------------------------
GPIO.setmode(GPIO.BOARD)
GPIO.setwarnings(False)

# 导入自定义模块
joystick_module = importlib.import_module('14_joystick_PS2')
temp_sensor = importlib.import_module('25_ds18b20')
buzzer_module = importlib.import_module('09_active_buzzer')
rgb_led_module = importlib.import_module('02_rgb_led')
fan_module = importlib.import_module('fan')

# RGB颜色字典（使用GRB顺序）
RGB_COLORS = {
    'Red': 0x00FFFF,
    'Green': 0xFF00FF,
    'Blue': 0xFFFF00
}

# --------------------------
# 全局变量
# --------------------------
temp_lower = 24  # 默认温度下限
temp_upper = 27  # 默认温度上限


def initialize_system():
    """系统初始化函数"""
    # 初始化各硬件模块
    fan_module.Makerobo_setup()
    joystick_module.makerobo_setup()
    temp_sensor.makerobo_setup()
    buzzer_module.makerobo_setup(BUZZER_PIN)
    rgb_led_module.makerobo_setup(LED_R_PIN, LED_G_PIN, LED_B_PIN)

    # 按钮引脚设置（启用内部上拉电阻）
    GPIO.setup(BUTTON_PIN, GPIO.IN, pull_up_down=GPIO.PUD_UP)
    GPIO.add_event_detect(BUTTON_PIN, GPIO.BOTH, callback=emergency_stop, bouncetime=200)

    # 电机控制引脚初始化
    GPIO.setup(MOTOR_PIN, GPIO.OUT)
    GPIO.output(MOTOR_PIN, GPIO.LOW)


def adjust_thresholds():
    """
    通过摇杆调整温度阈值
    操作逻辑：
    - 上/下：调整上限温度
    - 左/右：调整下限温度
    - 温度范围：下限[-5, 上限-1]，上限[下限+1, 125]
    """
    global temp_lower, temp_upper
    direction = joystick_module.makerobo_direction()

    if direction == 'up' and temp_lower < temp_upper - 1 and temp_upper <= 125:
        temp_upper += 1
    elif direction == 'down' and temp_upper > temp_lower + 1 and temp_upper >= -4:
        temp_upper -= 1
    elif direction == 'right' and temp_lower < temp_upper - 1 and temp_lower <= 124:
        temp_lower += 1
    elif direction == 'left' and temp_lower > -5 and temp_lower < temp_upper - 1:
        temp_lower -= 1


def emergency_stop(chn):
    """紧急停止按钮中断回调函数"""
    if GPIO.input(BUTTON_PIN) == 0:
        print("\n紧急停止触发！")
        shutdown_system()


def temperature_monitoring_loop():
    """主监控循环"""
    while True:
        adjust_thresholds()
        current_temp = temp_sensor.makerobo_read()

        # 打印当前温度状态
        print(f"当前温度阈值：下限 {temp_lower}℃ / 上限 {temp_upper}℃")
        print(f"当前检测温度：{current_temp}℃\n")

        # 温度状态处理
        if float(current_temp) < temp_lower:
            handle_low_temperature()
        elif temp_lower <= float(current_temp) < temp_upper:
            handle_normal_temperature()
        else:
            handle_high_temperature(current_temp)

        time.sleep(1)  # 降低CPU占用率


def handle_low_temperature():
    """低温处理：蓝灯+蜂鸣提示"""
    rgb_led_module.makerobo_rgb_reset()
    fan_module.Makerobo_close()
    rgb_led_module.makerobo_set_Color(RGB_COLORS['Blue'])
    [buzzer_module.makerobo_beep(0.5) for _ in range(3)]  # 三次长蜂鸣


def handle_normal_temperature():
    """正常温度处理：绿灯常亮"""
    rgb_led_module.makerobo_rgb_reset()
    fan_module.Makerobo_close()
    rgb_led_module.makerobo_set_Color(RGB_COLORS['Green'])


def handle_high_temperature(current_temp):
    """高温处理：红灯+风扇+急促蜂鸣"""
    rgb_led_module.makerobo_rgb_reset()
    fan_module.Makerobo_open()
    rgb_led_module.makerobo_set_Color(RGB_COLORS['Red'])
    [buzzer_module.makerobo_beep(0.1) for _ in range(3)]  # 三次短促蜂鸣

    # 额外风扇控制（可选）
    GPIO.output(MOTOR_PIN, GPIO.HIGH if float(current_temp) > temp_upper else GPIO.LOW)


def shutdown_system():
    """系统关闭前的清理操作"""
    print("\n正在执行系统清理...")
    buzzer_module.destroy()
    joystick_module.destroy()
    temp_sensor.destroy()
    rgb_led_module.destroy()
    GPIO.output(MOTOR_PIN, GPIO.LOW)
    GPIO.cleanup()
    print("系统安全关闭！")
    sys.exit(0)


if __name__ == "__main__":
    try:
        initialize_system()
        temperature_monitoring_loop()
    except KeyboardInterrupt:
        shutdown_system()