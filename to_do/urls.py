from django.urls import path


from . import views



app_name = "to_do"
urlpatterns = [
    path("", views.index, name="index"),
    path("login/", views.CustomLoginView.as_view(), name="login"),
    path("add_task/", views.add_task, name="add_task"),
    path("add_sub_task/<int:task_id>/", views.add_subtask, name="add_subtask"),
    path("complete_task/<int:task_id>/", views.complete_task, name="complete_task"),
    path("delete_task/<int:task_id>/", views.delete_task, name="delete_task"),
    path("completed/", views.completed_tasks, name="completed_tasks"),
    path("logout/", views.CustomLogoutView.as_view(), name="logout"),
]