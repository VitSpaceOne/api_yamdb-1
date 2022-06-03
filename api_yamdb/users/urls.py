from django.urls import path, include
from rest_framework.routers import SimpleRouter


from .views import sign_up, retrieve_token, UsersViewSet

router = SimpleRouter()

router.register('users', UsersViewSet, basename='users')

urlpatterns = [
    path('auth/signup/', sign_up, name='sign_up'),
    path('auth/token/', retrieve_token, name='retrieve_token'),
    path('', include(router.urls))
]
