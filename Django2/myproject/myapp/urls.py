# myapp/urls.py
from django import views
from django.urls import path
from .views import handle_post_request, index, ajax_update, stat,search, statfull
from . import views

urlpatterns = [
    # path('', index, name='index'),
    path('', views.login_view, name='login'),
    path('index/', views.index, name='index'),
    path('logout/', views.logout_view, name='logout'),
    path('your_post_endpoint/', handle_post_request, name='handle_post_request'),
    path('stat/', stat, name='stat'),
		path('search/', search, name='search'),		
		path('statfull/', statfull, name='statfull'),	
    path('ajax_update/', ajax_update, name='ajax_update'),
]



