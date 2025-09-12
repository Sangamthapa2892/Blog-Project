from django.shortcuts import render, redirect, get_object_or_404
from .models import *
from . forms import CustomUserCreationForm, LoginForm, BlogForm, CommentForm, EditProfileForm
from django.contrib import messages
from datetime import datetime, timedelta
from django.core.mail import send_mail
from django.template.loader import render_to_string
from django.contrib.auth import get_user_model
from django.contrib.auth import authenticate, login, logout
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.contrib.auth.decorators import login_required
from django.urls import reverse     
from django.urls import reverse_lazy
from django.core.paginator import Paginator
from django.core.mail import EmailMessage
from django.template.loader import render_to_string
from django.utils import timezone
from django.conf import settings
from django.contrib.auth.views import PasswordResetView

# Create your views here.
def home(request):
    User = get_user_model()
    admin_user = User.objects.get(username='admin1')
    admin_posts = Blog.objects.filter(author=admin_user).order_by('-created_at')
    paginator = Paginator(admin_posts, 4)  # Show 5 posts per page
    page = request.GET.get('page')
    try:
        posts = paginator.page(page)
    except PageNotAnInteger:
        posts = paginator.page(1)
    except EmptyPage:
        posts = paginator.page(paginator.num_pages)

    return render(request, 'index/home.html', {'posts': posts})


def signup_view(request):
    if request.method == 'POST':
        name = request.POST.get('username')
        email = request.POST.get('email')
        print(name,email)
        form = CustomUserCreationForm(request.POST, request.FILES)
        if form.is_valid():
            user = form.save(commit=False)
            user.save()
            messages.success(request, "Account created successfully!")
            subject = "Your form has been submitted successfully"
            message = render_to_string('user/register_msg.html', {'name':name, 'date':datetime.now()})
            from_email = settings.EMAIL_HOST_USER
            recipient_list = [email]
            send_mail(subject,message,from_email,recipient_list,fail_silently=False)
            return redirect('login') 
        else:
            messages.error(request, 'Please correct errors below.')
    else:
        form = CustomUserCreationForm()
    return render(request, 'user/signup.html', {'form':form})

def login_view(request):
    if request.method == 'POST':
        form = LoginForm(request.POST)
        if form.is_valid():
            username = form.cleaned_data['username']
            password = form.cleaned_data['password']
            user = authenticate(request, username=username, password=password)
            if user is not None:
                login(request, user)
                return redirect('blog_list')  # or wherever you want to go
            else:
                form.add_error(None, 'Invalid credentials')
    else:
        form = LoginForm()
    return render(request, 'user/login.html', {'form':form, 'fixed_footer': True})



def logout_view(request):
    logout(request)
    messages.success(request, "You have been logged out successfully.")
    return redirect('home')  # or redirect to 'home' or any landing page

def blog(request):
    search = request.GET.get('search')
    filter_type = request.GET.get('filter')  # 'recent', 'popular', or None
    if search:
        blog_list = Blog.objects.filter(title__icontains=search)
    else:
        blog_list = Blog.objects.all()
    post_count = blog_list.count()
    if filter_type == 'recent':
        blog_list = blog_list.order_by('-created_at')
    elif filter_type == 'popular':
        blog_list = blog_list.annotate(comment_count=Count('comments')).order_by('-comment_count')
    else:
        blog_list = blog_list.order_by('-created_at')
    paginator = Paginator(blog_list, 6)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    return render(request, 'index/blog.html', {
        'page_obj': page_obj,
        'filter_type': filter_type,
        'search': search,
        'post_count': post_count
    })

@login_required(login_url=reverse_lazy('login'))
def create_blog(request):
    if request.method == 'POST':
        form = BlogForm(request.POST, request.FILES)
        if form.is_valid():
            blog = form.save(commit=False)
            blog.author = request.user  # Assign logged-in user as author
            blog.save()
            messages.success(request, "Blog published successfully!")
            return redirect('blog_list')  # Replace with your blog listing URL name
        else:
            messages.error(request, "Please correct the errors below.")
    else:
        form = BlogForm()
    return render(request, 'blog/create_blog.html', {'form':form})

