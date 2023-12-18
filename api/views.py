# views.py
from django.http import JsonResponse
from django.shortcuts import render, redirect
from django.contrib.auth import get_user_model
from .forms import *
from django.contrib import messages
import json
from django.contrib.auth.decorators import login_required
import requests
from django.views.generic import View
from django.http import HttpResponse
from django.core.exceptions import ValidationError

User = get_user_model()

def main_spa(request):
    # Redirect to the Vue app
    return redirect('/')

class VueAppView(View):
    def get(self, request, *args, **kwargs):
        print("VueAppView URL:", request.path)
        vue_dev_server_url = 'http://localhost:5174'

        path = request.path
        url_to_fetch = f"{vue_dev_server_url}{path}"

        response = requests.get(url_to_fetch)

        return HttpResponse(response.content, content_type=response.headers['Content-Type'])

def sign_up(request):
    if request.method == 'POST':
        form = SignUpForm(request.POST)
        if form.is_valid():
            email = form.cleaned_data.get('email')
            if User.objects.filter(email=email).exists():
                messages.error(request, "A user with this email already exists.")
                return render(request, 'registration/sign_up.html', {'form': form})

            user = form.save()
            
            return redirect('/accounts/login')
        else:
            messages.error(request, "Please correct the error below.")
    else:
        form = SignUpForm()
    
    return render(request, 'registration/sign_up.html', {"form": form})

#PROFILE --------------------------------------------------------------------------------

@login_required
def get_profile(request):
    if request.method == 'GET':
        user = request.user
        profile_data = {
            'email': user.email,
            'date_of_birth': user.date_of_birth.strftime('%Y-%m-%d') if user.date_of_birth else '',
            'profile_image' : user.profile_image.url if user.profile_image else None
        }
        return JsonResponse(profile_data)
    return JsonResponse({'error':'Invlid request'}, status = 400)

@login_required
def update_profile(request):
    if request.method != "POST":
        return JsonResponse({"error": "Invalid request method"}, status=400)

    user = request.user

    email = request.POST.get('email')
    date_of_birth = request.POST.get('date_of_birth')

    if email and email != user.email:
        if User.objects.filter(email=email).exclude(pk=user.pk).exists():
            return JsonResponse({"error": "Email in use"}, status=400)
        user.email = email

    if date_of_birth:
        user.date_of_birth = date_of_birth

    profile_image = request.FILES.get('profile_image')
    if profile_image:
        user.profile_image = profile_image

    try:
        user.full_clean()
        user.save()
        return JsonResponse({'message': 'Updated Profile Successfully'}, status=200)
    except ValidationError as e:
        return JsonResponse({'errors': e.message_dict}, status=400)

#CATEGORIES --------------------------------------------------------------------------------

def get_categories(request):
    if request.method == 'GET':
        categories = Category.objects.all()
        categories_data = [{'id': category.id, 'name': category.name} for category in categories]
        return JsonResponse({'categories': categories_data})
    return JsonResponse({'error': 'Method not allowed'}, status = 405)

@login_required
def get_favourite_categories(request):
    if request.method == 'GET':
        favourite_categories = request.user.users_favourite_categories.select_related('category')
        category_data = [{'id': category.category_id, 'name': category.category.name} for category in favourite_categories]
        return JsonResponse({'favourite_categories': category_data}, status=200)
    return JsonResponse({'error': 'Invalid request'}, status=400)


@login_required
def update_favourite_categories(request):
    if request.method == 'PUT':
        try:
            data = json.loads(request.body)
            cat_ids = data.get('categories',[])
        except json.JSONDecodeError:
            return JsonResponse({'error':'Invalid JSON'}, status = 400)
        
        if not all(Category.objects.filter(id=cat_id).exists() for cat_id in cat_ids):
            return JsonResponse({'error':'invalid category id'}, status = 400)
        
        user = request.user
        user.users_favourite_categories.all().delete()

        for cat_id in cat_ids:
            category = Category.objects.get(id=cat_id)
            UsersFavouriteCategory.objects.create(user=user, category=category)
        return JsonResponse({'message':'favourite category/categories updated'}, status = 200)
        
    return JsonResponse({'error':'Invalid JSON'}, status = 400)


