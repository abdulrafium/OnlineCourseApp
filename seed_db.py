import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'myproject.settings')
django.setup()

from django.contrib.auth.models import User
from onlinecourse.models import Course, Lesson, Question, Choice, Enrollment, Submission, Instructor, Learner

# Create superuser
if not User.objects.filter(username='admin').exists():
    admin_user = User.objects.create_superuser('admin', 'admin@example.com', 'admin12345')
    print("Created superuser admin")
else:
    admin_user = User.objects.get(username='admin')

# Create student user
if not User.objects.filter(username='student1').exists():
    student_user = User.objects.create_user('student1', 'student1@example.com', 'student12345', first_name='John', last_name='Doe')
    print("Created user student1")
else:
    student_user = User.objects.get(username='student1')

# Create Instructor
instructor, _ = Instructor.objects.get_or_create(user=admin_user, defaults={'full_time': True, 'total_learners': 100})

# Create Course
course, created = Course.objects.get_or_create(
    name='Cloud Application Development',
    defaults={
        'description': 'Learn full stack development using Django, Cloud technologies, and SQL databases.',
        'total_enrollment': 1
    }
)
course.instructors.add(instructor)

# Create Lessons
l1, _ = Lesson.objects.get_or_create(title='Introduction to Django', order=0, course=course, content='Django is a high-level Python web framework that enables rapid development of secure and maintainable websites.')
l2, _ = Lesson.objects.get_or_create(title='Models and Databases', order=1, course=course, content='Django models define the data structure of your application and handle database migrations seamlessly.')

# Create Questions
q1, _ = Question.objects.get_or_create(
    course=course,
    lesson=l1,
    question_text='Which of the following are Python web frameworks?',
    defaults={'grade': 50}
)
c1_1, _ = Choice.objects.get_or_create(question=q1, choice_text='Django', defaults={'is_correct': True})
c1_2, _ = Choice.objects.get_or_create(question=q1, choice_text='Flask', defaults={'is_correct': True})
c1_3, _ = Choice.objects.get_or_create(question=q1, choice_text='Docker', defaults={'is_correct': False})
c1_4, _ = Choice.objects.get_or_create(question=q1, choice_text='Kubernetes', defaults={'is_correct': False})

q2, _ = Question.objects.get_or_create(
    course=course,
    lesson=l2,
    question_text='What is the primary role of Django ORM?',
    defaults={'grade': 50}
)
c2_1, _ = Choice.objects.get_or_create(question=q2, choice_text='Map Python objects to database tables and execute queries', defaults={'is_correct': True})
c2_2, _ = Choice.objects.get_or_create(question=q2, choice_text='Compile Python into machine code', defaults={'is_correct': False})
c2_3, _ = Choice.objects.get_or_create(question=q2, choice_text='Manage cloud container orchestration', defaults={'is_correct': False})

# Create Enrollment
enrollment, _ = Enrollment.objects.get_or_create(user=student_user, course=course, defaults={'mode': 'honor'})

# Create a successful Submission
sub, _ = Submission.objects.get_or_create(enrollment=enrollment)
sub.choices.set([c1_1, c1_2, c2_1])
sub.save()

print(f"Course ID: {course.id}, Submission ID: {sub.id}")
print("Database seeded successfully!")
