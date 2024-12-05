from django.urls import path
from . import views

app_name = 'voting_app'

urlpatterns = [
    path('', views.home, name='home'),  
    path('vote/', views.vote, name='vote'), 
    path('count/', views.count_votes, name='count_votes'), 
]
