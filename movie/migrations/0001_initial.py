

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Comment',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('content', models.CharField(max_length=255, verbose_name='内容')),
                ('create_time', models.DateTimeField(auto_now_add=True)),
            ],
            options={
                'verbose_name': '评论',
                'verbose_name_plural': '评论',
            },
        ),
        migrations.CreateModel(
            name='Movie',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=255, unique=True, verbose_name='电影名称')),
                ('director', models.CharField(max_length=255, verbose_name='导演名称')),
                ('country', models.CharField(max_length=255, verbose_name='国家')),
                ('years', models.DateField(verbose_name='上映日期')),
                ('leader', models.CharField(max_length=1024, verbose_name='主演')),
                ('d_rate_nums', models.IntegerField(verbose_name='豆瓣评价数')),
                ('d_rate', models.CharField(max_length=255, verbose_name='豆瓣评分')),
                ('intro', models.TextField(verbose_name='描述')),
                ('num', models.IntegerField(default=0, verbose_name='浏览量')),
                ('origin_image_link', models.URLField(max_length=255, null=True, verbose_name='豆瓣图片地址')),
                ('image_link', models.FileField(max_length=255, upload_to='movie_cover', verbose_name='封面图片')),
                ('imdb_link', models.URLField(null=True)),
            ],
            options={
                'verbose_name': '电影',
                'verbose_name_plural': '电影',
            },
        ),
        migrations.CreateModel(
            name='Tags',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=255, unique=True, verbose_name='标签')),
            ],
            options={
                'verbose_name': '标签',
                'verbose_name_plural': '标签',
            },
        ),
        migrations.CreateModel(
            name='User',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('username', models.CharField(max_length=255, unique=True, verbose_name='账号')),
                ('password', models.CharField(max_length=255, verbose_name='密码')),
                ('email', models.EmailField(max_length=254, verbose_name='邮箱')),
            ],
            options={
                'verbose_name': '用户',
                'verbose_name_plural': '用户',
            },
        ),
        migrations.CreateModel(
            name='UserTagPrefer',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('score', models.FloatField(default=0)),
                ('tag', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='movie.Tags', verbose_name='标签名')),
                ('user', models.ForeignKey(blank=True, on_delete=django.db.models.deletion.CASCADE, to='movie.User', verbose_name='用户id')),
            ],
            options={
                'verbose_name': '用户偏好',
                'verbose_name_plural': '偏好',
            },
        ),
        migrations.CreateModel(
            name='Rate',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('mark', models.FloatField(verbose_name='评分')),
                ('create_time', models.DateTimeField(auto_now_add=True, verbose_name='发布时间')),
                ('movie', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='movie.Movie', verbose_name='电影id')),
                ('user', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='movie.User', verbose_name='用户id')),
            ],
            options={
                'verbose_name': '评分信息',
                'verbose_name_plural': '评分信息',
            },
        ),
        migrations.AddField(
            model_name='movie',
            name='collect',
            field=models.ManyToManyField(blank=True, to='movie.User', verbose_name='收藏者'),
        ),
        migrations.AddField(
            model_name='movie',
            name='all_tags',
            field=models.ManyToManyField(blank=True, to='movie.Tags', verbose_name='标签'),
        ),
        migrations.CreateModel(
            name='LikeComment',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('comment', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='movie.Comment', verbose_name='评论')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='movie.User', verbose_name='用户')),
            ],
            options={
                'verbose_name': '评论点赞',
                'verbose_name_plural': '评论点赞',
            },
        ),
        migrations.AddField(
            model_name='comment',
            name='movie',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='movie.Movie', verbose_name='电影'),
        ),
        migrations.AddField(
            model_name='comment',
            name='user',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='movie.User', verbose_name='用户'),
        ),
    ]
