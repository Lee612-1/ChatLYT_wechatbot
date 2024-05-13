import json
import argparse
from gradio_client import Client
from utils import *

if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('--people', type=str, help='path of json')
    parser.add_argument('--person', type=str, default='object/xuhang', help='path of friend dir')
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
    img_client = Client("openbmb/MiniCPM-V-2")
    history_list = process_history(FRIENDS, MY_AVATAR)
    add_prompt = enhance_prompt()
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
            query, img_list = check_msg(LARGE_AVATAR, HER_AVATAR, MY_AVATAR)

            if query is not None:
                if 'exit' in query.lower():
                    break

                # process the image to text
                if img_list:
                    img_query = process_img_query(img_list, img_client)
                    if img_query is not None:
                        query += img_query

                # generate answers
                answer, history = generate_answer(query, history, SYSTEM_PROMPT, text_client)

                # process the answer and send the message
                answer_list = process_answer(answer, args.authentic)
                ids = reply(LARGE_AVATAR, HER_AVATAR, MY_AVATAR, answer_list)

                # update the history
                if ids != 0:
                    if ids is not None:
                        answer_list = answer_list[:ids]
                    history[-1][-1] = '。'.join(answer_list)
                    history_list[i] = history
                else:
                    pass

            else:
                print('no new message')

        attempt += 1
        if attempt >= 30000:
            break
