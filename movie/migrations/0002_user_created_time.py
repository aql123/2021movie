

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('movie', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='user',
            name='created_time',
            field=models.DateTimeField(default=datetime.datetime(2020, 5, 30, 22, 32, 7, 543161)),
        ),
    ]
