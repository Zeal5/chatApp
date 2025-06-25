from django.contrib.auth import get_user_model


def run():
    User = get_user_model()

    username = "z"
    email = "z@z.com"
    password = "z"

    if User.objects.filter(username=username).exists():
        print(
            f"email : {email}\npasswd : {password}\nusername : {username}\nAlready exists"
        )

    else:
        User.objects.create_superuser(username=username, email=email, password=password)
        print(
            f"email : {email}\npasswd : {password}\nusername : {username}\nwas created successfully"
        )
