#!/usr/bin/python
#  -*- coding: UTF-8 -*-
# 导入模块
from tkinter import *
import tkinter.filedialog
import tkinter.messagebox
import tkinter.simpledialog
from tkinter.filedialog import askopenfilename, askdirectory
from PIL import Image, ImageTk, ImageDraw
from aip import AipOcr
import os
import time
import glob

__author__ = '我肥我任性'
__email__ = 'yefengyun241@163.com'

"""
    数据集整理小工具
"""


class SetName(object):
    """
    设置文件名称路径类
    """

    def __init__(self, word=0, path='/usr/bin/python', filname='1', fillist='', imaglist=None, imgsuffix='jpg'):
        # 初始化名字列表和当前文件所在路径
        self.word = word  # 计数器
        self.path = path  # 默认路径
        self.filename = filname  # 默认文件名
        self.filelist = fillist  # 默认文件列表
        self.imglist = imaglist  # 默认图像列表
        self.imgsuffix = imgsuffix  # 默认图像后缀d

    def getPhotoName(self):
        # 以.jpg位格式
        self.word += 1
        photoname = self.filename[0:-3] + "_" + str(self.word) + '.' + self.imgsuffix
        self.imglist.append(photoname)
        return photoname

    def getFilename(self):
        return self.filename[0:-3]

    def getPointDataName(self):
        # 数据存储文件名称，以.txt为格式
        dataname = self.filename[0:-3] + ".txt"
        self.filelist = dataname
        return dataname

    def setDirName(self, name):
        # 获取当前文件所在路径
        result = os.path.split(name)
        self.path = result[0]
        # self.imgsuffix = name.split('.')[1]
        self.filename = self.getFileName(result[1])

    @staticmethod
    def getFileName(FN):
        name = FN[0:-4] + 'dir'
        return name


