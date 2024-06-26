import tkinter as tk
from tkinter import messagebox
import webbrowser
from tkinter import ttk
import json
import subprocess
import os
from tkinter import filedialog
import shutil
from PIL import Image, ImageTk
from pypinyin import lazy_pinyin
import random
import string
import sys

BASE_DIR = os.path.dirname(os.path.realpath(sys.argv[0]))
ASSET_DIR = os.path.join(BASE_DIR, 'assets')
OBJECT_DIR = os.path.join(BASE_DIR, 'object')
TEMP_DIR = os.path.join(BASE_DIR, 'temp')

def generate_random_string(length=10):
    letters = string.ascii_letters
    return ''.join(random.choice(letters) for _ in range(length))

class AboutFrame(tk.Frame):
    def __init__(self, root):
        super().__init__(root)
        self.sign_photo = tk.PhotoImage(file=os.path.join(ASSET_DIR,'sign.gif'))
        self.sign_label = tk.Label(self, image=self.sign_photo)
        self.sign_label.image = self.sign_photo  # 保持对图片的引用，防止被垃圾回收
        self.sign_label.pack()
        tk.Label(self, text='version 1.0.1', font=('Arial', 12, "bold"), width=15, height=3,
                 anchor="n").pack()
        tk.Label(self,
                 text='本项目仅供技术研究，请勿用于任何商业用途，请勿用于非法用途，\n如有任何人凭此做何非法事情，均于作者无关，特此声明。',
                 font=('微软雅黑', 10), width=80, height=18, anchor="n").pack()

        def open_url(event):
            webbrowser.open("https://github.com/Lee612-1/ChatLYT_wechatbot")

        def on_enter(event):
            connect_author.config(fg="royal blue")

        def on_leave(event):
            connect_author.config(fg="black")

        connect_author = tk.Label(self, text="联系作者", cursor="hand2", font=('微软雅黑', 10), width=15,
                                  anchor="s")
        connect_author.pack()
        connect_author.bind("<Button-1>", open_url)
        connect_author.bind("<Enter>", on_enter)
        connect_author.bind("<Leave>", on_leave)


class RunFrame(tk.Frame):
    def __init__(self, root):
        super().__init__(root)
        self.style = ttk.Style()
        self.style.configure('Custom.TRadiobutton', font=('微软雅黑', 10))
        self.style.configure('Custom.TButton', font=('微软雅黑', 10))
        self.style.configure('Custom.TCombobox', font=('微软雅黑', 10))
        self.style.configure('Config.TFrame')
        friend_path = os.path.join(BASE_DIR,'object/people.json')
        if os.path.exists(friend_path):
            with open(friend_path, 'r', encoding='utf-8') as f:
                friends = json.load(f)
            friend_name = [friend['name'] for friend in friends]
            friend_dir = [friend['dir'] for friend in friends]
        else:
            friend_name = []
            friend_dir = []
        api_options = ["huggingface", "openai"]
        config_path = os.path.join(BASE_DIR,'temp/config.json')
        if os.path.exists(config_path):
            with open(config_path, 'r', encoding='utf-8') as f:
                config = json.load(f)
            selected_api = tk.StringVar(value=config['api'])
            selected_mode = tk.IntVar(value=config['mode'])
            selected_authentic = tk.IntVar(value=config['authentic'])
            selected_friend = tk.StringVar(value=config['friend'])

        else:
            selected_api = tk.StringVar()
            selected_mode = tk.IntVar(value=0)
            selected_authentic = tk.IntVar(value=0)
            selected_friend = tk.StringVar()

        self.sign_photo = tk.PhotoImage(file=os.path.join(BASE_DIR,'assets/sign2.gif'))
        self.sign_label = tk.Label(self, image=self.sign_photo, width=350, anchor='e')
        self.sign_label.image = self.sign_photo  # 保持对图片的引用，防止被垃圾回收
        self.sign_label.pack()
        tk.Label(self, text='', height=2).pack()

        big_frame = ttk.Frame(self, style='Config.TFrame')
        big_frame.pack()
        buttons_frame2 = tk.Frame(big_frame)
        buttons_frame2.pack()
        tk.Label(buttons_frame2, text="选择api: ", font=('微软雅黑', 12, "bold"), width=10, anchor="w").pack(
            side=tk.LEFT)
        ttk.Combobox(buttons_frame2, style='Custom.TCombobox', textvariable=selected_api, values=api_options).pack(
            side=tk.RIGHT)
        tk.Label(big_frame, text='', height=1).pack()

        def show_combobox():
            if selected_mode.get() == 0:
                comb.config(values=friend_name)
                selected_friend.set('')
            else:
                comb.config(values=['全部好友'])
                selected_friend.set('全部好友')

        buttons_frame = tk.Frame(big_frame)
        buttons_frame.pack()
        radio_button1 = ttk.Radiobutton(buttons_frame, text="单人模式", style='Custom.TRadiobutton', cursor="hand2",
                                        variable=selected_mode, value=0, command=show_combobox)
        radio_button2 = ttk.Radiobutton(buttons_frame, text="海王模式", style='Custom.TRadiobutton', cursor="hand2",
                                        variable=selected_mode, value=1, command=show_combobox)
        radio_button1.pack(side=tk.LEFT, padx=10)
        radio_button2.pack(side=tk.RIGHT, padx=10)
        tk.Label(big_frame, text='', height=1).pack()

        buttons_frame3 = tk.Frame(big_frame)
        buttons_frame3.pack()
        tk.Label(buttons_frame3, text="选择好友: ", font=('微软雅黑', 12, "bold"), width=10, anchor="w").pack(
            side=tk.LEFT)
        comb = ttk.Combobox(buttons_frame3, style='Custom.TCombobox', textvariable=selected_friend, values=friend_name)
        comb.pack(side=tk.RIGHT)
        tk.Label(big_frame, text='', height=1).pack()

        buttons_frame4 = tk.Frame(big_frame)
        buttons_frame4.pack()

        def show_selected_value(value):
            selected_authentic.set(int(value))

        tk.Label(buttons_frame4, text="拟真度: ", font=('微软雅黑', 12, "bold"), width=13, anchor="w").pack(
            side=tk.LEFT)
        tk.Scale(buttons_frame4, from_=0, to=2, cursor="hand2", orient=tk.HORIZONTAL, length=120,
                 variable=selected_authentic, showvalue=0,
                 command=show_selected_value, activebackground='#808080', sliderlength=40, sliderrelief="flat",
                 relief="flat", troughcolor='white', bd=0, bg='royal blue').pack(side=tk.LEFT)
        tk.Label(big_frame, text='', height=1).pack()

        self.process = None

        def save_button():
            config = {'api': selected_api.get() if selected_api.get() else None,
                      'mode': selected_mode.get(),
                      'friend': selected_friend.get() if selected_friend.get() else None,
                      'authentic': selected_authentic.get(),
                      }
            with open(config_path, 'w', encoding='utf-8') as f:
                json.dump(config, f)

        def run_button():
            order = ["python", "-u"]
            if selected_api.get() == api_options[0]:
                order.append(os.path.join(BASE_DIR,'main.py'))
            elif selected_api.get() == api_options[1]:
                if os.path.exists(os.path.join(BASE_DIR,'temp/key.txt')):
                    order.append(os.path.join(BASE_DIR,"main_openai.py"))
                else:
                    top = tk.Toplevel()
                    top.title("输入api key")
                    top.geometry("300x150+1650+800")
                    top_frame1 = tk.Frame(top)
                    top_frame1.pack(pady=30)
                    tk.Label(top_frame1, text="输入api key:", font=('微软雅黑', 10)).pack(side=tk.LEFT, padx=5)
                    e = ttk.Entry(top_frame1, show="*")
                    e.pack(side=tk.RIGHT, padx=5)

                    def check_password():
                        api_key = e.get()
                        with open(os.path.join(BASE_DIR,'temp/key.txt'), "w", encoding='utf-8') as file:
                            file.write(api_key)
                        top.destroy()
                        run_button()

                    def cancel_password():
                        top.destroy()

                    top_frame2 = tk.Frame(top)
                    top_frame2.pack(pady=10)
                    ttk.Button(top_frame2, text="确定", cursor="hand2", command=check_password).pack(side=tk.LEFT,
                                                                                                     padx=10)
                    ttk.Button(top_frame2, text="取消", cursor="hand2", command=cancel_password).pack(side=tk.RIGHT,
                                                                                                      padx=10)
                    return
            else:
                messagebox.showinfo("提示", "请选择api")
                return
            if selected_mode.get() == 1:
                order.extend(['--people', os.path.join(BASE_DIR,'object/people.json')])
            else:
                if selected_friend.get():
                    try:
                        index = friend_name.index(selected_friend.get())
                        order.extend(['--person', os.path.join(BASE_DIR,friend_dir[index])])
                    except:
                        messagebox.showinfo("提示", "不存在该好友")
                        return
                else:
                    messagebox.showinfo("提示", "请选择好友")
                    return
            order.extend(['--authentic', str(selected_authentic.get())])
            save_button()
            self.process = subprocess.Popen(order)
            quit_label.config(text='按F10退出')

        tk.Label(self, text='', height=2).pack()
        big_frame2 = ttk.Frame(self)
        big_frame2.pack()
        tk.Label(big_frame2, text='请将聊天界面完全置于顶层，开始聊天后不要触碰鼠标',
                 font=('微软雅黑', 8, 'italic')).pack(
            pady=10)

        buttons_frame5 = tk.Frame(big_frame2)
        buttons_frame5.pack()
        ttk.Button(buttons_frame5, text="开始聊天", style='Custom.TButton', cursor="hand2", command=run_button).pack(
            side=tk.RIGHT, padx=20)
        ttk.Button(buttons_frame5, text="保存配置", style='Custom.TButton', cursor="hand2", command=save_button).pack(
            side=tk.LEFT, padx=20)
        quit_label = tk.Label(big_frame2, text='按F10退出', font=('微软雅黑', 8), fg="royal blue")
        quit_label.pack()

        def stop_process(event):
            if self.process is not None:
                self.process.terminate()
                self.process = None
                quit_label.config(text="已退出")

        root.bind("<F10>", stop_process)


