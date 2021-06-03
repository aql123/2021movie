import json
import random
from functools import wraps

from django.core.cache import cache
from django.core.paginator import Paginator
from django.db.models import Q, Count
from django.http import HttpResponse
from django.shortcuts import render, redirect
from django.urls import reverse
from django.views.decorators.csrf import csrf_exempt
from rest_framework.renderers import JSONRenderer

from movie_it.cache_keys import USER_CACHE, ITEM_CACHE
from movie_it.recommend_movies import recommend_by_user_id, recommend_by_item_id
from .forms import *


def movies_paginator(movies, page):
    paginator = Paginator(movies, 12)
    if page is None:
        page = 1
    movies = paginator.page(page)
    return movies


# from django.urls import HT
# json response
class JSONResponse(HttpResponse):
    def __init__(self, data, **kwargs):
        content = JSONRenderer().render(data)
        kwargs["content_type"] = "application/json;"
        super(JSONResponse, self).__init__(content, **kwargs)


# 登录功能
def login(request):
    if request.method == "POST":
        form = Login(request.POST)
        if form.is_valid():
            username = form.cleaned_data["username"]
            password = form.cleaned_data["password"]
            result = User.objects.filter(username=username)
            if result:
                user = User.objects.get(username=username)
                if user.password == password:
                    request.session["login_in"] = True
                    request.session["user_id"] = user.id
                    request.session["name"] = username
                    # 用户第一次注册，需要选标签
                    new = request.session.get('new')
                    if new:
                        tags = Tags.objects.all()
                        print('goto choose tag')
                        return render(request, 'choose_tag.html', {'tags': tags})
                    return redirect(reverse("index"))
                else:
                    return render(
                        request, "login.html", {"form": form, "message": "密码错误"}
                    )
            else:
                return render(
                    request, "login.html", {"form": form, "message": "账号不存在"}
                )
    else:
        form = Login()
        return render(request, "login.html", {"form": form})


# 注册功能
def register(request):
    if request.method == "POST":
        form = RegisterForm(request.POST)
        error = None
        if form.is_valid():
            username = form.cleaned_data["username"]
            password = form.cleaned_data["password2"]
            email = form.cleaned_data["email"]
            User.objects.create(
                username=username,
                password=password,
                email=email,
            )
            request.session['new'] = 'true'
            # 根据表单数据创建一个新的用户
            return redirect(reverse("login"))  # 跳转到登录界面
        else:
            return render(
                request, "register.html", {"form": form, "error": error}
            )  # 表单验证失败返回一个空表单到注册页面
    form = RegisterForm()
    return render(request, "register.html", {"form": form})


def logout(request):
    if not request.session.get("login_in", None):  # 不在登录状态跳转回首页
        return redirect(reverse("index"))
    request.session.flush()  # 清除session信息
    print('注销')
    return redirect(reverse("index"))


def login_in(func):  # 验证用户是否登录
    @wraps(func)
    def wrapper(*args, **kwargs):
        request = args[0]
        is_login = request.session.get("login_in")
        if is_login:
            return func(*args, **kwargs)
        else:
            return redirect(reverse("login"))

    return wrapper


# Create your views here.
def index(request):
    order =  request.POST.get("order") or request.session.get('order')
    request.session['order']=order
    if order == 'collect':
        movies = Movie.objects.annotate(collectors=Count('collect')).order_by('-collectors')
        print(movies.query)
        title = '收藏排序'
    elif order == 'rate':
        movies = Movie.objects.all().annotate(marks=Avg('rate__mark')).order_by('-marks')
        title = '评分排序'
    elif order == 'years':
        movies = Movie.objects.order_by('-years')
        title = '时间排序'
    else:
        movies = Movie.objects.order_by('-num')
        title = '热度排序'
    paginator = Paginator(movies, 8)
    new_list = Movie.objects.order_by('-years')[:8]
    current_page = request.GET.get("page", 1)
    movies = paginator.page(current_page)
    return render(request, 'items.html', {'movies': movies, 'new_list': new_list, 'title': title})

#电影详情
def movie(request, movie_id):
    movie = Movie.objects.get(pk=movie_id)
    movie.num += 1
    movie.save()
    comments = movie.comment_set.order_by("-create_time")
    user_id = request.session.get("user_id")
    movie_rate = Rate.objects.filter(movie=movie).all().aggregate(Avg('mark'))#电影评分
    if movie_rate:
        movie_rate = movie_rate['mark__avg']
    else:
        movie_rate = 0
    if user_id is not None:
        user_rate = Rate.objects.filter(movie=movie, user_id=user_id).first()
        user = User.objects.get(pk=user_id)
        is_collect = movie.collect.filter(id=user_id).first()
    return render(request, "movie.html", locals())


