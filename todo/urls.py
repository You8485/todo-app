from django.urls import path
from . import views
app_name='todo'
urlpatterns = [
    path('',views.user_login,name="login_url"),
    path('registration',views.registration,name="register_url"),
    path('index',views.index,name="homepage"),
    path('update_task/<str:pk>/',views.update_task,name="uptask"),
    path('delete_task/<str:pk>/',views.delete_task,name="deltask"),
    path('logout/',views.user_logout,name="logout"),
]
