import os

import django

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "movie.settings")

django.setup()

base_dir = '../media/movie_cover'
files = os.listdir(base_dir)
print(files)
from user.models import Movie

movies = Movie.objects.all()
for movie in movies:
    filename = str(movie.image_link).split('/')[1]
    print(filename)
    files.remove(filename)
print('extra image:', files)
for file in files:
    os.remove(os.path.join(base_dir,file))
    print('删除成功!',file)
