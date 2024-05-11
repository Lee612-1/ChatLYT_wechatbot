import pyautogui
import pyperclip
import time
from collections import Counter
from PIL import ImageGrab
import gradio_client

def mouseclick(img):
    location = pyautogui.locateCenterOnScreen(img, confidence=0.9)
    pyautogui.click(location.x, location.y, clicks=1, interval=0.2, duration=0.2, button="left")
    return None

def get_pos(img_path):
    matches = pyautogui.locateAllOnScreen(img_path)
    x_list = []
    y_list = []
    for match in matches:
        center_x, center_y = pyautogui.center(match)
        x_list.append(center_x)
        y_list.append(center_y)

    counts = Counter(x_list)
    x = counts.most_common(1)[0][0]
    return x, y_list

def get_msg_pos(her_avatar, my_avatar):
    her_x, her_y_list = get_pos(her_avatar)
    try:
        my_x, my_y_list = get_pos(my_avatar)
        my_y = max(my_y_list)
    except:
        my_y = -1000
    her_y = [x for x in her_y_list if x >= my_y]
    return her_x, her_y

def get_msg(large_avatar, her_avatar, my_avatar):
    try:
        x, ys = get_msg_pos(her_avatar, my_avatar)
        msg_list = []
        img_list = []
        if ys != []:
            for y in ys:
                pyautogui.click(x+45, y, clicks=1, interval=0.2, duration=0.2, button="right")
                time.sleep(0.2)
                try:
                    mouseclick('object/duplicate.png')
                    image_path = ImageGrab.grabclipboard()
                    time.sleep(0.2)
                    raw_msg = pyperclip.paste()
                    if raw_msg != '':
                        msg_list.append(raw_msg)
                    if isinstance(image_path, list):
                        img_list.extend(image_path)

                    time.sleep(0.2)
                except:
                    mouseclick(large_avatar)
            msg = '，'.join(msg_list)
            return msg, img_list
        else:
            return None, None
    except:
        print('not detected')
        return None, None

def get_img_query(query_list):
    if query_list == []:
        return None
    else:
        querys = ''
        for i, query in enumerate(query_list):
            querys+=f'[图片{i+1}](描述：{query})；'
        return  querys


def reply(large_avatar,answer):
    mouseclick(large_avatar)
    time.sleep(0.1)
    pyperclip.copy(answer)
    pyautogui.hotkey('ctrl', 'v')
    time.sleep(0.1)
    mouseclick('object/send.png')
    return None

def describe_img(img, client):
    _ = client.predict(
        image=gradio_client.file(img),
        _chatbot=[],
        api_name="/upload_img"
    )
    description = client.predict(
        _question='描述一下图片',
        _chat_bot=[],
        api_name="/respond"
    )
    raw_query = description[1][-1][-1]
    return raw_query




