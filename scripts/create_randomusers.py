from django.contrib.auth import get_user_model


def run():
    User = get_user_model()

    letters = ["a", "b", "c", "d", "e", "f", "g","h", "i"]

    # (name, emial)
    u = [(letter, f"{letter}@{letter}.com") for letter in letters]

    users = []
    for usr in u:
        print(usr[0], usr[1])
        _user = User(username=usr[0], email=usr[1])
        _user.set_password(usr[0])
        users.append(_user)

    User.objects.bulk_create(users, ignore_conflicts=True)
