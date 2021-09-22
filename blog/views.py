
from django.forms.forms import Form
from django.shortcuts import render, get_object_or_404, redirect
from .models import Post, Comment
from django.views.generic import (ListView, DeleteView, CreateView, DetailView, UpdateView)
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.contrib.auth.models import User
from django.utils import timezone
from blog.forms import CommentForm
from django.views.generic import FormView
from django.views.generic.detail import SingleObjectMixin
from django.views import View
from django.http import HttpResponseForbidden
from django.urls import reverse, reverse_lazy
from django.contrib import messages
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
        return Post.objects.filter(approved_post=True ,date_published__isnull=False).order_by('-date_published')

class PostApprovalListView(LoginRequiredMixin, UserPassesTestMixin,ListView):
    model = Post
    template_name = 'blog/post_approval.html'
    context_object_name ='posts'
    paginate_by = 5

    def get_queryset(self):
        #Get username from url 
        return Post.objects.filter(approved_post=False ,date_published__isnull=False).order_by('-date_published')

    def test_func(self):
        #Check if current user is the post author
        if  self.request.user.is_superuser:
            return True
        return False

    def approve_post(request,pk):
        post = get_object_or_404(Post, pk=pk)
        post.approve()
        messages.success(request, f'Post has been approved')
        return redirect('post-approval-list')

    def comment_approve(request, pk, cpk):
        comment = get_object_or_404(Comment, pk=cpk)
        comment.approve()
        messages.success(request, f'Comment has been approved')
        return redirect('post-detail', pk=comment.post.pk)

    def comment_delete(request,pk, cpk):
        comment = get_object_or_404(Comment, pk=cpk)
        comment.delete()
        messages.success(request, f'Comment has been deleted')
        return redirect('post-detail', pk=comment.post.pk)

class UserPostListView(ListView):
    model = Post
    template_name = 'blog/user_posts.html'
    context_object_name ='posts'
    paginate_by = 5
    
    def get_queryset(self):
        #Get username from url 
        user = get_object_or_404(User, username=self.kwargs.get('username'))
        return Post.objects.filter(author=user,approved_post=True,date_published__isnull=False).order_by('-date_published')

class UserDraftListView(ListView):
    model = Post
    template_name = 'blog/user_drafts.html'
    context_object_name ='posts'
    paginate_by = 5
    
    def get_queryset(self):
        #Get username from url 
        user = get_object_or_404(User, username=self.kwargs.get('username'))
        return Post.objects.filter(author=user, date_published__isnull=True).order_by('-date_posted')


class PostDetailView(DetailView):
    model = Post
    template_name = 'blog/post_detail.html'


    def get_context_data(self, **kwargs):
        #Adding a form context to the view
        context = super().get_context_data(**kwargs)
        context['form'] = CommentForm()
        
        return context
    

    

class CommentFormView(LoginRequiredMixin,CreateView):
    template_name = 'blog/post_detail.html'
    # form_class = CommentForm
    model = Comment
    fields = ['content']

    def get_success_url(self):
        return reverse_lazy('post-detail', kwargs={'pk': self.object.post.pk})
    
    #Set the author to logged in user when comment is made
    def form_valid(self, form):
        form.instance.author = self.request.user
        form.instance.post =Post.objects.get(pk =self.kwargs.get('pk'))
        form.save()
        return super().form_valid(form)
    

    
    
    
#Combination of Post Detail view and Comment Create view
class PostView(View):
    def get(self, request, *args, **kwargs):
        view = PostDetailView.as_view()
        return view(request, *args, **kwargs)

    def post(self, request, *args, **kwargs):
        view = CommentFormView.as_view()
        return view(request, *args, **kwargs)


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
        messages.info(request, f'Post has been published! A moderator must approve it before displaying on the site.')
        return redirect('post-detail', pk=pk)


class PostDeleteView(LoginRequiredMixin, UserPassesTestMixin, DeleteView):
    model = Post
    success_url = '/'
    #template_name = 'blog/post_confirm_delete.html'

    def test_func(self):
        post = self.get_object() #Gets the post we are currently trying to update
        
        #Check if current user is the post author
        if self.request.user == post.author or self.request.user.is_superuser:
            return True
        return False

def about(request):
    return render(request, 'blog/about.html', {'title':'About'})


