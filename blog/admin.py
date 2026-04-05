from django.contrib import admin
from .models import Post, Category, Tag, Comment, Follow, UserProfile

@admin.register(Post)
class PostAdmin(admin.ModelAdmin):
    list_display = ['title','author','status','created_at']
    list_filter  = ['status','categories']
    prepopulated_fields = {'slug': ('title',)}
    filter_horizontal   = ['categories','tags','likes','bookmarks']

@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    prepopulated_fields = {'slug': ('name',)}

admin.site.register(Tag)
admin.site.register(Comment)
admin.site.register(Follow)
admin.site.register(UserProfile)