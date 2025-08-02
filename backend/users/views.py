from django.shortcuts import render, redirect
from .models import Contact

def contact_form(request):
    if request.method == 'POST':
        name = request.POST.get('name')
        email = request.POST.get('email')
        Contact.objects.create(name=name, email=email)
        return redirect('success')  # optional success page
    return render(request, 'form.html')
