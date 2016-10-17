from django.contrib import admin

from .models import Feed, Article, UserProfile



class FeedAdmin(admin.ModelAdmin):
    list_display = ('name', 'url', 'is_active')
    prepopulated_fields = {'slug':('name',)}

#class CategoryAdmin(admin.ModelAdmin):
#    #fields that will be displayed on the djangoadmin page
#    list_display = ('name', 'views', 'likes')
#    # automatically pre populate the slug field of the admin model
#    prepopulated_fields = {'slug':('name',)}

class ArticleAdmin(admin.ModelAdmin):
    #fields that will be displayed on the djangoadmin page
    list_display = ('feed', 'title', 'publication_date', 'description')
    

class UserProfileAdmin(admin.ModelAdmin):
    pass

#register the model
admin.site.register(Feed, FeedAdmin)
#admin.site.register(Category, CategoryAdmin)
admin.site.register(Article, ArticleAdmin)
admin.site.register(UserProfile, UserProfileAdmin)



