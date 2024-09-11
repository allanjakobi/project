import os
import django

# Set the settings module
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'myproject.settings')  # Replace with your project name

# Initialize Django
django.setup()

from django.contrib.auth.models import User
from myapp.models import Users
from django.db import IntegrityError  # Import the IntegrityError exception


# For each user in the Users table, create a corresponding entry in auth_user

users = Users.objects.all()

for user_data in users:
    if User.objects.filter(email=user_data.email).exists():
        print(f"Skipping user with email {user_data.email}, already exists.")
        continue
    
    try:
        user = User.objects.create_user(
            username=user_data.email,  # Use email as username or modify as needed
            email=user_data.email,
            first_name=user_data.firstName,
            last_name=user_data.lastName,
            password='defaultpassword'  # Set a default password; user can change it later
        )
        user.save()
        
        # Now link the user with the Users table
        user_profile = Users.objects.get(userId=user_data.userId)
        user_profile.user = user
        user_profile.save()

        print(f"User profile created for {user_data.email}")
    except IntegrityError as e:
        print(f"Failed to create user profile for {user_data.email}: {e}")