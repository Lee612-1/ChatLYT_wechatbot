# 微信ai自动回复😅

## 注意
使用时间过长微信可能会强制退出！

## 介绍
这是一个用于个人微信的ai自动回复程序，
无需网页版微信即可使用。

## 更新说明
### 2024-5-14
1. 新增链接和表情识别

### 2024-5-13
1. 优化代码逻辑 
2. 优化连续信息读取 
3. 优化拟人模式效果 
4. 优化快速对话中的消息读取 
5. 系统提示中增加时间天气等环境信息
6. 新增启动时读取历史对话记录

### 2024-5-12
1. 优化代码逻辑
2. 新增回复多人功能
3. 新增拟人模式，增强拟真程度


### 2024-5-11
1. 修复bug
2. 新增图片信息回复功能


### 2024-5-10
1. 文字信息回复

## 环境配置
### 通过配置文件安装
```bash
# Create conda environment
conda create -n wechatbot python=3.9

# Activate the environment
conda activate wechatbot

# Install packages
pip install -r requirements.yml
```

## 使用说明
### 准备用户信息

用截图工具获取下面这些图片： 列表中朋友的头像，聊天框中双方的头像，复制按键，发送按键；并以下面的格式放入指定文件夹。在`role.txt`中写入希望ai扮演的角色。`people.json`中存放好友列表，用于同时回复多人消息。
```
object
|___friend1  # folder
|   |___large_avator.png # avator in the message list
|   |___avator # avator in chat window
|   |___role.txt # system prompt
|   
|___friend2 
|
|___myavatar.png # your own avatar
| 
|___duplicate.png # duplicate button
|
|___send.png # send button
|
|___people.json # list of friends
...
```
### 运行程序
在终端中输入以下代码开始运行；
为保证程序正常运行，请务必将微信窗口置于上层。
推荐将微信窗口长度拉到最大。

单人模式
```bash
python -u main.py --person object/friend
```

多人模式（建议5人以下）
```bash
python -u main.py --people object/people.json
```

拟人模式
```bash
python -u main.py --authentic 2
```

注意单人模式和多人模式不能混合使用，
拟人模式中`authentic`可以从0，1，2中进行选择，数字越大越像真人。

## 声明
**本项目仅供技术研究，请勿用于任何商业用途，请勿用于非法用途，如有任何人凭此做何非法事情，均于作者无关，特此声明。**