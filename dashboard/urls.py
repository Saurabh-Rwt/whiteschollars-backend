from django.urls import path
from . import views

urlpatterns = [
    path('', views.dashboard, name='dashboard'),
    path('courses/', views.course_list, name='course_list'),
    path('courses/add/', views.add_course, name='add_course'),
    path('courses/edit/<int:pk>/', views.edit_course, name='edit_course'),
    path('courses/delete/<int:pk>/', views.delete_course, name='delete_course'),
    path('add-section/', views.add_section, name='add_section'),
    path('add-key-highlight/', views.add_key_highlight, name='add_key_highlight'),
]
