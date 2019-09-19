from . import views
from django.urls import path, include

urlpatterns = [
    path('accounts/', include('django.contrib.auth.urls')),
    path('', views.PostList.as_view(), name='home'),
    path('<slug:slug>/', views.PostDetail.as_view(), name='post_detail'),
    path('post/<slug:slug>/comment', views.add_comment_to_post, name='add_comment_to_post'),
    path('tag/<str:slug>', views.tag_detail, name='tag_detail_url'),
]