class Windows(object):
    """
    主窗口
    """

    def __init__(self):
        # 初始化各个参数变量
        global root  # 全局变量TK窗口
        global mainframe  # 主容器mainframe
        global SN  # 类setName
        global win  # 标记and文件夹编号
        win = 0  # 初始化为0
        SN = SetName()  # 初始化类类setName
        root = Tk()  # 初始化组窗口
        root.title("OCR数据集小工具")  # 设置标题
        root.iconbitmap('./utils/favicon.ico')
        root.attributes("-alpha", 1.0)  # 设置窗口边缘透明度

        self.canvas = tkinter.Canvas(root, width=600, height=600, bg='grey')
        image = Image.open("./utils/bg.jpg")
        im = ImageTk.PhotoImage(image)
        self.canvas.create_image(image.size[0] / 2, image.size[1] / 2, image=im)
        self.setText()
        self.canvas.pack()

        mainframe = Frame(root, width=0, height=0)  # 设置主容器大小

        mainframe.pack(expand=True, fill=BOTH)

        self.menu()  # 调用menu菜单组件
        root.mainloop()  # 进入消息循环

    def setText(self):
        file = open("./utils/README.txt")
        txt = file.readlines()
        for i in range(len(txt)):
            tt = txt[i].split('\n')[0]
            if i == 0:
                self.canvas.create_text(250, 30, text=txt[i].split('\n')[0])
            else:
                self.canvas.create_text(len(tt) / 3 * 16, 30 + i * 20, text=tt)

    def menu(self):
        # 创建菜单栏
        menu__bar = Menu(root)
        root.config(menu=menu__bar)
        # 创建名为File的菜单项
        file_menu = Menu(menu__bar, tearoff=0)
        menu__bar.add_cascade(label="文件", menu=file_menu)
        file_menu.add_command(label="打开", command=self._open)
        file_menu.add_command(label="保存", command=self._save)
        file_menu.add_separator()
        file_menu.add_command(label="退出", command=self._quit)
        # 创建名为Tool的菜单项
        tool_menu = Menu(menu__bar, tearoff=0)
        menu__bar.add_cascade(label="工具", menu=tool_menu)
        tool_menu.add_command(label="统一大图大小", command=self._changeimg)
        tool_menu.add_command(label="大图批量重命名", command=self._imgrename)
        # 创建名为Edit的菜单项
        tool_menu = Menu(menu__bar, tearoff=0)
        menu__bar.add_cascade(label="编辑", menu=tool_menu)
        tool_menu.add_command(label="小标签批量重命名", command=self._smallchangeimg)
        tool_menu.add_command(label="小标签归一化", command=self._smallimgrename)
        # 创建名为Beta的菜单项
        tool_menu = Menu(menu__bar, tearoff=0)
        menu__bar.add_cascade(label="测试(不稳定)", menu=tool_menu)
        tool_menu.add_command(label="小标签批量识别(一天1750张)", command=self._ocrsmallchangeimg)
        # 创建名为Help的菜单项
        tool_menu = Menu(menu__bar, tearoff=0)
        menu__bar.add_cascade(label="更多", menu=tool_menu)
        tool_menu.add_command(label="关于", command=self._about)

    def _open(self):
        # 打开文件事件
        global win  # 使用全局变量win
        fname = askopenfilename(
            # filetypes=[('JPG', '.jpg'), ('BMP', '.bmp'), ('GIF', '.gif'), ("PNG", '.png')])  # 打开文件选取窗口
            filetypes=[('JPG', '.jpg'), ("PNG", '.png'), ('GIF', '.gif')])  # 打开文件选取窗口
        try:
            SN.setDirName(fname)  # 设置当前文件路径
        except AttributeError:
            print("无效路径")
            return
        else:
            SN.imglist = []  # 置图片列表为空

        if fname == '':  # 没用选中文件，返回
            return
        else:
            self.canvas.pack_forget()  # 设置画布不可见
            self.canvas.destroy()  # 销毁前一次画布
            if win == 0:  # 第一次打开文件
                win += 1
                EditImage(fname)  # 打开图像编辑
            else:
                win += 1
                SN.word = 0  # 文件计数器归零
                sonframe.pack_forget()  # 子容器不可见
                sonframe.destroy()  # 销毁前一次编辑
                EditImage(fname)  # 创建新的图像编辑

    def _save(self):
        # 保存已标记图片名称到txt文件
        strpath = SN.path + '/' + SN.filename + '/data' + SN.getPointDataName()
        filenames = ""
        for i in SN.imglist:  # 获取文件列表
            filenames = filenames + i + " " + "\n"

        with open(strpath, 'w') as file:  # 写入数据
            file.write(filenames)

            # print(strpath)

    def _changeimg(self):
        # 修改图片成标准A4纸大小(1240×1754 100px)
        flist = []
        fnlist = []
        paths = askdirectory()
        # print(paths)
        if paths is None: return
        files = os.walk(paths)
        for path, d, filelist in files:
            for filename in filelist:
                if filename.endswith('.jpg') or filename.endswith('.png') or filename.endswith(
                        '.jpeg') or filename.endswith('.bmp'):
                    fname = os.path.join(path, filename)
                    newfilename = "new" + filename
                    fnlist.append(newfilename)
                    flist.append(fname)

        for i in flist:
            im = Image.open(i)
            if im.size[0] >= 1240 or im.size[1] >= 1754:
                out = im.resize((1240, 1754), Image.ANTIALIAS)  # 1240×1754
                out.save(fnlist.pop(0))
            else:
                fnlist.pop(0)

    def _imgrename(self):
        # 重命名图片并把不合格图片更改格式
        num = 0
        num = self.getNum()
        paths = askdirectory()
        # print(paths)
        if paths is None: return
        files = os.walk(paths)
        for path, d, filelist in files:
            for filename in filelist:
                if filename.endswith('.jpg') or filename.endswith('.png') or filename.endswith(
                        '.JPG') or filename.endswith('.PNG'):
                    num = self.getNum()
                    newName = 'OCR_img' + str(num) + '.' + filename.split('.')[1]
                    # print(newName)
                    os.rename(os.path.join(path, filename), os.path.join(path, newName))
                elif filename.endswith('.gif') or filename.endswith('.GIF'):
                    num = self.getNum()
                    newName = 'OCR_img' + str(num) + '.jpg'
                    self.changeformat(filename, path, newName)
                else:
                    pass

    def _smallchangeimg(self):
        """
        小标签批量重命名
        :return:
        """
        headfilename = tkinter.simpledialog.askstring("文件名", "请输入新的文件名")
        if headfilename is None or headfilename is "":
            tkinter.messagebox.showinfo('提示', '请输入正确的文件名!')
        else:
            imgformats = tkinter.simpledialog.askstring("文件名", "请输入图片后缀名（png,jpg）")
            if imgformats.lower() == 'png' or imgformats.lower() == 'jpg':
                filedirname = tkinter.filedialog.askdirectory()
                if filedirname is None or filedirname is "":
                    tkinter.messagebox.showinfo('提示', '请选择文件夹！')
                else:
                    self.rename_file(filedirname, headfilename, imgformats.lower())
                    tkinter.messagebox.showinfo('提示', '完成')
            else:
                tkinter.messagebox.showinfo('提示', '请输入正确的文件格式!')

    def rename_file(self, dirname, headfilename, formats='png'):
        """
        批量修改文件名称
        :param dirname: 文件所在目录
        :param headfilename: 头文件名
        :param formats: 选择格式
        :return:
        """
        newnamelist = []
        t = time.localtime(time.time())
        date = '{}{}{}'.format(t.tm_year, t.tm_mon, t.tm_mday)
        filelists = glob.glob('{}/*.{}'.format(dirname, formats))
        for index in range(len(filelists)):
            newname = "%s/%s_%s_%06d.png" % (dirname, headfilename, date, index)
            os.rename(filelists[index], newname)
            newnamelist.append("%s_%s_%06d.png" % (headfilename, date, index))

        # 生成新的txt文件记录所有文件名称
        newnametxt = '{}/{}.txt'.format(dirname, headfilename)
        with open(newnametxt, 'w+') as text:
            string = ""
            for name in newnamelist:
                string += name + ' \n'
            text.write(string)

    def _smallimgrename(self):
        """
        小标签归一化(256*32)
        :return:
        """
        # 规定统一图片宽度（像素）
        imgW = 256
        # 规定统一图片高度（像素）
        imgH = 32
        formats = tkinter.simpledialog.askstring("文件格式", "请输入要归一化的图像格式（jpg，png）")
        if formats == 'jpg' or formats == 'png':
            filedirname = tkinter.filedialog.askdirectory()
            if filedirname is None or filedirname is "":
                tkinter.messagebox.showinfo('提示', '请选择文件夹！')
            else:
                files = glob.glob('{}/*.{}'.format(filedirname, formats))
                if len(files) < 1:
                    tkinter.messagebox.showinfo('提示', '没有此格式的文件!')
                else:
                    for imgpath in files:
                        # 生成图像对象
                        im = Image.open(imgpath)
                        # 获取图像宽高
                        width, high = im.size
                        if width > imgW and high > imgH:
                            h = float(imgW) / width * high
                            if h > imgH:
                                w = float(imgH) / h * imgW
                                im = im.resize((int(w), imgH), Image.ANTIALIAS)
                            else:
                                im = im.resize((imgW, int(h)), Image.ANTIALIAS)
                        elif width > imgW and high < imgH:
                            h = float(imgW) / width * high
                            im = im.resize((imgW, int(h)), Image.ANTIALIAS)
                        elif width < imgW and high > imgH:
                            w = float(imgH) / high * width
                            im = im.resize((int(w), imgH), Image.ANTIALIAS)
                        else:
                            im = im

                        newimg = Image.new('RGBA', (imgW, imgH), (255, 255, 255))
                        newimg.paste(im, ((imgW - im.size[0]) // 2, (32 - im.size[1]) // 2))
                        newimg = newimg.convert("RGB")
                        newimg.save(imgpath)
                    tkinter.messagebox.showinfo('提示', '完成')
        else:
            tkinter.messagebox.showinfo('提示', '格式不正确！')

    def _ocrsmallchangeimg(self):
        """
        小标签批量识别(一天1750张)
        :return:
        """
        """ 你的 APPID AK SK(一个账号一天只能识别1750张) """
        APP_ID = '10900774'
        API_KEY = 'r2vz8vcyMaYSBuIEj7USgkz5'
        SECRET_KEY = 'RZKlFBN77lwlcRCUo3LkFxEdOYXdAnF8'

        client = AipOcr(APP_ID, API_KEY, SECRET_KEY)

        '''使用次数（请填写你今天使用的次数）
        通用文字识别  0-500
        通用文字识别（含位置信息版）500-1000
        网络图片文字识别 1000-1500
        通用票据识别 1500-1700
        通用文字识别（高精度版）1700-1750
        '''

        def get_file_content(fpath):
            """
            读取图片流
            :param fpath:文件路径
            :return:图片流
            """
            with open(fpath, 'rb') as fp:
                return fp.read()

        def rename_file(dirtname, INDEX, formats='png'):
            """
            批量修改文件名称
            :param dirtname: 头文夹名
            :param INDEX:使用次数
            :param formats: 选择格式
            :return:
            """

            filelists = glob.glob('{}/*.{}'.format(dirtname, formats))
            with open("{}\default.txt".format(filelists[0].split('\\')[0]), 'w+') as files:
                for index in range(len(filelists)):
                    string = ""
                    image = get_file_content(filelists[index])
                    fname = filelists[index].split('\\')[1]
                    code = None
                    try:
                        # 调用通用文字识别, 图片参数为本地图片
                        if INDEX < 500:
                            code = client.basicGeneral(image)  # 通用文字识别500次/天
                        elif INDEX < 1000:
                            code = client.general(image)  # 通用文字识别（含位置信息版）500次/天
                        elif INDEX < 1500:
                            code = client.webImage(image)  # 网络图片文字识别500次/天
                        elif INDEX < 1700:
                            code = client.receipt(image)  # 通用票据识别200次/天
                        elif INDEX < 1750:
                            code = client.basicAccurate(image)  # 通用文字识别（高精度版）50次/天
                        else:
                            print('今天免费次数已用完，请更换账号')
                        # 获取值
                        # print(code)
                        words = code['words_result'][0]['words']
                    except (IndexError, KeyError):
                        words = ''
                    string += fname + ' ' + words + '\n'
                    files.write(string)
                    INDEX += 1
            tkinter.messagebox.showinfo('提示', '今天使用次数:{}！'.format(INDEX))

        INDEX = tkinter.simpledialog.askinteger("今天使用次数", "输入次数：")
        INDEX = int(abs(INDEX))
        gs = tkinter.simpledialog.askstring("文件格式", "请输入要归一化的图像格式（jpg，png）")
        if gs == 'jpg' or gs == 'png':
            filedirname = tkinter.filedialog.askdirectory()
            if filedirname is None or filedirname is "":
                tkinter.messagebox.showinfo('提示', '请选择文件夹！')
            else:
                rename_file(filedirname, INDEX, gs)
        else:
            tkinter.messagebox.showinfo('提示', '输入不符合！')

    def changeformat(self, filename, path, newName):
        im = Image.open(os.path.join(path, filename))
        # print(os.path.join(path, newName))
        im.save(os.path.join(path, newName))

    def getNum(self):
        # 获取当前计数
        with open("./utils/num.txt", 'r+') as files:
            string = files.readline()
            if string == "":
                file = open("num.txt", 'w')
                file.write('0')
                return 0
            else:
                # print(string)
                num = int(string)
                # print(num)
                file = open("./utils/num.txt", 'w')
                num += 1
                file.write(str(num))
                return num

    def _about(self):
        tkinter.messagebox.showinfo('关于', '作者：{}\n邮箱：{}'.format(__author__, __email__))

    @staticmethod
    def _quit():
        # 结束主事件循环
        root.quit()  # 关闭窗口
        root.destroy()  # 将所有的窗口小部件进行销毁，应该有内存回收的意思
        exit()


class EditImage(object):
    """
    图像类
    """

    def __init__(self, fillname):
        # 图像类初始化
        global res
        res = 1  # 比例
        self.L = []  # 一个数据点
        self.oldPoint = []  # 不变的数据点集
        self.resPoint = []  # 上一步的点集
        self.showpixel = None  # 提示txt对象
        self.lablename = []  # 删除的标签名称
        self.image = Image.open(fillname)  # 打开图片
        self.image2 = Image.open(fillname)
        self.image = self.image.convert('RGB')
        self.image2 = self.image2.convert('RGB')
        self.startImgWidth = self.image2.size[0]
        self.canvas_width = self.image.size[0]  # 图片宽度
        self.canvas_higth = self.image.size[1]  # 图片高度
        self.canvas = None  # 画布变量
        self.boxs = []  # 虚线框对象列表
        self.mainboxs = []  # 实线画框对象列表
        self.setImage(self.image, self.canvas_width, self.canvas_higth)

    def setImage(self, img, imgWidth, imgHeight):
        global sonframe  # 子容器sonframe
        sonframe = Frame(mainframe, bg='red')  # 生成子容器
        sonframe.pack(expand=True, fill=BOTH)

        self.canvas = Canvas(sonframe, width=imgWidth, height=imgHeight, bg='grey')  # 画布生

        self.canvas.config(scrollregion=(0, 0, imgWidth, imgHeight))
        self.canvas.config(highlightthickness=0)
        sbar = Scrollbar(self.canvas)  # 添加y轴滚动条
        sbar.config(orient=VERTICAL, command=self.canvas.yview)
        self.canvas.config(yscrollcommand=sbar.set)
        sbar.pack(side=RIGHT, fill=Y)
        self.canvas.pack(side=LEFT, expand=YES, fill=BOTH)

        sbar2 = Scrollbar(self.canvas)  # 添加x轴滚动条
        sbar2.config(orient=HORIZONTAL, command=self.canvas.xview)
        self.canvas.config(xscrollcommand=sbar2.set)
        sbar2.pack(side=BOTTOM, fill=X)
        self.canvas.pack(side=BOTTOM, expand=YES, fill=BOTH)

        im = ImageTk.PhotoImage(img)  # 获取图像
        self.canvas.create_image(imgWidth / 2, imgHeight / 2, image=im)  # 在画布绘制图像
        self.draw_old_boxs(self.canvas, (imgWidth / self.startImgWidth))
        root.geometry("%dx%d" % (imgWidth, imgHeight))

        root.bind("<B1-Motion>", self.mouseMove)  # 画布绑定鼠标左击移动事件
        self.canvas.bind("<Button-1>", self.mousePre)  # 画布绑定鼠标左击事件
        self.canvas.bind("<ButtonRelease-1>", self.mouseRel)  # 画布绑定鼠标左击释放事件
        root.bind("<Key>", self.keyPress)  # 画布绑定其他按键事件
        root.bind("<Down>", self.KBPreDown)  # 窗口绑定键盘下键
        root.bind("<Up>", self.KBPreUp)  # 窗口绑定键盘上键
        root.bind("<Left>", self.KBPreLeft)  # 窗口绑定键盘左键
        root.bind("<Right>", self.KBPreRight)  # 窗口绑定键盘右键
        root.bind("<Control-KeyPress-z>", self.callBack)  # 窗口绑定键盘ctrl+z
        root.bind("<Control-KeyPress-s>", self.savePhoto)  # 窗口绑定键盘ctrl+s
        root.bind("<Control-KeyPress-y>", self.restorePreStep)  # 窗口绑定键盘ctrl+y

        global draw, draw2
        draw = ImageDraw.Draw(self.image)  # 生成绘制对象（对保存绘制后的图片）
        draw2 = ImageDraw.Draw(self.image2)

        mainloop()  # 窗口主循环

    def callBack(self, event):
        # 撤销按钮 "ctrl+z"
        img = SN.imglist.pop()  # 图片列表移除前一张图片
        self.lablename.append(img)
        op = self.oldPoint.pop()  # 删除起一个苏据点
        self.resPoint.append(op)  # 添加到恢复列表
        imgpath = SN.path + '/' + SN.filename + '/' + img
        os.remove(imgpath)  # 删除前一张截图
        SN.word = SN.word - 1  # 计数器减一
        txt = SN.path + '/' + SN.filelist

        # 在文本删除前一张图的点数据
        str = []
        with open(txt, "r") as files:
            for i in files:
                str.append(i)
            str.pop()

        with open(txt, "w") as files2:
            for i in str:
                files2.write(i)

        # 在文本删除前一张图片名称
        imgnametxt = SN.path + '/' + SN.filename + '/data' + SN.getPointDataName()
        with open(imgnametxt, 'w') as files3:
            string = ""
            for imgname in SN.imglist:
                string += '{} \n'.format(imgname)
            files3.write(string)

        # 删除前一个框框
        self.canvas.delete(self.mainboxs.pop())
        try:
            self.canvas.delete(self.boxs.pop())
        except IndexError:
            print("无虚线框")
            self.boxs = []

    def restorePreStep(self, event):
        """
        返回上一步操作
        :param event: 事件监听的必要参数
        :return:无
        """
        ratio = float(self.startImgWidth) / float(self.canvas_width)

        if len(self.resPoint) < 1:
            pass
        else:
            data = self.resPoint.pop()  # 上一步点减一
            self.oldPoint.append(data)  # 原点加一
            canvas = self.canvas.create_rectangle(int(data[0] / ratio), int(data[1] / ratio), int(data[4] / ratio),
                                                  int(data[5] / ratio), outline='red')  # 恢复选框

            self.mainboxs.append(canvas)  # 实线画框对象列表加对象
            SN.word = SN.word + 1  # 计数器加一
            imgname = self.lablename.pop()  # 图名
            SN.imglist.append(imgname)  # 加图名
            imgpath = SN.path + '/' + SN.filename + '/' + imgname  # 图片路径
            img = self.image2.crop((data[0], data[1], data[4], data[5]))  # 裁剪图像
            img.save(imgpath, SN.imgsuffix.upper())  # 保存图像

            # 写入点数据
            datapath = SN.path + '/' + SN.filelist
            with open(datapath, 'a') as files:  # 追加写入
                string = "{},{},{},{},{},{},{},{},\n".format(data[0], data[1], data[2], data[3], data[4], data[5],
                                                             data[6], data[7])
                files.write(string)  # 向文件写入数据

            # 写入文件名数据
            strpath = SN.path + '/' + SN.filename + '/data' + SN.getPointDataName()
            with open(strpath, 'a') as files:  # 创建或打开文件
                files.write(imgname + " \n")

    def KBPreDown(self, event):
        # 键盘下键
        if self.canvas.yview()[0] == 0:
            self.canvas.yview_moveto(self.canvas.yview()[0] + 0.1)
        else:
            self.canvas.yview_moveto(self.canvas.yview()[0] + 0.1)

    def KBPreUp(self, event):
        # 键盘上键
        self.canvas.yview_moveto(self.canvas.yview()[0] - 0.1)

    def KBPreLeft(self, event):
        # 键盘左键
        self.canvas.xview_moveto(self.canvas.xview()[0] - 0.1)

    def KBPreRight(self, event):
        # 键盘右键
        if self.canvas.xview()[0] == 0:
            self.canvas.xview_moveto(self.canvas.xview()[0] + 0.1)
        else:
            self.canvas.xview_moveto(self.canvas.xview()[0] + 0.1)

    def mousePre(self, event):
        # 鼠标左击
        global endx, endy, showpixel
        xspan = self.canvas.xview()[0] * self.canvas_width
        yspan = self.canvas.yview()[0] * self.canvas_higth
        x, y = event.x, event.y  # 获取坐标
        endx = int(xspan + x)
        endy = int(yspan + y)
        # 设置提示内容
        self.showpixel = self.canvas.create_text(endx + 20, endy - 10, text='0 * 0', fill='brown', tags='txt')

    def mouseMove(self, event):
        # 鼠标左击按压事件
        global flag
        flag = TRUE
        xx, yy = event.x, event.y
        x1span = self.canvas.xview()[0] * self.canvas_width
        y1span = self.canvas.yview()[0] * self.canvas_higth
        endxx = int(xx + x1span)
        endyy = int(yy + y1span)

        size = "{} x {}".format(abs(endxx - endx), abs(endyy - endy))  # 计算框选的大小
        self.canvas.itemconfigure(self.showpixel, text='{}'.format(size))  # 提示款内容
        flags = xx > 10 and xx < root.winfo_width() - 10 and yy > 10 and yy < root.winfo_height() - 10
        if not flags:
            try:
                self.canvas.delete(self.boxs.pop())
            except IndexError:
                pass

        if len(self.boxs) == 0 and flags:
            try:
                box = self.canvas.create_rectangle(endx, endy, endxx, endyy, outline='blue', dash=3)
            except NameError:
                print("失效区域")
                self.canvas.delete(self.boxs.pop())
            else:
                self.boxs.append(box)
        else:
            try:
                if 32 * 255 > abs((endxx - endx)) * abs((endyy - endy)):
                    flag = TRUE
                    self.canvas.coords(self.boxs[0], (endx, endy, endxx, endyy))
                else:
                    flag = FALSE
                    size = "{} x {}".format(abs(endxx - endx), abs(endyy - endy))  # 计算框选的大小
                    self.canvas.itemconfigure(self.showpixel, text='{} More than the proportion'.format(size))  # 提示款内容
            except IndexError:
                print("拖到了滚动条")

    def keyPress(self, event):
        if event.char == "=":
            self.canvas.pack_forget()
            self.canvas.destroy()
            sonframe.pack_forget()
            sonframe.destroy()
            self.canvas_width *= 1.1
            self.canvas_higth *= 1.1
            width = int(self.canvas_width)
            height = int(self.canvas_higth)
            image = self.image.resize((width, height), Image.ANTIALIAS)
            self.setImage(image, width, height)
        elif event.char == "-":
            self.canvas.pack_forget()
            self.canvas.destroy()
            sonframe.pack_forget()
            sonframe.destroy()
            self.canvas_width /= 1.1
            self.canvas_higth /= 1.1
            width = int(self.canvas_width)
            height = int(self.canvas_higth)
            image = self.image.resize((width, height), Image.ANTIALIAS)
            self.setImage(image, width, height)

    def draw_old_boxs(self, canvas, ratio):
        """
        绘制框
        :param canvas: 画布对象
        :param ratio:比例
        :return:
        """
        self.changeRatio = ratio
        if len(self.oldPoint) < 1:
            pass
        else:
            for box in self.oldPoint:
                canvas.create_rectangle(int(box[0] * ratio), int(box[1] * ratio), int(box[4] * ratio),
                                        int(box[5] * ratio), outline='red')

    def savePhoto(self, event):
        # ctrl+S 图像保存
        strpath = ''
        try:
            strpath = SN.path + "/new" + SN.filename[:-3] + "_" + str(SN.word) + "." + SN.imgsuffix  # 文件全路径
        except IOError:
            pass

        temp = []
        for i in self.oldPoint:
            tempson = []
            for j in i:
                tempson.append(j)
            temp.append(tempson)

        # print(temp)
        for i in range(len(temp)):
            draw2.rectangle((int(temp[i][0]), int(temp[i][1]), int(temp[i][4]),
                             int(temp[i][5])), outline='red')
        self.image2.save(strpath)  # 保存图像

    def mouseRel(self, event):
        # 鼠标左击释放事件
        global strpath
        global res
        global flag
        region = None
        self.canvas.delete(self.showpixel)  # 删除提示txt对象
        self.showpixel = None  # 设置txt对象为空
        try:
            self.canvas.delete(self.boxs.pop())
        except IndexError:
            print("拖动滚动条")

        # print(flag)
        if flag == TRUE:
            x1, y1 = event.x, event.y  # 获取第二个坐标
            x1span = self.canvas.xview()[0] * self.canvas_width
            y1span = self.canvas.yview()[0] * self.canvas_higth
            endx1 = int(x1 + x1span)
            endy1 = int(y1 + y1span)
            res = float(self.startImgWidth) / float(self.canvas_width)

            if endx1 - endx > 0 and endy1 - endy > 0:  # 图像截取分情况
                region = self.image2.crop((int(endx * res), int(endy * res), int(endx1 * res), int(endy1 * res)))
            elif endx1 - endx > 0 and endy1 - endy < 0:
                region = self.image2.crop((int(endx * res), int(endy1 * res), int(endx1 * res), int(endy * res)))
            elif endx1 - endx < 0 and endy1 - endy < 0:
                region = self.image2.crop((int(endx1 * res), int(endy1 * res), int(endx * res), int(endy * res)))
            elif endx1 - endx < 0 and endy1 - endy > 0:
                region = self.image2.crop((int(endx1 * res), int(endy * res), int(endx * res), int(endy1 * res)))

            try:
                strpath = SN.path + '/' + SN.filename + '/' + SN.getPhotoName()  # 截图名称
                os.mkdir(SN.path + '/' + SN.filename)  # 创建文件夹
            except IOError:
                pass
            except OSError:
                pass

            # 修复无法取原点却产生截图的bug
            try:
                if SN.imgsuffix == 'jpg':
                    region.save(strpath, 'JPEG')  # 保存原截图
                else:
                    region.save(strpath, SN.imgsuffix.upper())
            except SystemError:
                print("距离太短无法选取")
                os.remove(strpath)
                SN.word = SN.word - 1
                SN.imglist.pop()
            except UnboundLocalError:
                print("距离太短无法选取")
                # os.remove(strpath)
                SN.word = SN.word - 1
                SN.imglist.pop()
            else:
                mainbox = self.canvas.create_rectangle(endx, endy, endx1, endy1, outline='red')  # 创建选取框
                self.mainboxs.append(mainbox)  # 增加实线框对象
                self.savedata(int(endx * res), int(endy * res), int(endx1 * res), int(endy1 * res))  # 保存顺时针点坐标

    def savedata(self, endx, endy, endx1, endy1):
        if endx1 - endx > 0 and endy1 - endy > 0:  # 取点保存分情况
            self.L.append(endx), self.L.append(endy)  # 分别获取选取框4个坐标
            self.L.append(endx1), self.L.append(endy)
            self.L.append(endx1), self.L.append(endy1)
            self.L.append(endx), self.L.append(endy1)  # 向列表中加入4个坐标为一个元祖
        elif endx1 - endx > 0 and endy1 - endy < 0:
            self.L.append(endx), self.L.append(endy1)  # 分别获取选取框4个坐标
            self.L.append(endx1), self.L.append(endy1)
            self.L.append(endx1), self.L.append(endy)
            self.L.append(endx), self.L.append(endy1)  # 向列表中加入4个坐标为一个元祖
        elif endx1 - endx < 0 and endy1 - endy < 0:
            self.L.append(endx1), self.L.append(endy1)  # 分别获取选取框4个坐标
            self.L.append(endx), self.L.append(endy1)
            self.L.append(endx), self.L.append(endy)
            self.L.append(endx1), self.L.append(endy)  # 向列表中加入4个坐标为一个元祖
        elif endx1 - endx < 0 and endy1 - endy > 0:
            self.L.append(endx1), self.L.append(endy)  # 分别获取选取框4个坐标
            self.L.append(endx), self.L.append(endy)
            self.L.append(endx), self.L.append(endy1)
            self.L.append(endx1), self.L.append(endy1)  # 向列表中加入4个坐标为一个元祖

        # print(self.L)
        self.oldPoint.append(self.L)

        if len(self.L) == 0: return  # 没有数据，返回

        strpath = SN.path + '/' + SN.getPointDataName()  # 生成最终文件绝对路径
        with open(strpath, 'a') as files:  # 创建或打开文件
            string = ''  # 最终点数据保存字符串
            for i in range(len(self.L)):  # 数据点格式整理
                if i != 0 and i % 7 == 0:
                    string = string + str(int(float(self.L[i]) * res)) + ",\n"
                else:
                    string = string + str(int(float(self.L[i]) * res)) + ","
            files.write(string)  # 向文件写入数据
            self.L = []

        strpath = SN.path + '/' + SN.filename + '/data' + SN.getPointDataName()
        with open(strpath, 'a') as files:  # 创建或打开文件
            files.write(SN.imglist[-1] + " \n")


if __name__ == '__main__':
    window = Windows()  # 启动程序
