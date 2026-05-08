from django.shortcuts import render

def dashboard(request):
    return render(request, "dashboard.html")

def course_summary(request, course_code=None):
    context = {'course_code': course_code}
    return render(request, "course_summary.html", context)

def course_planner(request):
    return render(request, "course_planner.html",)

def course_compare(request, course_code1=None, course_code2=None):
    context = {'course_code1': course_code1, 'course_code2' : course_code2}
    return render(request, "course_compare.html", context)
