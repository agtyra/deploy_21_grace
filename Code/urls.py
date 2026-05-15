from django.contrib import admin
from django.urls import path
from .views import dashboard, course_summary, course_planner, course_compare, course_search, peer_review, add_review

urlpatterns = [
    path("admin/", admin.site.urls),
    path("", dashboard, name="dashboard"),
    path("course/<str:course_code>/", course_summary, name="course_summary"),
    path("planner/", course_planner, name="course_planner"),
    path("compare/", course_compare, name="course_compare"),
    path("courses/", course_search, name="course_search"),
    path("peer-review/", peer_review, name="peer_review"),
    path("add-review/", add_review, name="add_review"),
]