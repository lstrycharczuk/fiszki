from django.urls import path
from .views import *

urlpatterns = [
    path('', fiszki, name='fiszki'),
    path('create_new/', new_fiszki, name='create_new'),
    path('word_list/', words, name='word_list'),
    path('revision/', revision, name='revision'),
]