class ChangeFrame(tk.Frame):
    def __init__(self, root):
        super().__init__(root)
        self.style = ttk.Style()
        self.style.configure('Change.TButton', font=('微软雅黑', 8))
        if os.path.exists(os.path.join(BASE_DIR,'temp/key.txt')):
            with open(os.path.join(BASE_DIR,'temp/key.txt'), "r", encoding='utf-8') as file:
                self.api_key = file.read()
        else:
            self.api_key = 'null'

        self.sign_photo = tk.PhotoImage(file=os.path.join(BASE_DIR,'assets/sign3.gif'))
        self.sign_label = tk.Label(self, image=self.sign_photo)
        self.sign_label.image = self.sign_photo  # 保持对图片的引用，防止被垃圾回收
        self.sign_label.pack()
        tk.Label(self, text='', height=2).pack()

        key_frame = tk.Frame(self)
        key_frame.pack()
        tk.Label(key_frame, text='当前api key', font=('微软雅黑', 15, 'bold')).pack(side=tk.LEFT)
        key = tk.Label(self, text='******', font=('微软雅黑', 10, 'bold'))

        def show(event):
            if show_key.cget("text") == '显示':
                key.config(text=self.api_key, font=('微软雅黑', 10, 'italic'))
                show_key.config(text="隐藏")
            else:
                key.config(text='******', font=('微软雅黑', 10, 'bold'))
                show_key.config(text="显示")

        def on_enter(event):
            show_key.config(fg="blue")

        def on_leave(event):
            show_key.config(fg="black")

        show_key = tk.Label(key_frame, text="显示", cursor="hand2", font=('微软雅黑', 10))
        show_key.pack(side=tk.RIGHT, padx=20)
        show_key.bind("<Button-1>", show)
        show_key.bind("<Enter>", on_enter)
        show_key.bind("<Leave>", on_leave)
        tk.Label(self, text='', height=1).pack()
        key.pack()

        tk.Label(self, text='', height=2).pack()
        frame2 = tk.Frame(self)
        frame2.pack(pady=30)
        frame3 = tk.Frame(frame2)
        frame3.pack(side=tk.LEFT)
        tk.Label(frame3, text="输入api key:", font=('微软雅黑', 10, 'bold')).pack(side=tk.LEFT, padx=10)
        e = ttk.Entry(frame3, show="*")
        e.pack(side=tk.RIGHT)

        def change():
            if e.get() == '':
                messagebox.showinfo("提示", "不可为空！")
                return
            return_value = messagebox.askquestion('提示', '确认修改？')
            if return_value == 'yes':
                self.api_key = e.get()
                if show_key.cget("text") == '隐藏':
                    key.config(text=self.api_key, font=('微软雅黑', 10, 'bold'))
                e.delete(0, 'end')
                with open(os.path.join(BASE_DIR,'temp/key.txt'), "w", encoding='utf-8') as file:
                    file.write(self.api_key)
                messagebox.showinfo("提示", "修改成功！")
            else:
                return

        ttk.Button(frame2, text="确定", style='Change.TButton', cursor="hand2", command=change, width=5).pack(
            side=tk.RIGHT, padx=5)

        def load_dir():
            file_path = filedialog.askopenfilename(filetypes=[("Text files", "*.txt")])
            if file_path:
                messagebox.showinfo("提示", "导入成功！")
                with open(file_path, "r", encoding='utf-8') as f:
                    self.api_key = f.read()
                with open('temp/key.txt', "w", encoding='utf-8') as f:
                    f.write(self.api_key)

        frame4 = tk.Frame(self)
        frame4.pack(pady=30)
        tk.Label(frame4, text="导入api key:", width=12, font=('微软雅黑', 10, 'bold'), anchor='w').pack(side=tk.LEFT)
        ttk.Button(frame4, text="从文件中导入", style='Custom.TButton', width=20, cursor="hand2",
                   command=load_dir).pack(side=tk.RIGHT)


