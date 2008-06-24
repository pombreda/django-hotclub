from django.contrib import admin
from blog.models import Post

class PostAdmin(admin.ModelAdmin):
    list_display  		= ('title', 'publish', 'status')
    list_filter   		= ('publish', 'status')
    search_fields 		= ('title', 'body', 'tease')

admin.site.register(Post, PostAdmin)
