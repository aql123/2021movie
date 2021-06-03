# -*-coding:utf-8-*-
import os

os.environ["DJANGO_SETTINGS_MODULE"] = "movie.settings"
import django

django.setup()
from movie.models import *
from math import sqrt, pow
import operator
from django.db.models import Subquery,Q,Count


# from django.shortcuts import render,render_to_response
class UserCf:

    # 获得初始化数据
    def __init__(self, all_user):
        self.all_user = all_user

    # 通过用户名获得列表，仅调试使用
    def getItems(self, username1, username2):
        return self.all_user[username1], self.all_user[username2]

    # 计算两个用户的皮尔逊相关系数
    def pearson(self, user1, user2):  # 数据格式为：物品id，浏览
        sum_xy = 0.0  # user1,user2 每项打分的的累加
        n = 0  # 公共浏览次数
        sum_x = 0.0  # user1 的打分总和
        sum_y = 0.0  # user2 的打分总和
        sumX2 = 0.0  # user1每项打分平方的累加
        sumY2 = 0.0  # user2每项打分平方的累加
        for movie1, score1 in user1.items():
            if movie1 in user2.keys():  # 计算公共的浏览次数
                n += 1
                sum_xy += score1 * user2[movie1]
                sum_x += score1
                sum_y += user2[movie1]
                sumX2 += pow(score1, 2)
                sumY2 += pow(user2[movie1], 2)
        if n == 0:
            # print("p氏距离为0")
            return 0
        molecule = sum_xy - (sum_x * sum_y) / n  # 分子
        denominator = sqrt((sumX2 - pow(sum_x, 2) / n) * (sumY2 - pow(sum_y, 2) / n))  # 分母
        if denominator == 0:
            return 0
        r = molecule / denominator
        return r

    # 计算与当前用户的距离，获得最临近的用户
    def nearest_user(self, current_user, n=1):
        distances = {}
        # 用户，相似度
        # 遍历整个数据集
        for user, rate_set in self.all_user.items():
            # 非当前的用户
            if user != current_user:
                distance = self.pearson(self.all_user[current_user], self.all_user[user])
                # 计算两个用户的相似度
                distances[user] = distance
        closest_distance = sorted(
            distances.items(), key=operator.itemgetter(1), reverse=True
        )
        # 最相似的N个用户
        print("closest user:", closest_distance[:n])
        return closest_distance[:n]

    # 给用户推荐电影
    def recommend(self, username, n=3):
        recommend = {}
        nearest_user = self.nearest_user(username, n)
        for user, score in dict(nearest_user).items():  # 最相近的n个用户
            for movies, scores in self.all_user[user].items():  # 推荐的用户的电影列表
                if movies not in self.all_user[username].keys():  # 当前username没有看过
                    if movies not in recommend.keys():  # 添加到推荐列表中
                        recommend[movies] = scores*score
        # 对推荐的结果按照电影
        # 浏览次数排序
        return sorted(recommend.items(), key=operator.itemgetter(1), reverse=True)


