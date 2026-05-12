from django.contrib import admin
from .models import Course, Resume, Quiz, Result

@admin.register(Course)
class CourseAdmin(admin.ModelAdmin):
    list_display = ('title', 'domain', 'created_at')
    search_fields = ('title', 'domain')
    list_filter = ('domain',)

@admin.register(Resume)
class ResumeAdmin(admin.ModelAdmin):
    list_display = ('user', 'domain_detected', 'updated_at')
    search_fields = ('user__username', 'domain_detected')

@admin.register(Quiz)
class QuizAdmin(admin.ModelAdmin):
    list_display = ('course', 'difficulty', 'created_at')
    list_filter = ('difficulty', 'course')

@admin.register(Result)
class ResultAdmin(admin.ModelAdmin):
    list_display = ('user', 'quiz', 'score', 'percentage', 'timestamp')
    list_filter = ('quiz__course', 'user')
