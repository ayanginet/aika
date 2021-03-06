# -*- coding: utf-8 -*- 
import pandas as pd
import datetime
import urllib.request
import urllib.parse
import json
from googletrans import Translator
from nltk.stem.snowball import RussianStemmer
import re
from cachetools import cached, TTLCache
import calendar
from nltk.corpus import stopwords
from emoji import emojize

stemmer = RussianStemmer()
cache = TTLCache(maxsize=500, ttl=1800)

Earth = emojize(":earth_asia:", use_aliases=True)
Drops = emojize(":sweat_drops:", use_aliases=True)
Fog = emojize(":fog:", use_aliases=True)
Thermometer = emojize(":thermometer:", use_aliases=True)
Clock = emojize(":clock12:", use_aliases=True)

class color:
   PURPLE = "\033[95m"
   CYAN = "\033[96m"
   DARKCYAN = "\033[36m"
   BLUE = "\033[94m"
   GREEN = "\033[92m"
   YELLOW = "\033[93m"
   RED = "\033[91m"
   BOLD = "\033[1m"
   UNDERLINE = "\033[4m"
   END = "\033[0m"


def get_date(time):
    date = time.split()[0]
    months = {'1':'января', '2':'февраля', '3':'марта', '4':'апреля', '5':'мая', '6':'июня', '7':'июля', '8':'августа', '9':'сентября', '10':'октября', '11':'ноября', '12':'декабря'}

    return date.split('-')[2] + ' ' + months[str(date.split('-')[1])]

def get_current_date(time):
    converted_time = datetime.datetime.fromtimestamp(
        int(time)
    ).strftime('%Y-%-m-%-d')

    return converted_time

def forecast_current_date(time):
    hour = get_time_hour(time)
    new_time = time
    if(hour < 6):
        new_time = time - datetime.timedelta(1)
    converted_time = datetime.datetime.fromtimestamp(
        int(new_time)
    ).strftime('%Y-%-m-%-d')

    return converted_time



def get_time_hour(time):
    converted_time = datetime.datetime.fromtimestamp(
        int(time)
    ).strftime('%-H')

    return int(converted_time)

def getEmoji(weather_id):
    # Openweathermap Weather codes and corressponding emojis
    thunderstorm = u'\U0001F4A8'  # Code: 200's, 900, 901, 902, 905
    drizzle = u'\U0001F4A7'  # Code: 300's
    rain = u'\U00002614'  # Code: 500's
    snowflake = u'\U00002744'  # Code: 600's snowflake
    snowman = u'\U000026C4'  # Code: 600's snowman, 903, 906
    atmosphere = u'\U0001F301'  # Code: 700's foogy
    clear_sky = u'\U00002600'  # Code: 800 clear sky
    few_clouds = u'\U000026C5'  # Code: 801 sun behind clouds
    clouds = u'\U00002601'  # Code: 802-803-804 clouds general
    hot = u'\U0001F525'  # Code: 904
    default_emoji = u'\U0001F300'

    if weather_id:
        if str(weather_id)[0] == '2' or weather_id in (900, 901, 902, 905):
            return thunderstorm
        elif str(weather_id)[0] == '3':
            return drizzle
        elif str(weather_id)[0] == '5':
            return rain
        elif str(weather_id)[0] == '6' or weather_id in (903, 906):
            return snowflake + ' ' + snowman
        elif str(weather_id)[0] == '7':
            return atmosphere
        elif weather_id == 800:
            return clear_sky
        elif weather_id == 801:
            return few_clouds
        elif weather_id == 802 or weather_id == 803 or weather_id == 804:
            return clouds
        elif weather_id == 904:
            return hot
        else:
            return default_emoji

    else:
        return default_emoji

def url_builder_geocoding(city):
    user_api = 'AIzaSyB43dwBw0qIRcKVoMvCYuCh4bHEZjS0bG0'
    full_api_url = 'https://maps.googleapis.com/maps/api/geocode/json?&address=' + urllib.parse.quote_plus(city) +'&components=administrative_area:1&key=' + user_api
    return full_api_url

def url_builder(city_name, state):
    user_api = '89f22ce44fe09b07e925aa6420546626'
    unit = 'metric'
    api = 'http://api.openweathermap.org/data/2.5/' + state + '?q='
    full_api_url = api + city_name + '&mode=json&units=' + unit +'&lang=ru&APPID=' + user_api
    return full_api_url

