import json


class User(dict):
    def __hash__(self):
        return self['uid']

    def __eq__(self, other):
        if self['uid'] == other['uid']:
            return True
        else:
            return False


def load_user_set(data_json_file):
    user_set = set()
    for item in json.load(open(data_json_file, 'r', encoding="utf-8")):
        user_set.add(User(item))
    return user_set


def save_user_set(user_set, data_json_file):
    json.dump(list(user_set), open(data_json_file, 'w', encoding="utf-8"), indent=4, ensure_ascii=False)


def get_user_in_set(user_set, user):
    for i in user_set:
        if i == user:
            return i
    return None


def update_user_in_set(user_set, user):
    if user in user_set:
        user_set.remove(user)
        user_set.add(user)
        return True
    else:
        return False


if __name__ == "__main__":
    UserSet2 = load_user_set('../data/user_data.json')
    print(list(UserSet2))
    save_user_set(UserSet2, '../data/user_data.json')
