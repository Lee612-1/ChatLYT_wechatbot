# 微信ai自动回复

## 更新说明

### 2024-5-10

1. 文字信息回复

### 2024-5-11

1. 修复bug
2. 新增图片信息回复功能

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

用截图工具获取下面这些图片： 列表中朋友的头像，聊天框中双方的头像，复制按键，发送按键；并以下面的格式放入指定文件夹。在`role.txt`中写入希望ai扮演的角色。
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
...
```
### 运行程序
在终端中输入以下代码开始运行；为保证程序正常运行，请务必将微信窗口置于上层。
```
python -u main.py
```
## 声明

**本项目仅供技术研究，请勿用于任何商业用途，请勿用于非法用途，如有任何人凭此做何非法事情，均于作者无关，特此声明。**