@cached(cache)
def data_fetch(full_api_url):
    url = urllib.request.urlopen(full_api_url)
    output = url.read().decode('utf-8')
    raw_api_dict = json.loads(output)
    url.close()
    return raw_api_dict

def data_organizer_forecast(raw_api_dict):
    s = 0
    for i in range(len(raw_api_dict.get('list'))):
        s = i
        h = get_time_hour(raw_api_dict['list'][i].get('dt'))
        if(h == 6):
            break
    data = dict(
        city = raw_api_dict.get('city').get('name'),
        country = raw_api_dict.get('city').get('country'),
        day_1 = dict(
            night_temp = raw_api_dict.get('list')[s].get('main').get('temp'),
            morning_temp = raw_api_dict.get('list')[s+3].get('main').get('temp'),
            afternoon_temp = raw_api_dict.get('list')[s+4].get('main').get('temp'),
            evening_temp = raw_api_dict.get('list')[s+6].get('main').get('temp'),
            night_weather = raw_api_dict.get('list')[s].get('weather'),
            morning_weather = raw_api_dict.get('list')[s+3].get('weather'),
            afternoon_weather = raw_api_dict.get('list')[s+4].get('weather'),
            evening_weather = raw_api_dict.get('list')[s+6].get('weather'),
            night_windspeed = raw_api_dict.get('list')[s].get('wind').get('speed'),
            morning_windspeed = raw_api_dict.get('list')[s+3].get('wind').get('speed'),
            afternoon_windspeed = raw_api_dict.get('list')[s+4].get('wind').get('speed'),
            evening_windspeed = raw_api_dict.get('list')[s+6].get('wind').get('speed'),
            night_humidity = raw_api_dict.get('list')[s].get('main').get('humidity'),
            morning_humidity = raw_api_dict.get('list')[s+3].get('main').get('humidity'),
            afternoon_humidity = raw_api_dict.get('list')[s+4].get('main').get('humidity'),
            evening_humidity = raw_api_dict.get('list')[s+6].get('main').get('humidity'),
            date = get_date(forecast_current_date(raw_api_dict.get('list')[s].get('dt')))
            ),
        day_2 = dict(
            night_temp = raw_api_dict.get('list')[s+8].get('main').get('temp'),
            morning_temp = raw_api_dict.get('list')[s+11].get('main').get('temp'),
            afternoon_temp = raw_api_dict.get('list')[s+12].get('main').get('temp'),
            evening_temp = raw_api_dict.get('list')[s+14].get('main').get('temp'),
            night_weather = raw_api_dict.get('list')[s+8].get('weather'),
            morning_weather = raw_api_dict.get('list')[s+11].get('weather'),
            afternoon_weather = raw_api_dict.get('list')[s+12].get('weather'),
            evening_weather = raw_api_dict.get('list')[s+14].get('weather'),
            night_windspeed = raw_api_dict.get('list')[s+8].get('wind').get('speed'),
            morning_windspeed = raw_api_dict.get('list')[s+11].get('wind').get('speed'),
            afternoon_windspeed = raw_api_dict.get('list')[s+12].get('wind').get('speed'),
            evening_windspeed = raw_api_dict.get('list')[s+14].get('wind').get('speed'),
            night_humidity = raw_api_dict.get('list')[s+8].get('main').get('humidity'),
            morning_humidity = raw_api_dict.get('list')[s+11].get('main').get('humidity'),
            afternoon_humidity = raw_api_dict.get('list')[s+12].get('main').get('humidity'),
            evening_humidity = raw_api_dict.get('list')[s+14].get('main').get('humidity'),
            date = get_date(forecast_current_date(raw_api_dict.get('list')[s+8].get('dt')))
            ),
        day_3 = dict(
            night_temp = raw_api_dict.get('list')[s+16].get('main').get('temp'),
            morning_temp = raw_api_dict.get('list')[s+19].get('main').get('temp'),
            afternoon_temp = raw_api_dict.get('list')[s+20].get('main').get('temp'),
            evening_temp = raw_api_dict.get('list')[s+22].get('main').get('temp'),
            night_weather = raw_api_dict.get('list')[s+16].get('weather'),
            morning_weather = raw_api_dict.get('list')[s+19].get('weather'),
            afternoon_weather = raw_api_dict.get('list')[s+20].get('weather'),
            evening_weather = raw_api_dict.get('list')[s+22].get('weather'),
            night_windspeed = raw_api_dict.get('list')[s+16].get('wind').get('speed'),
            morning_windspeed = raw_api_dict.get('list')[s+19].get('wind').get('speed'),
            afternoon_windspeed = raw_api_dict.get('list')[s+20].get('wind').get('speed'),
            evening_windspeed = raw_api_dict.get('list')[s+22].get('wind').get('speed'),
            night_humidity = raw_api_dict.get('list')[s+16].get('main').get('humidity'),
            morning_humidity = raw_api_dict.get('list')[s+19].get('main').get('humidity'),
            afternoon_humidity = raw_api_dict.get('list')[s+20].get('main').get('humidity'),
            evening_humidity = raw_api_dict.get('list')[s+22].get('main').get('humidity'),
            date = get_date(forecast_current_date(raw_api_dict.get('list')[s+16].get('dt')))
            ),
        day_4 = dict(
            night_temp = raw_api_dict.get('list')[s+24].get('main').get('temp'),
            morning_temp = raw_api_dict.get('list')[s+27].get('main').get('temp'),
            afternoon_temp = raw_api_dict.get('list')[s+28].get('main').get('temp'),
            evening_temp = raw_api_dict.get('list')[s+30].get('main').get('temp'),
            night_weather = raw_api_dict.get('list')[s+24].get('weather'),
            morning_weather = raw_api_dict.get('list')[s+27].get('weather'),
            afternoon_weather = raw_api_dict.get('list')[s+28].get('weather'),
            evening_weather = raw_api_dict.get('list')[s+30].get('weather'),
            night_windspeed = raw_api_dict.get('list')[s+24].get('wind').get('speed'),
            morning_windspeed = raw_api_dict.get('list')[s+27].get('wind').get('speed'),
            afternoon_windspeed = raw_api_dict.get('list')[s+28].get('wind').get('speed'),
            evening_windspeed = raw_api_dict.get('list')[s+30].get('wind').get('speed'),
            night_humidity = raw_api_dict.get('list')[s+24].get('main').get('humidity'),
            morning_humidity = raw_api_dict.get('list')[s+27].get('main').get('humidity'),
            afternoon_humidity = raw_api_dict.get('list')[s+28].get('main').get('humidity'),
            evening_humidity = raw_api_dict.get('list')[s+30].get('main').get('humidity'),
            date = get_date(forecast_current_date(raw_api_dict.get('list')[s+24].get('dt')))
            )
        )
    return data

