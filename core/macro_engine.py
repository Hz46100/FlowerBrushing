# core/macro_engine.py

import time
import random
import win32gui
import win32con
import win32api
from config import Config


class MacroEngine:
    def __init__(self, logger_callback=None):
        self.is_running = False
        self.hwnd = None
        self.logger = logger_callback  # 用于向外部(比如GUI)发送日志

    def log(self, msg):
        """记录日志"""
        if self.logger:
            self.logger(msg)
        else:
            print(msg)

    def safe_sleep(self, min_ms, max_ms):
        """切片睡眠，支持秒停"""
        target_time = random.uniform(min_ms, max_ms) / 1000.0
        elapsed = 0.0
        while elapsed < target_time:
            if not self.is_running:
                return False
            time.sleep(0.05)
            elapsed += 0.05
        return True

    def send_bg_key(self, key_name):
        """后台物理按键注入"""
        if not self.hwnd or not self.is_running: return
        vk = Config.VK_MAP.get(key_name.lower())
        if not vk: return

        sc = win32api.MapVirtualKey(vk, 0)
        lparam_down = 1 | (sc << 16)
        lparam_up = 1 | (sc << 16) | 0xC0000000

        win32gui.PostMessage(self.hwnd, win32con.WM_KEYDOWN, vk, lparam_down)
        if not self.safe_sleep(*Config.KEY_PRESS_DURATION): return
        win32gui.PostMessage(self.hwnd, win32con.WM_KEYUP, vk, lparam_up)

    def farm_loop(self):
        """刷花主逻辑"""
        # 1. 模拟真人发呆
        if random.random() <= Config.AFK_CHANCE:
            self.log("防封: 触发真人发呆模拟 (约10-20秒)...")
            if not self.safe_sleep(10000, 20000): return

        self.log("注入: [TAB] 锁定目标")
        self.send_bg_key('tab')
        if not self.safe_sleep(900, 1100): return

        self.log("注入: [2] 触发交互/鞠躬")
        self.send_bg_key('2')
        # 读取 config 里的 15秒 等待时间
        if not self.safe_sleep(*Config.BOW_WAIT): return

        self.log("注入: [ESC] 取消UI")
        self.send_bg_key('esc')
        if not self.safe_sleep(450, 550): return

        self.log("注入: [Space] 跳跃")
        self.send_bg_key('space')

        # 2. 循环结束喘息
        if random.random() <= Config.REST_CHANCE:
            self.log("防封: 循环结束，喝口水歇一下 (约5-10秒)...")
            if not self.safe_sleep(5000, 10000): return
        else:
            if not self.safe_sleep(*Config.ACTION_INTERVAL): return