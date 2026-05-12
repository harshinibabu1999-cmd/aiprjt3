import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'ailms_project.settings')
django.setup()

from django.contrib.auth.models import User
from ailms_app.models import Course
from django.core.files.base import ContentFile
import requests

def populate():
    # 1. Create Superuser
    if not User.objects.filter(username='admin').exists():
        User.objects.create_superuser('admin', 'admin@example.com', 'admin123')
        print("Superuser created: admin / admin123")

    # 2. Create Dummy Course
    if not Course.objects.exists():
        c = Course.objects.create(
            title="Introduction to Python Programming",
            domain="Python",
            description="Learn the basics of Python, from variables to AI integration.",
            pdf_file="courses/python_course.pdf",
            extracted_content="Chapter 1: Basics of Python. Python is a high-level programming language. UNIT 1: Variables. Variables are used to store data.",
            chapters=[
                {"title": "Chapter 1: Basics of Python", "content": "Python is a versatile and high-level programming language known for its readability and simplicity. It is widely used in AI, Data Science, and Web Development."},
                {"title": "UNIT 1: Variables and Data Types", "content": "Variables are containers for storing data values. Common types include Integers, Strings, and Booleans."}
            ]
        )
        print(f"Sample Course created: {c.title}")

if __name__ == "__main__":
    populate()
