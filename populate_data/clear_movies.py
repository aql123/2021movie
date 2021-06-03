import os

import django

#
# 清空数据库中的电影数据和标签数据
#

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "movie.settings")

django.setup()

from movie.models import Movie, Tags


def clear_movie_tags():
    Movie.objects.all().delete()
    Tags.objects.all().delete()
