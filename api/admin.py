# api/admin.py

from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import User, Category, Article, Comment, UsersFavouriteCategory


class CategoryAdmin(admin.ModelAdmin):
    list_display = ('id', 'name')

class ArticleAdmin(admin.ModelAdmin):
    list_display = ('get_category_id', 'get_category_name', 'id', 'title', 'author_name')
    ordering = ('category__id',)

    def get_category_id(self, obj):
        return obj.category.id if obj.category else None
    get_category_id.short_description = 'Category ID'
    get_category_id.admin_order_field = 'category__id'

    def get_category_name(self, obj):
        return obj.category.name if obj.category else None
    get_category_name.short_description = 'Category Name'
    get_category_name.admin_order_field = 'category__name'

    def author_name(self, obj):
        return obj.author.email if obj.author else "No Author"
    author_name.short_description = 'Author'

    def save_model(self, request, obj, form, change):
        if not obj.pk and not obj.author:
            obj.author = request.user
        super().save_model(request, obj, form, change)

class CommentAdmin(admin.ModelAdmin):
    list_display = ('id', 'short_content', 'author_email', 'article_title')
    ordering = ('id',)

    def short_content(self, obj):
        return (obj.content[:50] + '...') if len(obj.content) > 50 else obj.content
    short_content.short_description = 'Content'

    def author_email(self, obj):
        return obj.author.email if obj.author else "No Author"
    author_email.short_description = 'Author'

    def article_title(self, obj):
        return obj.article.title if obj.article else "No Article"
    article_title.short_description = 'Article'

    search_fields = ('author__email', 'article__title', 'content')
    list_filter = ('author__email', 'article__title')


@admin.register(User)
class CustomUserAdmin(UserAdmin):
    model = User
    list_display = ['email', 'is_staff', 'is_active']
    list_filter = ['email', 'is_staff', 'is_active']
    fieldsets = (
        (None, {'fields': ('email', 'password', 'date_of_birth', 'profile_image')}),
        ('Permissions', {'fields': ('is_staff', 'is_active')}),
    )
    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('email', 'date_of_birth', 'profile_image', 'password1', 'password2', 'is_staff', 'is_active')}
        ),
    )
    search_fields = ('email',)
    ordering = ('email',)

admin.site.register(Category, CategoryAdmin)
admin.site.register(Article, ArticleAdmin)
admin.site.register(Comment, CommentAdmin)
admin.site.register(UsersFavouriteCategory)