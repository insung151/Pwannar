from django.urls import path
from InformationBoard import views
from django.contrib import admin

app_name = 'InformationBoard'

urlpatterns = [
    path('', views.MainPage, name='mainpage'),
    path('admin/', admin.site.urls),
    path('create/', views.inform_create, name='inform_create'),
    path('detail/<int:pk>/', views.inform_detail, name='inform_detail'),
    path('list/', views.inform_list, name='inform_list'),
    path('update/<int:pk>/', views.inform_update, name='inform_update'),
    path('delete/<int:pk>/', views.inform_delete, name='inform_delete'),
    path('like/<int:pk>/', views.article_like, name='article_like'),
    path('<int:pk>/edit/', views.inform_edit, name='inform_edit'),
]