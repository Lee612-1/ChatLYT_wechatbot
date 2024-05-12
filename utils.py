import pyautogui
import pyperclip
import time
from collections import Counter
from PIL import ImageGrab
import gradio_client
import geocoder
import datetime
import requests
from lxml import etree
import re


def _mouseclick(img):
    location = pyautogui.locateCenterOnScreen(img, confidence=0.9)
    pyautogui.click(location.x, location.y, clicks=1, interval=0.2, duration=0.2, button="left")
    return None


def _get_pos(img_path):
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


def _get_msg_pos(her_avatar, my_avatar):
    her_x, her_y_list = _get_pos(her_avatar)
    try:
        my_x, my_y_list = _get_pos(my_avatar)
        my_y = max(my_y_list)
    except:
        my_y = -1000
    her_y = [x for x in her_y_list if x >= my_y]
    return her_x, her_y


def _get_msg(large_avatar, her_avatar, my_avatar):
    try:
        _mouseclick(large_avatar)
        x, ys = _get_msg_pos(her_avatar, my_avatar)
        msg_list = []
        img_list = []
        if ys:
            for y in ys:
                pyautogui.click(x + 45, y, clicks=1, interval=0.2, duration=0.2, button="right")
                time.sleep(0.2)
                try:
                    _mouseclick('object/duplicate.png')
                    image_path = ImageGrab.grabclipboard()
                    time.sleep(0.2)
                    raw_msg = pyperclip.paste()
                    if raw_msg != '':
                        msg_list.append(raw_msg)
                    if isinstance(image_path, list):
                        img_list.extend(image_path)

                    time.sleep(0.2)
                except:
                    _mouseclick(large_avatar)
            msg = '，'.join(msg_list)
            return msg, img_list
        else:
            return None, None
    except:
        print('not detected')
        return None, None


def _describe_img(img, client):
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


def _get_img_query(query_list):
    if not query_list:
        return None
    else:
        querys = ''
        for i, query in enumerate(query_list):
            querys += f'[图片{i + 1}](描述：{query})；'
        return querys


def process_img_query(img_list, img_client):
    img_query_list = []
    for img in img_list:
        try:
            raw_query = _describe_img(img, img_client)
            img_query_list.append(raw_query)
        except:
            print('fail to describe the img')
    img_query = _get_img_query(img_query_list)
    return img_query


def reply(large_avatar, her_avatar, my_avatar, answers):
    for ids, answer in enumerate(answers):
        if answer != '':
            _mouseclick(large_avatar)
            time.sleep(0.1)
            pyperclip.copy(answer)
            pyautogui.hotkey('ctrl', 'v')
            time.sleep(0.1)
            _mouseclick('object/send.png')
            _, ys = _get_msg_pos(her_avatar, my_avatar)
            if ys:
                return ids
            time.sleep(2)
    return None


def process_answer(answer, authentic, length=5):
    if authentic == 0:
        return [answer]
    elif authentic == 1:
        answer_list = re.split(r'[。!]', answer)
        if len(answer_list) > length:
            answer_list = answer_list[:length]
        return answer_list
    elif authentic == 2:
        raw_answer_list = re.split(r'[。!]', answer)
        answer_list = []
        for raw_answers in raw_answer_list:
            list_list = raw_answers.split('？')
            if len(list_list) > 1:
                for i in range(len(list_list) - 1):
                    list_list[i] = list_list[i] + '？'
            answer_list.extend(list_list)
            if len(answer_list) > length:
                answer_list = answer_list[:length]
            return answer_list


def _get_weather(city):
    url = f'https://www.tianqishi.com/{city}.html'
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/103.0.0.0 Safari/537.36',
    }
    res_data = requests.get(url=url, headers=headers)
    tree = etree.HTML(res_data.text)
    city = tree.xpath('//h3[@class="city-title ico"]')[0].text
    city = city.replace('实时天气', '')
    st = tree.xpath('//div[@class="ltlTemperature"]//span')[0].text  # 体感温度
    t_type = tree.xpath('(//div[@class="box pcity"])[3]//li//a[@target="_blank"]')[0].text.split('：')[1].split('，')[0]
    return city, st, t_type


