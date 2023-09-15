from django.shortcuts import render, redirect, get_object_or_404
from django.utils import timezone
from django.contrib.auth.decorators import login_required
from django.contrib.auth.views import LoginView, LogoutView
from django.contrib.auth.forms import AuthenticationForm, UserCreationForm
from django.http import HttpResponse

from .forms import CustomRegistrationForm, CustomLoginForm

from .models import Task


class CustomLoginView(LoginView):
    template_name = 'registration/login.html'

    def get(self, request, *args, **kwargs):
        # Render the login form and registration form on GET request
        login_form = AuthenticationForm()
        registration_form = UserCreationForm()
        return self.render_to_response(
            self.get_context_data(
                login_form=login_form,
                registration_form=registration_form,
                error_message=None
            )
        )

    def post(self, request, *args, **kwargs):
        error_message = None

        # Process the login form or registration form on POST request
        if 'login_submit' in request.POST:
            # Handle login submission
            login_form = AuthenticationForm(data=request.POST)
            if login_form.is_valid():
                print("login form is valid")
                from django.contrib.auth import login
                user = login_form.get_user()
                login(request, user)
                return redirect('to_do:index')  # Redirect to the home page after successful login
            else:
                # Handle login form errors
                print("login form is not valid")
                error_message = "Login failed. Please check your credentials."

        elif 'registration_submit' in request.POST:
            # Handle registration form submission
            registration_form = UserCreationForm(data=request.POST)
            if registration_form.is_valid():
                user = registration_form.save()  # Save the new user
                from django.contrib.auth import login
                login(request, user)  # Log in the newly registered user
                return redirect('to_do:index')  # Redirect to the home page after successful registration
            else:
                # Handle registration form errors
                error_message = "Registration failed. Please check your information."

        # If there was an error in either login or registration, render the form with an error message
        print("We got here")
        return self.render_to_response(
            self.get_context_data(
                login_form=AuthenticationForm(),
                registration_form=UserCreationForm(),
                error_message=error_message
            )
        )

@login_required
def index(request):
    # Call the common function to handle form submission
    handle_form_submission(request, 'to_do:index')

    if request.method == 'POST':
        # Check if the "complete" or "delete" form was submitted
        if 'complete' in request.POST:
            task_id = request.POST['complete']
            complete_task(request, task_id)
        elif 'delete' in request.POST:
            task_id = request.POST['delete']
            delete_task(request, task_id)

        # Retrieve all tasks, including completed tasks, for display
    all_root_tasks = Task.objects.filter(user=request.user, completed=False, parent_task__isnull=True).prefetch_related("subtask")

    return render(request,
                  'to_do/index.html',
                  {'all_root_tasks': all_root_tasks
                   })

@login_required
def complete_task(request, task_id):
    task = get_object_or_404(Task, id=task_id, user=request.user)

    # Toggle the completion status
    task.completed = not task.completed
    task.save()

    # If root task marked complete all subtasks updated to complete
    if not task.parent_task and task.completed:
        subtasks = Task.objects.filter(parent_task=task)
        subtasks.update(completed=True)

    return HttpResponse(status=204)  # 204 No Content response


@login_required
def delete_task(request, task_id):
    task = get_object_or_404(Task, id=task_id, user=request.user)
    task.delete()
    return redirect('to_do:index')

def handle_form_submission(request, redirect_url, parent_task=None):
    # Handle create task form submissions

    if request.method == 'POST':
        # Determine whether it's a new task or a subtask form based on the input name
        form_prefix = f'subtask_{parent_task.id}' if parent_task else 'new_task'

        # Get the task description from the form input
        task_description = request.POST.get(form_prefix)

        # Create a new Task object and save it to the database
        Task.objects.create(user=request.user, task_description=task_description, date_added=timezone.now(), parent_task=parent_task)

        # Redirect to the specified URL
        return redirect(redirect_url)

def add_task(request):
    # Call the common function to handle form submission
    handle_form_submission(request, 'to_do:index')

    return redirect("to_do:index")

def add_subtask(request, task_id):
    try:
        parent_task = Task.objects.get(pk=task_id)
    except Task.DoesNotExist:
        parent_task = None

    if parent_task:
            handle_form_submission(request, "to_do:index", parent_task=parent_task)

    return redirect("to_do:index")

@login_required
def completed_tasks(request):
    # Retrieve all completed tasks for the user
    completed_tasks = Task.objects.filter(user=request.user, completed=True).prefetch_related("subtask")

    return render(request, 'to_do/completed.html', {'completed_tasks': completed_tasks})

class CustomLogoutView(LogoutView):
    next_page = 'to_do:login'