class FriendFrame(tk.Frame):
    def __init__(self, root):
        super().__init__(root)
        self.file_path1 = None
        self.file_path2 = None

        if not os.path.exists(os.path.join(BASE_DIR,'object/people.json')):
            self.friend_dir = []
            self.friend_name = []
        else:
            with open(os.path.join(BASE_DIR,'object/people.json'), 'r', encoding='utf-8') as file:
                self.friend_dir = json.load(file)
                self.friend_name = [friend['name'] for friend in self.friend_dir]

        tk.Label(self, text='', height=2).pack()
        frame3 = tk.Frame(self)
        frame3.pack()
        tk.Label(frame3, text="好友名称:", font=('微软雅黑', 12, 'bold'), width=8, anchor='w').pack(side=tk.LEFT, padx=20)
        entry_text = tk.StringVar()
        e = ttk.Entry(frame3, width=25, textvariable=entry_text)

        def on_entry_change(*args):
            text = entry_text.get()
            if text in self.friend_name:
                name_label.config(text='     已存在改名称', fg='red')
            else:
                name_label.config(text='')
        e.pack(side=tk.LEFT, padx=35)
        entry_text.trace("w", on_entry_change)
        name_label = tk.Label(self, text='', height=1)
        name_label.pack()

        tk.Label(self, text='', height=1).pack()
        frame2 = tk.Frame(self)
        frame2.pack()
        canvas1 = tk.Canvas(self, width=300, height=70)
        canvas1.pack()
        sign_image = Image.open(os.path.join(BASE_DIR,'assets/sign4.png'))
        sign_photo = ImageTk.PhotoImage(sign_image)
        canvas1.create_image(150, 30, image=sign_photo, anchor='w')
        canvas1.image = sign_photo

        def load_large_avatar():
            self.file_path1 = filedialog.askopenfilename(filetypes=[('Image files', '*.png')])
            if self.file_path1:
                canvas1.delete("all")
                image = Image.open(self.file_path1)
                photo = ImageTk.PhotoImage(image)
                canvas1.create_image(150, 30, image=photo, anchor='w')
                canvas1.image = photo
                button1.config(text='重新选择')

        tk.Label(frame2, text="消息列表头像：", font=('微软雅黑', 12, 'bold')).pack(side=tk.LEFT, padx=10)
        button1 = ttk.Button(frame2, text="选择图片", width=30, cursor="hand2",
                             command=load_large_avatar)
        button1.pack(side=tk.RIGHT)

        frame = tk.Frame(self)
        frame.pack()
        canvas2 = tk.Canvas(self, width=300, height=70)
        canvas2.pack()
        canvas2.create_image(150, 30, image=sign_photo, anchor='w')
        canvas2.image = sign_photo

        def load_avatar():
            self.file_path2 = filedialog.askopenfilename(filetypes=[('Image files', '*.png')])
            if self.file_path2:
                canvas2.delete("all")
                image = Image.open(self.file_path2)
                photo = ImageTk.PhotoImage(image)
                canvas2.create_image(150, 30, image=photo, anchor='w')
                canvas2.image = photo
                button2.config(text='重新选择')

        tk.Label(frame, text="聊天界面头像：", font=('微软雅黑', 12, 'bold')).pack(side=tk.LEFT, padx=10)
        button2 = ttk.Button(frame, text="选择图片", width=30, cursor="hand2",
                             command=load_avatar)
        button2.pack(side=tk.RIGHT)

        frame6 = tk.Frame(self)
        frame6.pack(anchor='w')
        tk.Label(frame6, text="好友简介：", font=('微软雅黑', 12, 'bold'), width=14, anchor='e').pack(side=tk.LEFT,
                                                                                                     anchor='n',
                                                                                                     padx=10)
        self.intro_start = False

        def clear_text(event):
            if text.get(1.0, tk.END).strip() == "简单介绍一下它吧！（选填）" and not self.intro_start:
                text.delete(1.0, tk.END)
                text.config(fg="black")
                self.intro_start = True

        text = tk.Text(frame6, height=10, width=30, font=('微软雅黑', 10))
        text.insert(tk.END, "简单介绍一下它吧！（选填）")
        text.config(fg="gray")  # Set the default text color to gray
        text.bind("<Button-1>", clear_text)
        text.pack(side=tk.RIGHT, padx=30)

        def confirm():
            if e.get() == '':
                messagebox.showinfo("提示", "好友名称不可为空！")
                return
            elif not self.file_path1:
                messagebox.showinfo("提示", "请上传消息列表头像！")
                return
            elif not self.file_path2:
                messagebox.showinfo("提示", "请上传聊天界面头像！")
                return
            else:
                if e.get() in self.friend_name:
                    messagebox.showinfo("提示", "好友名称已存在！")
                    return
                folder = ''.join(lazy_pinyin(e.get()))
                base_path = os.path.join(BASE_DIR,'object')
                folder_list = [f for f in os.listdir(base_path) if os.path.isdir(os.path.join(base_path, f))]
                add = 1
                folder_re = folder
                while True:
                    if folder_re in folder_list:
                        folder_re = folder + str(add)
                        add += 1
                    else:
                        break
                folder_path = os.path.join(base_path, folder_re)
                os.makedirs(folder_path)
                self.friend_dir.append({'name': e.get(), "dir": folder_path})
                shutil.copy(self.file_path1, folder_path)
                shutil.copy(self.file_path2, folder_path)

                file_name1 = os.path.basename(self.file_path1)
                file_name2 = os.path.basename(self.file_path2)
                target_file1 = os.path.join(folder_path, file_name1)
                target_file2 = os.path.join(folder_path, file_name2)
                new_file_name1 = 'large_avatar.' + file_name1.split(".")[-1]
                new_file_name2 = 'avatar.' + file_name2.split(".")[-1]
                os.rename(target_file1, os.path.join(folder_path, new_file_name1))
                os.rename(target_file2, os.path.join(folder_path, new_file_name2))
                role = f'你现在正在网络上和你的朋友聊天，下面是你朋友的信息：{text.get(1.0, tk.END).strip()}。' \
                    if not text.get(1.0, tk.END).strip() == "简单介绍一下它吧！（选填）" and not text.get(1.0,
                                                                                                       tk.END).strip() == "" \
                    else '你现在正在网络上和你的朋友聊天。'
                with open(os.path.join(folder_path, 'role.txt'), "w", encoding='utf-8') as file:
                    file.write(role)
                with open(os.path.join(BASE_DIR,'object/people.json'), 'w', encoding='utf-8') as file:
                    json.dump(self.friend_dir, file)
                messagebox.showinfo("提示", "新建成功！")
                e.delete(0, 'end')
                canvas1.delete("all")
                canvas2.delete("all")
                text.delete(1.0, tk.END)
                button1.config(text='选择图片')
                button2.config(text='选择图片')
                if not os.path.exists(os.path.join(BASE_DIR,'object/people.json')):
                    self.friend_dir = []
                    self.friend_name = []
                else:
                    with open(os.path.join(BASE_DIR,'object/people.json'), 'r', encoding='utf-8') as file:
                        self.friend_dir = json.load(file)
                        self.friend_name = [friend['name'] for friend in self.friend_dir]

        tk.Label(self, text='', height=3).pack()
        ttk.Button(self, text="确定", cursor="hand2", command=confirm, width=10).pack(padx=5)