def blog_detail(request, slug):
    post = get_object_or_404(Blog, slug=slug)
    # Only top-level comments for pagination
    comments = post.comments.filter(approved=True, parent__isnull=True).order_by('-created_at')
    comment_count = post.comments.filter(approved=True).count()
    # Track views
    view_key = f'viewed_post_{post.id}'
    if not request.session.get(view_key):
        post.views += 1
        post.save(update_fields=['views'])
        request.session[view_key] = True
    paginator = Paginator(comments, 3)
    page_number = request.POST.get('page') or request.GET.get('page')
    comments_page = paginator.get_page(page_number)
    # Handle comment/reply submission
    if request.method == 'POST':
        if not request.user.is_authenticated:
            messages.error(request, "You must be logged in to post a comment.")
            return redirect(f"{reverse('login')}?next={request.path}")
        form = CommentForm(request.POST)
        if form.is_valid():
            parent_id = request.POST.get('parent_id')
            parent_comment = None
            if parent_id:
                parent_comment = Comment.objects.filter(id=parent_id, blog=post).first()
            comment = form.save(commit=False)
            comment.blog = post
            comment.author = request.user
            comment.parent = parent_comment
            comment.approved = True
            comment.save()
            messages.success(request, "Your comment was posted successfully!")
            return redirect(f'{reverse("blog_detail", kwargs={"slug": slug})}?page={page_number}#comments')
    else:
        form = CommentForm()

    return render(request, 'blog/blog_detail.html', {
        'post': post,
        'comments_page': comments_page,
        'form': form,
        'comment_count': comment_count
    })

@login_required
def edit_comment(request, comment_id):
    comment = get_object_or_404(Comment, id=comment_id, author=request.user)
    if request.method == 'POST':
        form = CommentForm(request.POST, instance=comment)
        if form.is_valid():
            form.save()
            messages.success(request, "Comment updated successfully.")
            return redirect(f'{comment.blog.get_absolute_url()}#comments')
    else:
        form = CommentForm(instance=comment)
    return render(request, 'blog/edit_comment.html', {'form': form})

@login_required
def delete_comment(request, comment_id):
    comment = get_object_or_404(Comment, id=comment_id, author=request.user)
    blog_slug = comment.blog.slug
    comment.delete()
    messages.success(request, "Comment deleted successfully.")
    return redirect(f"{reverse('blog_detail', kwargs={'slug': blog_slug})}#comments")

@login_required    
def profile_view(request):
    user = request.user
    return render(request, 'user/profile.html', {'user': user, 'fixed_footer': True})

@login_required
def edit_profile(request):
    user = request.user
    if request.method == 'POST':
        form = EditProfileForm(request.POST, request.FILES, instance=user)
        if form.is_valid():
            form.save()
            return redirect('profile')  # or redirect to a success page
    else:
        form = EditProfileForm(instance=user)
    return render(request, 'user/edit_profile.html', {'form': form, 'user': user})

@login_required
def mypost(request):
    user = request.user
    search = request.GET.get('search')
    filter_type = request.GET.get('filter')
    blogs = Blog.objects.filter(author=user).order_by('-created_at')
    if search:
        blogs = blogs.filter(title__icontains=search)
    paginator = Paginator(blogs, 6)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    post_count = blogs.count()
    return render(request, 'blog/mypost.html', {
        'fixed_footer': True,
        'blogs': blogs,
        'page_obj': page_obj,
        'filter_type': filter_type,
        'search': search,
        'post_count': post_count
    })
@login_required
def edit_blog(request, slug):
    blog = get_object_or_404(Blog, slug=slug, author=request.user)

    if request.method == 'POST':
        form = BlogForm(request.POST, request.FILES, instance=blog)
        if form.is_valid():
            form.save()
            return redirect('mypost')  # or redirect to blog detail
    else:
        form = BlogForm(instance=blog)

    return render(request, 'blog/edit_blogpost.html', {'form': form, 'blog': blog})

@login_required
def delete_blog(request, slug):
    blog = get_object_or_404(Blog, slug=slug, author=request.user)
    blog.delete()
    return redirect('mypost')


def aboutus(request):
    return render(request, 'index/aboutus.html')

def contactus(request):
    if request.method == 'POST':
        name = request.POST.get('name', '').strip()
        email = request.POST.get('email', '').strip()
        message_text = request.POST.get('message', '').strip()
        if not name or not email or not message_text:
            messages.error(request, "All fields are required.")
            return redirect('contact')
        Contact.objects.create(name=name, email=email, message=message_text)
        messages.success(request, "Message sent successfully!")
        subject = "Contact Us"
        html_message = render_to_string('user/contact_msg.html', {
            'name': name,
            'date': timezone.now()
        })
        from_email = settings.EMAIL_HOST_USER
        recipient_list = [email]
        email_msg = EmailMessage(subject, html_message, from_email, recipient_list)
        email_msg.content_subtype = "html"
        email_msg.send(fail_silently=False)
        return redirect('contact')
    return render(request, 'index/contact.html')

class CustomPasswordResetView(PasswordResetView):
    email_template_name = 'user/password_reset_email.html'
    success_url = reverse_lazy('password_reset_done')
    template_name = 'user/password_reset_form.html'

    def get_email_context(self):
        context = super().get_email_context()
        context['domain'] = settings.DEFAULT_DOMAIN
        return context

def redirect_with_next(request, default='home'):
    return redirect(request.GET.get('next') or reverse(default))