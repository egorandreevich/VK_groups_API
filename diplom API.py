import requests
from pprint import pprint

my_token = 'ed1271af9e8883f7a7c2cefbfddfcbc61563029666c487b2f71a5227cce0d1b533c4af4c5b888633c06ae'
user_id = 171691064
user_name = 'eshmargunov'
'''
https://vk.com/dev/users.getSubscriptions
https://vk.com/dev/groups.get
У всего списка друзей вернуть группы и добавить их в список-множество, и группы евгения во множество. Далее сравнить множества
Помимо идентификаторов групп, нужно о них название и тп (см задание.тхт)
'''


def groups_get(id, token): #получил группы Евгения
    params = {
        'access_token': token,
        'v': '5.92',
        'extended' : 1,
        'user_id': id,
        'fields' : ['members_count'] #непонятно, почему он все, а не только поле нейм выдает
        # 'count': '500'
    }
    response = requests.get('https://api.vk.com/method/groups.get', params)
    return response.json() #на выходе должен быть джсон, записанный в файл

raw_json_groups = groups_get(user_id, my_token)
# pprint(raw_json_groups)
groups_list = raw_json_groups['response']['items']
# pprint(groups_list)

final_json = {}
final_json_list = list()

for dict_item in groups_list:
    for key, value in dict_item.items():
        if key == 'id':
            final_json['gid'] = value
        elif key == 'name':
            final_json['name'] = value
        elif key == 'members_count':
            final_json['members_count'] = value
    final_json_list.append(final_json)
pprint(final_json_list)