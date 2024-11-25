from rest_framework import serializers
from .models import Course, Enrollment


class CourseSerializer(serializers.ModelSerializer):
    enrollments = serializers.StringRelatedField(many=True, read_only=True)

    class Meta:
        model = Course
        fields = ['id', 'name', 'description', 'instructor', 'enrollments']
        extra_kwargs = {
            'instructor': {'read_only': True}
        }


class EnrollmentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Enrollment
        fields = ['id', 'student', 'course', 'enrollment_date']
        extra_kwargs = {
            'enrollment_date': {'read_only': True},
        }
