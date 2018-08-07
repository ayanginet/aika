from weather_predict import *
import random
from classify import *
from translate import *
import telebot
from speech_to_text import *
import requests
from emoji import emojize
from telebot import types



token = '695195394:AAEsxvvCgKTClHNKL2ElIYbN_iBZYhHki-U'
answer_greetings = ["Привет!", "Здравствуй", "Приветствую!", "Здравствуйте"]
answer_greetings_mood = ["Привет. Пойдет. Как у тебя?", "Здравствуй. Хорошо. Как у тебя?", "Приветствую. Нормально. Как у тебя?", "Здарова. Неплохо. Как у тебя?", "Здравствуйте. Все отлично. Как у вас?"]
answer_mood = ["Замечательно, спасибо!!", "Хорошо. Как у тебя дела?", "Все нормально. Как у вас?", "Все отлично. Как у тебя?", "Пойдет. А у тебя?"]
answer_philosophy = ['42']
answer_action = ['Разговариваю с тобой', 'Существую', 'Тихо жду здесь пока у меня что-то спросят']
answer_status_good = ['Рада слышать', 'Круто', 'Отлично!', 'Я очень рада :)']
start_text = ('''Здравствуйте!
        Я виртуальный помощник Айка. С моей помощью вы можете получить прогноз погоды на ближайшие дни, найти для себя сеанс в кино а также я просто умею разговаривать подробней обо каждой функций вы можете узнать по запросу /help''')

help_text = ('''    Данный бот имеет следующий список команд;

    • Команда предназначена для того чтобы вы могли узнать сеансы на фильмы 
    • Команда Погода дает вам прогноз погоды на ближайшие дни для ее активаций вы можете прописать обычный текст, например "Покажи мне прогноз погоды на сегодня в Астане"
    • Команда Помощь покажет вам данный список если вы забудете
    • Команда Собеседник вызовет голосового помощника, с которым вы сможете вести обычный диалог с помощью чата либо с помощью голосовых сообщений''')

command = '1'
bot = telebot.TeleBot(token)
KEYBOARD = {
    'CINEMA': ':movie camera: Кино',
    'WEATHER': ':earth_asia: Погода',
    'HELP': ':book: Помощь',
    'COMPANION': ':speech_balloon: Собеседник '
}

markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
markup.row(KEYBOARD['CINEMA'], KEYBOARD['WEATHER'])
markup.row(KEYBOARD['HELP'], KEYBOARD['COMPANION'])


print("Программа запущена")

@bot.message_handler(commands=['start'])
def info(message):
    bot.send_message(message.chat.id, start_text, reply_markup = markup)

@bot.message_handler(commands=['help'])
def help(message):
    bot.send_message(message.chat.id, help_text, reply_markup = markup)


def get_voice(message):
    speech_url = 'https://tts.voicetech.yandex.net/generate?text={}&format=mp3&quality=lo&lang=ru-RU&speaker=oksana&emotion=good&key=c3667808-f5a2-4c52-8f90-699a3e23e4f2'.format(message)
    doc = requests.get(speech_url)
    with open('audio.ogg', 'wb') as f:
        f.write(doc.content)
    voice = open('audio.ogg', 'rb')
    return voice

