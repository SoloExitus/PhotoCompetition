from django.urls import path
from competition import views

urlpatterns = [
    path('', views.HomePageView.as_view(), name='main'),
    path('post/<int:post_id>', views.PostDetailView.as_view(), name='post'),
    path('profile/', views.ProfileView.as_view(), name='profile'),
    path('add/', views.PhotoPostCreateView.as_view(), name='add'),
    path('post/<int:post_id>', views.PhotoPostEditView.as_view(), name='update'),
]