def data_organizer_current(raw_api_dict):
    data = dict(
        city=raw_api_dict.get('name'),
        country=raw_api_dict.get('sys').get('country'),
        temp=raw_api_dict.get('main').get('temp'),
        humidity=raw_api_dict.get('main').get('humidity'),
        weather=raw_api_dict['weather'],
        wind=raw_api_dict.get('wind').get('speed'),
        date = get_date(get_current_date(raw_api_dict.get('dt')))
    )
    return data

def replace_dates(command):
    dates = {
        'первое' : 1,
        'второе' : 2,
        'третье' : 3,
        'четвертое' : 4,
        'пятое' : 5,
        'шестое' : 6,
        'седьмое' : 7,
        'восьмое' : 8,
        'девятое' : 9,
        'десятое' : 10,
        'одиннадцатое' : 11,
        'двеннадцатое' : 12,
        'тринадцатое' : 13,
        'четырнадцатое' : 14,
        'пятнадцатое' : 15,
        'шестнадцатое' : 16,
        'семнадцатое' : 17,
        'восемнадцатое' : 18,
        'девятнадцатое' : 19,
        'двадцатое' : 20,
        'двадцать первое' : 21,
        'двадцать второе' : 22,
        'двадцать третье' : 23,
        'двадцать четвертое' : 24,
        'двадцать пятое' : 25,
        'двадцать шестое' : 26,
        'двадцать седьмое' : 27,
        'двадцать восьмое' : 28,
        'двадцать девятое' : 29,
        'тридцатое' : 30,
        'тридцать первое' : 31
        }

    word_list = command.split()
    word_list = [stemmer.stem(a).lower() for a in word_list]
    for i in dates:
        if(stemmer.stem(i) in word_list):
            command = re.sub(i, str(dates[i]), command)

    return command

def extract_feature_list(command):
    features = []
    feature_list = ['погода','температура','влажность','скорость','ветер']
    command = re.sub(r'[^\w\s]', ' ', command)
    word_list = command.split()
    word_list = [stemmer.stem(a).lower() for a in word_list]
    for i in feature_list:
        if stemmer.stem(i) in word_list:
            features.append(i)

    return features

