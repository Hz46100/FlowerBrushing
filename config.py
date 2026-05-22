# config.py

class Config:
    # 目标游戏进程名
    TARGET_EXE = "NRC-Win64-Shipping.exe"

    # 虚拟键码映射表 (VK_CODE)
    VK_MAP = {
        'tab': 0x09,
        '2': 0x32,
        'esc': 0x1B,
        'space': 0x20
    }

    # === 时间与延迟配置 (单位：毫秒) ===
    # 每一个按键按下与抬起之间的粘滞时间
    KEY_PRESS_DURATION = (80, 120)

    # 鞠躬(2)按下后的等待时间 (14.5秒 - 15.5秒)
    BOW_WAIT = (14500, 15500)

    # 普通动作之间的间隔
    ACTION_INTERVAL = (800, 1200)

    # === 防封概率配置 ===
    AFK_CHANCE = 0.03  # 3% 的概率发呆 10-20秒
    REST_CHANCE = 0.05  # 5% 的概率一轮结束休息 5-10秒