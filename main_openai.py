import json
import argparse
from openai import OpenAI
from utils import *
import os


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
        with open(args.people, 'r', encoding='utf-8') as file:
            friend_dir = json.load(file)
        FRIENDS = [friend['dir'] for friend in friend_dir]

    for file in os.listdir('object'):
        if file.startswith('myavatar'):
            MY_AVATAR = os.path.join('object', file)
            break
        else:
            MY_AVATAR = ''

    with open('temp/key.txt', 'r') as file:
        api_key = file.read()
    client = OpenAI(
        # defaults to os.environ.get("OPENAI_API_KEY")
        api_key=api_key,
        base_url="https://api.chatanywhere.tech/v1"
    )
    print('connected to openai')
    text_model = 'gpt-4o'
    img_model = 'dall-e-3'
    history_list = process_history(FRIENDS, MY_AVATAR)
    start_history_list = history_list[:]
    history_save_path = get_history_save_path()
    remain_msg_list = creat_remain_list(FRIENDS)
    add_prompt = ''
    start_chat = start_chat(content=None)
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
            if query != '' or img_list:
                msg_count = count_msg(HER_AVATAR, MY_AVATAR)
            else:
                msg_count = 0
            query = remain_query + query
            img_list = remain_img_list + img_list

            if query != '' or img_list:
                if query != '' and 'exit' in query.lower():
                    break
                messages, full_query = process_msg_openai(SYSTEM_PROMPT, history[-10:], query, img_list)

                # generate answers
                answer = generate_answer_openai(messages, client, text_model)
                history.append([full_query, answer])
                # 5% probability of generating images
                img_path = generate_img_openai(get_img_prompt(answer), client, img_model, opp=0.05)
                msg_count = count_msg(HER_AVATAR, MY_AVATAR) - msg_count
                remain_query, remain_img_list = get_remain_msg(LARGE_AVATAR, HER_AVATAR, MY_AVATAR, msg_count)

                # process the answer and send the message
                answer_list = process_answer(answer, args.authentic)
                if img_path != '':
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
            elif history and start_chat not in history[-1][-1] and not start:
                answer_list = [start_chat]
                reply(LARGE_AVATAR, HER_AVATAR, MY_AVATAR, answer_list)
                history[-1][-1] += ',' + start_chat
                history_list[i] = history
                start = True

            else:
                print('no new message')

        attempt += 1
        if attempt % 5 == 0:
            save_history(history_list, start_history_list, history_save_path)
        if attempt >= 30000:
            break