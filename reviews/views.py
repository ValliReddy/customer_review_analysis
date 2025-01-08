from django.shortcuts import render, redirect
from .forms import UserRegistrationForm
from .models import User
import subprocess
import bcrypt
import os
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
    try:
        # Get the absolute path to the 'streamlit_app.py' inside the 'reviews' folder
        streamlit_script_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'streamlit_app.py')

        # Print the path to confirm it's correct
        print("Streamlit script path:", streamlit_script_path)

        # Check if the file exists at that path
        if os.path.exists(streamlit_script_path):
            # Run the Streamlit app (ensure the path is correct)
            subprocess.Popen(["streamlit", "run", streamlit_script_path])
        else:
            print(f"Streamlit script not found at: {streamlit_script_path}")
    except Exception as e:
        # If there's an error running the Streamlit app, log or handle it
        print(f"Error running Streamlit app: {e}")

    # Render the reviews page
    return render(request, "login.html")
