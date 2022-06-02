from django.urls import path, include
from django.views.generic import TemplateView

urlpatterns = [
    path(
        'redoc/',
        TemplateView.as_view(template_name='redoc.html'),
        name='redoc'
    ),
    path('api/v1/', include('users.urls'))
]
