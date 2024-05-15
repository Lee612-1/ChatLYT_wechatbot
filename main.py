import json
import argparse
from gradio_client import Client
from utils import *


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('--people', type=str, help='path of json')
    parser.add_argument('--person', type=str, default='object/xingdaiyan', help='path of friend dir')
    parser.add_argument('--authentic', type=int, choices=[0, 1, 2], default=2, help='more real')
    args = parser.parse_args()

    # load parameters
    if args.people is None:
        FRIENDS = [args.person]
    else:
        with open('object/people.json', 'r') as file:
            friend_dir = json.load(file)
        FRIENDS = [friend['dir'] for friend in friend_dir]

    MY_AVATAR = 'object/myavatar.png'
    text_client = Client("Qwen/Qwen1.5-110B-Chat-demo")
    img2text_client = Client("openbmb/MiniCPM-V-2")
    text2img_client = Client("ByteDance/Hyper-SDXL-1Step-T2I")
    history_list = process_history(FRIENDS, MY_AVATAR)
    start_history_list = history_list[:]
    history_save_path = get_history_save_path()
    remain_msg_list = creat_remain_list(FRIENDS)
    add_prompt = ''
    start_chat = '哈哈哈，这张图真搞笑！'
    start = False
    attempt = 0

    # loop
    while True:
        # update time and weather in prompt every 3000 attempts
        if attempt % 3000 == 0:
            add_prompt = enhance_prompt()
        for i in range(len(FRIENDS)):
            HER_AVATAR = f'{FRIENDS[i]}/avatar.png'
            LARGE_AVATAR = f'{FRIENDS[i]}/large_avatar.png'

            # set the system prompt
            with open(f'{FRIENDS[i]}/role.txt', 'r', encoding='utf-8') as file:
                SYSTEM_PROMPT = file.read()
            SYSTEM_PROMPT = SYSTEM_PROMPT + add_prompt

            # get history chat and new message
            history = history_list[i]
            remain_query, remain_img_list = remain_msg_list[i][0], remain_msg_list[i][1]
            query, img_list = check_msg(LARGE_AVATAR, HER_AVATAR, MY_AVATAR)
            query = remain_query + query
            img_list = remain_img_list + img_list
            msg_count = count_msg(HER_AVATAR, MY_AVATAR)

            if query != '':
                if 'exit' in query.lower():
                    break

                # process image to text and text to image
                img_path = ''
                text2img = False
                if img_list:
                    img_query = process_img_query(img_list, img2text_client)
                    if img_query is not None:
                        query += img_query
                else:
                    if roll_dice(0.01):
                        _, img_path = generate_img(text_client, text2img_client, query)
                        text2img = True

                # generate answers
                # print(query, history, SYSTEM_PROMPT)
                answer, history = generate_answer(query, history, SYSTEM_PROMPT, text_client)
                msg_count = count_msg(HER_AVATAR, MY_AVATAR) - msg_count
                remain_query, remain_img_list = get_remain_msg(LARGE_AVATAR, HER_AVATAR, MY_AVATAR, msg_count)

                # process the answer and send the message
                answer_list = process_answer(answer, args.authentic)
                if text2img:
                    send_img(img_path, LARGE_AVATAR)
                ids = reply(LARGE_AVATAR, HER_AVATAR, MY_AVATAR, answer_list)

                # update the history
                if ids is not None:
                    answer_list = answer_list[:ids+1]
                history[-1][-1] = '。'.join(answer_list)
                history_list[i] = history
                remain_msg_list[i][0], remain_msg_list[i][1] = remain_query, remain_img_list
                start = True

            # actively start the chat
            elif start_chat not in history[-1][-1] and not start:
                answer_list = [start_chat]
                description, img_path = generate_img(text_client, text2img_client)
                msg_count = count_msg(HER_AVATAR, MY_AVATAR) - msg_count
                remain_query, remain_img_list = get_remain_msg(LARGE_AVATAR, HER_AVATAR, MY_AVATAR, msg_count)
                send_img(img_path, LARGE_AVATAR)
                reply(LARGE_AVATAR, HER_AVATAR, MY_AVATAR, answer_list)
                history[-1][-1] += ',' + start_chat + f'[图片](描述{description})'
                history_list[i] = history
                start = True

            else:
                print('no new message')

        attempt += 1
        if attempt % 5 == 0:
            save_history(history_list, start_history_list, history_save_path)
        if attempt >= 30000:
            break

