from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from .models import UntimedQuestion, UntimedUserResponse, UntimedCategory
from .forms import UntimedQuizForm
from django.http import JsonResponse
from django.urls import reverse
from django.utils import timezone
import difflib
from .models import UntimedQuestion, UntimedUserResponse
from .utils import similarity_score  # Ensure you have this function in utils.py
from pasApp.models import Product


@login_required
def untimed_quiz_view(request, category_id):
    """View to handle untimed quiz"""
    category = get_object_or_404(UntimedCategory, id=category_id)
    questions = UntimedQuestion.objects.filter(category=category)

    if request.method == "POST":
        form = UntimedQuizForm(request.POST)
        question_id = request.POST.get("question_id")
        question = get_object_or_404(UntimedQuestion, id=question_id)

        if form.is_valid():
            user_response = form.save(commit=False)
            user_response.user = request.user
            user_response.question = question
            user_response.save()  # Triggers similarity check

            return redirect("untimed_quiz:quiz2_main.html", category_id=category.id)  # Refresh quiz page

    else:
        form = UntimedQuizForm()

    return render(request, "untimed_quiz/quiz2_main.html", {
        "category": category,
        "questions": questions,
        "form": form,
    })


@login_required
def quiz2_page(request):
    """View to display category selection form"""
    categories = UntimedCategory.objects.all()

    if request.method == "POST":
        selected_category_id = request.POST.get("category")
        return redirect("untimed_quiz:start_quiz2", category_id=selected_category_id)

    return render(request, "untimed_quiz/quiz2_page.html", {"categories": categories})


@login_required
def start_quiz2(request, category_id):
    """View to start the untimed quiz based on selected category"""
    category = UntimedCategory.objects.get(id=category_id)
    questions = UntimedQuestion.objects.filter(category=category)

    if request.method == "POST":
        score = 0
        total_questions = questions.count()
        responses = []

        for question in questions:
            user_answer = request.POST.get(f"question_{question.id}", "").strip()
            similarity = difflib.SequenceMatcher(None, user_answer.lower(), question.correct_answer.lower()).ratio()
            is_correct = similarity >= 0.5

            # Save the response to the database
            UntimedUserResponse.objects.create(
                user=request.user,
                question=question,
                user_answer=user_answer,
                is_correct=is_correct
            )

            responses.append({
                "question": question.text,
                "user_answer": user_answer,
                "correct_answers": question.correct_answer,
                "correct": is_correct
            })

            if is_correct:
                score += 1

        # Calculate percentage score
        percent = round((score / total_questions) * 100, 2) if total_questions > 0 else 0

        # Render the results page instead of returning JSON
        return render(request, "untimed_quiz/quiz2_result.html", {
            "score": score,
            "total": total_questions,
            "correct": score,
            "wrong": total_questions - score,
            "percent": percent,
            "user_answers": responses,
        })

    return render(request, "untimed_quiz/quiz2_main.html", {"questions": questions, "category": category})

@login_required
def quiz2_result(request):
    """View to display quiz results"""
    responses = UntimedUserResponse.objects.filter(user=request.user).order_by("-id")[:10]  # Get last 10 responses
    correct_answers = sum(response.is_correct for response in responses)  # ✅ Use sum() instead of .filter()
    total_attempts = len(responses)  # ✅ Count responses correctly

    # Fetch product based on the last answered question
    product = None
    if responses.exists():
        last_question = responses.first().question
        product = last_question.category  # Assuming category is linked to a product

    context = {
        "responses": responses,
        "correct_answers": correct_answers,
        "total_attempts": total_attempts,
        "score_percentage": (correct_answers / total_attempts) * 100 if total_attempts > 0 else 0,
        "product": product,  # Pass product to the template
    }

    return render(request, "untimed_quiz/quiz2_result.html", context)



def submit_quiz2(request):
    if request.method == "POST":
        score = 0
        responses = []
        total_questions = UntimedQuestion.objects.count()

        for question in UntimedQuestion.objects.all():
            user_answer = request.POST.get(f"answer_{question.id}", "").strip()
            correct_answer = question.correct_answer.strip()

            is_correct = similarity_score(user_answer, correct_answer) >= 50
            if is_correct:
                score += 1

            responses.append({
                "question": question.text,
                "user_answer": user_answer,
                "correct_answers": correct_answer,
                "correct": is_correct
            })

        return redirect("untimed_quiz:quiz2_result", score=score, total=total_questions, responses=responses)

    return redirect("untimed_quiz:quiz2_page")


@login_required
def submit_quiz2(request):
    if request.method == "POST":
        score = 0
        responses = []
        total_questions = UntimedQuestion.objects.count()

        for question in UntimedQuestion.objects.all():
            user_answer = request.POST.get(f"answer_{question.id}", "").strip()
            correct_answer = question.correct_answer.strip()

            is_correct = similarity_score(user_answer, correct_answer) >= 50
            if is_correct:
                score += 1

            # Save user response to database
            UntimedUserResponse.objects.create(
                user=request.user,
                question=question,
                user_answer=user_answer,
                is_correct=is_correct
            )

            responses.append({
                "question": question.text,
                "user_answer": user_answer,
                "correct_answers": correct_answer,
                "correct": is_correct
            })

        # Render the quiz2_result page with styled output
        return render(request, "untimed_quiz/quiz2_result.html", {
            "score": score,
            "total": total_questions,
            "correct": score,
            "wrong": total_questions - score,
            "percent": round((score / total_questions) * 100, 2) if total_questions > 0 else 0,
            "user_answers": responses,
        })

    return redirect("untimed_quiz:quiz2_page")