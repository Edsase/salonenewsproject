from django.shortcuts import render, redirect

from django.http import HttpResponse

from django.contrib import humanize

#import authentication functions
#from django.contrib.auth import login, logout, authenticate
#from django.contrib.auth.decorators import login_required

from django.http import HttpResponseRedirect, HttpResponse

from django.core.urlresolvers import reverse

from django.shortcuts import redirect

import datetime

from models import Feed, Article, User, UserProfile
#from forms import CategoryForm, PageForm, UserForm, UserProfileForm


#import articles from news paper...check out  https://github.com/codelucas/newspaper
from newspaper import Article as NewsArticle
#import feed parser
import feedparser
#import dateutil parser
from dateutil import parser



def index(request):
    """
    view that will render the index.html template
    It will display latest articles, most viewed articles and most liked articles
    """
    #create a context dictionary
    context_dict = {}
    #query the database for list of all stored articles
    #order the queryset by publication date
    #retrieve only the top 5 most recent articles
    most_recent_articles = Article.objects.all().order_by('-publication_date')[:5]
    #retrieve only the top 5 most viewed articles
    most_viewed_articles = Article.objects.all().order_by('-views')[:5]
    #retrieve all articles
    all_articles = Article.objects.all().order_by('-publication_date')
    #populate context_dictionary
    context_dict = {'most_recent_articles': most_recent_articles, 'most_viewed_articles': most_viewed_articles, 'all_articles':all_articles }
    #render the html index.html
    return render(request, 'news/index.html', context = context_dict)

def about(request):
    """view to render the about template"""
    #construct context dictionary to pass to template engine as context
    context_dict = {"owner": "salonebizness community", "date": datetime.datetime.today()}
    return render(request, 'news/about.html', context=context_dict)

def show_feed(request, feed_name_slug):
    #create context dictionary for template rendering
    context_dict = {}
    #get the requested category based on the slug name if it exists
    
    try:
        feed = Feed.objects.get(slug = feed_name_slug)
        #get the articles associated with this category
        articles = Article.objects.filter(feed = feed)
        #update the context_dict
        context_dict ['feed'] =feed
        context_dict ['articles'] = articles
    #abouve will raise a feed does not exist exception 
    except Feed.DoesNotExist:
        #update context dict with none
        context_dict['feed'] = None
        context_dict['articles'] = None

    return render(request, 'news/feed.html', context=context_dict)

#def add_category(request):
#    """form to enable user add new categories"""
#    #ensure that only registered users can add categories
#    if request.user.is_authenticated():
#        form = CategoryForm()

#        if request.method=="POST":
#            form = CategoryForm(request.POST)
#            #check if form is valid
#            if form.is_valid():
#                #save the new category to the database
#                cat = form.save(commit=True)
#                #print cat on console to confirm that it has been save
#                #print cat.slug
#                #return to the success page, in this case the index page which shows top 5 categories
#                return index(request)
#            else:
#                #form contains invalid data, so print errors
#                print form.errors
#        #render the form with error messages if any
#        return render(request, 'news/add_category.html', {'form': form})
#    #since user is not authenticated, redirect to login page
#    else:
#        return HttpResponseRedirect(reverse('news:login'))



##Below function was decommisioned. We use instead the django auth app
##def register(request):
##    """
##    view to register users
##    """
##    #variable that tracks if form registration is successful
##    #initially set a boolean value to not registered
##    registered = False

##    #process the data submitted in the forms  if its a http post
##    if request.method=="POST":
##        #attempt to grab the information from the raw form inputs
##        #we use the two forms Userform and UserProfileForm
##        user_form = UserForm(data = request.POST)
##        profile_form = UserProfileForm(data = request.POST)

#        ##check if the two forms are valid and process them accordingly
#        #if user_form.is_valid() and profile_form.is_valid():
#        #    #save the users form data to the database
#        #    user = user_form.save()

#        #    #hash the users password with the set password method
#        #    user.set_password(user.password)
#        #    #update the user object
#        #    user.save()

#        #    #handle the profile form
#        #    #dont commit to saving until after setting the user attribute
#        #    profile = profile_form.save(commit=False)
#        #    #set the user attribute
#        #    profile.user=user
#        #    #check if user provided picture and save it if so
#        #    if 'picture' in request.FILES:
#        #        #set the profile picture attribute
#        #        profile.picture = request.FILES['picture']

#        #    #now save the user profile instance
#        #    profile.save()

#        #    #update form registration success variable
#        #    registered = True

#    #    #show errows if any of the forms is invalid
#    #    else:
#    #        #print errors to the terminal
#    #        print profile_form.errors, user_form.errors

#    ##display the forms to the user
#    #else: 
#    #    user_form = UserForm()
#    #    profile_form = UserProfileForm()

#    ##render the template depending on the context
#    #return render(request, 'news/register.html', {'user_form':user_form, 'profile_form':profile_form, 'registered':registered})


