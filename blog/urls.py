from django.urls import path
from .views import PostListView, PostDetailView, PostCreateView, PostUpdateView, PostDeleteView, UserPostListView, UserDraftListView, PostView, CommentFormView, PostApprovalListView
from . import views

urlpatterns = [
    path('', PostListView.as_view(), name='blog-home'),
    path('mod/approvals/', PostApprovalListView.as_view(), name='post-approval-list'),
    path('user/<str:username>/', UserPostListView.as_view(), name='user-posts'),
    path('user/<str:username>/drafts/', UserDraftListView.as_view(), name='user-drafts'),
    #path('post/<int:pk>/', PostDetailView.as_view(), name='post-detail'),
    path('post/<int:pk>/', PostView.as_view(), name='post-detail'),
    path('post/new/', PostCreateView.as_view(), name='post-create'),
    path('post/<int:pk>/update/', PostUpdateView.as_view(), name='post-update'),
    path('post/<int:pk>/publish/', PostUpdateView.post_publish, name='post-publish'),
    path('post/<int:pk>/delete/', PostDeleteView.as_view(), name='post-delete'),
    path('post/<int:pk>/approve/',PostApprovalListView.approve_post , name='post-approve'),
    path('post/<int:pk>/comment_delete/<int:cpk>', PostApprovalListView.comment_delete, name='comment-delete'),
    path('post/<int:pk>/comment_approve/<int:cpk>', PostApprovalListView.comment_approve, name='comment-approve'),
    path('about/',views.about, name='blog-about'),
    
]