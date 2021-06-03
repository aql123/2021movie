

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('movie', '0002_user_created_time'),
    ]

    operations = [
        migrations.AlterField(
            model_name='user',
            name='created_time',
            field=models.DateTimeField(auto_now_add=True),
        ),
    ]
