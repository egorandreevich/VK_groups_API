import requests
from pprint import pprint
import json

class User: #Опишем юзера как класс
    def __init__(self, i):
        self.user_id_number = i
        self.friends_dic = self.get_friends()
        try:
            self.friends_list = self.friends_dic['response']['items']
        except KeyError:
            pass

    def groups_get(self):  # получил группы юзера
        params = {
            'access_token': self.my_token,
            'v': '5.92',
            'extended': 0,
            'user_id': self.user_id_number,
            'fields': ['members_count']
            # 'count': '500'
        }
        response = requests.get('https://api.vk.com/method/groups.get', params)
        return response.json()  # на выходе должен быть джсон, записанный в файл


    def get_friends(self):
        params = {
            'access_token': self.my_token,
            'v': '5.92',
            'user_id': self.user_id_number,
            'count' : '5' #пока ограничимся пятью, тормозит нереально
        }
        response = requests.get('https://api.vk.com/method/friends.get', params)
        return response.json()

    def info_about_group(self, group_id):
        params = {
            'access_token': self.my_token,
            'v': '5.92',
            'group_id': group_id,
            'fields' : 'members_count'
            'count': '5'  # пока ограничимся пятью, тормозит нереально
        }
        response = requests.get('https://api.vk.com/method/groups.getById', params)
        return response.json()

    def make_class_items(self):
        list_1 = self.friends_list
        list_2 = []
        # print(list_1)
        counter = 0
        for user in list_1:
            counter +=1
            print('Получаем айди друга номер {} и превращаем его в экземпляр класса'.format(counter))
            # print(user)
            user = User(user)
            list_2.append(user)
        return list_2

    def get_groups_of_friends(self): #функция для получения групп друзей
        response_list = []
        # process_dict = {}
        list_2 = self.make_class_items() #получаем список друзей по уже написанной функции
        counter = 0
        for friend in list_2: #итерируемся по списку друзей и для каждого вызываем функцию groups_get()
            counter +=1
            print('Проверяем друга номер {}'.format(counter))
            process_dict = friend.groups_get()
            try:
                response_list.extend(process_dict['response']['items'])
            except KeyError:
                pass
        return response_list

    def find_unique_groups(self):
        set_1 = set(self.groups_get()['response']['items'])
        set_2 = set(self.get_groups_of_friends())
        set_3 = set_1.difference(set_2)
        print('Уникальные группы у указанного юзера: {}'.format(set_3))
        return set_3

    def info_unique_groups(self):
        list_1 = list(self.find_unique_groups())
        # print(list_1)
        final_json_list = []
        counter = 0
        for group in list_1:
            counter += 1
            print('Обрабатываю группу номер {}'.format(counter))
            group_dict_resp = self.info_about_group(group)
            group_list_resp = group_dict_resp['response']
            # pprint(group_list_resp)
            for item in group_list_resp:
                final_json = {}
                for key, value in item.items():
                    if key == 'id':
                        final_json['gid'] = value
                    elif key == 'name':
                        final_json['name'] = value
                    elif key == 'members_count':
                        final_json['members_count'] = value
            final_json_list.append(final_json)
        # pprint(final_json_list)
        return final_json_list

    def save_to_file(self):
        final_json_list = self.info_unique_groups()
        with open ('groups.json', 'w') as f:
            f.write(json.dumps(final_json_list, ensure_ascii=False))
            print('Готово!\nЗаписал результат в groups.json')

    my_token = 'ed1271af9e8883f7a7c2cefbfddfcbc61563029666c487b2f71a5227cce0d1b533c4af4c5b888633c06ae'
    user_id_number = 0
    # user_name = 'eshmargunov'

def get_id(user):
    params = {
        'access_token': 'ed1271af9e8883f7a7c2cefbfddfcbc61563029666c487b2f71a5227cce0d1b533c4af4c5b888633c06ae',
        'v': '5.92',
        'user_ids': user,
        'fields': 'id'
    }
    response = requests.get('https://api.vk.com/method/users.get', params)
    for dictionary in response.json()['response']:
        for key, value in dictionary.items():
            if key == 'id':
                id = value
        return id



if __name__ == "__main__":
    user = get_id(input('Сейчас будем искать уникальные группы пользователя.\nНапишите короткую ссылку или айди страницы, которую будем исследовать:\n'))
    evgeniy = User(user)
# evgeniy = User(40635795)
# pprint(evgeniy.friends_list)
# pprint(evgeniy.groups_get())
# set_1 = set(evgeniy.groups_get()['response']['items'])
# set_2 = set(evgeniy.get_groups_of_friends())
# pprint(set_2)
# print('Уникальные группы у указанного юзера: {}'.format(set_1.difference(set_2)))
# evgeniy.find_unique_groups()
# evgeniy.info_unique_groups()
# evgeniy.info_about_group()
    evgeniy.save_to_file()








