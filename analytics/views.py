from rest_framework.views import APIView
from rest_framework.response import Response
from analytics.models import APIRequestLog, PopularCourse
from django.db.models import Count


class AnalyticsDashboard(APIView):
    def get(self, request):
        top_users = (
            APIRequestLog.objects.values('user__username')
            .annotate(request_count=Count('id'))
            .order_by('-request_count')[:5]
        )
        popular_courses = PopularCourse.objects.order_by('-views')[:5]

        return Response({
            'top_users': top_users,
            'popular_courses': [
                {'course': course.course.name, 'views': course.views}
                for course in popular_courses
            ],
        })
