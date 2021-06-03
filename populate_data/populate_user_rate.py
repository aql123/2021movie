import os
import random

import django

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "movierecomend.settings")

django.setup()
strs = 'abcdefghijk_mnopqrstuvwxyz'
from movie.models import *


# 随机生成username
def random_user_name(length=5):
    return ''.join(random.choices(strs, k=length))


def random_phone():
    res = ''.join([str(random.randint(0, 9)) for _ in range(11)])
    return res


def random_mark():
    return random.randint(1, 5)


def populate_user(nums):
    for i in range(nums):
        user_name = random_user_name()
        user, created = User.objects.get_or_create(username=user_name, defaults={
            'password': user_name,
            'email': user_name + '@163.com'
        })
        print(user, 'created:', created)


def populate_user_rating(rating_numbers):
    for i in range(rating_numbers):
        user = User.objects.order_by('?').first()
        movie = Movie.objects.order_by('?').first()
        rating, created = Rate.objects.get_or_create(user=user, movie=movie, defaults={"mark": random_mark()})
        print(rating, 'created', created)


if __name__ == '__main__':
    # 随机生成用户
    populate_user(100)
    # 随机生成打分 参数为生成数量
    populate_user_rating(1000)
