

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('movie', '0003_auto_20200530_2235'),
    ]

    operations = [
        migrations.RenameField(
            model_name='movie',
            old_name='all_tags',
            new_name='tags',
        ),
    ]
