from django.shortcuts import redirect, render
from datetime import datetime


# Temporary in-memory store for demo reviews.
# Data resets whenever the Django process restarts.
IN_MEMORY_REVIEWS = []

STATIC_REVIEWS = [
    {
        "id": "review-sarah",
        "author": "Sarah T.",
        "initials": "ST",
        "grade": "7",
        "term": "Sem 1, 2023",
        "academic_year": "2022-2023",
        "overall_rating": "4",
        "difficulty": "4",
        "workload": "5",
        "lecturer_quality": "5",
        "review_text": (
            "Assignments are heavy and require starting early, but the concepts "
            "taught are incredibly useful for technical interviews. Great lecturers."
        ),
        "submission_date": "Oct 12, 2023",
        "submitted_at": datetime(2023, 10, 12),
        "helpful_count": 18,
    },
    {
        "id": "review-michael",
        "author": "Michael R.",
        "initials": "MR",
        "grade": "6",
        "term": "Sem 2, 2022",
        "academic_year": "2022-2023",
        "overall_rating": "4",
        "difficulty": "5",
        "workload": "4",
        "lecturer_quality": "4",
        "review_text": (
            "The exam is worth 50% so you really need to understand the theoretical "
            "proofs. Don't just memorize the code."
        ),
        "submission_date": "Sep 28, 2023",
        "submitted_at": datetime(2023, 9, 28),
        "helpful_count": 11,
    },
]


def academic_year_for_term(term):
    year = None
    for part in term.replace(",", " ").split():
        if part.isdigit() and len(part) == 4:
            year = int(part)
            break

    if year is None:
        return "Unknown"

    if "Semester 1" in term:
        return f"{year - 1}-{year}"
    return f"{year}-{year + 1}"


def grade_matches(review_grade, grade_filter):
    if not grade_filter:
        return True
    if grade_filter == "1, 2":
        return review_grade in {"1", "2", "1, 2"}
    if grade_filter == "3S-, NS-":
        return review_grade in {"3S-", "NS-", "3S-, NS-"}
    return review_grade == grade_filter


def rating_number(review, field):
    try:
        return int(review[field])
    except (KeyError, TypeError, ValueError):
        return 0

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

def course_search(request):
    return render(request, "course_search.html")

def peer_review(request):
    reviews = STATIC_REVIEWS + IN_MEMORY_REVIEWS
    
    # Get filter parameters from query string
    sort_by = request.GET.get("sort_by", "Most Recent")
    academic_year = request.GET.get("academic_year", "All Years")
    grade_filter = request.GET.get("grade_filter", "")
    difficulty_filter = request.GET.get("difficulty_filter", "")
    workload_filter = request.GET.get("workload_filter", "")
    lecturer_filter = request.GET.get("lecturer_filter", "")
    
    # Apply academic year filter
    if academic_year != "All Years":
        reviews = [r for r in reviews if r["academic_year"] == academic_year]

    # Apply grade filter
    if grade_filter:
        reviews = [r for r in reviews if grade_matches(r["grade"], grade_filter)]
    
    # Apply difficulty filter
    if difficulty_filter:
        reviews = [r for r in reviews if r["difficulty"] == difficulty_filter]
    
    # Apply workload filter
    if workload_filter:
        reviews = [r for r in reviews if r["workload"] == workload_filter]
    
    # Apply lecturer filter
    if lecturer_filter:
        reviews = [r for r in reviews if r["lecturer_quality"] == lecturer_filter]
    
    # Apply sorting
    if sort_by == "Highest Rating":
        reviews = sorted(reviews, key=lambda x: rating_number(x, "overall_rating"), reverse=True)
    elif sort_by == "Lowest Rating":
        reviews = sorted(reviews, key=lambda x: rating_number(x, "overall_rating"))
    elif sort_by == "Most Helpful":
        reviews = sorted(reviews, key=lambda x: x.get("helpful_count", 0), reverse=True)
    else:
        reviews = sorted(reviews, key=lambda x: x["submitted_at"], reverse=True)
    
    context = {
        "reviews": reviews,
        "sort_by": sort_by,
        "academic_year": academic_year,
        "grade_filter": grade_filter,
        "difficulty_filter": difficulty_filter,
        "workload_filter": workload_filter,
        "lecturer_filter": lecturer_filter,
    }
    return render(request, "peer_review.html", context)

def add_review(request):
    if request.method == "POST":
        review_text = request.POST.get("review_text", "").strip()
        if len(review_text) < 50:
            return render(
                request,
                "add_review.html",
                {
                    "form_error": "Review must be at least 50 characters.",
                },
            )

        IN_MEMORY_REVIEWS.append(
            {
                "id": f"review-{len(IN_MEMORY_REVIEWS) + 1}",
                "author": "Alex Johnson",
                "initials": "AJ",
                "grade": request.POST.get("grade", "Not shared"),
                "term": request.POST.get("term", "Unknown term"),
                "academic_year": academic_year_for_term(request.POST.get("term", "Unknown term")),
                "overall_rating": request.POST.get("overall_rating", "5"),
                "difficulty": request.POST.get("difficulty", "3"),
                "workload": request.POST.get("workload", "3"),
                "lecturer_quality": request.POST.get("lecturer_quality", "3"),
                "review_text": review_text,
                "submission_date": datetime.now().strftime("%b %d, %Y"),
                "submitted_at": datetime.now(),
                "helpful_count": 0,
            }
        )
        return redirect("peer_review")

    return render(request, "add_review.html")
