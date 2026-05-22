# core/window_manager.py

import win32gui
import win32process
import psutil

class WindowManager:
    @staticmethod
    def get_hwnd_by_exe(exe_name):
        """通过进程名精确获取游戏主窗口句柄"""
        target_pid = None
        for proc in psutil.process_iter(['pid', 'name']):
            if proc.info['name'] and proc.info['name'].lower() == exe_name.lower():
                target_pid = proc.info['pid']
                break

        if not target_pid: 
            return None

        hwnds = []
        def callback(hwnd, hwnds_list):
            if win32gui.IsWindowVisible(hwnd) and win32gui.IsWindowEnabled(hwnd):
                _, pid = win32process.GetWindowThreadProcessId(hwnd)
                if pid == target_pid and win32gui.GetWindowText(hwnd):
                    hwnds_list.append(hwnd)
            return True

        win32gui.EnumWindows(callback, hwnds)
        return hwnds[0] if hwnds else None