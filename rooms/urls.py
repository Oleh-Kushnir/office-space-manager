from django.urls import path
from . import views

urlpatterns = [
    path('submit-reading/', views.submit_reading, name='submit_reading'),
]