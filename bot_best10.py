import requests
from time import sleep

import vk_api
import random


def vk_message(id, text):
    vk.method("messages.send", {"peer_id": id, "message": text, "random_id": random.randint(1, 1000000)})


def thousand_posts():
    '''
    В данном примере будет отфильтровано 1000 постов с официальной группы РБК 
    фильтрация: по количеству лайков под записью
    '''
    token = 'ваш access_token'
    version = 5.103
    domain = 'rbc' # 'rbc'
    count = 100 # count = 100
    offset = 0
    posts = []
    while offset < 1000: # while offset < 1000
        responce = requests.get('https://api.vk.com/method/wall.get',
                                params={
                                    'access_token': token,
                                    'v': version,
                                    'domain': domain,
                                    'count': count,
                                    'offset': offset
                                }
                                )
        data = responce.json()['response']['items']
        offset += 100 # offset += 100
        posts.extend(data)
        sleep(0.1)
    print("\n"*6 , " "*20, "Всё, я разогрелся. Выпускай зверя!!!!", "\n"*3)
    return posts


all_posts = thousand_posts()

max_likes = []
for post in all_posts:
    max_likes.append(post['likes']['count'])
max_likes.sort(reverse=True)
max_likes = max_likes[:10]

best_10 = []
last_likes = []
for post in all_posts:
    if post['likes']['count'] in max_likes:
        best_10.append(post)
        last_likes.append(post['likes']['count']) # неотсортированный список максимальных значений лайков
        if len(best_10) == 10:
            last_likes.sort(reverse=True)
            break

best_10_sorted = []
for num in last_likes:
    for post in best_10:
        if post['likes']['count'] == num and post not in best_10_sorted:
            best_10_sorted.append(post)
            continue


group_token = "70acd0892653a9e24a9c6c6349d2f0f069818127014e834898e3ac8a1099c1044837bf04f76d06d4fce17"
vk = vk_api.VkApi(token=group_token)
vk._auth_token()

while True:
    mas = vk.method("messages.getConversations", {"offset": 0, "count": 20, "filter": "unanswered"})
    if mas["count"] >= 1:
        id = mas["items"][0]["last_message"]["from_id"]
        body = mas["items"][0]["last_message"]["text"]
        vk_message(id, "Посмотрел, значит, я последние 1000 постов. \n И вот, пожалуйста, топ 10 записей группы к вашему вниманию:")
        sleep(4)        
        for post in best_10_sorted:
            vk_message(id, "Запись " + 'https://vk.com/wall' + str(post['from_id']) + '_' + str(post['id']) + " набрала " + str(post['likes']['count']))
        sleep(3)
        vk_message(id, "...")
        sleep(6)
        vk_message(id, "Спасибо мне, верно?")