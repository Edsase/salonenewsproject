from django import template
from news.models import Feed

#register this module as a template library
register = template.Library()

#add template tag by wrapping the inclusion template tag
#the action of this inclusion tag will be wrapped up in the template cat.html
@register.inclusion_tag('news/feeds.html')
def get_feed_list(feed = None):

    """function returns all categories in the db"""

    return {'feeds': Feed.objects.all(), 'act_feed': feed}