class FriendReviseFrame(tk.Frame):
    def __init__(self, root):
        super().__init__(root)
        self.file_path1 = None
        self.file_path2 = None
        self.path = None
        self.role = None
        friend_path = os.path.join(BASE_DIR,'object/people.json')
        if os.path.exists(friend_path):
            with open(friend_path, 'r', encoding='utf-8') as f:
                self.friends = json.load(f)
            self.friend_name = [friend['name'] for friend in self.friends]
            self.friend_dir = [friend['dir'] for friend in self.friends]
        else:
            self.friend_name = []
            self.friend_dir = []
        selected_friend = tk.StringVar()

        top_canvas = tk.Canvas(self, width=300, height=100)
        top_canvas.pack()
        top_image1 = Image.open(os.path.join(BASE_DIR,'assets/sign6/step1.png'))
        top_photo1 = ImageTk.PhotoImage(top_image1)
        top_image2 = Image.open(os.path.join(BASE_DIR,'assets/sign6/step2.png'))
        top_photo2 = ImageTk.PhotoImage(top_image2)
        top_image3 = Image.open(os.path.join(BASE_DIR,'assets/sign6/step3.png'))
        top_photo3 = ImageTk.PhotoImage(top_image3)
        top_image4 = Image.open(os.path.join(BASE_DIR,'assets/sign6/step4.png'))
        top_photo4 = ImageTk.PhotoImage(top_image4)
        top_canvas.create_image(150, 50, image=top_photo1)
        top_canvas.image = top_photo1

        revise_frame = tk.Frame(self)
        revise_frame.pack()
        sign_canvas = tk.Canvas(revise_frame, width=500, height=202)
        sign_canvas.pack()
        sign_image = Image.open(os.path.join(BASE_DIR,'assets/sign7.png'))
        sign_photo = ImageTk.PhotoImage(sign_image)
        sign_canvas.create_image(250, 70, image=sign_photo)
        sign_canvas.image = sign_photo
        buttons_frame3 = tk.Frame(revise_frame)
        buttons_frame3.pack()
        tk.Label(buttons_frame3, text="选择好友: ", font=('微软雅黑', 12, "bold"), width=10, anchor="w").pack(
            side=tk.LEFT)
        comb = ttk.Combobox(buttons_frame3, style='Custom.TCombobox', textvariable=selected_friend, values=self.friend_name)
        comb.pack(side=tk.RIGHT)
        b_frame = tk.Frame(revise_frame)
        b_frame.pack()

        def next1():
            if not selected_friend.get():
                messagebox.showinfo("提示", "请选择好友！")
                return
            revise_frame.pack_forget()
            revise_frame2.pack()
            e.delete(0, tk.END)
            e.insert(0, selected_friend.get())
            top_canvas.delete("all")
            top_canvas.create_image(150, 50, image=top_photo2)
            top_canvas.image = top_photo2

        tk.Label(b_frame, text='', height=3).pack()
        ttk.Button(b_frame, text="下一步", cursor="hand2", command=next1, width=10).pack(side=tk.LEFT)

        revise_frame2 = tk.Frame(self)
        sign_canvas2 = tk.Canvas(revise_frame2, width=500, height=202)
        sign_canvas2.pack()
        sign_image2 = Image.open(os.path.join(BASE_DIR,'assets/sign8.png'))
        sign_photo2 = ImageTk.PhotoImage(sign_image2)
        sign_canvas2.create_image(250, 70, image=sign_photo2)
        sign_canvas2.image = sign_photo2
        frame3 = tk.Frame(revise_frame2)
        frame3.pack()
        tk.Label(frame3, text="修改名称:", font=('微软雅黑', 12, 'bold'), width=10, anchor="w").pack(side=tk.LEFT)
        e = ttk.Entry(frame3, width=23)
        e.pack(side=tk.RIGHT)
        b_frame2 = tk.Frame(revise_frame2)
        b_frame2.pack()

        def prev2():
            revise_frame2.pack_forget()
            revise_frame.pack()
            top_canvas.delete("all")
            top_canvas.create_image(150, 50, image=top_photo1)
            top_canvas.image = top_photo1

        def next2():
            revise_frame2.pack_forget()
            revise_frame3.pack()
            top_canvas.delete("all")
            top_canvas.create_image(150, 50, image=top_photo3)
            top_canvas.image = top_photo3
        tk.Label(b_frame2, text='', height=3).pack()
        ttk.Button(b_frame2, text="上一步", cursor="hand2", command=prev2, width=10).pack(side=tk.LEFT, padx=20)
        ttk.Button(b_frame2, text="下一步", cursor="hand2", command=next2, width=10).pack(side=tk.LEFT, padx=20)

        revise_frame3 = tk.Frame(self)
        frame2 = tk.Frame(revise_frame3)
        frame2.pack()
        canvas1 = tk.Canvas(revise_frame3, width=300, height=70)

        def load_large_avatar():
            self.file_path1 = filedialog.askopenfilename(filetypes=[('Image files', '*.png')])
            if self.file_path1:
                canvas1.delete("all")
                image = Image.open(self.file_path1)
                photo = ImageTk.PhotoImage(image)
                canvas1.create_image(150, 30, image=photo, anchor='w')
                canvas1.image = photo
                button1.config(text='重新选择')

        tk.Label(frame2, text="消息列表头像：", font=('微软雅黑', 12, 'bold')).pack(side=tk.LEFT, padx=10)
        button1 = ttk.Button(frame2, text="选择图片", width=30, cursor="hand2",
                             command=load_large_avatar)
        button1.pack(side=tk.RIGHT)
        canvas1.pack()

        frame = tk.Frame(revise_frame3)
        frame.pack()

        def load_avatar():
            self.file_path2 = filedialog.askopenfilename(filetypes=[('Image files', '*.png')])
            if self.file_path2:
                canvas2.delete("all")
                image = Image.open(self.file_path2)
                photo = ImageTk.PhotoImage(image)
                canvas2.create_image(150, 25, image=photo, anchor='w')
                canvas2.image = photo
                button2.config(text='重新选择')

        tk.Label(frame, text="聊天界面头像：", font=('微软雅黑', 12, 'bold')).pack(side=tk.LEFT, padx=10)
        button2 = ttk.Button(frame, text="选择图片", width=30, cursor="hand2",
                             command=load_avatar)
        button2.pack(side=tk.RIGHT)
        canvas2 = tk.Canvas(revise_frame3, width=300, height=60)
        canvas2.pack()

        b_frame3 = tk.Frame(revise_frame3)
        b_frame3.pack()
        tk.Label(b_frame3, text='', height=2).pack()

        def prev3():
            revise_frame3.pack_forget()
            revise_frame2.pack()
            top_canvas.delete("all")
            top_canvas.create_image(150, 50, image=top_photo2)
            top_canvas.image = top_photo2

        def next3():
            revise_frame3.pack_forget()
            revise_frame4.pack()
            top_canvas.delete("all")
            top_canvas.create_image(150, 50, image=top_photo4)
            top_canvas.image = top_photo4

        tk.Label(b_frame3, text='', height=3).pack()
        ttk.Button(b_frame3, text="上一步", cursor="hand2", command=prev3, width=10).pack(side=tk.LEFT, padx=20)
        ttk.Button(b_frame3, text="下一步", cursor="hand2", command=next3, width=10).pack(side=tk.LEFT, padx=20)

        revise_frame4 = tk.Frame(self)
        frame6 = tk.Frame(revise_frame4)
        frame6.pack()
        tk.Label(frame6, text="修改简介：", font=('微软雅黑', 12, 'bold')).pack(side=tk.LEFT, anchor='ne')

        text = tk.Text(frame6, height=10, width=30, font=('微软雅黑', 10))
        text.pack(side=tk.RIGHT, padx=30)
        b_frame4 = tk.Frame(revise_frame4)
        b_frame4.pack()
        tk.Label(b_frame4, text='', height=2).pack()

        def prev4():
            revise_frame4.pack_forget()
            revise_frame3.pack()
            top_canvas.delete("all")
            top_canvas.create_image(150, 50, image=top_photo3)
            top_canvas.image = top_photo3

        def confirm():
            if e.get() == '':
                messagebox.showinfo("提示", "好友名称不可为空！")
                revise_frame4.pack_forget()
                revise_frame2.pack()
                return
            if e.get() != selected_friend.get() and e.get() in self.friend_name:
                messagebox.showinfo("提示", "好友名称已存在！")
                revise_frame4.pack_forget()
                revise_frame2.pack()
                return
            if not self.path:
                messagebox.showinfo("提示", "路径错误！")
                return
            if (self.file_path1 and not self.file_path2) or (self.file_path1 and self.file_path2):
                messagebox.showinfo("提示", "请上传两张头像！")
                revise_frame4.pack_forget()
                revise_frame3.pack()
                return

            if messagebox.askokcancel("确认", "确认修改？"):
                if self.file_path1 and self.file_path2:
                    for filename in os.listdir(self.path):
                        file_path = os.path.join(self.path, filename)
                        if os.path.isfile(file_path) and filename != 'role.txt':
                            os.remove(file_path)
                    shutil.copy(self.file_path1, self.path)
                    shutil.copy(self.file_path2, self.path)
                    file_name1 = os.path.basename(self.file_path1)
                    file_name2 = os.path.basename(self.file_path2)
                    target_file1 = os.path.join(self.path, file_name1)
                    target_file2 = os.path.join(self.path, file_name2)
                    new_file_name1 = 'large_avatar.' + file_name1.split(".")[-1]
                    new_file_name2 = 'avatar.' + file_name2.split(".")[-1]
                    os.rename(target_file1, os.path.join(self.path, new_file_name1))
                    os.rename(target_file2, os.path.join(self.path, new_file_name2))

                if role := text.get(1.0, tk.END).strip() != self.role:
                    with open(os.path.join(self.path, 'role.txt'), "w", encoding='utf-8') as file:
                        file.write(role)
                if e.get() != selected_friend.get():
                    for fd in self.friends:
                        if fd['name'] == selected_friend.get():
                            fd['name'] = e.get()
                    with open('object/people.json', 'w', encoding='utf-8') as file:
                        json.dump(self.friends, file)

                messagebox.showinfo("提示", "修改成功！")
                self.friend_name = [friend['name'] for friend in self.friends]
                comb.config(values=self.friend_name)
                comb.set('')
                top_canvas.delete("all")
                top_canvas.create_image(150, 50, image=top_photo1)
                top_canvas.image = top_photo1
                e.delete(0, 'end')
                canvas1.delete("all")
                canvas2.delete("all")
                text.delete(1.0, tk.END)
                button1.config(text='选择图片')
                button2.config(text='选择图片')
                if os.path.exists(friend_path):
                    with open(friend_path, 'r', encoding='utf-8') as f:
                        self.friends = json.load(f)
                    self.friend_name = [friend['name'] for friend in self.friends]
                    self.friend_dir = [friend['dir'] for friend in self.friends]
                else:
                    self.friend_name = []
                    self.friend_dir = []
                revise_frame4.pack_forget()
                revise_frame.pack()

        tk.Label(b_frame4, text='', height=3).pack()
        ttk.Button(b_frame4, text="上一步", cursor="hand2", command=prev4, width=10).pack(side=tk.LEFT, padx=20)
        ttk.Button(b_frame4, text="完成", cursor="hand2", command=confirm, width=10).pack(side=tk.LEFT, padx=20)

        def on_select(event):
            index = self.friend_name.index(selected_friend.get())
            self.path = self.friend_dir[index]
            role_path = os.path.join(self.path, 'role.txt')
            with open(role_path, 'r', encoding='utf-8') as file:
                self.role = file.read()
            text.delete(1.0, tk.END)
            text.insert(tk.END, self.role)
            for file in os.listdir(self.path):
                if file.startswith('avatar'):
                    avatar_path = os.path.join(self.path, file)
                    canvas2.delete("all")
                    image = Image.open(avatar_path)
                    photo = ImageTk.PhotoImage(image)
                    canvas2.create_image(150, 30, image=photo, anchor='w')
                    canvas2.image = photo
                if file.startswith('large_avatar'):
                    large_avatar_path = os.path.join(self.path, file)
                    canvas1.delete("all")
                    image = Image.open(large_avatar_path)
                    photo = ImageTk.PhotoImage(image)
                    canvas1.create_image(150, 30, image=photo, anchor='w')
                    canvas1.image = photo

        comb.bind("<<ComboboxSelected>>", on_select)


