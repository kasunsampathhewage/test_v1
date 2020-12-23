from django.urls import path

from. import views
from django.conf.urls import url

urlpatterns =[
    
    url('home/',views.indexpage,name='home'),
    path('brand/',views.brand, name='brand'),
    path('comparision/',views.comparision, name='comparision'),
    path('predict/',views.predict, name='predict'),
      
]