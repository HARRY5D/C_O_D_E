# from django.urls import path
# from hello import views
# from hello.models import LogMessage

# home_list_view = views.HomeListView.as_view(
#     queryset=LogMessage.objects.order_by("-log_date")[:5],  # :5 limits the results to the five most recent
#     context_object_name="message_list",
#     template_name="hello/home.html",
# )

# urlpatterns = [
#     path("", home_list_view, name="home"),
#     path("about/", views.about, name="about"),
#     path("log/", views.log_message, name="log"),

# ]

from django.contrib import admin
from django.urls import path, include
from django.contrib.auth import views as auth_views
from hello import views  

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', views.home, name='home'),  # Ensure home is directly accessible
    path('about/', views.about, name='about'),
    path('contact/', views.contact, name='contact'),
    path('accounts/login/', auth_views.LoginView.as_view(template_name='hello/login.html'), name='login'),
    path('accounts/logout/', auth_views.LogoutView.as_view(next_page='/'), name='logout'),
    path('signup/', views.signup_view, name='signup'),  # Signup view
]