from django.shortcuts import render
from .forms import SignUpForm, LoginForm
from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages


def login_or_signup(request):

    if request.method == "POST":

        if "signup" in request.POST:
            signup_form = SignUpForm(request.POST, prefix="signup")
            login_form = LoginForm(prefix="login")
            if signup_form.is_valid():
                user = signup_form.save(commit=False)
                user.set_password(signup_form.cleaned_data["password"])
                user.save()
                messages.success(request, "Signup successful. Please log in.")
            else:
                if "username" in signup_form.errors:
                    messages.error(
                        request, "Username is not unique. Please choose another."
                    )
                else:
                    messages.error(
                        request, "Signup failed. Please correct the errors below."
                    )

        elif "login" in request.POST:
            login_form = LoginForm(request.POST, prefix="login")
            signup_form = SignUpForm(prefix="signup")
            if login_form.is_valid():
                email = login_form.cleaned_data["email"]
                password = login_form.cleaned_data["password"]
                user = authenticate(request, email=email, password=password)
                if user is not None:
                    login(request, user)
                    return redirect("chats_page")
                else:
                    messages.error(request, "Invalid email or password")

        return redirect("login_or_signup")

    else:
        signup_form = SignUpForm(prefix="signup")
        login_form = LoginForm(prefix="login")

    return render(
        request,
        "login_or_signup.html",
        {
            "signup_form": signup_form,
            "login_form": login_form,
        },
    )


def user_logout(request):
    logout(request)
    return redirect("login_or_signup")
