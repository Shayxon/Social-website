from django.shortcuts import render
from .forms import LoginForm
from django.contrib.auth import authenticate, login
from django.http import HttpResponse

def login_view(request):

    if request.method == 'POST':
        form = LoginForm(request.POST)

        if form.is_valid():
            cd = form.cleaned_data
            user = authenticate(request, username=cd['username'], password = cd['password'])

            if user is not None:
                if user.is_active:
                    login(request, user)
                    return HttpResponse("Succesfully Logged In!")
                else:
                    return HttpResponse("User disabled")    
            else:
                return HttpResponse('Wrong login!')
    else:
        form = LoginForm()

    return render(request, 'account/login.html', {'form':form})                
