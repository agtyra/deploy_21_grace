from django.contrib import admin
from django.urls import path
from .views import dashboard, course_summary, course_planner, course_compare

urlpatterns = [
    path("admin/", admin.site.urls),
    path("", dashboard, name="dashboard"),
    path("course/<str:course_code>/", course_summary, name="course_summary"),
    path("planner/", course_planner, name="course_planner"),
    path("compare/", course_compare, name="course_compare")
]