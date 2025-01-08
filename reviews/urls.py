from django.urls import path
from . import views

from django.urls import path
from . import views

# urlpatterns = [
#     path("sign/", views.sign, name="sign"),
#     path("login/", views.login, name="login"),
#     path("reviews/", views.reviews, name="reviews"),
# ]


urlpatterns = [
    path('', views.landing, name='landing'),  # Root URL that renders the landing page
    path('sign/', views.sign, name='sign'),
    path('login/', views.login, name='login'),
]