from django.contrib import admin
from django.urls import path, include
from main import views
from django.conf.urls.static import static

urlpatterns = [
    path('main/',views.main,name='main'),
    path('datasetup/',views.datasetup,name='datasetup'),
    path('output/',views.output,name='output'),


    
]
from django.conf import settings
from django.conf.urls.static import static

urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

