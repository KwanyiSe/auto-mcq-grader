from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('create-key/', views.create_answer_key, name='create_key'),
    path('grade/', views.upload_and_grade, name='grade'),
    path('sample/', views.sample_grade, name='sample_grade'),
]