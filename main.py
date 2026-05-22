# main.py

import time
import threading
import tkinter as tk
from tkinter import ttk, scrolledtext
import keyboard
import win32gui

from config import Config
from core.window_manager import WindowManager
from core.macro_engine import MacroEngine


class MacroApp:
    def __init__(self, root):
        self.root = root
        self.root.title("向阳花 / 鬼火 自动挂机 Pro")
        self.root.geometry("450x420")  # 稍微拉长一点高度容纳下拉框
        self.root.attributes("-topmost", True)

        self.engine = MacroEngine(logger_callback=self.log)

        # --- UI 组件搭建 ---
        self.lbl_status = tk.Label(root, text="状态: 等待启动", font=("Microsoft YaHei", 12, "bold"), fg="gray")
        self.lbl_status.pack(pady=10)

        # 模式选择下拉框
        self.lbl_mode = tk.Label(root, text="挂机模式选择:", font=("Microsoft YaHei", 10, "bold"))
        self.lbl_mode.pack(pady=(5, 0))

        self.mode_var = tk.StringVar()
        self.mode_combo = ttk.Combobox(root, textvariable=self.mode_var, values=Config.MODES, state="readonly",
                                       width=30)
        self.mode_combo.current(0)  # 默认选中第一个
        self.mode_combo.pack(pady=5)

        # 启动按钮
        self.btn_toggle = tk.Button(root, text="▶ 启动 (F9)", font=("Microsoft YaHei", 12),
                                    bg="#4CAF50", fg="white", width=20, command=self.toggle_script)
        self.btn_toggle.pack(pady=10)

        # 日志区
        self.log_area = scrolledtext.ScrolledText(root, width=55, height=10, font=("Consolas", 9))
        self.log_area.pack(pady=5)

        self.log("=== 欢迎使用纯后台挂机助手 ===")
        self.log(f"目标进程: {Config.TARGET_EXE}")

        keyboard.add_hotkey('f9', self.toggle_script_from_hotkey)

        self.macro_thread = threading.Thread(target=self.macro_thread_worker, daemon=True)
        self.macro_thread.start()

    def log(self, message):
        current_time = time.strftime("%H:%M:%S", time.localtime())
        msg = f"[{current_time}] {message}\n"
        self.root.after(0, self._append_log, msg)

    def _append_log(self, msg):
        self.log_area.insert(tk.END, msg)
        self.log_area.see(tk.END)

    def toggle_script_from_hotkey(self):
        self.root.after(0, self.toggle_script)

    def toggle_script(self):
        self.engine.is_running = not self.engine.is_running
        if self.engine.is_running:
            # 启动时：读取当前下拉框选中的模式索引，并禁用下拉框
            self.engine.current_mode = self.mode_combo.current()
            self.mode_combo.config(state="disabled")

            mode_name = Config.MODES[self.engine.current_mode].split(" ")[0]
            self.lbl_status.config(text=f"状态: 运行中 ({mode_name})", fg="green")
            self.btn_toggle.config(text="⏸ 暂停 (F9)", bg="#F44336")
            self.log(f"▶ 已启动: {Config.MODES[self.engine.current_mode]}")
        else:
            # 暂停时：恢复下拉框可用状态
            self.mode_combo.config(state="readonly")
            self.lbl_status.config(text="状态: 已暂停", fg="red")
            self.btn_toggle.config(text="▶ 恢复 (F9)", bg="#4CAF50")
            self.log("⏸ 挂机已暂停。")

    def macro_thread_worker(self):
        self.engine.hwnd = WindowManager.get_hwnd_by_exe(Config.TARGET_EXE)
        if not self.engine.hwnd:
            self.log(f"[严重错误] 未找到 {Config.TARGET_EXE} 进程！")
            self.log("请先打开游戏，然后重启本软件。")
        else:
            self.log(f"[成功] 已绑定游戏句柄: {self.engine.hwnd}")

        while True:
            if self.engine.is_running:
                if win32gui.IsWindow(self.engine.hwnd):
                    # 根据选中的模式，执行不同的函数
                    if self.engine.current_mode == 0:
                        self.engine.farm_loop()
                    elif self.engine.current_mode == 1:
                        self.engine.ghost_fire_loop()
                else:
                    self.log("[错误] 游戏窗口已关闭！自动停止。")
                    self.root.after(0, self.toggle_script)
                    self.engine.hwnd = None
            else:
                time.sleep(0.1)


if __name__ == "__main__":
    root = tk.Tk()
    app = MacroApp(root)
    root.mainloop()