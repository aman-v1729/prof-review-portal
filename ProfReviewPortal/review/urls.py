from django.urls import path
from . import views
from .views import (
	ProfCreateView, 
	CourseCreateView, 
	CourseReviewDetailView, 
	CourseReviewCreateView, 
	CourseReviewUpdateView,
	CourseReviewDeleteView,
	ProfReviewDetailView, 
	ProfReviewCreateView, 
	ProfReviewUpdateView,
	ProfReviewDeleteView
)

urlpatterns = [
	path('', views.home, name = 'review-home'),
	path('professor/', views.findprof, name = 'review-findprof'),
	path('course/', views.findcourse, name = 'review-findcourse'),
	path('professor/new/', ProfCreateView.as_view(), name = 'addprof'),
	path('course/new/', CourseCreateView.as_view(), name = 'addcourse'),
	path('course/<slug:cname>/', views.findcoursename, name = 'review-find-course-name'),
	path('professor/<int:pk>/', views.findprofname, name = 'review-find-prof-name'),
	path('course/<slug:cname>/review/<int:pk>/', CourseReviewDetailView.as_view(), name = 'course-review-detail'),
	path('course/<slug:cname>/review/new/', CourseReviewCreateView.as_view(), name = 'course-review-create'),
	path('course/<slug:cname>/review/<int:pk>/edit/', CourseReviewUpdateView.as_view(), name = 'course-review-update'),
	path('course/<slug:cname>/review/<int:pk>/delete/', CourseReviewDeleteView.as_view(), name = 'course-review-delete'),
	path('professor/<int:ppk>/review/<int:pk>/', ProfReviewDetailView.as_view(), name = 'prof-review-detail'),
	path('professor/<int:ppk>/review/new/', ProfReviewCreateView.as_view(), name = 'prof-review-create'),
	path('professor/<int:ppk>/review/<int:pk>/edit/', ProfReviewUpdateView.as_view(), name = 'prof-review-update'),
	path('professor/<int:ppk>/review/<int:pk>/delete/', ProfReviewDeleteView.as_view(), name = 'prof-review-delete'),
	path('professor/<int:ppk>/review/<int:pk>/preference/<int:pref>/', views.ProfReviewPref, name = 'prof-review-pref'),
	path('course/<slug:cname>/review/<int:pk>/preference/<int:pref>/', views.CourseReviewPref, name = 'course-review-pref'),
	path('professor/<int:ppk>/review/<int:pk>/report/', views.ProfReviewReport, name = 'prof-review-report'),
	path('course/<slug:cname>/review/<int:pk>/report/', views.CourseReviewReport, name = 'course-review-report'),


]