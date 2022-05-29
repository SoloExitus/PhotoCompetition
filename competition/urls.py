from django.urls import path
from competition import views

urlpatterns = [
    path('', views.HomePageView.as_view(), name='main'),
    path('post/<int:pk>', views.PostDetailView.as_view(), name='post'),
    path('profile/', views.ProfileView.as_view(), name='profile'),
    path('add/', views.PhotoPostCreateView.as_view(), name='create'),
    path('post/edit/<int:pk>', views.PhotoPostEditView.as_view(), name='edit'),
]