# 基于用户的推荐
def recommend_by_user_id(user_id):
    user_prefer = UserTagPrefer.objects.filter(user_id=user_id).order_by('-score').values_list('tag_id', flat=True)
    current_user = User.objects.get(id=user_id)
    # 如果当前用户没有打分 则看是否选择过标签，选过的话，就从标签中找
    # 没有的话，就按照浏览度推荐15个
    if current_user.rate_set.count() == 0:
        if len(user_prefer) != 0:
            movie_list = Movie.objects.filter(tags__in=user_prefer)[:15]
        else:
            movie_list = Movie.objects.order_by("-num")[:15]
        return movie_list
    # 选取评分最多的10个用户
    users_rate = Rate.objects.values('user').annotate(mark_num=Count('user')).order_by('-mark_num')
    user_ids = [user_rate['user'] for user_rate in users_rate]
    user_ids.append(user_id)
    users = User.objects.filter(id__in=user_ids)#users 为评分最多的10个用户
    all_user = {}
    for user in users:
        rates = user.rate_set.all()#查出10名用户的数据
        rate = {}
        # 用户有给电影打分 在rate和all_user中进行设置
        if rates:
            for i in rates:
                rate.setdefault(str(i.movie.id), i.mark)#填充电影数据
            all_user.setdefault(user.username, rate)
        else:
            # 用户没有为电影打过分，设为0
            all_user.setdefault(user.username, {})

    user_cf = UserCf(all_user=all_user)
    recommend_list = [each[0] for each in user_cf.recommend(current_user.username, 15)]
    movie_list = list(Movie.objects.filter(id__in=recommend_list).order_by("-num")[:15])
    other_length = 15 - len(movie_list)
    if other_length > 0:
        fix_list = Movie.objects.filter(~Q(rate__user_id=user_id)).order_by('-collect')
        for fix in fix_list:
            if fix not in movie_list:
                movie_list.append(fix)
            if len(movie_list) >= 15:
                break
    return movie_list


# 计算相似度
def similarity(movie1_id, movie2_id):
    movie1_set = Rate.objects.filter(movie_id=movie1_id)
    # movie1的打分用户数
    movie1_sum = movie1_set.count()
    # movie_2的打分用户数
    movie2_sum = Rate.objects.filter(movie_id=movie2_id).count()
    # 两者的交集
    common = Rate.objects.filter(user_id__in=Subquery(movie1_set.values('user_id')), movie=movie2_id).values('user_id').count()
    # 没有人给当前电影打分
    if movie1_sum == 0 or movie2_sum == 0:
        return 0
    similar_value = common / sqrt(movie1_sum * movie2_sum)#余弦计算相似度
    return similar_value


#基于物品
def recommend_by_item_id(user_id, k=15):
    # 前三的tag，用户评分前三的电影
    user_prefer = UserTagPrefer.objects.filter(user_id=user_id).order_by('-score').values_list('tag_id', flat=True)
    user_prefer = list(user_prefer)[:3]
    current_user = User.objects.get(id=user_id)
    # 如果当前用户没有打分 则看是否选择过标签，选过的话，就从标签中找
    # 没有的话，就按照浏览度推荐15个
    if current_user.rate_set.count() == 0:
        if len(user_prefer) != 0:
            movie_list = Movie.objects.filter(tags__in=user_prefer)[:15]
        else:
            movie_list = Movie.objects.order_by("-num")[:15]
        print('from here')
        return movie_list
    # most_tags = Tags.objects.annotate(tags_sum=Count('name')).order_by('-tags_sum').filter(movie__rate__user_id=user_id).order_by('-tags_sum')
    # 选用户最喜欢的标签中的电影，用户没看过的30部，对这30部电影，计算距离最近
    un_watched = Movie.objects.filter(~Q(rate__user_id=user_id), tags__in=user_prefer).order_by('?')[:30]  # 看过的电影
    watched = Rate.objects.filter(user_id=user_id).values_list('movie_id', 'mark')
    distances = []
    names = []
    # 在未看过的电影中找到
    for un_watched_movie in un_watched:
        for watched_movie in watched:
            if un_watched_movie not in names:
                names.append(un_watched_movie)
                distances.append((similarity(un_watched_movie.id, watched_movie[0]) * watched_movie[1], un_watched_movie))#加入相似的电影
    distances.sort(key=lambda x: x[0], reverse=True)
    print('this is distances', distances[:15])
    recommend_list = []
    for mark, movie in distances:
        if len(recommend_list) >= k:
            break
        if movie not in recommend_list:
            recommend_list.append(movie)
    # print('this is recommend list', recommend_list)
    # 如果得不到有效数量的推荐 按照未看过的电影中的热度进行填充
    print('recommend list', recommend_list)
    return recommend_list


if __name__ == '__main__':
    similarity(2003, 2008)
    recommend_by_item_id(1)
