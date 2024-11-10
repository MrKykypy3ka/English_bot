import json


def read_config():
    with open("data/config.json", "r", encoding='utf-8') as file:
        return json.load(file)


def write_config(data):
    with open("data/config.json", "w", encoding='utf-8') as file:
        json.dump(data, file, ensure_ascii=True, indent=4)


def read_user():
    with open("data/users.txt", "r", encoding="utf-8") as f:
        return list(map(str.strip, f.readlines()))


def write_user(user):
    users = read_user()
    if str(user) not in users:
        users.append(str(user))
    with open("data/users.txt", "w", encoding="utf-8") as f:
        f.write(f'{"\n".join(users)}\n')


async def check_subscriptions(callback):
    user_id = callback.from_user.id
    subscription = read_config()["newsletter"]["subscription"]
    for chanel in subscription:
        member = await callback.message.bot.get_chat_member(chat_id="@"+chanel, user_id=user_id)
        if member.status not in ["member", "administrator", "creator"]:
            return False
    return True
