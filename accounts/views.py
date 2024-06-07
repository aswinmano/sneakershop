from django.shortcuts import render, redirect
from .forms import RegistrationForm
from .models import Account
from django.contrib import messages,auth
from django.contrib.auth.decorators import login_required

def register(request):
    if request.method == 'POST':
        form = RegistrationForm(request.POST)
        if form.is_valid():
            first_name = form.cleaned_data['first_name']
            last_name = form.cleaned_data['last_name']
            phone_number = form.cleaned_data['phone_number']
            email = form.cleaned_data['email']
            password = form.cleaned_data['password']
            username = email
            

            # Adding +91 to the phone number
            phone_number = phone_number.strip()
            if not phone_number.startswith('+91'):
                phone_number = '+91' + phone_number
            

            # Check if user with the given phone number already exists or not
            if Account.objects.filter(phone_number=phone_number).exists():
                # Add an error message to the form
                form.add_error('phone_number', 'Phone number is already registered!')
                return render(request, 'accounts/register.html', {'form': form})

            # Create the new user
            user = Account.objects.create_user(
                first_name=first_name,
                last_name=last_name,
                phone_number=phone_number,
                email=email,
                username=username,
                password=password
            )

            

            # Redirect to login page with a success message
            return redirect('login')
    else:
        form = RegistrationForm()

    context = {
        'form': form,
    }
    return render(request, 'signup_page.html', context)

def login(request):
    if request.user.is_authenticated:  
        return redirect('index') 
    
    if request.method == 'POST':
        email= request.POST.get('email')
        password = request.POST.get('password')
        # Authenticate user
        user = auth.authenticate(username=email, password=password)

        if user is not None:
            if user.is_active:
                # Log in user
                auth.login(request, user)
                # messages.success(request, 'You are logged in.')
                
                
                return redirect('index')
            else:
                # User is inactive
                # messages.error(request, 'Your account is inactive. Please check your mail box or contact us')
                return redirect('login')
        else:
            # Authentication failed
            # messages.error(request, 'Invalid email/phone or password.')
            return redirect('login')

    return render(request,"login_page.html")

@login_required(login_url = 'login')
def logout(request):
    auth.logout(request)
    # messages.success(request, "You are Logged out")
    return redirect('login')
