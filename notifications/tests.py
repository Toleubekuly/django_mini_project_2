from unittest.mock import patch
from django.core.mail import send_mail
from students.models import Student
from grades.models import Grade
from attendance.models import Attendance
from courses.models import Course
from users.models import CustomUser
from notifications.tasks import (
    send_daily_attendance_reminder,
    notify_grade_update,
    send_daily_summary,
    send_weekly_performance_summary,
)
from django.test import TestCase
import os


class CeleryTaskTestCase(TestCase):
    def setUp(self):
        self.teacher = CustomUser.objects.create_user(
            username="teacher",
            email="Ertoshka04@gmail.com",
            password="teacherpass",
            role="teacher"
        )
        self.student = Student.objects.create(
            name="John Doe",
            email="Ertoshka04@gmail.com",
            dob="2000-01-01"
        )
        self.course = Course.objects.create(
            name="Math",
            description="Math Course",
            instructor=self.teacher
        )
        self.grade = Grade.objects.create(
            student=self.student,
            course=self.course,
            grade=95,
            teacher=self.teacher
        )
        self.attendance = Attendance.objects.create(
            student=self.student,
            course=self.course,
            status="present"
        )

    @patch("notifications.tasks.send_mail")
    def test_send_daily_attendance_reminder(self, mock_send_mail):
        send_daily_attendance_reminder()
        mock_send_mail.assert_called_once_with(
            subject="Daily Attendance Reminder",
            message="Please mark your attendance for today.",
            from_email=os.environ.get('EMAIL_FROM'),
            recipient_list=[self.student.email],
        )

    @patch("notifications.tasks.send_mail")
    def test_notify_grade_update(self, mock_send_mail):
        notify_grade_update(self.student.id, "Math", 95)
        mock_send_mail.assert_called_once_with(
            subject="Grade Update Notification",
            message=f"Your grade for Math has been updated to 95.",
            from_email=os.environ.get('EMAIL_FROM'),
            recipient_list=[self.student.email],
        )

    @patch("notifications.tasks.send_mail")
    def test_send_daily_summary(self, mock_send_mail):
        send_daily_summary()
        mock_send_mail.assert_called_once_with(
            subject="Daily Summary",
            message="Attendance records: 1. Grades: Math: 95.",
            from_email=os.environ.get('EMAIL_FROM'),
            recipient_list=[self.student.email],
        )


    @patch("notifications.tasks.send_mail")
    def test_send_weekly_performance_summary(self, mock_send_mail):
        send_weekly_performance_summary()
        mock_send_mail.assert_called_once_with(
            subject="Weekly Performance Summary",
            message=f"Hello {self.student.name}, here is your weekly performance summary:\nGrades: Math: 95.",
            from_email=os.environ.get('EMAIL_FROM'),
            recipient_list=[self.student.email],
        )
