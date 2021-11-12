from django.urls import path
from competition import views


urlpatterns = [
    path('', views.HomePageView.as_view(), name='main')
]