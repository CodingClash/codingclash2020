from django.urls import path
from django.contrib.auth.views import LogoutView
from django.contrib.auth import login, authenticate
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.shortcuts import render, redirect
from django.contrib.auth import get_user_model
from django.contrib import messages
from django.contrib.auth import logout

app_name = "auth"
class SignUpForm(UserCreationForm):
    
    class Meta:
        User = get_user_model()
        model = User
        fields = ('username', 'password1', 'password2', )


def login_request(request):
    if request.method == 'POST':
        form = AuthenticationForm(request=request, data=request.POST)
        if form.is_valid():
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')
            user = authenticate(username=username, password=password)
            if user is not None:
                login(request, user)
                messages.info(request, f"You are now logged in as {username}")
                return redirect('/')
            else:
                messages.error(request, "Invalid username or password.")
        else:
            messages.error(request, "Invalid username or password.")
    form = AuthenticationForm()
    return render(request = request,
                    template_name = f"auth/login.html",
                    context={"form":form})

def register(request):
    if request.method == 'POST':
        form = SignUpForm(request.POST)
        if form.is_valid():
            form.save()
            username = form.cleaned_data.get('username')
            raw_password = form.cleaned_data.get('password1')
            user = authenticate(username=username, password=raw_password)
            login(request, user)
            return redirect('/')
    else:
        form = SignUpForm()
    return render(request, f"auth/register.html", {'form': form})


def logout_view(request):
    logout(request)
    return redirect("/")

def default(request):
    return render(request, f"auth/{request.resolver_match.url_name}.html")


urlpatterns = [
    path("", default, name="index"),
    path("login/", login_request, name="login"),
    path("register/", register, name="register"),
    path("logout/", logout_view, name="logout"),
]
