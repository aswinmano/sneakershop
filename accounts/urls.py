from django.urls import path
from .views import register,login,logout

urlpatterns=[
    path("SignUp/",register,name="register"),
    path("SignIn/",login,name="login"),
    path("Logout/",logout,name="logout"),
    
]