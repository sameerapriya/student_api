from django.urls import path, include

from rest_framework.routers import DefaultRouter

from .views import StudentRegisterView, StudentUpdateView,\
    StudentTokenView, CourseView, CourseEnrollView

router = DefaultRouter()
router.register('courses', CourseView)
router.register('courseenroll', CourseEnrollView)

urlpatterns = [
    path('user/create/', StudentRegisterView.as_view()),
    path('user/token/', StudentTokenView.as_view()),
    path('user/update/', StudentUpdateView.as_view()),
    path('', include(router.urls))
]
