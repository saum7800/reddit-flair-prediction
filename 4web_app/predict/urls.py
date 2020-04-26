from django.urls import path
from . import views
from django.views.decorators.csrf import csrf_exempt

urlpatterns = [
    path('', views.home, name='predict-home'),
    path('about/', views.about, name='predict-about'),
    path('automated_testing/', csrf_exempt(views.automated_testing), name='predict-automated_testing')
]