class FlstFrame(tk.Frame):
    def __init__(self, root):
        super().__init__(root)
        friend_path = 'object/people.json'
        if os.path.exists(friend_path):
            with open(friend_path, 'r', encoding='utf-8') as f:
                friends = json.load(f)
            friend_name = [friend['name'] for friend in friends]
            friend_dir = [friend['dir'] for friend in friends]
        else:
            friend_name = []
            friend_dir = []
        self.friend_list_names = []
        list_file_names = []
        self.json_file = []
        if os.path.exists('object/friend_list'):
            list_file_names = os.listdir('object/friend_list')
            if os.path.exists('object/friend_list/list_name.json'):
                with open('object/friend_list/list_name.json', 'r', encoding='utf-8') as f:
                    self.json_file = json.load(f)
                self.friend_list_names = [list['name'] for list in self.json_file]
        else:
            os.makedirs('object/friend_list')
        self.sign_image = Image.open('assets/sign9.png')
        self.sign_photo = ImageTk.PhotoImage(self.sign_image)
        self.sign_label = tk.Label(self, image=self.sign_photo)
        self.sign_label.image = self.sign_photo  # 保持对图片的引用，防止被垃圾回收
        self.sign_label.pack()
        tk.Label(self, text='', height=2).pack()
        frame3 = tk.Frame(self)
        frame3.pack()
        tk.Label(frame3, text="列表名称:", font=('微软雅黑', 12, 'bold'), width=8, anchor='w').pack(side=tk.LEFT,                                                                                     padx=20)
        entry_text = tk.StringVar()
        e = ttk.Entry(frame3, width=25, textvariable=entry_text)

        def on_entry_change(*args):
            text = entry_text.get()
            if text in self.friend_list_names:
                name_label.config(text='     已存在改名称', fg='red')
            else:
                name_label.config(text='')
        e.pack(side=tk.LEFT, padx=35)
        entry_text.trace("w", on_entry_change)
        name_label = tk.Label(self, text='', height=1)
        name_label.pack()
        tk.Label(self, text='', height=1).pack()

        def create_list():
            list_ = []
            selected_names = [name for name, var in zip(friend_name, check_vars) if var.get()]
            selected_dir = [dir for dir, var in zip(friend_dir, check_vars) if var.get()]
            if e.get() == '':
                messagebox.showinfo("提示", "请输入列表名称！")
                return
            if not selected_dir or not selected_names:
                messagebox.showinfo("提示", "请选择好友！")
                return
            if e.get() in self.friend_list_names:
                messagebox.showinfo("提示", "列表名称已存在！")
                return
            for name, dir in zip(selected_names, selected_dir):
                list_.append({'name': name, 'dir': dir})
            if messagebox.askokcancel("确认", "确认创建？"):
                while True:
                    this_file_name = generate_random_string() + '.json'
                    this_file_path = os.path.join('object/friend_list', this_file_name)
                    if this_file_name not in list_file_names:
                        break
                with open(this_file_path, 'w', encoding='utf-8') as f:
                    json.dump(list_, f)
                self.json_file.append({'name': e.get(), 'dir': this_file_path})
                with open('object/friend_list/list_name.json', 'w', encoding='utf-8') as f:
                    json.dump(self.json_file, f)
                messagebox.showinfo("提示", "创建成功！")
                e.delete(0, 'end')
                for var in check_vars:
                    var.set(0)
                if os.path.exists('object/friend_list/list_name.json'):
                    with open('object/friend_list/list_name.json', 'r', encoding='utf-8') as f:
                        self.json_file = json.load(f)
                    self.friend_list_names = [list['name'] for list in self.json_file]

        def on_mousewheel(event):
            canvas.yview_scroll(int(-1 * (event.delta / 120)), "units")

        # 创建一个BooleanVar列表用于存储每个多选框的状态
        check_vars = [tk.BooleanVar() for _ in friend_name]

        frame2 = ttk.Frame(self)
        frame2.pack()
        # 创建滚动条
        scrollbar = ttk.Scrollbar(frame2)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)

        # 创建Canvas
        canvas = tk.Canvas(frame2, borderwidth=0, width=300, height=200)
        canvas.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)

        # 将滚动条与Canvas关联
        scrollbar.config(command=canvas.yview)
        canvas.config(yscrollcommand=scrollbar.set)

        # 在Windows和Linux系统中绑定鼠标滚轮滚动事件
        canvas.bind_all("<MouseWheel>", on_mousewheel)  # 对于Windows
        canvas.bind_all("<Button-4>", on_mousewheel)  # 对于Linux, 向上滚动
        canvas.bind_all("<Button-5>", on_mousewheel)  # 对于Linux, 向下滚动

        # 创建一个frame放置在canvas上
        frame = tk.Frame(canvas)
        canvas.create_window((0, 0), window=frame, anchor='nw')
        # 为列表中的每个name创建一个多选框
        avatar_path = 'assets/sign4.png'
        for i, name in enumerate(friend_name):
            for file in os.listdir(friend_dir[i]):
                if file.startswith('avatar'):
                    avatar_path = os.path.join(friend_dir[i], file)
            checkbox_image = Image.open(avatar_path)
            checkbox_image = checkbox_image.resize((35, 35))
            checkbox_photo = ImageTk.PhotoImage(checkbox_image)
            cb = ttk.Checkbutton(frame, text=name, image=checkbox_photo, compound="left", variable=check_vars[i])
            cb.image = checkbox_photo
            cb.pack(anchor='w', fill='x')

        # 更新滚动区域大小
        frame.update_idletasks()
        canvas.config(scrollregion=canvas.bbox("all"))

        # 添加一个按钮，当点击时会显示被选中的names
        tk.Label(self, text='', height=3).pack()
        btn_show = ttk.Button(self, text="确定", style='Custom.TButton', command=create_list)
        btn_show.pack()


