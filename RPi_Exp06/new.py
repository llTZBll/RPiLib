#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
智能温控报警系统
功能：
1. 通过摇杆设置温度阈值区间
2. 根据实时温度显示不同颜色LED指示灯
3. 温度异常时触发蜂鸣器报警
4. 超温时发送邮件通知（5分钟冷却机制）
硬件模块：
- RGB LED灯
- 有源蜂鸣器
- PS2摇杆
- DS18B20温度传感器
"""

import RPi.GPIO as GPIO
import importlib
import time
import sys
import smtplib
from email.mime.text import MIMEText

# 硬件引脚定义（BCM编号模式）
LED_RED_PIN = 11  # 红色LED引脚
LED_GREEN_PIN = 12  # 绿色LED引脚
LED_BLUE_PIN = 36  # 蓝色LED引脚
BUZZER_PIN = 15  # 蜂鸣器引脚

# 动态导入自定义模块
joystick_module = importlib.import_module('14_joystick_PS2')
temp_sensor_module = importlib.import_module('25_ds18b20')
buzzer_module = importlib.import_module('09_active_buzzer')
rgb_led_module = importlib.import_module('02_rgb_led')

# 模块初始化
joystick_module.makerobo_setup()  # PS2摇杆初始化
temp_sensor_module.makerobo_setup()  # 温度传感器初始化
buzzer_module.makerobo_setup(BUZZER_PIN)  # 蜂鸣器初始化
rgb_led_module.makerobo_setup(LED_RED_PIN, LED_GREEN_PIN, LED_BLUE_PIN)  # RGB LED初始化

# 颜色定义（十六进制RGB值）
COLOR_MAP = {
    'Red': 0xFF0000,  # 红色
    'Green': 0x00FF00,  # 绿色
    'Blue': 0x0000FF  # 蓝色
}


def send_temp_alert_email(current_temp, threshold_temp):
    """
    发送温度警报邮件
    参数：
        current_temp: 当前温度值
        threshold_temp: 设置的阈值温度
    """
    # 邮件配置（建议将敏感信息移至配置文件中）
    sender = "3206997548@qq.com"  # 发件邮箱
    receiver = "3206997548@qq.com"  # 收件邮箱
    smtp_server = "smtp.qq.com"  # SMTP服务器
    username = "3206997548@qq.com"  # 邮箱账号
    password = "sujonttfjecqddee"

    # 构建邮件内容
    subject = "温度异常警报！"
    body = f"警告！当前温度 {current_temp}°C 已超过设定阈值 {threshold_temp}°C"

    msg = MIMEText(body, 'plain', 'utf-8')
    msg['From'] = sender
    msg['To'] = receiver
    msg['Subject'] = subject

    try:
        # 建立SMTP连接并发送邮件
        with smtplib.SMTP(smtp_server, 587) as server:
            server.starttls()
            server.login(username, password)
            server.sendmail(sender, receiver, msg.as_string())
        print("警报邮件发送成功！")
        return True
    except Exception as e:
        print(f"邮件发送失败：{str(e)}")
        return False


def system_init():
    """系统全局变量初始化"""
    global temp_lower, temp_upper, last_email_time
    temp_lower = 24  # 默认温度下限(°C)
    temp_upper = 28  # 默认温度上限(°C)
    last_email_time = 0  # 邮件发送时间记录（防频发）


def handle_joystick_input():
    """
    处理摇杆输入控制
    控制逻辑：
    - 按下摇杆：退出系统
    - 方向右：提高温度下限
    - 方向上：提高温度上限
    - 方向左：降低温度下限
    - 方向下：降低温度上限
    """
    global temp_lower, temp_upper
    direction = joystick_module.makerobo_direction()

    if direction == 'pressed':
        system_shutdown()
    elif direction == 'right' and temp_upper <= 35:
        temp_lower += 1
    elif direction == 'up' and temp_lower < temp_upper - 1:
        temp_upper += 1
    elif direction == 'left' and temp_lower < temp_upper - 1:
        temp_lower -= 1
    elif direction == 'down' and temp_lower >= 10:
        temp_upper -= 1


def main_loop():
    """主控制循环"""
    global last_email_time
    EMAIL_COOLDOWN = 300  # 邮件发送冷却时间（秒）

    while True:
        handle_joystick_input()  # 处理摇杆输入

        # 读取温度并显示阈值信息
        current_temp = temp_sensor_module.makerobo_read()
        print(f"[阈值下限] {temp_lower}°C\t[阈值上限] {temp_upper}°C\t[当前温度] {current_temp}°C")

        if current_temp is None:
            continue  # 跳过无效温度读数

        current_temp = float(current_temp)

        # 温度状态判断与控制逻辑
        if current_temp < temp_lower:
            # 低温状态：蓝灯 + 蜂鸣器慢响
            rgb_led_module.set_Color(COLOR_MAP['Blue'])
            [buzzer_module.makerobo_beep(0.5) for _ in range(3)]
        elif temp_lower <= current_temp < temp_upper:
            # 正常状态：绿灯常亮
            rgb_led_module.set_Color(COLOR_MAP['Green'])
        else:
            # 超温状态：红灯 + 蜂鸣器快响
            rgb_led_module.set_Color(COLOR_MAP['Red'])
            [buzzer_module.makerobo_beep(0.1) for _ in range(3)]

            # 冷却时间检查与邮件发送
            if time.time() - last_email_time >= EMAIL_COOLDOWN:
                if send_temp_alert_email(current_temp, temp_upper):
                    last_email_time = time.time()


def system_shutdown():
    """系统清理与资源释放"""
    buzzer_module.destroy()
    joystick_module.destroy()
    temp_sensor_module.destroy()
    rgb_led_module.destroy()
    sys.exit("系统已安全关闭")


if __name__ == "__main__":
    try:
        system_init()
        main_loop()
    except KeyboardInterrupt:
        system_shutdown()
    except Exception as e:
        print(f"系统运行异常：{str(e)}")
        system_shutdown()