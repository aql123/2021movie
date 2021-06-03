import os

import django

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "movie.settings")

django.setup()

base_dir = '../media/movie_cover'
files = os.listdir(base_dir)
from populate_data.populate_movies import replace_special_char

for file in files:
    os.rename(os.path.join(base_dir, file), os.path.join(base_dir, replace_special_char(file)))

# from user.models import Movie
#
# movies = Movie.objects.all()
# for movie in movies:
#     movie.image_link = replace_special_char(str(movie.image_link))
#     # movie.pic.file.name=movie.pic.file.name.replac
#     # movie.pic=movie.pic.replace(' ','_')
#     movie.save()