class FlstReviseFrame(tk.Frame):
    def __init__(self, root):
        super().__init__(root)
        friend_path = 'object/people.json'
        if os.path.exists(friend_path):
            with open(friend_path, 'r', encoding='utf-8') as f:
                friends = json.load(f)
            friend_name = [friend['name'] for friend in friends]
            friend_dir = [friend['dir'] for friend in friends]
        else:
            friend_name = []
            friend_dir = []
        self.json_file = []
        if os.path.exists('object/friend_list'):
            if os.path.exists('object/friend_list/list_name.json'):
                with open('object/friend_list/list_name.json', 'r', encoding='utf-8') as f:
                    self.json_file = json.load(f)
                self.friend_list_names = [list['name'] for list in self.json_file]
                self.list_path_names = [list['dir'] for list in self.json_file]
            else:
                self.friend_list_names = []
                self.list_path_names = []
        else:
            os.makedirs('object/friend_list')
        self.sign_image = Image.open('assets/sign10.png')
        self.sign_photo = ImageTk.PhotoImage(self.sign_image)
        self.sign_label = tk.Label(self, image=self.sign_photo)
        self.sign_label.image = self.sign_photo  # 保持对图片的引用，防止被垃圾回收
        self.sign_label.pack()
        tk.Label(self, text='', height=1).pack()
        selected_list = tk.StringVar()
        buttons_frame2 = tk.Frame(self)
        buttons_frame2.pack()
        tk.Label(buttons_frame2, text="选择好友列表: ", font=('微软雅黑', 12, "bold"), width=13, anchor="w").pack(
            side=tk.LEFT)
        comb = ttk.Combobox(buttons_frame2, style='Custom.TCombobox', textvariable=selected_list, values=self.friend_list_names)
        comb.pack(side=tk.RIGHT, padx=15)

        tk.Label(self, text='', height=2).pack()

        def create_list():
            list_ = []
            selected_names = [name for name, var in zip(friend_name, check_vars) if var.get()]
            selected_dir = [dir for dir, var in zip(friend_dir, check_vars) if var.get()]
            if not selected_list.get():
                messagebox.showinfo("提示", "请选择列表！")
                return
            if e.get() == '':
                messagebox.showinfo("提示", "请输入列表名称！")
                return
            if e.get() != selected_list.get() and e.get() in self.friend_list_names:
                messagebox.showinfo("提示", "列表名称已存在！")
                return
            if not selected_dir or not selected_names:
                messagebox.showinfo("提示", "请选择好友！")
                return
            for name, dir in zip(selected_names, selected_dir):
                list_.append({'name': name, 'dir': dir})
            if messagebox.askokcancel("确认", "确认创建？"):
                for it in self.json_file:
                    if it['name'] == selected_list.get():
                        it['name'] = e.get()
                        with open(it['dir'], 'w', encoding='utf-8') as f:
                            json.dump(list_, f)
                with open('object/friend_list/list_name.json', 'w', encoding='utf-8') as f:
                    json.dump(self.json_file, f)
                if os.path.exists('object/friend_list/list_name.json'):
                    with open('object/friend_list/list_name.json', 'r', encoding='utf-8') as f:
                        self.json_file = json.load(f)
                    self.friend_list_names = [list['name'] for list in self.json_file]
                    self.list_path_names = [list['dir'] for list in self.json_file]
                else:
                    self.friend_list_names = []
                    self.list_path_names = []
                messagebox.showinfo("提示", "创建成功！")
                e.delete(0, 'end')
                comb.set('')
                for var in check_vars:
                    var.set(0)
                comb.config(values=self.friend_list_names)

        def on_mousewheel(event):
            canvas.yview_scroll(int(-1 * (event.delta / 120)), "units")

        # 创建一个BooleanVar列表用于存储每个多选框的状态
        check_vars = [tk.BooleanVar() for _ in friend_name]

        frame2 = ttk.Frame(self)
        frame2.pack()
        # 创建滚动条
        scrollbar = ttk.Scrollbar(frame2)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)

        # 创建Canvas
        canvas = tk.Canvas(frame2, borderwidth=0, width=300, height=200)
        canvas.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)

        # 将滚动条与Canvas关联
        scrollbar.config(command=canvas.yview)
        canvas.config(yscrollcommand=scrollbar.set)

        # 在Windows和Linux系统中绑定鼠标滚轮滚动事件
        canvas.bind_all("<MouseWheel>", on_mousewheel)  # 对于Windows
        canvas.bind_all("<Button-4>", on_mousewheel)  # 对于Linux, 向上滚动
        canvas.bind_all("<Button-5>", on_mousewheel)  # 对于Linux, 向下滚动

        # 创建一个frame放置在canvas上
        frame = tk.Frame(canvas)
        canvas.create_window((0, 0), window=frame, anchor='nw')
        # 为列表中的每个name创建一个多选框
        avatar_path = 'assets/sign4.png'
        for i, name in enumerate(friend_name):
            for file in os.listdir(friend_dir[i]):
                if file.startswith('avatar'):
                    avatar_path = os.path.join(friend_dir[i], file)
            checkbox_image = Image.open(avatar_path)
            checkbox_image = checkbox_image.resize((35, 35))
            checkbox_photo = ImageTk.PhotoImage(checkbox_image)
            cb = ttk.Checkbutton(frame, text=name, image=checkbox_photo, compound="left", variable=check_vars[i])
            cb.image = checkbox_photo
            cb.pack(anchor='w', fill='x')

        # 更新滚动区域大小
        frame.update_idletasks()
        canvas.config(scrollregion=canvas.bbox("all"))

        tk.Label(self, text='', height=2).pack()
        frame3 = tk.Frame(self)
        frame3.pack()
        tk.Label(frame3, text="修改列表名称:", font=('微软雅黑', 12, 'bold'), width=10, anchor='w').pack(side=tk.LEFT,
                                                                                                         padx=20)
        e = ttk.Entry(frame3, width=25)
        e.pack(side=tk.LEFT, padx=20)

        # 添加一个按钮，当点击时会显示被选中的names
        tk.Label(self, text='', height=3).pack()
        btn_show = ttk.Button(self, text="确定", style='Custom.TButton', command=create_list)
        btn_show.pack()

        def on_select(event):
            e.delete(0, 'end')
            for var in check_vars:
                var.set(0)
            e.insert(0, selected_list.get())
            for name, path in zip(self.friend_list_names, self.list_path_names):
                if name == selected_list.get():
                    with open(path, 'r', encoding='utf-8') as f:
                        temp = json.load(f)
            temp_name = [name['name'] for name in temp]
            for name, var in zip(friend_name,check_vars):
                if name in temp_name:
                    var.set(1)

        comb.bind("<<ComboboxSelected>>", on_select)


