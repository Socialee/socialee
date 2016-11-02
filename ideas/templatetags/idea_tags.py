import random
from django import template
from ideas.models import Idea

register = template.Library()


@register.simple_tag
def idea_list():
    ideas = Idea.objects.filter(active=True)

    return ideas