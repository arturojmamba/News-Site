# urls.py
from django.urls import path, re_path
from .views import VueAppView, main_spa, sign_up, get_profile, update_profile, get_favourite_categories, update_favourite_categories, get_categories, get_all_articles, get_article, get_articles_from_category, get_comments, add_comment, update_comment, delete_comment
from django.contrib.auth.decorators import login_required
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('home/', login_required(main_spa), name='main_spa'),
    path('sign-up/', sign_up, name='sign_up'),

    # Profile
    path('get-profile/', login_required(get_profile), name='get_profile'),
    path('update-profile/', login_required(update_profile), name='update_profile'),
    path('get-favourites/', login_required(get_favourite_categories), name='get_favorite_categories'),
    path('update-favourites/', login_required(update_favourite_categories), name='update_favorite_categories'),

    # Content
    path('get-categories/', login_required(get_categories), name='get_categories'),
    path('articles/', login_required(get_all_articles), name='get_all_articles'),
    path('articles/<int:article_id>/', login_required(get_article), name='get_article'),
    path('categories/<int:category_id>/articles/', login_required(get_articles_from_category), name='get_articles_from_category'),

    # Comments
    path('articles/<int:article_id>/comments/', login_required(get_comments), name='get_comments'),
    path('articles/<int:article_id>/comments/add/', login_required(add_comment), name='add_comment'),
    path('comments/<int:comment_id>/update/', login_required(update_comment), name='update_comment'),
    path('comments/<int:comment_id>/delete/', login_required(delete_comment), name='delete_comment'),

    # Vue App View (Authenticated users only)
    path('', login_required(VueAppView.as_view()), name='home'),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

urlpatterns += [
    re_path(r'^(?!' + settings.MEDIA_URL.lstrip('/') + r').*$', login_required(VueAppView.as_view()), name='vue_app'),
]