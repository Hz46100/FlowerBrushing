import win32gui
import win32con
import win32api
import win32process
import psutil
import time
import random
import keyboard

TARGET_EXE = "NRC-Win64-Shipping.exe"
is_running = False

# 虚拟键码映射表 (VK_CODE)
VK_MAP = {
    'tab': 0x09,
    '2': 0x32,
    'esc': 0x1B,
    'space': 0x20
}

#进程级窗口
def get_hwnd_by_exe(exe_name):
    """通过进程名精确获取游戏主窗口句柄"""
    target_pid = None
    #  遍历进程，找到游戏的 PID
    for proc in psutil.process_iter(['pid', 'name']):
        if proc.info['name'] and proc.info['name'].lower() == exe_name.lower():
            target_pid = proc.info['pid']
            break

    if not target_pid:
        return None

    # 根据 PID 寻找对应的可见窗口
    def callback(hwnd, hwnds):
        if win32gui.IsWindowVisible(hwnd) and win32gui.IsWindowEnabled(hwnd):
            _, pid = win32process.GetWindowThreadProcessId(hwnd)
            if pid == target_pid:
                # 虚幻引擎通常主窗口是有标题或尺寸最大的
                title = win32gui.GetWindowText(hwnd)
                if title:
                    hwnds.append(hwnd)
        return True

    hwnds = []
    win32gui.EnumWindows(callback, hwnds)

    if hwnds:
        return hwnds[0]
    return None

def safe_sleep(min_ms, max_ms):
    """
    将长睡眠切片为 50ms 的小段，允许脚本秒停
    """
    global is_running
    target_time = random.uniform(min_ms, max_ms) / 1000.0
    elapsed = 0.0

    while elapsed < target_time:
        if not is_running:
            return False  # 检测到停止信号，立刻打断
        time.sleep(0.05)
        elapsed += 0.05
    return True

# 后台消息注入
def send_bg_key(hwnd, key_name):
    """向游戏后台信箱投递真实的物理按键扫描码"""
    if not hwnd or not is_running: return

    vk = VK_MAP.get(key_name.lower())
    if not vk: return

    sc = win32api.MapVirtualKey(vk, 0)

    # 构造硬件级 LParam
    lparam_down = 1 | (sc << 16)
    lparam_up = 1 | (sc << 16) | 0xC0000000

    #  按下
    win32gui.PostMessage(hwnd, win32con.WM_KEYDOWN, vk, lparam_down)

    #  按键粘滞时长 80ms - 120ms
    if not safe_sleep(80, 120): return

    #  松开
    win32gui.PostMessage(hwnd, win32con.WM_KEYUP, vk, lparam_up)

# 刷花连招与防封逻辑
def farm_loop(hwnd):
    # --- 反检测 ：模拟玩家低头看手机发呆 (3% 概率) ---
    if random.random() <= 0.03:
        print("\n[防封机制] 触发真人发呆模拟 (预计 10-20 秒)...")
        if not safe_sleep(10000, 20000): return

    # --- 动作开始 ---
    print(">> 后台注入: [TAB] 锁定目标")
    send_bg_key(hwnd, 'tab')
    if not safe_sleep(900, 1100): return

    print(">> 后台注入: [2] 触发交互/鞠躬")
    send_bg_key(hwnd, '2')
    # 鞠躬动画等待，时间加入随机浮动，确保在 15 秒左右
    if not safe_sleep(14500, 15500): return

    print(">> 后台注入: [ESC] 取消/关闭界面")
    send_bg_key(hwnd, 'esc')
    if not safe_sleep(450, 550): return

    print(">> 后台注入: [Space] 跳跃")
    send_bg_key(hwnd, 'space')

    # --- 反检测 一轮结束后的随机喘息 (5% 概率) ---
    if random.random() <= 0.05:
        print("[防封机制] 循环结束，喝口水歇一下 (预计 5-10 秒)...")
        if not safe_sleep(5000, 10000): return
    else:
        # 正常的两轮之间的短间隔
        if not safe_sleep(800, 1200): return

# 主控程序
def toggle_script():
    global is_running
    is_running = not is_running
    if is_running:
        print("\n[▶] 脚本已启动！你现在可以把游戏切到后台或干别的事情了。(按 F9 暂停)")
    else:
        print("\n[⏸] 脚本已暂停！ (按 F9 恢复)")

def main():
    print("=======================================")
    print("  洛克王国：世界 - 纯后台防封终极版")
    print(f"  目标进程: {TARGET_EXE}")
    print("  操作说明: 按下 [F9] 键启动/暂停")
    print("=======================================\n")

    print("正在寻找游戏进程...")
    hwnd = get_hwnd_by_exe(TARGET_EXE)

    if not hwnd:
        print(f"[严重错误] 未找到进程 {TARGET_EXE}！")
        print("请确保《洛克王国：世界》已经启动，然后再运行此脚本。")
        return

    print(f"[成功] 锁定游戏进程，分配句柄 ID: {hwnd}")
    print(">> 准备就绪，请按 F9 键开始挂机。")

    # 绑定 F9 热键 (全局监听)
    keyboard.add_hotkey('f9', toggle_script)

    try:
        while True:
            if is_running:
                # 每一轮执行前，校验游戏是否意外关闭
                if win32gui.IsWindow(hwnd):
                    farm_loop(hwnd)
                else:
                    print("\n[错误] 游戏进程已丢失或关闭！脚本停止。")
                    break
            else:
                # 暂停状态下极低占用休眠
                time.sleep(0.1)

    except KeyboardInterrupt:
        print("\n=== 脚本已手动退出 ===")

if __name__ == "__main__":
    main()