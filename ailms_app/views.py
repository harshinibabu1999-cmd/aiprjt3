from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import login, authenticate, logout
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .models import Course, Resume, Quiz, Result
from .pdf_utils import extract_text_from_pdf, segment_into_chapters
from .ai_utils import parse_resume, generate_quiz, suggest_jobs, recommend_courses_ai
import json

def register_view(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)

        if form.is_valid():
            form.save()

            messages.success(request, "Account created successfully! Please login.")
            return redirect('login')   # ✅ go to login page

        else:
            messages.error(request, form.errors)

    else:
        form = UserCreationForm()

    return render(request, 'auth/register.html', {'form': form})

def login_view(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']

        user = authenticate(request, username=username, password=password)

        if user is not None:
            login(request, user)
            return redirect('dashboard')   # ✅ after login
        else:
            messages.error(request, "Invalid username or password")

    return render(request, 'auth/login.html')

def logout_view(request):
    logout(request)
    return redirect('login')

@login_required
def dashboard(request):
    # 9 Domains for Symmetric Grid
    all_domains = [
        {'name': 'Python', 'icon': 'ri-python-fill', 'color': '#3776AB'},
        {'name': 'AI & ML', 'icon': 'ri-brain-line', 'color': '#FF4B4B'},
        {'name': 'Full Stack', 'icon': 'ri-layout-masonry-line', 'color': '#61DBFB'},
        {'name': 'Java Dev', 'icon': 'ri-java-line', 'color': '#f89820'},
        {'name': 'Data Science', 'icon': 'ri-database-line', 'color': '#58C4DC'},
        {'name': 'Blockchain', 'icon': 'ri-bit-coin-line', 'color': '#F7931A'},
        {'name': 'Cybersecurity', 'icon': 'ri-shield-keyhole-line', 'color': '#00A19D'},
        {'name': 'Cloud', 'icon': 'ri-cloud-line', 'color': '#0078D4'},
        {'name': 'DevOps', 'icon': 'ri-terminal-window-line', 'color': '#24292e'},
    ]
    
    return render(request, 'dashboard.html', {'all_domains': all_domains})

@login_required
def courses_list(request):
    courses = Course.objects.all()
    ai_suggestion = None
    ai_skills_query = ""
    
    if request.method == 'POST':
        ai_skills_query = request.POST.get('skills_query', '')
        if ai_skills_query:
            recs = recommend_courses_ai([ai_skills_query])
            if recs:
                prompt_text = ai_skills_query if len(ai_skills_query) < 40 else ai_skills_query[:37] + "..."
                ai_suggestion = {
                    "query": prompt_text,
                    "courses": recs
                }
                
    return render(request, 'courses_list.html', {
        'courses': courses, 
        'ai_suggestion': ai_suggestion,
        'ai_skills_query': ai_skills_query
    })

@login_required
def upload_resume(request):
    if request.method == 'POST' and request.FILES.get('resume'):
        resume_file = request.FILES['resume']
        resume, created = Resume.objects.get_or_create(user=request.user)
        resume.resume_file = resume_file
        resume.save()
        
        # Process Resume
        text = extract_text_from_pdf(resume.resume_file.path)
        skills, domain = parse_resume(text)
        
        resume.extracted_text = text
        resume.skills = skills
        resume.domain_detected = domain
        resume.save()
        
        messages.success(request, "Resume analyzed successfully!")
        return redirect('upload_resume')
        
    resume = Resume.objects.filter(user=request.user).first()
    job_recommendations = []
    if resume and resume.resume_file and resume.skills:
        job_recommendations = suggest_jobs(resume.skills)
        
    return render(request, 'upload_resume.html', {
        'resume': resume,
        'job_recommendations': job_recommendations
    })

@login_required
def course_detail(request, pk):
    course = get_object_or_404(Course, pk=pk)
    
    # Defensive check: if user typed a number in Admin panel instead of a JSON list
    if course.chapters and not isinstance(course.chapters, list):
        course.chapters = None
        course.save()

    # Process PDF if not already done, or if it was cleared by the check above
    if not course.chapters and course.pdf_file:
        try:
            text = extract_text_from_pdf(course.pdf_file.path)
            if text.strip():
                course.extracted_content = text
                course.chapters = segment_into_chapters(text)
                course.save()
            else:
                # Failsafe correctly handled by segment_into_chapters, just save the output
                course.chapters = segment_into_chapters(text)
                course.save()
        except Exception as e:
            messages.error(request, f"Error processing PDF: {str(e)}")
            course.chapters = []
            
    current_chapter_idx = int(request.GET.get('chapter', 0))
    chapter = course.chapters[current_chapter_idx] if course.chapters and current_chapter_idx < len(course.chapters) else None
    
    total_chapters = len(course.chapters)
    progress_percent = ((current_chapter_idx + 1) / total_chapters * 100) if total_chapters > 0 else 0
    
    context = {
        'course': course,
        'chapter': chapter,
        'current_chapter_idx': current_chapter_idx,
        'total_chapters': total_chapters,
        'progress_percent': progress_percent,
    }
    return render(request, 'course_detail.html', context)

@login_required
def take_quiz(request, course_id):
    course = get_object_or_404(Course, id=course_id)
    difficulty = request.GET.get('difficulty', 'medium').lower()
    
    # Check if quiz already exists for this difficulty
    quiz = Quiz.objects.filter(course=course, difficulty=difficulty).first()
    
    if not quiz:
        # Generate new quiz using AI / content-based engine
        content = course.extracted_content or ""
        if not content:
            messages.error(request, "No content available to generate a quiz. Please ensure the PDF is processed correctly.")
            return redirect('course_detail', pk=course.id)
        questions = generate_quiz(content, difficulty)
        if not questions:
            messages.error(request, "Quiz generation failed. The course content may be too short. Please try again.")
            return redirect('course_detail', pk=course.id)
        quiz = Quiz.objects.create(course=course, difficulty=difficulty, questions=questions)
        
    if request.method == 'POST':
        score = 0
        total = len(quiz.questions)
        user_answers = request.POST
        
        for idx, q in enumerate(quiz.questions):
            selected = user_answers.get(f'q_{idx}')
            if selected == q['answer']:
                score += 1
        
        percentage = (score / total) * 100 if total > 0 else 0
        result = Result.objects.create(
            user=request.user,
            quiz=quiz,
            score=score,
            total_questions=total,
            percentage=percentage
        )
        return redirect('quiz_result', result_id=result.id)
        
    return render(request, 'quiz.html', {'quiz': quiz, 'course': course})

@login_required
def quiz_result(request, result_id):
    result = get_object_or_404(Result, id=result_id)
    return render(request, 'quiz_result.html', {'result': result})

from django.db.models import Sum, Count

@login_required
def leaderboard(request):
    top_users = Result.objects.values('user__username').annotate(
        total_score=Sum('score'),
        quizzes_taken=Count('id')
    ).order_by('-total_score')[:10]
    
    return render(request, 'leaderboard.html', {'top_users': top_users})