def search(request):  # 搜索
    if request.method == "POST":  # 如果搜索界面
        key = request.POST["search"]
        request.session["search"] = key  # 记录搜索关键词解决跳页问题
    else:
        key = request.session.get("search")  # 得到关键词
    movies = Movie.objects.filter(
        Q(name__icontains=key) | Q(intro__icontains=key) | Q(director__icontains=key)
    )  # 进行内容的模糊搜索
    page_num = request.GET.get("page", 1)
    movies = movies_paginator(movies, page_num)
    return render(request, "items.html", {"movies": movies, 'title': '搜索结果'})

#所有标签
def all_tags(request):
    tags = Tags.objects.all()
    return render(request, "all_tags.html", {'all_tags': tags})

#一个标签
def one_tag(request, one_tag_id):
    tag = Tags.objects.get(id=one_tag_id)
    movies = tag.movie_set.all()
    page_num = request.GET.get("page", 1)
    movies = movies_paginator(movies, page_num)
    return render(request, "items.html", {"movies": movies, 'title': tag.name})

#收藏最多
def hot_movie(request):
    page_number = request.GET.get("page", 1)#分页
    movies = Movie.objects.annotate(user_collector=Count('collect')).order_by('-user_collector')[:10]#查出所有电影，按收藏人数排序
    movies = movies_paginator(movies[:10], page_number)
    return render(request, "items.html", {"movies": movies, "title": "收藏最多"})#返回给items.html


# 评分最多
def most_mark(request):
    page_number = request.GET.get("page", 1)
    movies = Movie.objects.all().annotate(num_mark=Count('rate')).order_by('-num_mark')
    movies = movies_paginator(movies, page_number)
    return render(request, "items.html", {"movies": movies, "title": "评分最多"})


# 浏览最多
def most_view(request):
    page_number = request.GET.get("page", 1)
    movies = Movie.objects.annotate(user_collector=Count('num')).order_by('-num')
    movies = movies_paginator(movies, page_number)
    return render(request, "items.html", {"movies": movies, "title": "浏览最多"})

#最新电影
def latest_movie(request):
    movie_list = Movie.objects.order_by("-years")[:10]
    json_movies = [movie.to_dict(fields=['name', 'image_link', 'id', 'years', 'd_rate']) for movie in movie_list]
    return HttpResponse(json.dumps(json_movies), content_type="application/json")


# 某个导演的电影
def director_movie(request, director_name):
    page_number = request.GET.get("page", 1)
    movies = Movie.objects.filter(director=director_name)
    movies = movies_paginator(movies, page_number)
    return render(request, "items.html", {"movies": movies, "title": "{}的电影".format(director_name)})

#修改个人信息
@login_in
def personal(request):
    user = User.objects.get(id=request.session.get("user_id"))
    if request.method == "POST":
        form = Edit(instance=user, data=request.POST)
        if form.is_valid():
            form.save()
            request.session['name'] = user.username
            return render(
                request, "personal.html", {"message": "修改成功!", "form": form, 'title': '我的信息', 'user': user}
            )
        else:
            return render(
                request, "personal.html", {"message": "修改失败", "form": form, 'title': '我的信息', 'user': user}
            )
    form = Edit(instance=user)
    return render(request, "personal.html", {"user": user, 'form': form, 'title': '我的信息'})


@login_in
@csrf_exempt
def choose_tags(request):
    tags_name = json.loads(request.body)
    user_id = request.session.get('user_id')
    for tag_name in tags_name:
        tag = Tags.objects.filter(name=tag_name.strip()).first()
        UserTagPrefer.objects.create(tag_id=tag.id, user_id=user_id, score=5)
    request.session.pop('new')
    return redirect(reverse("index"))


@login_in
# 给电影进行评论
def make_comment(request, movie_id):
    user = User.objects.get(id=request.session.get("user_id"))
    movie = Movie.objects.get(id=movie_id)
    comment = request.POST.get("comment")
    Comment.objects.create(user=user, movie=movie, content=comment)
    return redirect(reverse("movie", args=(movie_id,)))


@login_in
# 展示我的评论的地方
def my_comments(request):
    user = User.objects.get(id=request.session.get("user_id"))
    comments = user.comment_set.all()
    print('comment:', comments)
    return render(request, "my_comment.html", {"item": comments})


