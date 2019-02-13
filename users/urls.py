from django.conf.urls import url
from rest_framework_jwt.views import obtain_jwt_token

from users.views import Register

app_name = 'users'

urlpatterns = [
    url(r'^users', Register.as_view()),
    url(r'^users/register', Register.as_view()),
    url(r'^users/login', obtain_jwt_token),
    url(r'^auth/login', obtain_jwt_token),
]
