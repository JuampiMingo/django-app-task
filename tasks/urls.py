from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name="home"),
    path('tasks/', views.tasks, name="tasks"),
    path('tasks_completed/', views.tasks_completed, name="tasks_completed"),
    path('signup/', views.signup, name="signup"),
    path('logout/', views.signout, name="logout"),
    path('signin/', views.signin, name="signin"),
    path('tasks/create/', views.create_task, name='create_task'),
    path('tasks/<int:task_id>/', views.task_detail, name='task_detail'),
    path('tasks/<int:task_id>/delete', views.task_delete, name='task_delete'), # type: ignore
    path('tasks/<int:task_id>/complete', views.task_complete, name='task_complete') # type: ignore
]