import requests
from config import ACCESS_TOKEN as token
from config import VERSION as version
from config import FIELDS_FRIENDS as fields_f
from datetime import date, datetime


def retrieval_data(version, token, user_ids):
    response = requests.get('https://api.vk.com/method/users.get',
                            params={
                                'v': version,
                                'access_token': token,
                                'user_ids': user_ids
                            }
                            )
    return response.json()['response'][0]['id']


def calc_age(version, token, uid, fields_f):
    response = requests.get('https://api.vk.com/method/friends.get',
                            params={
                                'v': version,
                                'access_token': token,
                                'user_id': uid,
                                'fields': fields_f
                            }
                            )
    items = response.json()['response']['items']
    year_now = date.today().year
    calc_dict = {}
    calc_list = list()
    for dict_it in items:
        if ('bdate' in dict_it) and (len(dict_it['bdate']) > 6):
            # Не во всех аккаунтах указан возраст -> в ответе может не быть этого ключа, выдаст исключение
            # Не у всех указан год рождения -> в ответе может быть неподходящий формат, проверяем по длине записи
            year = datetime.strptime(dict_it['bdate'], '%d.%m.%Y').year
            calc = str(year_now - year)
            if calc in calc_dict:
                calc_dict[calc] += 1
            else:
                calc_dict[calc] = 1
    for key in calc_dict:
        temp = (key, calc_dict[key])
        calc_list.append(temp)
    return sorted(calc_list, key=lambda x: (-x[1], int(x[0])))   # сортировка, сначала по 1му потом по 2му


if __name__ == '__main__':
    user_ids = 'default_derevnya'
    data = retrieval_data(version, token, user_ids)
    res = calc_age(version, token, data, fields_f)
    print(date.today().year)
    print(retrieval_data(version, token, user_ids))
    print(res)
