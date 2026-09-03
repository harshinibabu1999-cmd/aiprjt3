from django.db import models
from django.contrib.auth.models import User

class Course(models.Model):
    title = models.CharField(max_length=255)
    domain = models.CharField(max_length=100, default='General')
    description = models.TextField()
    pdf_file = models.FileField(upload_to='courses/')
    extracted_content = models.TextField(blank=True, null=True)
    chapters = models.JSONField(blank=True, null=True)  # List of {title: "...", content: "..."}
    created_at = models.DateTimeField(auto_now_add=True)

    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)
        if self.pdf_file and (not self.extracted_content or not self.chapters or not isinstance(self.chapters, list)):
            try:
                import os
                from .pdf_utils import extract_text_from_pdf, segment_into_chapters
                if os.path.exists(self.pdf_file.path):
                    text = extract_text_from_pdf(self.pdf_file.path)
                    if text and text.strip():
                        extracted = text
                        chaps = segment_into_chapters(text)
                        Course.objects.filter(pk=self.pk).update(extracted_content=extracted, chapters=chaps)
                        self.extracted_content = extracted
                        self.chapters = chaps
            except Exception as e:
                print(f"Error extracting PDF text for course '{self.title}': {e}")

    def __str__(self):
        return self.title

class Resume(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    resume_file = models.FileField(upload_to='resumes/')
    extracted_text = models.TextField(blank=True, null=True)
    skills = models.JSONField(blank=True, null=True) # List of skills
    domain_detected = models.CharField(max_length=100, blank=True, null=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"Resume of {self.user.username}"

class Quiz(models.Model):
    DIFFICULTY_CHOICES = [
        ('easy', 'Easy'),
        ('medium', 'Medium'),
        ('hard', 'Hard'),
    ]
    course = models.ForeignKey(Course, on_delete=models.CASCADE, related_name='quizzes')
    difficulty = models.CharField(max_length=10, choices=DIFFICULTY_CHOICES)
    questions = models.JSONField() # List of {question: "...", options: ["...", "..."], answer: "..."}
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Quiz for {self.course.title} ({self.difficulty})"

class Result(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    quiz = models.ForeignKey(Quiz, on_delete=models.CASCADE)
    score = models.IntegerField()
    total_questions = models.IntegerField(default=10)
    percentage = models.FloatField(default=0.0)
    timestamp = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.user.username} - {self.quiz.course.title} - {self.score}"
