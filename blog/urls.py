from django.contrib.auth.views import LogoutView
from django.urls import path
from django.views.generic import TemplateView

from blog import views

urlpatterns = [
    path('', views.PostListView.as_view(), name='index'),
    path('login/', views.Login.as_view(), name='login'),
    path('signup/', views.SignUp.as_view(), name='signup'),
    path('logout/', LogoutView.as_view(), name="logout"),
    path('dashboard/', views.DashboardListView.as_view(), name="dashboard"),
    path('post/', views.PostCreateView.as_view(), name='post'),
    path('update/<int:pk>', views.PostUpdate.as_view(), name="updatepost"),
    path('delete/<int:pk>', views.PostDelete.as_view(), name="deletepost"),

]