class DeleteFrame(tk.Frame):
    def __init__(self, root):
        super().__init__(root)
        friend_path = 'object/people.json'
        self.friends = []
        if os.path.exists(friend_path):
            with open(friend_path, 'r', encoding='utf-8') as f:
                self.friends = json.load(f)
            self.friend_name = [friend['name'] for friend in self.friends]
            self.friend_dir = [friend['dir'] for friend in self.friends]
        else:
            self.friend_name = []
            self.friend_dir = []
        self.json_file = []
        if os.path.exists('object/friend_list'):
            if os.path.exists('object/friend_list/list_name.json'):
                with open('object/friend_list/list_name.json', 'r', encoding='utf-8') as f:
                    self.json_file = json.load(f)
                self.friend_list_names = [list['name'] for list in self.json_file]
                self.list_path_names = [list['dir'] for list in self.json_file]
            else:
                self.friend_list_names = []
                self.list_path_names = []
        else:
            os.makedirs('object/friend_list')

        self.sign_image = Image.open('assets/sign11.png')
        self.sign_photo = ImageTk.PhotoImage(self.sign_image)
        self.sign_label = tk.Label(self, image=self.sign_photo)
        self.sign_label.image = self.sign_photo  # 保持对图片的引用，防止被垃圾回收
        self.sign_label.pack()
        tk.Label(self, text='', height=3).pack()
        selected_mode = tk.IntVar(value=0)
        selected_delete = tk.StringVar()
        def show_combobox():
            if selected_mode.get() == 0:
                comb.config(values=self.friend_name)
                selected_delete.set('')
            else:
                comb.config(values=self.friend_list_names)
                selected_delete.set('')

        buttons_frame = tk.Frame(self)
        buttons_frame.pack()
        radio_button1 = ttk.Radiobutton(buttons_frame, text="删除好友资料", style='Custom.TRadiobutton', cursor="hand2",
                                        variable=selected_mode, value=0, command=show_combobox)
        radio_button2 = ttk.Radiobutton(buttons_frame, text="删除好友列表", style='Custom.TRadiobutton', cursor="hand2",
                                        variable=selected_mode, value=1, command=show_combobox)
        radio_button1.pack(side=tk.LEFT, padx=10)
        radio_button2.pack(side=tk.RIGHT, padx=10)
        tk.Label(self, text='', height=3).pack()

        buttons_frame3 = tk.Frame(self)
        buttons_frame3.pack()
        tk.Label(buttons_frame3, text="选择好友/列表: ", font=('微软雅黑', 12, "bold"), width=15, anchor="w").pack(
            side=tk.LEFT)
        comb = ttk.Combobox(buttons_frame3, style='Custom.TCombobox', textvariable=selected_delete, values=self.friend_name)
        comb.pack(side=tk.RIGHT)
        tk.Label(self, text='', height=5).pack()

        def delete():
            if not selected_delete.get():
                messagebox.showinfo("提示", "请选择删除对象！")
                return
            if messagebox.askokcancel("确认", "确认删除？"):
                if selected_mode.get() == 0:
                    index = self.friend_name.index(selected_delete.get())
                    shutil.rmtree(self.friend_dir[index])
                    self.friends = [x for x in self.friends if x['name'] != selected_delete.get()]
                    with open('object/people.json', 'w', encoding='utf-8') as f:
                        json.dump(self.friends, f)
                if selected_mode.get() == 1:
                    index = self.friend_list_names.index(selected_delete.get())
                    os.remove(self.list_path_names[index])
                    self.json_file = [x for x in self.json_file if x['name'] != selected_delete.get()]
                    with open('object/friend_list/list_name.json', 'w', encoding='utf-8') as f:
                        json.dump(self.json_file, f)

                with open(friend_path, 'r', encoding='utf-8') as f:
                    self.friends = json.load(f)
                self.friend_name = [friend['name'] for friend in self.friends]
                self.friend_dir = [friend['dir'] for friend in self.friends]
                with open('object/friend_list/list_name.json', 'r', encoding='utf-8') as f:
                    self.json_file = json.load(f)
                self.friend_list_names = [list['name'] for list in self.json_file]
                self.list_path_names = [list['dir'] for list in self.json_file]

                messagebox.showinfo("提示", "删除成功！")
                selected_mode.set(0)
                comb.set('')
                comb.config(values=self.friend_name)

        btn_show = ttk.Button(self, text="确定", style='Custom.TButton', command=delete)
        btn_show.pack()



