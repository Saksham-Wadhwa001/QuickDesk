#!/bin/bash

echo "🚀 Setting up QuickDesk..."

# Install Python dependencies
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt

# Setup database
python manage.py makemigrations
python manage.py makemigrations tickets
python manage.py migrate

# Create sample data
python manage.py shell -c "
from django.contrib.auth.models import User
from tickets.models import UserProfile, Category

# Create admin user
admin, created = User.objects.get_or_create(username='admin', defaults={
    'email': 'admin@example.com',
    'is_staff': True,
    'is_superuser': True,
    'first_name': 'Admin',
    'last_name': 'User'
})
if created:
    admin.set_password('admin123')
    admin.save()
    UserProfile.objects.get_or_create(user=admin, defaults={'role': 'admin'})

# Create sample categories
Category.objects.get_or_create(name='Technical Support', defaults={
    'description': 'Hardware and software issues',
    'created_by': admin
})
Category.objects.get_or_create(name='Account Issues', defaults={
    'description': 'Login and account problems',
    'created_by': admin
})
Category.objects.get_or_create(name='General Inquiry', defaults={
    'description': 'General questions',
    'created_by': admin
})

# Create sample users
user, created = User.objects.get_or_create(username='john_user', defaults={
    'email': 'john@example.com',
    'first_name': 'John',
    'last_name': 'Doe'
})
if created:
    user.set_password('password123')
    user.save()
    UserProfile.objects.get_or_create(user=user, defaults={
        'role': 'end_user',
        'phone': '555-0123',
        'department': 'IT'
    })

agent, created = User.objects.get_or_create(username='jane_agent', defaults={
    'email': 'jane@example.com',
    'first_name': 'Jane',
    'last_name': 'Smith'
})
if created:
    agent.set_password('password123')
    agent.save()
    UserProfile.objects.get_or_create(user=agent, defaults={
        'role': 'support_agent',
        'phone': '555-0124',
        'department': 'Support'
    })

print('✅ Sample data created!')
"

echo "✅ Setup complete!"
echo "🎯 Run: python manage.py runserver"
echo "🌐 Open: http://127.0.0.1:8000"