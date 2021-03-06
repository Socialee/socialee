import random
from django import template
from ideas.models import Idea

register = template.Library()


@register.simple_tag
def featured_idea_list():
    '''
    Das ist jetzt so gebaut, dass von allen gefeaturten Ideen 9 zufällige ausgesucht und angezeigt werden.
    Heißt, dass bei jedem Neuladen der Seite andere Ideen angezeigt werden, sofern mehr als acht featured = True sind.
    '''
    ideas = Idea.objects.filter(private=False, active=True, featured=True, enabled=True )
    random_ideas = ideas.order_by('-subm_date')[:12]

    return random_ideas

@register.simple_tag
def own_idea_list(email):
    own_idea_list = Idea.objects.filter(author=email).order_by('-subm_date')
    return own_idea_list

@register.simple_tag
def idea_count():
    return Idea.objects.filter(active=True, enabled=True).count()

@register.simple_tag
def ideas_left():
    all_ideas = Idea.objects.filter(private=False, active=True, enabled=True).count()
    ideas_in_landingpage = 9
    return all_ideas - ideas_in_landingpage