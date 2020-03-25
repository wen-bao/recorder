#! /usr/bin/python3
# coding=utf-8
"""
screen.py 

Author: wenbao 
Description: my screen recoreder
"""
import cv2
import datetime
import numpy as np
import threading

import pyscreenshot as ImageGrab
from tkinter import Button
from tkinter import Frame
from tkinter import Tk


flag = None  # 停止标志位


def video_record():
    """屏幕录制！
    """
    print('开始录制!')
    date = datetime.datetime.now().strftime('%Y-%m-%d %H-%M-%S')  # 当前的时间
    p = ImageGrab.grab()  # 获得当前屏幕
    a, b = p.size  # 获得当前屏幕的大小
    fourcc = cv2.VideoWriter_fourcc(*'XVID')  # 编码格式
    filename = '{}.avi'.format(date)
    fps = 20  # 24
    #cv2.VideoWriter(filename, fourcc, fps, frameSize, isColor)
    # filename 要保存的文件的路径
    # fourcc 指定编码器
    # fps 要保存的视频的帧率
    # frameSize 要保存的文件的画面尺寸
    # isColor 指示是黑白画面还是彩色的画面
    video = cv2.VideoWriter(filename=filename, fourcc=fourcc,
                            fps=fps, frameSize=(a, b))
    while True:
        im = ImageGrab.grab()
        imm = cv2.cvtColor(np.array(im), cv2.COLOR_RGB2BGR)  # 转为opencv的BGR格式
        video.write(imm)
        if not flag:
            print("录制结束！")
            break
    video.release()


class Application(Frame):
    def __init__(self, master=None):
        Frame.__init__(self, master=master, height=2, bd=1, relief="groove")
        self.pack()
        self.createWidgets()

    def createWidgets(self):
        self.start = Button(self, text='start', fg='black',
                            bg='white', command=self.start)
        self.start.pack(side='left')

        self.stop = Button(self, text='stop', fg='black',
                           bg='white', command=self.stop, state='disable')
        self.stop.pack(side='right')

    def start(self):
        self.start['state'] = 'disabled'
        self.stop['state'] = 'normal'
        global flag
        flag = True
        self.th = threading.Thread(target=video_record)
        self.th.start()

    def stop(self):
        self.start['state'] = 'normal'
        self.stop['state'] = 'disabled'
        global flag
        flag = False


def main():
    try:
        root = Tk()   # 创建顶级窗口
        root.minsize(180, 30)  # 最小尺寸
        root.maxsize(180, 30)   # 最大尺寸
        root.resizable(0, 0)
        root.attributes('-topmost', True, '-alpha', 0.95)

        app = Application(master=root)
        # 设置窗口标题:
        app.master.title('wenbao recorder')
        # 主消息循环:
        app.mainloop()
    except Exception as err:
        raise


if __name__ == '__main__':
    main()
