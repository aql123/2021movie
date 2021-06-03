
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


def populate_user_collect(collect_number):
    for i in range(collect_number):
        user = User.objects.order_by('?').first()
        movie = Movie.objects.order_by('?').first()
        print('user{} collect {}'.format(user.username, movie.name))
        movie.collect.add(user)


if __name__ == '__main__':
    # 随机生成用户打分 参数为生成数量
    # 每部电影有5个用户收藏
    pass
    # populate_user_collect(collect_number=5000)