class InitFrame(tk.Frame):
    def __init__(self, root):
        super().__init__(root)
        self.file_path1 = None
        self.file_path2 = None
        self.file_path3 = None
        self.file_path4 = None
        self.file_path5 = None
        tk.Label(self, text='', height=1).pack()
        frame1 = tk.Frame(self)
        frame1.pack()
        canvas1 = tk.Canvas(self, width=300, height=70)
        canvas1.pack()
        if os.path.exists('object/myavatar.png'):
            avatar_image = Image.open('object/myavatar.png')
        else:
            avatar_image = Image.open('assets/sign4.png')
        avatar_photo = ImageTk.PhotoImage(avatar_image)
        canvas1.create_image(150, 30, image=avatar_photo, anchor='w')
        canvas1.image = avatar_photo

        def load_my_avatar():
            self.file_path1 = filedialog.askopenfilename(filetypes=[('Image files', '*.jpg;*.jpeg;*.png;*.gif')])
            if self.file_path1:
                canvas1.delete("all")
                image = Image.open(self.file_path1)
                photo = ImageTk.PhotoImage(image)
                canvas1.create_image(150, 30, image=photo, anchor='w')
                canvas1.image = photo
                button1.config(text='重新选择')

        tk.Label(frame1, text="我的头像：", font=('微软雅黑', 12, 'bold'),width=8,anchor='w').pack(side=tk.LEFT, padx=10)
        button1 = ttk.Button(frame1, text="选择图片", width=30, cursor="hand2",
                             command=load_my_avatar)
        button1.pack(side=tk.RIGHT)

        frame2 = tk.Frame(self)
        frame2.pack()
        canvas2 = tk.Canvas(self, width=300, height=70)
        canvas2.pack()
        if os.path.exists('object/send.png'):
            send_image = Image.open('object/send.png')
        else:
            send_image = Image.open('assets/sign4.png')
        send_photo = ImageTk.PhotoImage(send_image)
        canvas2.create_image(150, 30, image=send_photo, anchor='w')
        canvas2.image = send_photo

        def load_send():
            self.file_path2 = filedialog.askopenfilename(filetypes=[('Image files', '*.jpg;*.jpeg;*.png;*.gif')])
            if self.file_path2:
                canvas2.delete("all")
                image = Image.open(self.file_path2)
                photo = ImageTk.PhotoImage(image)
                canvas2.create_image(150, 30, image=photo, anchor='w')
                canvas2.image = photo
                button2.config(text='重新选择')

        tk.Label(frame2, text="发送：", font=('微软雅黑', 12, 'bold'),width=8,anchor='w').pack(side=tk.LEFT, padx=10)
        button2 = ttk.Button(frame2, text="选择图片", width=30, cursor="hand2",
                             command=load_send)
        button2.pack(side=tk.RIGHT)

        frame3 = tk.Frame(self)
        frame3.pack()
        canvas3 = tk.Canvas(self, width=300, height=70)
        canvas3.pack()
        if os.path.exists('object/duplicate.png'):
            dup_image = Image.open('object/duplicate.png')
        else:
            dup_image = Image.open('assets/sign4.png')
        dup_photo = ImageTk.PhotoImage(dup_image)
        canvas3.create_image(150, 30, image=dup_photo, anchor='w')
        canvas3.image = dup_photo

        def load_dup():
            self.file_path3 = filedialog.askopenfilename(filetypes=[('Image files', '*.jpg;*.jpeg;*.png;*.gif')])
            if self.file_path3:
                canvas3.delete("all")
                image = Image.open(self.file_path3)
                photo = ImageTk.PhotoImage(image)
                canvas3.create_image(150, 30, image=photo, anchor='w')
                canvas3.image = photo
                button3.config(text='重新选择')

        tk.Label(frame3, text="复制：", font=('微软雅黑', 12, 'bold'), width=8, anchor='w').pack(side=tk.LEFT, padx=10)
        button3 = ttk.Button(frame3, text="选择图片", width=30, cursor="hand2",
                             command=load_dup)
        button3.pack(side=tk.RIGHT)

        frame4 = tk.Frame(self)
        frame4.pack()
        canvas4 = tk.Canvas(self, width=300, height=70)
        canvas4.pack()
        if os.path.exists('object/meme.png'):
            meme_image = Image.open('object/meme.png')
        else:
            meme_image = Image.open('assets/sign4.png')
        meme_photo = ImageTk.PhotoImage(meme_image)
        canvas4.create_image(150, 30, image=meme_photo, anchor='w')
        canvas4.image = meme_photo

        def load_meme():
            self.file_path4 = filedialog.askopenfilename(filetypes=[('Image files', '*.jpg;*.jpeg;*.png;*.gif')])
            if self.file_path4:
                canvas4.delete("all")
                image = Image.open(self.file_path4)
                photo = ImageTk.PhotoImage(image)
                canvas4.create_image(150, 30, image=photo, anchor='w')
                canvas4.image = photo
                button4.config(text='重新选择')

        tk.Label(frame4, text="添加表情：", font=('微软雅黑', 12, 'bold'), width=8, anchor='w').pack(side=tk.LEFT, padx=10)
        button4 = ttk.Button(frame4, text="选择图片", width=30, cursor="hand2",
                             command=load_meme)
        button4.pack(side=tk.RIGHT)

        frame5 = tk.Frame(self)
        frame5.pack()
        canvas5 = tk.Canvas(self, width=300, height=70)
        canvas5.pack()
        if os.path.exists('object/audio.png'):
            audio_image = Image.open('object/audio.png')
        else:
            audio_image = Image.open('assets/sign4.png')
        audio_photo = ImageTk.PhotoImage(audio_image)
        canvas5.create_image(150, 30, image=audio_photo, anchor='w')
        canvas5.image = audio_photo

        def load_audio():
            self.file_path5 = filedialog.askopenfilename(filetypes=[('Image files', '*.jpg;*.jpeg;*.png;*.gif')])
            if self.file_path5:
                canvas5.delete("all")
                image = Image.open(self.file_path5)
                photo = ImageTk.PhotoImage(image)
                canvas5.create_image(150, 30, image=photo, anchor='w')
                canvas5.image = photo
                button5.config(text='重新选择')

        tk.Label(frame5, text="转文字：", font=('微软雅黑', 12, 'bold'), width=8, anchor='w').pack(side=tk.LEFT,
                                                                                                    padx=10)
        button5 = ttk.Button(frame5, text="选择图片", width=30, cursor="hand2",
                             command=load_audio)
        button5.pack(side=tk.RIGHT)

        def confirm():
            if self.file_path1:
                os.remove('object/myavatar.png')
                shutil.copy(self.file_path1, 'object')
                file_name = os.path.basename(self.file_path1)
                target_file = os.path.join('object', file_name)
                os.rename(target_file, 'object/myavatar.png')
                canvas1.delete("all")
                image = Image.open('object/myavatar.png')
                photo = ImageTk.PhotoImage(image)
                canvas1.create_image(150, 30, image=photo, anchor='w')
                canvas1.image = photo
            if self.file_path2:
                os.remove('object/send.png')
                shutil.copy(self.file_path1, 'object')
                file_name = os.path.basename(self.file_path2)
                target_file = os.path.join('object', file_name)
                os.rename(target_file, 'object/send.png')
                canvas2.delete("all")
                image = Image.open('object/send.png')
                photo = ImageTk.PhotoImage(image)
                canvas2.create_image(150, 30, image=photo, anchor='w')
                canvas2.image = photo
            if self.file_path3:
                os.remove('object/duplicate.png')
                shutil.copy(self.file_path1, 'object')
                file_name = os.path.basename(self.file_path3)
                target_file = os.path.join('object', file_name)
                os.rename(target_file, 'object/duplicate.png')
                canvas3.delete("all")
                image = Image.open('object/duplicate.png')
                photo = ImageTk.PhotoImage(image)
                canvas3.create_image(150, 30, image=photo, anchor='w')
                canvas3.image = photo
            if self.file_path4:
                os.remove('object/meme.png')
                shutil.copy(self.file_path1, 'object')
                file_name = os.path.basename(self.file_path4)
                target_file = os.path.join('object', file_name)
                os.rename(target_file, 'object/meme.png')
                canvas4.delete("all")
                image = Image.open('object/meme.png')
                photo = ImageTk.PhotoImage(image)
                canvas4.create_image(150, 30, image=photo, anchor='w')
                canvas4.image = photo
            if self.file_path5:
                os.remove('object/audio.png')
                shutil.copy(self.file_path1, 'object')
                file_name = os.path.basename(self.file_path5)
                target_file = os.path.join('object', file_name)
                os.rename(target_file, 'object/audio.png')
                canvas5.delete("all")
                image = Image.open('object/audio.png')
                photo = ImageTk.PhotoImage(image)
                canvas5.create_image(150, 30, image=photo, anchor='w')
                canvas5.image = photo

            messagebox.showinfo("提示", "初始化完成！")

        tk.Label(self, text='', height=1).pack()
        btn_show = ttk.Button(self, text="确定", style='Custom.TButton', command=confirm)
        btn_show.pack()

