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
        self.logger = logger_callback
        self.current_mode = 0  # 0代表刷花，1代表刷鬼火

    def log(self, msg):
        if self.logger:
            self.logger(msg)
        else:
            print(msg)

    def safe_sleep(self, min_ms, max_ms):
        target_time = random.uniform(min_ms, max_ms) / 1000.0
        elapsed = 0.0
        while elapsed < target_time:
            if not self.is_running:
                return False
            time.sleep(0.05)
            elapsed += 0.05
        return True

    # --- 基础按键收发 ---
    def send_bg_key(self, key_name):
        if not self.hwnd or not self.is_running: return
        vk = Config.VK_MAP.get(key_name.lower())
        if not vk: return
        sc = win32api.MapVirtualKey(vk, 0)
        lparam_down = 1 | (sc << 16)
        lparam_up = 1 | (sc << 16) | 0xC0000000
        win32gui.PostMessage(self.hwnd, win32con.WM_KEYDOWN, vk, lparam_down)
        if not self.safe_sleep(*Config.KEY_PRESS_DURATION): return
        win32gui.PostMessage(self.hwnd, win32con.WM_KEYUP, vk, lparam_up)

    def hold_bg_key(self, key_name):
        """物理按住某个键 (不断开)"""
        if not self.hwnd: return
        vk = Config.VK_MAP.get(key_name.lower())
        sc = win32api.MapVirtualKey(vk, 0)
        lparam_down = 1 | (sc << 16)
        win32gui.PostMessage(self.hwnd, win32con.WM_KEYDOWN, vk, lparam_down)

    def release_bg_key(self, key_name):
        """松开某个键"""
        if not self.hwnd: return
        vk = Config.VK_MAP.get(key_name.lower())
        sc = win32api.MapVirtualKey(vk, 0)
        lparam_up = 1 | (sc << 16) | 0xC0000000
        win32gui.PostMessage(self.hwnd, win32con.WM_KEYUP, vk, lparam_up)

    # 模式一：刷花
    def farm_loop(self):
        if random.random() <= Config.AFK_CHANCE:
            self.log("防封: 触发真人发呆模拟 (约10-20秒)...")
            if not self.safe_sleep(10000, 20000): return

        self.log("注入: [TAB] 锁定目标")
        self.send_bg_key('tab')
        if not self.safe_sleep(900, 1100): return

        self.log("注入: [2] 触发交互/鞠躬")
        self.send_bg_key('2')
        if not self.safe_sleep(*Config.BOW_WAIT): return

        self.log("注入: [ESC] 取消UI")
        self.send_bg_key('esc')
        if not self.safe_sleep(450, 550): return

        self.log("注入: [Space] 跳跃")
        self.send_bg_key('space')

        if random.random() <= Config.REST_CHANCE:
            self.log("防封: 循环结束，喝口水歇一下 (约5-10秒)...")
            if not self.safe_sleep(5000, 10000): return
        else:
            if not self.safe_sleep(*Config.ACTION_INTERVAL): return

    # 模式二：刷鬼火
    def ghost_fire_loop(self):
        self.log("注入: [按住 W 键] 开始前进")
        self.hold_bg_key('w')

        self.log("警告: 正在控制物理鼠标左转，此时请勿抢夺鼠标控制权！")

        # 只要还在运行状态，就不停移动鼠标
        while self.is_running and win32gui.IsWindow(self.hwnd):
            # 物理鼠标相对偏移 (向左)
            win32api.mouse_event(win32con.MOUSEEVENTF_MOVE, Config.GHOST_FIRE_MOUSE_SPEED, 0, 0, 0)

            # 使用高频物理休眠，保证鼠标顺滑不卡顿
            time.sleep(Config.GHOST_FIRE_TICK / 1000.0)

        # 循环结束 (用户按下 F9 或 窗口关闭时)
        self.log("注入: [松开 W 键] 停止前进")
        self.release_bg_key('w')