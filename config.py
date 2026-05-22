# config.py

class Config:
    # 目标游戏进程名
    TARGET_EXE = "NRC-Win64-Shipping.exe"

    # === 挂机模式 ===
    MODES = [
        "刷花",
        "刷鬼火"
    ]

    # 虚拟键码映射表 (VK_CODE)
    VK_MAP = {
        'tab': 0x09,
        '2': 0x32,
        'esc': 0x1B,
        'space': 0x20,
        'w': 0x57
    }

    # 刷花模式 - 延迟配置 (单位：毫秒)
    KEY_PRESS_DURATION = (80, 120)  # 按键粘滞时间
    BOW_WAIT = (14500, 15500)  # 鞠躬等待 (15秒)
    ACTION_INTERVAL = (800, 1200)  # 动作间隔

    # 刷鬼火模式 - 移动配置
    GHOST_FIRE_MOUSE_SPEED = -5  # 鼠标向左移动的速度 (负数向左，正数向右，数值越大转越快)
    GHOST_FIRE_TICK = 30  # 鼠标每隔多少毫秒移动一次 (30ms 视觉上比较顺滑)

    # 防封概率配置
    AFK_CHANCE = 0.03  # 3% 的概率发呆 10-20秒
    REST_CHANCE = 0.05  # 5% 的概率一轮结束休息 5-10秒