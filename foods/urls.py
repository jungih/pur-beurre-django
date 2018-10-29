from django.urls import path
from . import views

app_name = 'foods'
urlpatterns = [
    path('', views.index),
    path('search/', views.search, name='search'),
    path('<str:category>/<str:code>/', views.subs, name='subs'),
    path('save/', views.save, name='save'),
]
