from django.urls import path
from . import views

app_name = 'planningboard'

urlpatterns = [
    path('list/', views.detail_list, name='list'),
    path('recent/', views.recent, name='recent'),
    path('alphabet/', views.alphabet, name='alphabet'),
    path('get_subregion/<int:pk>', views.get_subregion, name='get_subregion'),
    path('like/<int:pk>', views.like, name='like'),
    path('detail/<int:pk>/', views.detail, name='detail'),
    path('create/', views.create, name='create'),
    path('update/<int:pk>/', views.update, name='update'),
    path('comment/create/<int:detail_pk>/', views.comment_create, name='comment_create'),
    path('detail_list/',views.detail_list_html, name='detail_list_html'),
path('delete/<int:pk>/', views.delete, name='delete'),
]