@bot.message_handler(content_types=["text","voice"])
def start_function(message):
    if message.text == KEYBOARD['HELP']:
        bot.send_message(message.chat.id, help_text)
    elif message.text == KEYBOARD['WEATHER']:
        def weather(message):
            if message.text:
                command = message.text
                try:
                    predicted_class = classify(command)
                    if(predicted_class == 'weather'):
                        output, speech = get_weather(command)
                        bot.send_message(message.chat.id, output)
                    else:
                        bot.send_message(message.chat.id, 'Извините, я вас не понимаю, но я учусь :3')
                except:
                    pass
            else:
                file_info = bot.get_file(message.voice.file_id)
                file = requests.get('https://api.telegram.org/file/bot{0}/{1}'.format(token, file_info.file_path))
                # try:
                command = speech_to_text(bytes=file.content)
                # except:
                    # bot.send_message(message.chat.id, 'Распознование голоса не удалось, попробуйте снова')
                try:    
                    predicted_class = classify(command)
                    if(predicted_class == 'weather'):
                        output, speech = get_weather(command)
                        voice = get_voice(speech)
                        bot.send_message(message.chat.id, output)
                        bot.send_voice(message.chat.id, voice)
                    else:
                        answer = 'Извините, я вас не понимаю, но я учусь :3'
                        voice = get_voice(answer)
                        # bot.send_message(message.chat.id, answer)
                        bot.send_voice(message.chat.id, voice)
                except:
                    pass
    elif message.text == KEYBOARD['COMPANION']:
        def handle_message(message):
            if message.text:
                command = message.text
                try:
                    predicted_class = classify(command)
                    if(predicted_class == 'greetings'):
                        bot.send_message(message.chat.id, answer_greetings[random.randint(0,(len(answer_greetings)-1))])
                    elif(predicted_class == 'greetings_mood'):
                        bot.send_message(message.chat.id, answer_greetings_mood[random.randint(0,(len(answer_greetings_mood)-1))])
                    elif(predicted_class == 'mood'):
                        bot.send_message(message.chat.id, answer_mood[random.randint(0,(len(answer_mood)-1))])
                    elif(predicted_class == 'philosophy'):
                        bot.send_message(message.chat.id, answer_philosophy[0]) 
                    elif(predicted_class == 'action'):
                        bot.send_message(message.chat.id, answer_action[random.randint(0,(len(answer_action)-1))])
                    elif(predicted_class == 'status_good'):
                        bot.send_message(message.chat.id, answer_status_good[random.randint(0,(len(answer_status_good)-1))])
                    # elif(predicted_class == 'translate'):
                    #         bot.send_message(message.chat.id, print(translate(command)))
                    else:
                        bot.send_message(message.chat.id, 'Извините, я вас не понимаю, но я учусь :3')
                except:
                    pass
            else:
                file_info = bot.get_file(message.voice.file_id)
                file = requests.get('https://api.telegram.org/file/bot{0}/{1}'.format(token, file_info.file_path))
                # try:
                command = speech_to_text(bytes=file.content)
                # except:
                    # bot.send_message(message.chat.id, 'Распознование голоса не удалось, попробуйте снова')
                try:    
                    predicted_class = classify(command)
                    if(predicted_class == 'greetings'):
                        answer = answer[random.randint(0,(len(answer)-1))]
                        voice = get_voice(answer)
                        # bot.send_message(message.chat.id, message)
                        bot.send_voice(message.chat.id, voice)
                    elif(predicted_class == 'greetings_mood'):
                        answer = answer_greetings_mood[random.randint(0,(len(answer_greetings_mood)-1))]
                        voice = get_voice(answer)
                        # bot.send_message(message.chat.id, answer)
                        bot.send_voice(message.chat.id, voice)
                    elif(predicted_class == 'mood'):
                        answer = answer_mood[random.randint(0,(len(answer_mood)-1))]
                        voice = get_voice(answer)
                        # bot.send_message(message.chat.id, answer)
                        bot.send_voice(message.chat.id, voice)
                    elif(predicted_class == 'philosophy'):
                        answer = answer_philosophy[0]
                        voice = get_voice(answer)
                        # bot.send_message(message.chat.id, answer)
                        bot.send_voice(message.chat.id, voice) 
                    elif(predicted_class == 'action'):
                        answer = answer_action[random.randint(0,(len(answer_action)-1))]
                        voice = get_voice(answer)
                        # bot.send_message(message.chat.id, answer)
                        bot.send_voice(message.chat.id, voice)
                    elif(predicted_class == 'status_good'):
                        answer = answer_status_good[random.randint(0,(len(answer_status_good)-1))]
                        voice = get_voice(answer)
                        # bot.send_message(message.chat.id, answer)
                        bot.send_voice(message.chat.id, voice)
                    # elif(predicted_class == 'translate'):
                    #         bot.send_message(message.chat.id, print(translate(command)))
                    else:
                        answer = 'Извините, я вас не понимаю, но я учусь :3'
                        voice = get_voice(answer)
                        # bot.send_message(message.chat.id, answer)
                        bot.send_voice(message.chat.id, voice)
                except:
                    pass


if __name__ == '__main__':
    bot.polling(none_stop=True)