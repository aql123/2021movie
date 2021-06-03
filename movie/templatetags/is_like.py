from django import template

register = template.Library()
from movie.models import LikeComment


@register.filter
# 是否点赞
def is_like(comment_id, user_id):
    comment = LikeComment.objects.filter(comment_id=comment_id, user_id=user_id)
    return len(comment) > 0
