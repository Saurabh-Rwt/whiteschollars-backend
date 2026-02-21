from django.urls import path
from . import views
from .views import CourseListAPIView, get_course_full_data, get_course_page

urlpatterns = [
    path('login/', views.user_login, name='login'),
    path('logout/', views.user_logout, name='logout'),

    path('course/<slug:course_slug>/', views.dashboard, name='dashboard_course'),
    path('', views.dashboard, name='dashboard'),
    path('courses/', views.course_list, name='course_list'),
    path('courses/add/', views.add_course, name='add_course'),
    path('courses/edit/<int:pk>/', views.edit_course, name='edit_course'),
    path('courses/delete/<int:pk>/', views.delete_course, name='delete_course'),
    path('sections/reorder/', views.reorder_sections, name='reorder_sections'),
    path('sections/toggle/', views.toggle_section, name='toggle_section'),
    path('add-section/', views.add_section, name='add_section'),
    path('sections/edit/<int:pk>/', views.edit_section, name='edit_section'),
    path('sections/delete/<int:pk>/', views.delete_section, name='delete_section'),
    path('add-key-highlight/', views.add_key_highlight, name='add_key_highlight'),
    path('add-accreditation-and-certification/', views.add_accreditation_and_certification, name='add_accreditation_and_certification'),
    path('add-why-choose/', views.add_why_choose, name='add_why_choose'),
    path('add-mentor/', views.add_mentor, name='add_mentor'),
    path('add-program-highlight/', views.add_program_highlight, name='add_program_highlight'),
    path('add-career-assistance/', views.add_career_assistance, name='add_career_assistance'),
    path('add-career-transition/', views.add_career_transition, name='add_career_transition'),
    path('add-our-alumni/', views.add_our_alumni, name='add_our_alumni'),
    path('add-on-campus-class/', views.add_on_campus_class, name='add_on_campus_class'),
    path('add-fee-structure/', views.add_fee_structure, name='add_fee_structure'),
    path('add-program-for/', views.add_program_for, name='add_program_for'),
    path('add-why-white-scholars/', views.add_why_white_scholars, name='add_why_white_scholars'),
    path('add-listen-our-expert/', views.add_listen_our_expert, name='add_listen_our_expert'),

    path('api/courses/', CourseListAPIView.as_view(), name='course-list'),
    path('api/courses/<slug:slug>', get_course_full_data, name='course-full-data'),
    path('api/courses/<slug:slug>/page/', get_course_page, name='course-page'),
]
