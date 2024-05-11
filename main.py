import time
import gradio_client
from utils import get_msg, reply, get_img_query, describe_img

if __name__ == '__main__':
    MY_AVATAR = 'object/myavatar.png'
    OBJECT = 'yourfriend'
    HER_AVATAR = f'object/{OBJECT}/avatar.png'
    LARGE_AVATAR = f'object/{OBJECT}/large_avatar.png'
    with open(f'object/{OBJECT}/role.txt', 'r', encoding='utf-8') as file:
        SYSTEM_PROMPT = file.read()

    text_client = gradio_client.Client("Qwen/Qwen1.5-110B-Chat-demo")
    img_client = gradio_client.Client("openbmb/MiniCPM-V-2")
    result = ('',[])
    while True:
        query, img_list = get_msg(LARGE_AVATAR, HER_AVATAR, MY_AVATAR)
        if query is not None:
            if query.lower() == 'exit':
                break
            time.sleep(5)
            check_query, check_img_list = get_msg(LARGE_AVATAR, HER_AVATAR, MY_AVATAR)
            if check_query==query and check_img_list==img_list:
                if img_list != []:
                    img_query_list = []
                    for img in img_list:
                        try:
                            raw_query = describe_img(img, img_client)
                            img_query_list.append(raw_query)
                        except:
                            print('fail to answer the img')
                            img_list = []

                    img_query = get_img_query(img_query_list)
                    if img_query is not None:
                        query += img_query
                    else:
                        print('fail to describe the img')

                if query == '':
                    answer = '暂时不支持回复此类消息，我们聊点别的吧！'
                else:
                    try:
                        result = text_client.predict(
                            query=query,
                            history=result[1],
                            system=SYSTEM_PROMPT,
                            api_name="/model_chat"
                        )
                        answer = result[1][-1][-1]
                    except:
                        answer = '未响应，输入exit退出自动回复'
                reply(LARGE_AVATAR, answer)
            else:
                print('wait for more message')
                pass

        else:
            print('no new message')
            time.sleep(10)