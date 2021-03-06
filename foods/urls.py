from django.urls import path
from . import views
# from .views import DeleteFoods

app_name = 'foods'
urlpatterns = [
    path('', views.index, name='index'),
    path('search/', views.search, name='search'),
    path('subs/<str:code>/', views.subs, name='subs'),
    path('mentions-legales/', views.mentions, name='mentions'),
    path('myfoods/', views.myfoods, name='myfoods'),
    # path('delete/<int:pk>', DeleteFoods.as_view(), name='delete'),
    path('<int:id>/delete', views.delete,
         {'sub_id': None}, name='delete_selected'),
    path('<int:id>/<int:sub_id>/delete', views.delete, name='delete_sub'),
    path('detail/<str:code>', views.detail, name='detail'),
    path('save/', views.save, name='save'),
]
