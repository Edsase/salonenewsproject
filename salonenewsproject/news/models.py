from django.db import models
from django.template.defaultfilters import slugify
from django.contrib.auth.models import User #django's own user class

class Feed(models.Model):
    """feeds are the newspaper sources"""
    name = models.CharField(max_length = 200)
    url = models.URLField()
    is_active = models.BooleanField(default = False)
    slug = models.SlugField(unique=True, ) #to slugify category names and used unique to ensure unique names

    def __unicode__(self):
        return self.name

    def __str__(self):
        return (self.name).encode('ascii', errors='replace')

#class Category(models.Model):
#    """model that stores the different categories an article could belong to"""
#    name = models.CharField(max_length = 128, unique=True, default="unknown")
#    views = models.IntegerField(default=0)
#    likes = models.IntegerField(default=0)
#    slug = models.SlugField(unique=True, ) #to slugify category names and used unique to ensure unique names

#    def save(self, *args, **kwargs):
#        #to slugify category names (convert blank spaces to hyphens
#        if not self.id:
#            self.slug = slugify(self.name)
#        super(Category,self).save(*args, **kwargs)

#    class Meta:
#        verbose_name_plural = "categories"

#    def __str__(self):
#        return self.name

#    def __unicode__(self):
#        return self.name


class Article(models.Model):
    feed = models.ForeignKey(Feed)
    title = models.CharField(max_length = 200)
    url = models.URLField()
    description = models.TextField()
    publication_date = models.DateTimeField()
    views = models.IntegerField(default=0) #number of times the article was visited
    likes = models.IntegerField(default=0) #the number of likes the article recieved
    comment = models.TextField(max_length = 200) #for users to comment on the description
    #category = models.ForeignKey(Category)


    def __unicode__(self):
        return self.title

    def __str__(self):
        return self.title




#user model  to manage user.
class UserProfile(models.Model):
    #link this model to django's User model in order to take advantage of its defualt attributes line username, password, email, first name and surname
    #better to use one-to-one linking between the defualt user model and this user model that for this user model to inherit from the defualt user model
    user = models.OneToOneField(User) #will inherit all the attributes of default django User model
    #additional attributes we wish to include
    website = models.URLField(blank=True)
    # upload to specifies where the images will be loaded #make sure pillow has been installed to manage image files
    picture = models.ImageField(upload_to='profile_images', blank = True) 

    def __str__(self):
        return self.user.username
    #override the unicode method to return something meaningful
    def __unicode__(self):
        return self.user.username





