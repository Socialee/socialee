import random
from django import template
from landingpage.models import Landingpage

register = template.Library()


@register.simple_tag
def random_landingpagecontent():
    landingpage = Landingpage.objects.filter(active=True)
    if landingpage:
        alllandingpages = list(Landingpage.objects.filter(active=True))
        random_landingpage = random.choice(alllandingpages)

        return {
        	'bg_img':random_landingpage.bg_img,
        	'symbol':random_landingpage.symbol,
        	'claim':random_landingpage.claim,
        	'tagline':random_landingpage.tagline,
        	'cta':random_landingpage.cta,
            'active':random_landingpage.active
        	}

    else:
        return '...'

