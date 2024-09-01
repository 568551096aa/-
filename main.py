import cv2
import numpy as np
import pyautogui
import matplotlib.pyplot as plt
import win32gui
import win32con
import tkinter as tk
import threading
import time
import pygame
from pynput import keyboard

def get_window_handle_by_title(title):
    # 获取窗口句柄
    hwnd = win32gui.FindWindow(None, title)
    if hwnd == 0:
        raise ValueError(f"窗口 '{title}' 未找到")
    return hwnd

def get_window_rect(hwnd):
    # 获取窗口的矩形坐标 (left, top, right, bottom)
    rect = win32gui.GetWindowRect(hwnd)
    left, top, right, bottom = rect
    width = right - left
    height = bottom - top
    return (left, top, width, height)
class TemplateMatcher:
    def __init__(self, region):
        # 定义屏幕截取区域 (left, top, width, height)
        self.region = region
        self.template = None
        self.background_color = None
        self.isShow = False

    def load_template(self, template_path):
        # 加载模板图像
        self.template = cv2.imread(template_path)
        if self.template is None:
            raise ValueError(f"无法加载模板图像: {template_path}")
        # 获取模板的背景颜色
        self.background_color = self.get_background_color(self.template)

    def get_background_color(self, image):
        # 获取图片四个顶点的颜色（假设背景颜色是均匀的）
        top_left = image[0, 0]
        top_right = image[0, -1]
        bottom_left = image[-1, 0]
        bottom_right = image[-1, -1]
        
        # 计算四个顶点颜色的平均值，作为背景色
        background_color = np.mean([top_left, top_right, bottom_left, bottom_right], axis=0)
        return background_color.astype(int)

    def preprocess_image(self, image, threshold=30):
        # 转换为灰度图像
        gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
        # 创建掩膜，过滤掉背景色
        lower_bound = np.array(self.background_color - threshold, dtype=np.uint8)
        upper_bound = np.array(self.background_color + threshold, dtype=np.uint8)
        mask = cv2.inRange(image, lower_bound, upper_bound)
        mask_inv = cv2.bitwise_not(mask)
        
        # 应用掩膜，仅保留非背景区域
        filtered_image = cv2.bitwise_and(gray, gray, mask=mask_inv)
        
        return filtered_image

    def capture_screenshot(self):
        # 截取屏幕指定区域
        screenshot = pyautogui.screenshot(region=self.region)
        image = cv2.cvtColor(np.array(screenshot), cv2.COLOR_RGB2BGR)
        return image

    def set_screenRect(self, region):
        self.region = region

    def match_template(self, threshold=0.8):
        if self.template is None:
            raise ValueError("模板未加载。请使用 load_template 方法加载模板图像。")
        
        # 截取屏幕
        image = self.capture_screenshot()
        
        # 预处理输入图像和模板，过滤掉背景色
        processed_image = self.preprocess_image(image)
        processed_template = self.preprocess_image(self.template)
        
        # 执行模板匹配
        result = cv2.matchTemplate(processed_image, processed_template, cv2.TM_CCOEFF_NORMED)
        
        # 获取匹配结果的最大值和其位置
        min_val, max_val, min_loc, max_loc = cv2.minMaxLoc(result)
        
        # 检查最大值是否超过阈值
        if max_val >= threshold:
            print(f"匹配成功！匹配值: {max_val}")
            # 获取模板的宽高
            h, w = processed_template.shape
            # 获取匹配到的区域的左上角坐标
            top_left = max_loc
            bottom_right = (top_left[0] + w, top_left[1] + h)
            cv2.rectangle(image, top_left, bottom_right, (0, 255, 0), 2)
            
            # 返回匹配到的坐标点（相对于截取的区域）
            matched_position = (top_left[0] + w // 2, top_left[1] + h // 2)
            self.matched_image = image
            return matched_position
        else:
            print("未找到匹配的模板。")
            return None
    
    def set_show(self, isShow):
        self.isShow = isShow
    
    def show_matched_image(self):
        if hasattr(self, 'matched_image'):
            if self.isShow == True:
                plt.imshow(cv2.cvtColor(self.matched_image, cv2.COLOR_BGR2RGB))
                plt.title("Matched Image")
                plt.axis('off')
                plt.show()
        else:
            print("没有可显示的匹配结果。请先进行模板匹配。")


'''
# 示例使用
window_title = "夜神模拟器1"  # 替换为你要查找的窗口标题
try:
    hwnd = get_window_handle_by_title(window_title)
    print(f"窗口句柄: {hwnd}")

    rect = get_window_rect(hwnd)
    print(f"窗口坐标和大小: {rect}")
except ValueError as e:
    print(e)

# 示例使用
region = rect  # 定义屏幕截取区域
matcher = TemplateMatcher(region)

# 加载模板
matcher.load_template('5.png')

# 执行模板匹配
matched_position = matcher.match_template(threshold=0.7)
matcher.set_show(True)
if matched_position:
    print(f"匹配到的位置: {matched_position}")
    # 显示匹配结果
    matcher.show_matched_image()
else:
    print("模板匹配失败")
'''

def MouseMove(position, hwndPos=(0,0),delay=0.3):
    print(f"移动到的位置: {position}")
    pyautogui.moveTo(position[0] + hwndPos[0], position[1] + hwndPos[1], delay)  # duration 参数用于设置移动的时间（秒）

def MouseClick(delay=0.25):
    time.sleep(delay)
    pyautogui.click()

def FindHwnd(hwndStr):
    window_title = hwndStr  # 替换为你要查找的窗口标题
    try:
        hwnd = get_window_handle_by_title(window_title)
        print(f"窗口句柄: {hwnd}")

        rect = get_window_rect(hwnd)
        print(f"窗口坐标和大小: {rect}")
    except ValueError as e:
        print(e)
    return rect

def myCode():

    region = FindHwnd("夜神模拟器1")  # 定义屏幕截取区域
    matcher = TemplateMatcher(region)
    matcher.set_show(False)
    
    # 查找图片
    matcher.load_template('4.bmp')
    # 执行模板匹配
    matched_position = matcher.match_template(threshold=0.7)
    if matched_position:
        print(f"匹配到的位置: {matched_position}")
        # 显示匹配结果
        matcher.show_matched_image()
    else:
        print("模板匹配失败")
        return

    MouseMove(matched_position, (region[0], region[1]))
    MouseClick()


class Application(tk.Tk):
    def __init__(self):
        super().__init__()

        # 设置窗口标题和大小
        self.title("开始和结束按钮")
        self.geometry("300x150")

        # 初始化pygame用于播放音效
        pygame.mixer.init()

        # 加载音效
        #self.start_sound = pygame.mixer.Sound("start_sound.wav")
        #self.stop_sound = pygame.mixer.Sound("stop_sound.wav")

        # 创建变量来控制代码A的执行
        self.running = False
        self.lock = threading.Lock()  # 添加锁
        self.task_thread = None

        # 创建开始按钮
        self.start_button = tk.Button(self, text="开始 num1", command=self.start_action)
        self.start_button.pack(pady=20)

        # 创建结束按钮
        self.stop_button = tk.Button(self, text="结束 num2", command=self.stop_action)
        self.stop_button.pack(pady=20)

        # 启动全局按键监听器
        self.listener = keyboard.Listener(on_press=self.on_key_press)
        self.listener.start()
        # 处理窗口关闭事件
        self.protocol("WM_DELETE_WINDOW", self.on_closing)

    def start_action(self):
        with self.lock:  # 使用锁防止多次点击
            if not self.running:
                self.running = True
                # 使用线程执行代码A
                self.task_thread = threading.Thread(target=self.code_a)
                self.task_thread.start()
                #self.start_sound.play()  # 播放开始音效
                print("代码A开始执行")

    def stop_action(self):
        with self.lock:  # 使用锁防止多次点击
            if self.running:
                self.running = False
                if self.task_thread:
                    self.task_thread.join()  # 等待线程结束
                #self.stop_sound.play()  # 播放结束音效
                print("代码A已终止")

    def code_a(self):
        if self.running:
            # 执行代码A的实际任务
            print("代码A正在执行...")
            myCode()
            #self.stop_sound.play()  # 播放结束音效
            print("代码A执行完成")
        self.running = False  # 确保任务完成后更新状态

    def on_closing(self):
        self.listener.stop()  # 停止监听器
        self.stop_action()  # 停止任务
        self.destroy()  # 关闭窗口并释放资源

    def on_key_press(self, key):
        try:
            print(key.vk)
            # 检查是否按下小键盘的1键
            if key.vk == 97:  # 97 是小键盘 1 的虚拟键代码
                self.start_action()
            # 检查是否按下小键盘的2键
            elif key.vk == 98:  # 98 是小键盘 2 的虚拟键代码
                self.stop_action()
        except AttributeError:
            pass

if __name__ == "__main__":
    app = Application()
    app.protocol("WM_DELETE_WINDOW", app.on_closing)
    app.mainloop()

