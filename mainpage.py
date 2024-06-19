import tkinter as tk
from views import *
from PIL import Image, ImageTk
from tkinter import filedialog
import shutil
import os
import pyautogui
import time

class Mainpage:
    def __init__(self, root: tk.Tk):
        self.root = root
        self.root.title('ChatLYT😅')
        self.root.geometry('600x800+1500+500')
        self.crate_page()
        temp_folder = 'temp'
        obj_folder = 'object'
        if not os.path.exists(temp_folder):
            os.makedirs(temp_folder)
        if not os.path.exists(obj_folder):
            os.makedirs(obj_folder)

    def crate_page(self):
        self.top_frame = tk.Frame(self.root)

        def on_click(event=None):
            self.top_frame.pack_forget()
            self.start_frame.pack()
            self.run_frame.pack_forget()
            self.change_frame.pack_forget()
            self.friend_frame.pack_forget()
            self.friend_revise_frame.pack_forget()
            self.flst_frame.pack_forget()
            self.flst_revise_frame.pack_forget()
        img = Image.open('assets/sign5.png')
        imgTk = ImageTk.PhotoImage(img)
        return_label = tk.Label(self.top_frame, image=imgTk)
        return_label.image = imgTk
        tk.Label(self.top_frame, text='', width=5).pack(side=tk.LEFT)
        return_label.pack(side=tk.LEFT, padx=15)
        return_label.bind('<Button-1>', on_click)
        self.title = tk.Label(self.top_frame, text="", font=('微软雅黑', 24, 'bold'), height=1, width=30, anchor="nw")
        self.title.pack(side=tk.RIGHT, pady=40)

        self.start_frame = tk.Frame(self.root)
        self.sign_photo = tk.PhotoImage(file='assets/sign.gif')
        self.sign_label = tk.Label(self.start_frame, image=self.sign_photo)
        self.sign_label.image = self.sign_photo  # 保持对图片的引用，防止被垃圾回收
        self.sign_label.pack()
        ttk.Button(self.start_frame, text="开始聊天", cursor="hand2", width=20, style='Custom.TButton', command=self.show_run).pack(pady=10)
        ttk.Button(self.start_frame, text="查看好友", cursor="hand2", width=20, style='Custom.TButton', command=self.show_flst).pack(pady=10)
        ttk.Button(self.start_frame, text="退出", cursor="hand2", width=20, style='Custom.TButton', command=self.root.quit).pack(pady=10)

        self.about_frame = AboutFrame(self.root)
        self.run_frame = RunFrame(self.root)
        self.change_frame = ChangeFrame(self.root)
        self.friend_frame = FriendFrame(self.root)
        self.friend_revise_frame = FriendReviseFrame(self.root)
        self.flst_frame = FlstFrame(self.root)
        self.flst_revise_frame = FlstReviseFrame(self.root)
        self.init_frame = InitFrame(self.root)
        self.start_frame.pack()


        menubar = tk.Menu(self.root)
        set_menu = tk.Menu(menubar, tearoff=0)
        set_menu.add_command(label="帮助", command=self.guide)
        set_menu.add_command(label="文件夹中打开", command=self.open_dir)
        set_menu.add_command(label="更改api key", command=self.show_change)
        set_menu.add_separator()
        set_menu.add_command(label="退出", command=self.root.quit)
        menubar.add_cascade(label="设置", menu=set_menu)
        menubar.add_command(label='初始化', command=self.show_init)
        friend_menu = tk.Menu(menubar, tearoff=0)
        new_menu = tk.Menu(friend_menu, tearoff=0)
        new_menu.add_command(label="好友资料", command=self.show_friend)
        new_menu.add_command(label="好友列表", command=self.show_flst)
        revise_menu = tk.Menu(friend_menu, tearoff=0)
        revise_menu.add_command(label="好友资料", command=self.show_friend_revise)
        revise_menu.add_command(label="好友列表", command=self.show_flst_revise)
        friend_menu.add_cascade(label='新建', menu=new_menu)
        friend_menu.add_cascade(label='修改', menu=revise_menu)
        menubar.add_cascade(label="好友", menu=friend_menu)
        menubar.add_command(label='开始', command=self.show_run)
        menubar.add_command(label='关于', command=self.show_about)
        self.root['menu'] = menubar

    def show_about(self):
        self.start_frame.pack_forget()
        self.top_frame.pack_forget()
        self.about_frame.pack()
        self.run_frame.pack_forget()
        self.change_frame.pack_forget()
        self.friend_frame.pack_forget()
        self.friend_revise_frame.pack_forget()
        self.flst_frame.pack_forget()
        self.flst_revise_frame.pack_forget()
        self.init_frame.pack_forget()

    def show_run(self):
        self.start_frame.pack_forget()
        self.top_frame.pack()
        self.about_frame.pack_forget()
        self.run_frame.pack_forget()
        self.change_frame.pack_forget()
        self.friend_frame.pack_forget()
        self.friend_revise_frame.pack_forget()
        self.flst_frame.pack_forget()
        self.flst_revise_frame.pack_forget()
        self.init_frame.pack_forget()
        self.run_frame = RunFrame(self.root)
        self.title.config(text='开始聊天')
        self.run_frame.pack()
        if not os.path.exists('object/people.json'):
            messagebox.showinfo("提示", "暂无好友资料，请新建")
            self.run_frame.pack_forget()
            self.friend_frame.pack()

    def show_change(self):
        self.start_frame.pack_forget()
        self.top_frame.pack()
        self.about_frame.pack_forget()
        self.run_frame.pack_forget()
        self.change_frame.pack_forget()
        self.friend_frame.pack_forget()
        self.friend_revise_frame.pack_forget()
        self.flst_frame.pack_forget()
        self.flst_revise_frame.pack_forget()
        self.init_frame.pack_forget()
        self.change_frame = ChangeFrame(self.root)
        self.title.config(text='更改 api key')
        self.change_frame.pack()

    def show_friend(self):
        self.start_frame.pack_forget()
        self.top_frame.pack()
        self.about_frame.pack_forget()
        self.run_frame.pack_forget()
        self.change_frame.pack_forget()
        self.friend_frame.pack_forget()
        self.friend_revise_frame.pack_forget()
        self.flst_frame.pack_forget()
        self.flst_revise_frame.pack_forget()
        self.init_frame.pack_forget()
        self.friend_frame = FriendFrame(self.root)
        self.title.config(text='新建好友资料')
        self.friend_frame.pack()

    def show_friend_revise(self):
        self.start_frame.pack_forget()
        self.top_frame.pack()
        self.about_frame.pack_forget()
        self.run_frame.pack_forget()
        self.change_frame.pack_forget()
        self.friend_frame.pack_forget()
        self.friend_revise_frame.pack_forget()
        self.flst_frame.pack_forget()
        self.flst_revise_frame.pack_forget()
        self.init_frame.pack_forget()
        self.friend_revise_frame = FriendReviseFrame(self.root)
        self.title.config(text='修改好友资料')
        self.friend_revise_frame.pack()

    def show_flst(self):
        self.start_frame.pack_forget()
        self.top_frame.pack()
        self.about_frame.pack_forget()
        self.run_frame.pack_forget()
        self.change_frame.pack_forget()
        self.friend_frame.pack_forget()
        self.friend_revise_frame.pack_forget()
        self.flst_frame.pack_forget()
        self.flst_revise_frame.pack_forget()
        self.init_frame.pack_forget()
        self.flst_frame = FlstFrame(self.root)
        self.title.config(text='新建好友列表')
        self.flst_frame.pack()

    def show_flst_revise(self):
        self.start_frame.pack_forget()
        self.top_frame.pack()
        self.about_frame.pack_forget()
        self.run_frame.pack_forget()
        self.change_frame.pack_forget()
        self.friend_frame.pack_forget()
        self.friend_revise_frame.pack_forget()
        self.flst_frame.pack_forget()
        self.flst_revise_frame.pack_forget()
        self.init_frame.pack_forget()
        self.flst_revise_frame = FlstReviseFrame(self.root)
        self.title.config(text='修改好友列表')
        self.flst_revise_frame.pack()

    def show_init(self):
        self.start_frame.pack_forget()
        self.top_frame.pack()
        self.about_frame.pack_forget()
        self.run_frame.pack_forget()
        self.change_frame.pack_forget()
        self.friend_frame.pack_forget()
        self.friend_revise_frame.pack_forget()
        self.flst_frame.pack_forget()
        self.flst_revise_frame.pack_forget()
        self.init_frame.pack_forget()
        self.init_frame = InitFrame(self.root)
        self.title.config(text='初始化')
        self.init_frame.pack()



    def guide(self):
        webbrowser.open("https://github.com/Lee612-1/ChatLYT_wechatbot")

    def open_dir(self):
        os.startfile('object')


if __name__ == '__main__':
    # pyautogui.hotkey('winleft', 'down')
    # time.sleep(0.3)
    root = tk.Tk()
    Mainpage(root)
    root.attributes("-topmost", False)
    root.mainloop()
