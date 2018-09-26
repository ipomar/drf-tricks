import json

from django.contrib.auth.hashers import make_password
from django.contrib.auth.models import User


DEFAULT_PASSWORD = '111'


def create_user(username, **kwargs):
    password = kwargs.pop('password', DEFAULT_PASSWORD)
    first_name = kwargs.pop('first_name', "John")
    last_name = kwargs.pop('last_name', "Doe")
    email = kwargs.pop('email', f'{username}@test.com')

    user_kw = dict(
        username=username,
        first_name=first_name,
        last_name=last_name,
        email=email,
        password=make_password(password),
        **kwargs
    )
    return User.objects.create(**user_kw)


def login_user(client, user, password=DEFAULT_PASSWORD):
    client.login(username=user.username, password=password)


def dump(response):
    """ Print DRF response data

        Useful for debugging tests. Prints response code and indented JSON data
    """

    print(response.status_code)

    print("\nURL:", response.request['PATH_INFO'])
    print("Method:", response.request['REQUEST_METHOD'])
    if response.request['QUERY_STRING']:
        print("Query:", response.request['QUERY_STRING'])
    print("\n")
    print("Status code:\n{}\n\nData:\n{}\n".format(
        response.status_code,
        json.dumps(response.data, indent=4, ensure_ascii=False) if hasattr(response, 'data') else None
    ))