def extract_city(command):
    fname = 'regex.txt'
    out = []
    city = ''
    with open(fname, encoding='cp1251') as f:
        regex = f.readlines()
    regex = [line.rstrip('\n') for line in regex]
    match_list = []
    for i in regex:
        result = re.findall(i, command)
        if(result):
            match_list.append(result[0])
    match_list = [word for word in match_list if word.strip() not in stopwords.words('russian')]
    for i in match_list:
        data = data_fetch(url_builder_geocoding(i))
        if(data.get('status') != 'ZERO_RESULTS'):
            out.append(data.get('results')[0].get('address_components')[0].get('long_name'))
    if(out):
        if(out[0].isdigit()):
            try:
                if(out[1].isdigit()):
                    try:
                        if(out[2].isdigit()):
                            try:
                                city = out[3]
                            except:
                                pass
                        else:
                            city = out[2]
                    except:
                        pass
                else:
                    city = out[1]
            except:
                pass
        else:
            city = out[0]

    return city

def extract_date_and_time(command):
    time_of_the_day = ''
    days_ahead = ''
    command = re.sub(r'[^\w\s]', ' ', command)
    word_list = command.split()
    word_list = [stemmer.stem(a).lower() for a in word_list]
    day_of_the_week = dict(
        понедельник = 0,
        вторник = 1,
        среда = 2,
        четверг = 3,
        пятница = 4,
        суббота = 5,
        воскресенье = 6
        )
    nearest_days = dict(
        сегодня = 0,
        завтра = 1,
        послезавтра = 2
        )
    daytime = dict(
        днем = 2,
        дня = 2,
        полдень = 2,
        полночь = 0,
        ночь = 0,
        ночью = 0,
        утро = 1,
        обед = 2,
        вечер = 3
        )

    date_words_before = ['на','за']
    date_words_after = ['число']
    for word in date_words_before:
        try:
            if(stemmer.stem(word).lower() in word_list):
                current_day = datetime.date.today().timetuple().tm_mday
                forecast_day = int(word_list[word_list.index(stemmer.stem(word).lower()) + 1])
                if(forecast_day > current_day):
                    days_ahead = forecast_day - current_day
                else:
                    number_of_days = int(calendar.monthrange(datetime.datetime.now().year, datetime.datetime.now().month)[1])
                    days_ahead = (number_of_days - current_day) + forecast_day
        except:
            pass

    for word in date_words_after:
        try:
            if(stemmer.stem(word).lower() in word_list):
                current_day = datetime.date.today().timetuple().tm_mday
                forecast_day = int(word_list[word_list.index(stemmer.stem(word).lower()) - 1])
                if(forecast_day > current_day):
                    days_ahead = forecast_day - current_day
                else:
                    number_of_days = int(calendar.monthrange(datetime.datetime.now().year, datetime.datetime.now().month)[1])
                    days_ahead = (number_of_days - current_day) + forecast_day
        except:
            pass

    for weekday in day_of_the_week:
        if(stemmer.stem(weekday).lower() in word_list):
            current_day_of_the_week = datetime.datetime.today().weekday()
            difference = day_of_the_week[weekday] - current_day_of_the_week
            if(difference >= 0):
                days_ahead = difference
            else:
                days_ahead = 7 + difference

    for nearday in nearest_days:
        if(stemmer.stem(nearday).lower() in word_list):
            days_ahead = nearest_days[nearday]

    for day_hour in daytime:
        if(stemmer.stem(day_hour) in word_list):
            time_of_the_day = daytime[day_hour]

    return_array = [str(days_ahead), str(time_of_the_day)]

    return return_array

