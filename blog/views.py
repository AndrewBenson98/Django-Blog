
from django.shortcuts import render, get_object_or_404, redirect
from .models import Post
from django.views.generic import (ListView, DeleteView, CreateView, DetailView, UpdateView)
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.contrib.auth.models import User
from django.utils import timezone


# Create your views here.
# def home(request):
#     posts = Post.objects.all()
#     return render(request, 'blog/home.html', {'posts': posts})

class PostListView(ListView):
    model = Post
    template_name = 'blog/home.html'
    context_object_name ='posts'
    paginate_by = 5

    def get_queryset(self):
        #Get username from url 
        return Post.objects.filter(date_published__isnull=False).order_by('date_published')

class UserPostListView(ListView):
    model = Post
    template_name = 'blog/user_posts.html'
    context_object_name ='posts'
    paginate_by = 5
    
    def get_queryset(self):
        #Get username from url 
        user = get_object_or_404(User, username=self.kwargs.get('username'))
        return Post.objects.filter(author=user,date_published__isnull=False).order_by('date_published')

class UserDraftListView(ListView):
    model = Post
    template_name = 'blog/user_drafts.html'
    context_object_name ='posts'
    paginate_by = 5
    
    def get_queryset(self):
        #Get username from url 
        user = get_object_or_404(User, username=self.kwargs.get('username'))
        return Post.objects.filter(author=user, date_published__isnull=True).order_by('date_posted')

class PostDetailView(DetailView):
    model = Post
    #template_name = 'blog/post_detail.html'

class PostCreateView(LoginRequiredMixin, CreateView):
    model = Post
    fields = ['title', 'content']
    #template_name = 'blog/post_form.html'

    #Set the author to logged in user when post is made
    def form_valid(self, form):
        form.instance.author = self.request.user
        return super().form_valid(form)


class PostUpdateView(LoginRequiredMixin, UserPassesTestMixin,UpdateView):
    model = Post
    fields = ['title', 'content']
    #template_name = 'blog/post_form.html'

    #Set the author to logged in user when post is made
    def form_valid(self, form):
        form.instance.author = self.request.user
        return super().form_valid(form)
    
    def test_func(self):
        post = self.get_object() #Gets the post we are currently trying to update
        
        #Check if current user is the post author
        if self.request.user == post.author:
            return True
        return False

    #Publishes the post by setting a time for date_published attribute
    def post_publish(request, pk):
        post = get_object_or_404(Post, pk=pk)
        post.date_published = timezone.now()
        post.save()
        return redirect('post-detail', pk=pk)


class PostDeleteView(LoginRequiredMixin, UserPassesTestMixin, DeleteView):
    model = Post
    success_url = '/'
    #template_name = 'blog/post_detail.html'

    def test_func(self):
        post = self.get_object() #Gets the post we are currently trying to update
        
        #Check if current user is the post author
        if self.request.user == post.author:
            return True
        return False

def about(request):
    return render(request, 'blog/about.html', {'title':'About'})

