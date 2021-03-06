"""keralaschools URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path
from schools.views import home, school_view, schools, sub_districts, parse_a_school
urlpatterns = [
    path('admin/', admin.site.urls),
    path('', home, name='home'),
    path('school/<code>/',school_view, name='school_view'),
    path('schools/',schools, name='schools'),
    path('schools/<int:district>/',sub_districts, name='sub_districts'),
    path('parse/',parse_a_school, name='parse_a_school'),
]
