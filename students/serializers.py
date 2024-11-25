# students/serializers.py
from rest_framework import serializers
from .models import Student


class StudentSerializer(serializers.ModelSerializer):
    enrollments = serializers.StringRelatedField(many=True, read_only=True)

    class Meta:
        model = Student
        fields = ['id', 'name', 'email', 'dob', 'registration_date', 'enrollments']