##def user_login(request):
##    """code to log-in the user through a form and authenticate him"""
##    #get the relevant information from the form when the use clicks the login buttom
##    # only process this form if the request to this view is a post request
##    if request.method == "POST":
##        #gather the username and password from the form
##        username= request.POST.get('username')
##        password = request.POST.get('password')

##        #use django machinery to authenticate.
##        #the authenticate method returns a user object if authenticated
##        user = authenticate(username=username, password=password)

##        #allow login of user if authenticated
##        if user:
##            #check if the account is still active
##            if user.is_active:
##                #login in the user
##                login(request, user)
##                #redirect user to the home page
##                return HttpResponseRedirect(reverse('news:index'))
##            else:
##                #inform user that he has been disabled
##                return HttpResponse("Your news account has been disabled")
##        else: #bad login details were provided so we cant login the user
##            message= "Invalid login details: {0}, {1}".format(username, 'x'*len(password))
#    #        return HttpResponse(message)
#    #else: #form is been accessed via the get method so display the form
#    #    return render(request, 'news/login.html', {})

###wrapper function for login_required function
##@login_required
##def restricted(request):
##    return HttpResponse("You are seeing this text because you're not logged in")


###wrapper for log-out
###ensure that only user who are already logged in can log out by using the restricted function above
##@login_required
##def user_logout(request):
##    #since we know that the user is logged in, we can log-out the user
##    logout(request)
##    #redirect the user to the homepage
##    return HttpResponseRedirect(reverse('news:index'))


##def visitor_cookie_handler(request, response):
##    """
##    this function gets the number of visitors to our site
##    uses cookies stored on the clients side
##    """
##    #use cookies.get function to obtain the cookie that tracks the number of visits
##    #if the cookie exists, the value returned is cast to an integer
##    #if the cookie does not exists, return 1
##    visits = int(request.COOKIES.get('visits', 1)) #cookie that counts the number of visits to our site...all cookies are returned as strings
##    #get the cookie that tracks the last time of visit from the request
##    last_visit_cookie = request.COOKIES.get('last_visit', str(datetime.now())) 
##    #strip the last visit cookie to get out the time of visit
##    last_visit_time = datetime.strptime(last_visit_cookie[:-7], '%Y-%m-%d %H:%M:%S') 
##    #check last visit time if it is more than one day old
##    if (datetime.now()-last_visit_time).days>1:
##        #increase the visits counter cookie
##        visits = visits + 1
##        #update the last visit cookie now that we've updated the last visit counter cookie
##        #use the set cookie method of the response
##        response.set_cookie('last_visit', str(datetime.now()))
##    #if last visit cookie is less than one day
##    else:
##        #update and set the last visit cookie in the response to the last visit cookie in the request
##        last_visit_cookie = response.set_cookie('last_visit', last_visit_cookie)
##    #update and set the visits cookie in the response to the visit cookie counter
##    response.set_cookie('visits',visits)


#def get_server_side_cookie(request, cookie, defualt_value = None):
#    """ Helper function to get cookie value from the server side session"""
#    val = request.session.get(cookie)
#    if not val:
#        val = defualt_value
#    return val

#def visitor_cookie_handler(request):
#    """
#    this function gets the number of visitors to our site
#    uses the get server side cookies to obtain session cookies stored on the server side
#    """
#    #use cookies.get function to obtain the cookie that tracks the number of visits
#    #if the cookie exists, the value returned is cast to an integer
#    #if the cookie does not exists, return 1
#    visits = int(get_server_side_cookie(request, 'visits', '1'))#cookie that counts the number of visits to our site...all cookies are returned as strings
#    #get the server side cookie that tracks the last time of visit from the request
#    last_visit_cookie = get_server_side_cookie(request, 'last_visit', str(datetime.now()))
#    #strip the last visit cookie to get out the time of visit
#    last_visit_time = datetime.strptime(last_visit_cookie[:], '%Y-%m-%d %H:%M:%S.%f') 
#    #check last visit time if it is more than one day old--changed to seconds for testing
#    if (datetime.now()-last_visit_time).seconds>1:
#        #increase the visits counter cookie
#        visits = visits + 1
#        #update the last visit cookie now that we've updated the last visit counter cookie
#        #use the request.session dictionary to update
#        request.session['last_visit'] = str(datetime.now())
#    else:
#        #set the last visit cookie
#        #use the request.session dictionary to update
#        request.session['last_visit'] = last_visit_cookie
    
#    #update and set the visit cookie
#    request.session['visits'] = visits
  
def track_article_url(request):
    """
    function that counts the number of times an article is clicked
    Used as a measure of popularity
    """

    article_id = None
    url = '/news/'
    if request.method == 'GET':
        if 'article_id' in request.GET:
            article_id = request.GET['article_id']
            try:
                article = Article.objects.get(id=article_id)
                article.views = article.views + 1
                article.save()
                url = article.url
            except:
                pass

    return redirect(url)  