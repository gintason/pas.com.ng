from django.http import HttpResponse, JsonResponse
from django.shortcuts import render, redirect, get_object_or_404
from .models import *
from .forms import *
import random
from django.urls import reverse
from pasApp.models import Product, Category
from .forms import EssayAnswerForm
from .models import  Question
# Create your views here.
from django.http import HttpResponse, JsonResponse
from django.shortcuts import render, redirect
from .models import Category, Question
import random


def quiz_page(request, pk):
    """Render quiz page and process user responses."""
    product = get_object_or_404(Product, id=pk)  # Fetch the product
    interview = product.interview_set.all()  # Fetch related interviews
    categories = Category.objects.all()
    
    selected_category = request.GET.get('category')
    questions = Question.objects.filter(category__name=selected_category) if selected_category else None

    if request.method == "POST":
        form = EssayAnswerForm(request.POST)
        if form.is_valid():
            user_answer = form.cleaned_data['user_answer']
            question = form.cleaned_data['question']
            is_correct = question.check_answer(user_answer)

            return redirect(reverse("quiz:result", kwargs={"pk": pk}) + f"?correct={is_correct}")

    else:
        form = EssayAnswerForm()

    context = {
        'categories': categories,
        'interview': interview,
        'product': product,
        'questions': questions,
        'form': form,
        'selected_category': selected_category,
        'product': product,  # Ensure this is passed!
    }

    return render(request, "quiz/quiz_page.html", context)



def quiz(request, pk):
    """Render quiz page with filtered questions and process essay answers."""
    
    print(f"DEBUG: Fetching product with ID: {pk}")
    product = get_object_or_404(Product, id=pk)  # Fetch the product

    category_name = request.GET.get('category')
    print(f"DEBUG: Selected category: {category_name}")

    # Filter questions by category
    if category_name:
        questions = Question.objects.filter(category__category_name=category_name)
    else:
        questions = Question.objects.all()

    print(f"DEBUG: Retrieved {questions.count()} questions")

    if request.method == 'POST':
        score = 0
        correct = 0
        wrong = 0
        total = questions.count()
        user_answers = []

        print("DEBUG: Processing user answers...")
        for q in questions:
            print(f"DEBUG: Processing Question: {q.question}")
            user_answer = request.POST.get(f"answer_{q.id}", "").strip().lower()  # Get user input
            print(f"DEBUG: User Answer for '{q.question}': {user_answer}")

            is_correct = q.check_answer(user_answer)  # Use the model's check_answer method
            print(f"DEBUG: Correct? {is_correct}")

            if is_correct:
                score += 10
                correct += 1
            else:
                wrong += 1

            user_answers.append({
                'question': q.question,
                'user_answer': user_answer if user_answer else "No Answer",  # Handle empty inputs
                'correct_answer': ", ".join(q.correct_answers) if isinstance(q.correct_answers, list) else q.correct_answers,  
                'is_correct': is_correct
            })

        percent = (score / (total * 10)) * 100 if total > 0 else 0
        print(f"DEBUG: Final Score: {score}, Percentage: {percent}, Correct: {correct}, Wrong: {wrong}, Total: {total}")

        # Pass data to result page
        context = {
            'score': score,
            'correct': correct,
            'wrong': wrong,
            'percent': percent,
            'total': total,
            'user_answers': user_answers,
            'category_name': category_name,
            'product': product,  # Ensure this is passed!
            'questions': questions,
        }
        return render(request, 'quiz/result.html', context)

    # ✅ Ensure 'product' is passed in GET request
    context = {
        'questions': questions,
        'category_name': category_name,
        'product': product,  # ✅ Add this
    }
    print("DEBUG: Rendering quiz page with context:", context)
    return render(request, 'quiz/quiz.html', context)




def quiz_result(request):
    """Processes quiz submission and calculates the score."""
    
    if request.method != "POST":
        return redirect("quiz:quiz_page")  # Redirect if accessed improperly

    category_name = request.POST.get("category_name")
    questions = Question.objects.filter(category__category_name=category_name)

    score = 0
    correct = 0
    wrong = 0
    total = questions.count()
    user_answers = []

    for q in questions:
        user_answer = request.POST.get(f"answer_{q.id}", "").strip().lower()
        correct_answers = [ans.strip().lower() for ans in q.correct_answers.split(",")]

        is_correct = user_answer in correct_answers

        if is_correct:
            score += 10  # 10 points per correct answer
            correct += 1
        else:
            wrong += 1

        user_answers.append({
            "question": q.question,
            "user_answer": user_answer or "No Answer",
            "correct_answers": ", ".join(correct_answers),
            "is_correct": is_correct,
        })

    percent = (score / (total * 10)) * 100 if total > 0 else 0
    elapsed_time = request.POST.get("timer", "Unknown")  # Time taken to complete

    context = {
        "score": score,
        "percent": round(percent, 2),
        "time": elapsed_time,
        "correct": correct,
        "wrong": wrong,
        "total": total,
        "user_answers": user_answers,
        "category_name": category_name
    }

    return render(request, "quiz/result.html", context)



def quiz_home(request):

    return redirect('quiz:quiz_page', pk=1) 



def addQuestion(request):    
    if request.user.is_staff:
        form=addQuestionform()
        if(request.method=='POST'):
            form=addQuestionform(request.POST)
            if(form.is_valid()):
                form.save()
                return redirect('/')
        context={'form':form}
        return render(request,'quiz/add_question.html',context)
    else: 
        return redirect('quiz:quiz') 

