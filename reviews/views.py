from django.shortcuts import render, redirect
from .forms import UserRegistrationForm
from .models import User
import subprocess
import bcrypt
def landing(request):
    return render(request, 'index.html')
# def sign(request):
#     """Handle the user registration."""
#     if request.method == "POST":
#         form = UserRegistrationForm(request.POST)
#         if form.is_valid():
#             password = form.cleaned_data['password']
#             # Hash the password before saving to the database
#             hashed_password = bcrypt.hashpw(password.encode("utf-8"), bcrypt.gensalt()).decode("utf-8")
#             user = form.save(commit=False)
#             user.password = hashed_password
#             user.save()
#             return redirect("/login")
#     else:
#         form = UserRegistrationForm()
#     return render(request, "sign.html", {"form": form})
def sign(request):
    """Handle the user registration."""
    if request.method == "POST":
        form = UserRegistrationForm(request.POST)
        if form.is_valid():
            password = form.cleaned_data['password']
            hashed_password = bcrypt.hashpw(password.encode("utf-8"), bcrypt.gensalt()).decode("utf-8")
            user = form.save(commit=False)
            user.password = hashed_password
            user.save()
            return redirect("/login")
    else:
        form = UserRegistrationForm()
    return render(request, "sign.html", {"form": form})

# def login(request):
#     """Handle user login and start Streamlit app if successful."""
#     if request.method == "POST":
#         email = request.POST["email"]
#         password = request.POST["password"]
#         try:
#             user = User.objects.get(email=email)
#             # Check the password
#             if bcrypt.checkpw(password.encode("utf-8"), user.password.encode("utf-8")):
#                 request.session["email"] = user.email
#                 # Start Streamlit app as a subprocess
#                 subprocess.Popen(["streamlit", "run", "streamlit_app.py"])
#                 return redirect("/reviews")
#             else:
#                 return render(request, "login.html", {"error": "Invalid credentials"})
#         except User.DoesNotExist:
#             return render(request, "login.html", {"error": "User does not exist"})
#     return render(request, "login.html")
def login(request):
    """Handle user login."""
    if request.method == "POST":
        email = request.POST["email"]
        password = request.POST["password"]
        try:
            user = User.objects.get(email=email)
            if bcrypt.checkpw(password.encode("utf-8"), user.password.encode("utf-8")):
                request.session["email"] = user.email
                return redirect("/reviews")
            else:
                return render(request, "login.html", {"error": "Invalid credentials"})
        except User.DoesNotExist:
            return render(request, "login.html", {"error": "User does not exist"})
    return render(request, "login.html")

def reviews(request):
    """Render the reviews page."""
    # Optionally run the Streamlit app when the page is accessed (if needed).
    # subprocess.Popen(["streamlit", "run", "path/to/your/streamlit_app.py"])

    return render(request, "reviews.html")
