from celery import shared_task
from django.core.mail import send_mail
from django.conf import settings
from students.models import Student
from grades.models import Grade
from attendance.models import Attendance

@shared_task
def send_daily_attendance_reminder():
    students = Student.objects.all()
    for student in students:
        send_mail(
            subject="Daily Attendance Reminder",
            message="Please mark your attendance for today.",
            from_email=settings.EMAIL_FROM,
            recipient_list=[student.email],
        )

@shared_task
def notify_grade_update(student_id, course_name, grade):
    student = Student.objects.get(id=student_id)
    send_mail(
        subject="Grade Update Notification",
        message=f"Your grade for {course_name} has been updated to {int(grade)}.",
        from_email=settings.EMAIL_FROM,
        recipient_list=[student.email],
    )

@shared_task
def send_daily_summary():
    students = Student.objects.all()
    for student in students:
        attendance_count = Attendance.objects.filter(student=student).count()
        grades = Grade.objects.filter(student=student)
        grade_summary = ", ".join([f"{g.course.name}: {int(g.grade)}" for g in grades])

        send_mail(
            subject="Daily Summary",
            message=f"Attendance records: {attendance_count}. Grades: {grade_summary}.",
            from_email=settings.EMAIL_FROM,
            recipient_list=[student.email],
        )

@shared_task
def send_weekly_performance_summary():
    students = Student.objects.all()
    for student in students:
        grades = Grade.objects.filter(student=student)
        grade_summary = ", ".join([f"{g.course.name}: {int(g.grade)}" for g in grades])

        send_mail(
            subject="Weekly Performance Summary",
            message=f"Hello {student.name}, here is your weekly performance summary:\nGrades: {grade_summary}.",
            from_email=settings.EMAIL_FROM,
            recipient_list=[student.email],
        )
