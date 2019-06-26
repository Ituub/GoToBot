import schedule
import csv
import telebot
import random
from telebot import types
import time

# Обходим блокировку с помощью прокси
telebot.apihelper.proxy = {'https': 'socks5://dn2q2y:b3Xn9s@196.18.0.160:8000'}

token = "896976707:AAE08Boy2yXfPR5GjnKHlzA-8Vy0hYcLjKA"
bot = telebot.TeleBot(token=token)
users = {}
locations = ['Беседка 1', 'Беседка 2', 'Беседка 3']
used = []

filepath = r"D:\Sheets\test - Лист1 (1).csv"
arr1 = ['']
arr2 = ['']
arr3 = ['']
places = ["беседку у костра", "дальнюю беседку у костра", "беседку за прудом", "в охотничий домик", "веранду у столовой"]
pcopy = places

with open(filepath, "r", newline="", encoding='utf-8') as file:
    #читаем файл целиком
    reader = csv.reader(file)
    '''
    Циклом for проходим по строкам 
    '''
    for row in reader:
        cur_arr = row[0].split(';')
        cur_arr1 = row[1].split(';')
        cur_arr2 = row[2].split(';')
        '''
        В этом случае вы получите список значений
        '''
        arr1.extend(cur_arr)
        arr2.extend(cur_arr1)
        arr3.extend(cur_arr2)
    arr1.remove(arr1[0])
    arr2.remove(arr2[0])
    arr3.remove(arr3[0])
    copy = arr2

@bot.message_handler(content_types=['text'])
def echo(message):
    if message.text == "/start":
        instr = "Привет! Просто добавь меня в чат и я рассортирую людей для ЧАЙку."
        bot.send_message(message.chat.id, instr)
    if message.text == "/help":
        commands = "Список команд:\n" \
                   "/chaiku - рассортировать людей для ЧАЙку\n" \
                   "/help - список команд\n" \
                   "/remind - напомнить ваш ID "
        bot.send_message(message.chat.id, commands)
    if message.text == "/chaiku":
        chaiku(message)

@bot.message_handler(commands=['start'])
def repeat_all_messages(message):
    user_id = message.chat.id
    if user_id not in users:
        bot.send_message(user_id, "Вы мне еще не писали.")
    else:
        bot.send_message(message.chat.id, users[user_id])
    echo(message)

@bot.message_handler(content_types=['photo'])
def eyes(message):
    bot.send_message(message.chat.id, "Если бы были глаза, я бы оценил...")

def metrics(participant_A, participant_B):
    return abs(participant_A[1] - participant_B[1]) + (22 - abs(participant_A[2] - participant_B[2]))


@bot.message_handler(commands=['chaiku'])
def chaiku(message):
    x = 0
    y = 0
    if len(copy) <= 1:
        bot.send_message(message.chat.id, "Кажется, что всех уже распределили :с")
        return

    people = []
    pairs = []
    for i in range(1, len(arr2)):
        people.append((arr2[i], int(arr1[i]), int(arr3[i])))
    random.shuffle(people)
    while len(people) > 1:
        current = people[0]
        del people[0]
        variants = list(filter(lambda x:x[2]!=current[2], people))
        variants = sorted(variants, key=lambda x:abs(x[1] - current[1]))
        for i in variants:
            if (i, current) not in used and (current, i) not in used:
                partner = i
                break
        people.remove(partner)
        pairs.append((current, partner))
    random.shuffle(pairs)

    for i, j in pairs[:3]:
        used.append((i, j))

    pairs = list(map(lambda x:(x[0][0], x[1][0]), pairs))
    print(pairs)
    for i in range(3):
        bot.send_message(message.chat.id, "{}: {} vs {}".format(locations[i], *pairs[i]))


bot.polling(none_stop=True)