#ARTICLES --------------------------------------------------------------------------------

def get_all_articles(request):
    if request.method == 'GET':
        articles = Article.objects.all().values('id', 'title')
        return JsonResponse({'articles': list(articles)})
    else:
        return JsonResponse({'error': 'Method not allowed'}, status=405)

def get_article(request, article_id):
    if request.method == 'GET':
        article = Article.objects.get(pk=article_id)
        article_data = {
            'id': article.id,
            'title': article.title,
            'content': article.content,
            'published': article.published,
            'author_email': article.author.email if article.author else None,
            'category_id': article.category.id if article.category else None,
            'category_name': article.category.name if article.category else None
        }
        return JsonResponse(article_data)
    else:
        return JsonResponse({'error': 'Method not allowed'}, status=405)
    
def get_articles_from_category(request, category_id):
    if request.method == 'GET':
        articles = Article.objects.filter(category_id = category_id).values('id','title','content','published','author__email')
        return JsonResponse({'articles': list(articles)})
    return JsonResponse({'error': 'Method not allowed'}, status = 405)


#COMMENTS --------------------------------------------------------------------------------

@login_required
def get_comments(request, article_id):
    try:
        article = Article.objects.get(pk=article_id)
    except Article.DoesNotExist:
        return JsonResponse({'error': 'Article not found'}, status=404)

    comments = Comment.objects.filter(article=article).select_related('author')

    comments_dict = {comment.id: {
        'id': comment.id, 
        'content': comment.content, 
        'author__email': comment.author.email, 
        'parent_id': comment.parent_id,
        'uploaded':comment.uploaded,
        'replies': []
    } for comment in comments}

    for comment in comments:
        if comment.parent_id and comment.parent_id in comments_dict:
            comments_dict[comment.parent_id]['replies'].append(comments_dict[comment.id])

    top_level_comments = [comment for comment in comments_dict.values() if not comment['parent_id']]

    return JsonResponse({'comments': top_level_comments}, safe=False)

@login_required
def add_comment(request, article_id):
    if request.method == 'POST':
        data = json.loads(request.body)

        try:
            article = Article.objects.get(pk=article_id)
        except Article.DoesNotExist:
            return JsonResponse({'error': 'Article not found'}, status=404)

        parent_id = data.get('parent_id')
        if parent_id:
            try:
                Comment.objects.get(pk=parent_id, article=article)
            except Comment.DoesNotExist:
                return JsonResponse({'error': 'Parent comment not found or does not belong to the same article'}, status=400)

        comment = Comment(article=article, author=request.user, content=data['content'], parent_id=parent_id)
        comment.save()
        return JsonResponse({'message': 'Comment added', 'comment_id': comment.id}, status=201)
    else:
        return JsonResponse({'error': 'Method not allowed'}, status=405)

@login_required
def update_comment(request, comment_id):
    if request.method == 'PUT':
        data = json.loads(request.body)
        try:
            comment = Comment.objects.get(id=comment_id, author=request.user)
            comment.content = data['content']
            comment.save()
            return JsonResponse({'message': 'Comment updated'})
        except Comment.DoesNotExist:
            return JsonResponse({'error': 'Comment not found or not authorized'}, status=404)
    else:
        return JsonResponse({'error': 'Method not allowed'}, status=405)

@login_required
def delete_comment(request, comment_id):
    if request.method == 'DELETE':
        try:
            comment = Comment.objects.get(id=comment_id, author=request.user)
            comment.delete()
            return JsonResponse({'message': 'Comment deleted'})
        except Comment.DoesNotExist:
            return JsonResponse({'error': 'Comment not found or not authorized'}, status=404)
    else:
        return JsonResponse({'error': 'Method not allowed'}, status=405)
