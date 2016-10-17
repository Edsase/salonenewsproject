from django_cron import CronJobBase, Schedule # see http://django-cron.readthedocs.io/en/latest/installation.html

#import feed parser
import feedparser
#import dateutil parser
from dateutil import parser
import datetime
from django.utils import timezone
import pytz

from models import Feed, Article, User, UserProfile


class UpdateArticles(CronJobBase):
    RUN_EVERY_MINS = 1 # every 2 hours

    schedule = Schedule(run_every_mins=RUN_EVERY_MINS)
    code = 'news.cron'    # a unique code
 
    def do(self):
        """
        - function for adding news articles from feeds in the database
        - its a cron job that runs every hour
        -it loops through all the feeds in the db
        - parses the feeds to extract the articles
        - updates the articles model
        - does not return anything
        """
        all_feeds = Feed.objects.all()
        for feed in all_feeds:
            #parse the feed
            feed_data = feedparser.parse(feed.url)
            #extract the articles in feed_data
            for entry in feed_data.entries:
                
                #make an article ojbject
                article = Article()
                #assign the entry url to the article url
                article.url = entry.link
                #check if url already exist in db. If not yet exist, continue assigning and save entry 
                #get the existing articles in the db
                existing_articles = Article.objects.filter(url = article.url)
                if len(existing_articles)==0: #then entry does not already exist in db
                    article.title = entry.title    
                    #article.description = entry.description[:20]
                    #dont store description
                    article.description = ""
                    #get the publication date of the article
                    
                    try:
                        d = datetime.datetime(entry.published_parsed[0:6])
                    except TypeError:
                        #error due to no tzoneinfo
                        #so make the date timezone aware
                        pub_date = entry.published
                        d = parser.parse(pub_date)
                        #add tzone info if d does not have already
                        if '+' not in pub_date:
                            gmt = pytz.timezone('GMT')
                            d = gmt.localize(d)                                   
                    #change date to datestring
                    gmt = pytz.timezone('GMT')
                    today = gmt.localize(datetime.datetime.today())

                    #check if article is less than three days old
                    if (today-d).days<3:
                        #since article is less than 2 days, extract and save it into db
                        article.publication_date = d
                        article.feed = feed
                        #article.category=Category()
                        article.save()
                        

class DeleteOldArticles(CronJobBase):
    RUN_EVERY_MINS = 600 # every 10 hours

    schedule = Schedule(run_every_mins=RUN_EVERY_MINS)
    code = 'news.delete_old_articles'    # a unique code
    
    def do(self):
        """
        - function for deleting old articles in the database
        - its a cron job that runs every 10 hours
        -it loops through all the feeds in the db
        - deletes those that are more than five days old
        - updates the articles model
        - does not return anything
        """
        five_days_ago = datetime.datetime.now()-datetime.timedelta(days=5)
        gmt = pytz.timezone('GMT')
        five_days_ago = gmt.localize(five_days_ago)
        #delete all the articles in the db older than five days
        old_articles = Article.objects.filter(publication_date__gte=five_days_ago).delete()