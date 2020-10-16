
from django.shortcuts import render, redirect, HttpResponse
from .models import *
from django.contrib import messages
import bcrypt

# Create your views here.

def index(request):
    return render(request, "index.html")

def register(request):
    if request.method == "POST":
        user = User.objects.filter(email = request.POST["email"])
        if len(user) > 0:
            messages.error(request, "This email is already in use", extra_tags = "email")
            return redirect("/")
        errors = User.objects.reg_validator(request.POST)
        if len(errors) > 0:
            for key, val in errors.items():
                messages.error(request, val, extra_tags = key)
            return redirect("/")
        
        # need to hash pw after check all of the invalid information
        pw = bcrypt.hashpw(request.POST["password"].encode(), bcrypt.gensalt()).decode()

        User.objects.create(
            first_name = request.POST["first_name"],
            last_name = request.POST["last_name"],
            email = request.POST["email"],
            password = pw
        )

        request.session["user_id"] = User.objects.last().id
        return redirect("/dashboard")
    else:
        return redirect("/")

def dashboard(request):
    if "user_id" not in request.session:
        return redirect("/")
    else:
        context = {
            "user": User.objects.get(id=request.session["user_id"]),
            "all_quotes": Quote.objects.all()
        }
        return render(request, "dashboard.html", context)

def login(request):
    if request.method == "POST":
        errors = User.objects.login_validator(request.POST)
        if len(errors) > 0:
            for key, val in errors.items():
                messages.error(request, val, extra_tags = key)
            return redirect("/")

        user = User.objects.filter(email = request.POST["login_email"])

        if not user:
            messages.error(request, "Invalid Email/Password", extra_tags = "login")
            return redirect("/")

        if not bcrypt.checkpw(request.POST["login_password"].encode(), user[0].password.encode()):
            messages.error(request, "Invalid Email/Password", extra_tags = "login")
            return redirect("/")

        request.session["user_id"] = user[0].id
        return redirect("/dashboard")
    else:
        return redirect("/")
    
def logout(request):
    if "user_id" in request.session:
        del request.session["user_id"]
    return redirect("/")

def create_quote(request):
    if request.method == "POST":
        errors = Quote.objects.quote_validator(request.POST)
        if len(errors) > 0:
            for key, val in errors.items():
                messages.error(request, val, extra_tags = key)
            return redirect("/dashboard")
        
        Quote.objects.create(
            author = request.POST["author"],
            quote = request.POST["quote"],
            user = User.objects.get(id = request.session["user_id"])
        )
        return redirect("/dashboard")
    else:
        return redirect("/logout")

def delete_quote(request, quote_id):
    this_quote = Quote.objects.get(id = quote_id)
    this_quote.delete()
    return redirect("/dashboard")

def user_quotes(request, user_id):
    display_user = User.objects.get(id = user_id)
    display_user_quotes = display_user.quotes.all()
    context = {
        "user": User.objects.get(id = request.session["user_id"]),
        "display_user": display_user,
        "display_user_quotes": display_user_quotes
    }

    return render(request, "user_quotes.html", context)

def edit_account(request, user_id):
    context = {
        "edit_user": User.objects.get(id = user_id)
    }
    return render(request, "edit_account.html", context)

def edit_account_process(request, edit_user_id):
    if request.method == "POST":
        errors = User.objects.edit_validator(request.POST)
        if len(errors) > 0:
            for key, val in errors.items():
                messages.error(request, val, extra_tags = key)
            return redirect(f"/edit_account/{edit_user_id}")
        update_user = User.objects.get(id = edit_user_id)
        update_user.first_name = request.POST["edit_first_name"]
        update_user.last_name = request.POST["edit_last_name"]
        update_user.email = request.POST["edit_email"]
        update_user.save()

        return redirect("/dashboard")
    else:
        return redirect("/logout")

def like(request, quote_id, user_id):
    quote = Quote.objects.get(id = quote_id)
    user = User.objects.get(id = user_id)

    quote.liked_by.add(user)

    return redirect("/dashboard")