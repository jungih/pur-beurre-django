from django.urls import path
from . import views
from .views import FoodsDelete

app_name = 'foods'
urlpatterns = [
    path('', views.index),
    path('search/', views.search, name='search'),
    path('<str:code>/', views.subs, name='subs'),
    path('mentions-legales/', views.mentions, name='mentions'),
    path('myfoods/', views.myfoods, name='myfoods'),
    path('delete/<int:pk>', FoodsDelete.as_view(), name='delete'),
    path('detail/<str:code>', views.detail, name='detail'),
    path('save/', views.save, name='save'),
]