def enhance_prompt():
    formatted_datetime = datetime.datetime.now().strftime("%Y-%m-%d %A %H:%M")
    city = geocoder.ip('me').city
    city = city.replace(' ', '')
    city = city.lower()
    try:
        city, st, t_type = _get_weather(city)
        add = f"当前日期和时间是{formatted_datetime},你所在的城市是{city},温度{st},天气{t_type}。"
    except:
        add = f"当前日期和时间是{formatted_datetime},你所在的城市是{city}。"
    return add


def check_msg(large_avatar, her_avatar, my_avatar):
    check_list = [[], []]
    flag = 1
    attempt = 0
    while True:
        query, img_list = _get_msg(large_avatar, her_avatar, my_avatar)
        if flag == 1:
            check_list[1] = [query, img_list]
            flag = -flag
        else:
            check_list[0] = [query, img_list]
            flag = -flag

        if check_list[0] == check_list[1]:
            break
        else:
            print('wait for more message')
        if attempt >= 10:
            break
        time.sleep(7)
        attempt += 1

    if attempt >= 10:
        return None, None
    else:
        return query, img_list


def _list_trans(input_list):
    result = []
    current_group = []
    prev_value = None
    for pair in input_list:
        if prev_value is None or pair[1] != prev_value:
            if current_group:
                result.append(current_group)
            current_group = [pair[0]]
        else:
            current_group.append(pair[0])
        prev_value = pair[1]
    if current_group:
        result.append(current_group)
    result = [result[i:i + 2] for i in range(0, len(result), 2)]
    return result


def _get_history(large_avatar, her_avatar, my_avatar):
    try:
        _mouseclick(large_avatar)
        her_x, her_y_list = _get_pos(her_avatar)
        my_x, my_y_list = _get_pos(my_avatar)
        my_y_list = [x for x in my_y_list if x >= min(her_y_list)]
        her_y_list = [x for x in her_y_list if x <= max(my_y_list)]
        pos_list = _list_trans(sorted([(x, 1) for x in her_y_list] + [(y, 2) for y in my_y_list]))
        msg_list = []
        if pos_list:
            for pos in pos_list:
                temp_msg_list = ['', '']
                for p in pos[0]:
                    pyautogui.click(her_x + 45, p, clicks=1, interval=0.2, duration=0.2, button="right")
                    time.sleep(0.2)
                    try:
                        _mouseclick('object/duplicate.png')
                        image_path = ImageGrab.grabclipboard()
                        time.sleep(0.2)
                        raw_msg = pyperclip.paste()
                        if raw_msg != '':
                            temp_msg_list[0] += raw_msg + '，'
                        if isinstance(image_path, list):
                            temp_msg_list[0] += '[图片]，'
                        time.sleep(0.2)
                    except:
                        _mouseclick(large_avatar)
                for p in pos[1]:
                    pyautogui.click(my_x - 45, p, clicks=1, interval=0.2, duration=0.2, button="right")
                    time.sleep(0.2)
                    try:
                        _mouseclick('object/duplicate.png')
                        image_path = ImageGrab.grabclipboard()
                        time.sleep(0.2)
                        raw_msg = pyperclip.paste()
                        if raw_msg != '':
                            temp_msg_list[1] += raw_msg + '，'
                        if isinstance(image_path, list):
                            temp_msg_list[1] += '[图片]，'
                        time.sleep(0.2)
                    except:
                        _mouseclick(large_avatar)
                msg_list.append(temp_msg_list)
        return msg_list
    except:
        return []


def process_history(friend_list, my_avatar):
    len_friend_list = len(friend_list)
    history_list = [[] for _ in range(len_friend_list)]
    for i in range(len_friend_list):
        her_avatar = f'{friend_list[i]}/avatar.png'
        large_avatar = f'{friend_list[i]}/large_avatar.png'
        history_list[i] = _get_history(large_avatar, her_avatar, my_avatar)
        return history_list


def generate_answer(query, history, system_prompt, text_client):
    if query == '':
        answer = '暂时不支持回复此类消息，我们聊点别的吧！'
    else:
        try:
            result = text_client.predict(
                query=query,
                history=history,
                system=system_prompt,
                api_name="/model_chat"
            )
            history = result[1]
            answer = result[1][-1][-1]
        except:
            answer = '未响应，输入\'exit\'退出自动回复'
    return answer, history