def get_weather(command):
    command = replace_dates(command)
    output = ''
    speech = ''
    days_ahead = '1'
    time_of_the_day = '2'
    m_symbol = '\xb0' + 'C'
    translator = Translator()
    feature_list = extract_feature_list(command)
    city = extract_city(command)
    date_and_time_array = extract_date_and_time(command)
    try:
        if((not date_and_time_array[0]) and (not date_and_time_array[1])):
            data = data_organizer_current(data_fetch(url_builder(city, 'weather')))
            if('погода' in feature_list or not feature_list):
                output = output + ":::: " + Clock + " " + data['date'] + "::::\n\n"
                output = output + Earth + '{}, {} \n'.format(data['city'], data['country'])
                output = output + Thermometer + str(data['temp']) + m_symbol + ' ' + getEmoji(data['weather'][0]['id']) + data['weather'][0]['description'] + '\n'
                output = output + Drops + 'Влажность воздуха: {} %\n'.format(data['humidity'])
                output = output + Fog + 'Скорость ветра: {} м/сек\n'.format(data['wind'])
                speech = 'В городе {} {}, {} градусов по цельсию'.format(city, data['weather'][0]['description'], str(int(data['temp'])))
                return output, speech
            elif('температура' in feature_list):
                output = output + Thermometer + 'Температура воздуха на {}: {}'.format(data['date'], data['temp']) + m_symbol
                speech = 'Температура воздуха в городе {} {} градусов по цельсию'.format(city, int(data['temp']))
                return output, speech
            elif('влажность' in feature_list):
                output = output + Drops +'Влажность воздуха на {}: {} %'.format(data['date'], data['humidity'])
                speech = 'Влажность воздуха в городе {} {} процентов'.format(city, int(data['humidity']))
                return output, speech
            elif('скорость' in feature_list or 'ветер' in feature_list):
                output = output + Fog + 'Скорость ветра на {}: {} м/сек'.format(data['date'], data['wind'])
                speech = 'Скорость ветра в городе {} {} метров в секунду'.format(city, data['wind'])
                return output, speech
        else:
            data = data_organizer_forecast(data_fetch(url_builder(city, 'forecast')))
            if date_and_time_array[0]:
                if(date_and_time_array[0] != '0'):
                    days_ahead = date_and_time_array[0]
                if(int(days_ahead) > 4):
                    return 'У нас имеется прогноз погоды на ближайшие четыре дня', 'У нас имеется прогноз погоды на ближайшие четыре дня'
            if date_and_time_array[1]:
                time_of_the_day = date_and_time_array[1]
            day_dict = 'day_' + days_ahead
            time_of_the_day_array = ['night', 'morning', 'afternoon', 'evening']

            if('погода' in feature_list or not feature_list):
                output = output + ":::: " + Clock + " " + data[day_dict]['date'] + "::::\n\n"
                output = output + Earth + '{}:{}\n'.format(data['city'], data['country'])
                output = output + Thermometer + str(data[day_dict][time_of_the_day_array[int(time_of_the_day)] + '_temp']) + m_symbol + ' ' + getEmoji(data[day_dict][time_of_the_day_array[int(time_of_the_day)] + '_weather'][0]['id']) + data[day_dict][time_of_the_day_array[int(time_of_the_day)] + '_weather'][0]['description'] + '\n'
                output = output + Drops + 'Влажность воздуха: {} %\n'.format(data[day_dict][time_of_the_day_array[int(time_of_the_day)] + '_humidity'])
                output = output + Fog + 'Скорость ветра: {} м/сек'.format(data[day_dict][time_of_the_day_array[int(time_of_the_day)] + '_windspeed'])
                speech = 'В городе {} будет {}, {} градусов по цельсию'.format(city, data[day_dict][time_of_the_day_array[int(time_of_the_day)] + '_weather'][0]['description'], str(int(data[day_dict][time_of_the_day_array[int(time_of_the_day)] + '_temp'])))
                return output, speech
            elif('температура' in feature_list):
                output = output + Thermometer + 'Температура воздуха на {}: {}'.format(data[day_dict]['date'], data[day_dict][time_of_the_day_array[int(time_of_the_day)] + '_temp']) + m_symbol
                speech = 'Температура воздуха в городе {} будет {} градусов по цельсию'.format(city, str(int(data[day_dict][time_of_the_day_array[int(time_of_the_day)] + '_temp'])))
                return output, speech
            elif('влажность' in feature_list):
                output = output + Drops + 'Влажность воздуха на {} : {} %'.format(data[day_dict]['date'], data[day_dict][time_of_the_day_array[int(time_of_the_day)] + '_humidity'])
                speech = 'Влажность водуха в городе {} будет {} процентов'.format(city, int(data[day_dict][time_of_the_day_array[int(time_of_the_day)] + '_humidity']))
                return output, speech
            elif('скорость' in feature_list or 'ветер' in feature_list):
                output = output + Fog + 'Скорость ветра на {} : {} м/сек'.format(data[day_dict]['date'], data[day_dict][time_of_the_day_array[int(time_of_the_day)] + '_windspeed'])
                speech = 'Скорость ветра в городе {} будет {} метров в секунду'.format(city, data[day_dict][time_of_the_day_array[int(time_of_the_day)] + '_windspeed'])
                return output, speech
    except:
        return 'Я не нашла название города. Повторите запрос с именем города', 'Я не нашла название города. Повторите запрос с именем города'
