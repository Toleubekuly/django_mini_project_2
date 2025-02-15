from django.db import models


class Student(models.Model):
    name = models.CharField(max_length=255)
    email = models.EmailField(unique=True)
    dob = models.DateField("Date of Birth")
    registration_date = models.DateField(auto_now_add=True)

    def __str__(self):
        return self.name
