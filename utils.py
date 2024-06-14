import os.path
from io import BytesIO
import pickle
import re
import random
import time
import datetime
from collections import Counter
import requests
from lxml import etree
import pyautogui
import pyperclip
from PIL import ImageGrab, Image
import gradio_client
import geocoder
import win32clipboard
import base64


def _mouseclick(img):
    location = pyautogui.locateCenterOnScreen(img, confidence=0.9)
    pyautogui.click(location.x, location.y, clicks=1, interval=0.2, duration=0.2, button="left")
    return None


def _locate(img):
    try:
        location = pyautogui.locateCenterOnScreen(img, confidence=0.9)
        return location
    except:
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


def _get_msg(large_avatar, her_avatar, my_avatar, remain):
    try:
        _mouseclick(large_avatar)
        x, ys = _get_msg_pos(her_avatar, my_avatar)
        if remain is not None:
            ys = ys[-remain:]
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
                    if _locate('object/meme.png') is not None:
                        msg_list.append('[动画表情]')
                    else:
                        try:
                            _mouseclick('object/audio.png')
                            time.sleep(2)
                            _mouseclick('object/duplicate.png')
                            raw_msg = pyperclip.paste()
                            raw_msg = '[语音]' + raw_msg
                            msg_list.append(raw_msg)
                        except:
                            msg_list.append('[链接]')
                    _mouseclick(large_avatar)
            msg = '，'.join(msg_list)
            return msg, img_list
        else:
            return '', []
    except:
        print('not detected')
        return '', []


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
        raw_answer_list = re.split(r'[，。!]', answer)
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


def check_msg(large_avatar, her_avatar, my_avatar, wait=7, remain=None):
    check_list = [[], []]
    flag = 1
    attempt = 0
    while True:
        query, img_list = _get_msg(large_avatar, her_avatar, my_avatar, remain)
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
        time.sleep(wait)
        attempt += 1

    if attempt >= 10:
        return '', []
    else:
        return query, img_list


def count_msg(her_avatar, my_avatar):
    x, ys = _get_msg_pos(her_avatar, my_avatar)
    return len(ys)


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
                if temp_msg_list[0] == '':
                    temp_msg_list[0] = '[消息]'
                if temp_msg_list[1] == '':
                    temp_msg_list[1] = '[消息]'
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
        new_history = history
    else:
        try:
            result = text_client.predict(
                query=query,
                history=history,
                system=system_prompt,
                api_name="/model_chat"
            )
            new_history = result[1]
            answer = result[1][-1][-1]
        except:
            answer = '未响应，输入\'exit\'退出自动回复'
            new_history = history
    return answer, new_history


def _send_to_clipboard(clip_type, data):
    win32clipboard.OpenClipboard()
    win32clipboard.EmptyClipboard()
    win32clipboard.SetClipboardData(clip_type, data)
    win32clipboard.CloseClipboard()
    return None


def _copy_image_to_clipboard(image_path):
    try:
        image = Image.open(image_path)
    except:
        response = requests.get(image_path)
        if response.status_code == 200:
            image_bytes = BytesIO(response.content)
            image = Image.open(image_bytes)
    output = BytesIO()
    # Convert to BMP format here, as the Windows clipboard supports BMP
    image.convert("RGB").save(output, "BMP")
    data = output.getvalue()[14:]  # BMP file header needs to remove the first 14 bytes
    output.close()
    _send_to_clipboard(win32clipboard.CF_DIB, data)
    return None


def send_img(img_path, large_avatar):
    _copy_image_to_clipboard(img_path)
    _mouseclick(large_avatar)
    time.sleep(0.1)
    pyautogui.hotkey('ctrl', 'v')
    time.sleep(0.1)
    _mouseclick('object/send.png')
    time.sleep(0.5)
    return None


def generate_img(text_client, img_client, user_description=None):
    if user_description is None:
        result1 = text_client.predict(
            query="say a joke",
            history=[],
            system="You are a comedian.",
            api_name="/model_chat"
        )
        description = result1[1][-1][-1]
    else:
        description = user_description
    result2 = img_client.predict(
        num_images=1,
        height=1024,
        width=1024,
        prompt=description,
        seed=random.randint(1000, 4000),
        api_name="/process_image"
    )
    img_path = result2[0]['image']
    return description, img_path


def get_history_save_path(bath_path='history'):
    save_time = datetime.datetime.now().strftime("%Y%m%d%H%M")
    save_path = os.path.join(bath_path, save_time + '.pkl')
    return save_path


def save_history(history, start_history, save_path):
    his_len = len(history)
    if his_len != len(start_history):
        print('fail to save')
    else:
        end_history = []
        for i in range(his_len):
            small_list = start_history[i]
            big_list = history[i]
            temp_small_list = small_list[:]

            new_list = []
            for item in big_list:
                if item in temp_small_list:
                    temp_small_list.remove(item)
                else:
                    new_list.append(item)
            end_history.append(new_list)
        with open(save_path, 'wb') as f:
            pickle.dump(end_history, f)
        print('history saved')
    return None


def roll_dice(odd=0.2):
    return random.random() <= odd


def creat_remain_list(friend_list):
    remain = []
    len_friend_list = len(friend_list)
    for i in range(len_friend_list):
        remain.append(['', []])
    return remain


def get_remain_msg(large_avatar, her_avatar, my_avatar, msg_count, wait=3):
    if msg_count > 0:
        remain_query, remain_img_list = check_msg(large_avatar, her_avatar, my_avatar, wait, msg_count)
    else:
        remain_query, remain_img_list = '', []
    return remain_query, remain_img_list


def encode_image(image_list):
    base64_img_list = []
    for image_path in image_list:
        with open(image_path, "rb") as image_file:
            base64_img_list.append(base64.b64encode(image_file.read()).decode('utf-8'))
    return base64_img_list


def start_chat(content=None):
    if content is not None:
        return content
    now = datetime.datetime.now()
    current_hour = now.hour
    if 4 < current_hour < 10:
        return "早上好"
    elif current_hour < 14:
        return "中午好"
    elif current_hour < 18:
        return "下午好"
    elif current_hour < 24:
        return "晚上好"
    else:
        return "睡了吗"


def process_msg_openai(prompt, history, query, img_list):
    messages = []
    messages.append({"role": "system", "content": prompt})
    for pair in history:
        messages.append({"role": "user", "content": pair[0]})
        messages.append({"role": "assistant", "content": pair[0]})
    if query != '' and not img_list:
        messages.append({"role": "user", "content": query})
        full_query = query
    else:
        if query != '':
            content = [{"type": "text", "text": query}]
            full_query = query + '[图片]'
        else:
            content = [{"type": "text", "text": '说说你看到这张图片的感受'}]
            full_query = '[图片]'
        bs64_list = encode_image(img_list)
        for url in bs64_list:
            content.append({"type": "image_url", "image_url": {"url": f"data:image/jpeg;base64,{url}"}})
        messages.append({"role": "user", "content": content})

    return messages, full_query


def generate_answer_openai(messages, client, model):
    completion = client.chat.completions.create(model=model, messages=messages)
    answer = completion.choices[0].message.content
    return answer


def generate_img_openai(text, client, model, opp):
    if roll_dice(opp):
        response = client.images.generate(
            model=model,
            prompt=text,
            size="1024x1024",
            quality="standard",
            n=1,
        )
        image_url = response.data[0].url
        return image_url
    else:
        return ''


def get_img_prompt(answer):
    answer_list = re.split(r'[，。!？]', answer)
    return answer_list[-2]
