import random
from django import template
from ideas.models import Idea

register = template.Library()


@register.simple_tag
def idea_list():
    ideas = Idea.objects.filter(active=True).order_by('-subm_date')
    return ideas

@register.simple_tag
def featured_idea_list():
    ideas = Idea.objects.filter(active=True).filter(featured=True)
    random_ideas = ideas.order_by('?')[:8]

    return random_ideas

@register.simple_tag
def own_idea_list(email):
    own_idea_list = Idea.objects.filter(author=email).order_by('-subm_date')
    return own_idea_list

@register.simple_tag
def idea_count():
    return Idea.objects.filter(active=True).count()

# Das ist jetzt so gebaut, dass von allen gefeaturten Ideen 8 zufällige ausgesucht und angezeigt werden.
# Heißt, dass bei jedem Neuladen der Seite andere Ideen angezeigt werden, sofern mehr als acht featured = True sind.