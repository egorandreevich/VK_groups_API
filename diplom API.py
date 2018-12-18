import requests
from pprint import pprint

class User: #Опишем юзера как класс
    def __init__(self, i):
        self.user_id_number = i
        self.friends_dic = self.get_friends()
        self.friends_list = self.friends_dic['response']['items']

    def groups_get(self):  # получил группы юзера
        params = {
            'access_token': self.my_token,
            'v': '5.92',
            'extended': 1,
            'user_id': self.user_id_number,
            'fields': ['members_count']
            # 'count': '500'
        }
        response = requests.get('https://api.vk.com/method/groups.get', params)
        return response.json()  # на выходе должен быть джсон, записанный в файл

    def make_groups_systematic(self):
        final_json = {}
        final_json_list = []
        try:
            raw_json_groups = self.groups_get()
            # pprint(raw_json_groups)
            groups_list = raw_json_groups['response']['items']
            for dict_item in groups_list:
                for key, value in dict_item.items():
                    if key == 'id':
                        final_json['gid'] = value
                    elif key == 'name':
                        final_json['name'] = value
                    elif key == 'members_count':
                        final_json['members_count'] = value
                print(final_json)

                final_json_list.append(final_json)
        except KeyError:
            pass
        finally:
            return (final_json_list)

    def get_friends(self):
        params = {
            'access_token': self.my_token,
            'v': '5.92',
            'user_id': self.user_id_number,
            'count' : '5' #пока ограничимся пятью, тормозит нереально
        }
        response = requests.get('https://api.vk.com/method/friends.get', params)
        return response.json()

    def make_class_items(self):
        list_1 = self.friends_list
        list_2 = []
        # print(list_1)
        for user in list_1:
            # print(user)
            user = User(user)
            list_2.append(user)
        return list_2

    def get_groups_of_friends(self): #функция для получения групп друзей
        response_list = []
        list_2 = self.make_class_items() #получаем список друзей по уже написанной функции
        for friend in list_2: #итерируемся по списку друзей и для каждого вызываем функцию friend.make_groups_systematic()
            print(friend.make_groups_systematic())
        # return response_list


    my_token = 'ed1271af9e8883f7a7c2cefbfddfcbc61563029666c487b2f71a5227cce0d1b533c4af4c5b888633c06ae'
    user_id_number = 0
    # user_name = 'eshmargunov'


evgeniy = User(171691064)
pprint(evgeniy.make_groups_systematic())
# pprint(evgeniy.friends_list)
# pprint(evgeniy.make_class_items())
# pprint(evgeniy.get_groups_of_friends())

# pprint(final_json_list)