# 给评论点赞
@login_in
def like_comment(request, comment_id, movie_id):
    user_id = request.session.get("user_id")
    LikeComment.objects.get_or_create(user_id=user_id, comment_id=comment_id)
    return redirect(reverse("movie", args=(movie_id,)))


# 取消点赞
@login_in
def unlike_comment(request, comment_id, movie_id):
    user_id = request.session.get("user_id")
    LikeComment.objects.filter(user_id=user_id, comment_id=comment_id).delete()
    return redirect(reverse("movie", args=(movie_id,)))


@login_in
def delete_comment(request, comment_id):
    Comment.objects.get(pk=comment_id).delete()
    return redirect(reverse("my_comments"))


@login_in
# 给电影打分 在打分的时候清除缓存
def score(request, movie_id):
    user_id = request.session.get("user_id")
    # user = User.objects.get(id=user_id)
    movie = Movie.objects.get(id=movie_id)
    score = float(request.POST.get("score"))
    get, created = Rate.objects.get_or_create(user_id=user_id, movie=movie, defaults={"mark": score})
    if created:
        for tag in movie.tags.all():
            prefer, created = UserTagPrefer.objects.get_or_create(user_id=user_id, tag=tag, defaults={'score': score})
            if not created:
                # 更新分数
                prefer.score += (score - 3)
                prefer.save()
        print('create data')
        # 清理缓存
        user_cache = USER_CACHE.format(user_id=user_id)
        item_cache = ITEM_CACHE.format(user_id=user_id)
        cache.delete(user_cache)
        cache.delete(item_cache)
        print('cache deleted')
    return redirect(reverse("movie", args=(movie_id,)))

#我的评分
@login_in
def my_rate(request):
    user = User.objects.get(id=request.session.get("user_id"))
    rate = user.rate_set.all()
    return render(request, "my_rate.html", {"item": rate})


def delete_rate(request, rate_id):
    Rate.objects.filter(pk=rate_id).delete()
    return redirect(reverse("my_rate"))

#收藏电影
@login_in
def collect(request, movie_id):
    user = User.objects.get(id=request.session.get("user_id"))
    movie = Movie.objects.get(id=movie_id)
    movie.collect.add(user)
    movie.save()
    return redirect(reverse("movie", args=(movie_id,)))

#取消收藏电影
@login_in
def decollect(request, movie_id):
    user = User.objects.get(id=request.session.get("user_id"))
    movie = Movie.objects.get(id=movie_id)
    movie.collect.remove(user)
    # movie.rate_set.count()
    movie.save()
    return redirect(reverse("movie", args=(movie_id,)))

#我的收藏
@login_in
def mycollect(request):
    user = User.objects.get(id=request.session.get("user_id"))
    movie = user.movie_set.all()
    return render(request, "mycollect.html", {"item": movie})

#基于用户推荐
def user_recommend(request):
    # cache_key = USER_CACHE.format(user_id=user_id)
    user_id = request.session.get("user_id")
    if user_id is None:
        movie_list = Movie.objects.order_by('?')
    else:
        cache_key = USER_CACHE.format(user_id=user_id)
        movie_list = cache.get(cache_key)
        if movie_list is None:
            movie_list = recommend_by_user_id(user_id)
            cache.set(cache_key, movie_list, 60 * 5)
            print('设置缓存')
        else:
            print('缓存命中!')

    json_movies = [movie.to_dict(fields=['name', 'image_link', 'id', 'years', 'd_rate']) for movie in movie_list]
    random.shuffle(json_movies)
    return HttpResponse(json.dumps(json_movies[:3]), content_type="application/json")

#基于物品推荐
def item_recommend(request):
    # return render(request,'index.html')
    user_id = request.session.get("user_id")
    if user_id is None:
        movie_list = Movie.objects.order_by('?')
    else:
        cache_key = ITEM_CACHE.format(user_id=user_id)
        movie_list = cache.get(cache_key)
        if movie_list is None:
            movie_list = recommend_by_item_id(user_id)
            cache.set(cache_key, movie_list, 60 * 5)
            print('设置缓存')
        else:
            print('缓存命中!')
    json_movies = [movie.to_dict(fields=['name', 'image_link', 'id', 'years', 'd_rate']) for movie in movie_list]
    random.shuffle(json_movies)
    return HttpResponse(json.dumps(json_movies[:3]), content_type="application/json")
