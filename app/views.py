from django.shortcuts import render
from app.forms import *
from django.http import HttpResponse,HttpResponseRedirect
from django.core.mail import send_mail
from django.urls import reverse
from django.contrib.auth import authenticate,login,logout
from django.contrib.auth.decorators import login_required 


# Create your views here.
def registration(request):
    d={'EUFO':UserForm(),'EPFO':ProfileForm()}
    if request.method=='POST' and request.FILES:
        NMUFDO=UserForm(request.POST) #here only data is coming from the frontend
        NMPFDO=ProfileForm(request.POST,request.FILES)
        if NMUFDO.is_valid() and NMPFDO.is_valid():
            MUFDO=NMUFDO.save(commit=False) #NMUFDO.save() it will directly save into the database but i want to make some modifications so commit=false 
                                     #if commit=false then it will convert non modifiable user form data object into modifiable
            pw=NMUFDO.cleaned_data['password']
            MUFDO.set_password(pw)
            MUFDO.save()



            MPFDO=NMPFDO.save(commit=False)
            MPFDO.username=MUFDO
            MPFDO.save()


            send_mail(
                'REGISTRATION',
                'thank your for using',
                'nandithanarayan1999@gmail.com',
                [MUFDO.email],
                fail_silently=False
            )




            return HttpResponse('registration is successfully')
        else:
            return HttpResponse('invalid data')
    
            
    return render(request,'registration.html',d)





def home(request):
    if request.session.get('username'):
        username=request.session.get('username')
        d={'username':username}
        return render(request,'home.html',d)
    return render(request,'home.html')

    

def user_login(request):
    if request.method=='POST':
        username=request.POST['un']
        password=request.POST['pw']
        AUO=authenticate(username=username,password=password)
        if AUO and AUO.is_active:
            login(request,AUO)
            request.session['username']=username
            return HttpResponseRedirect(reverse('home'))
        else:
            return HttpResponse('invalid data')
            
    return render(request,'user_login.html')


@login_required
def user_logout(request):
    logout(request)
    return HttpResponseRedirect(reverse('home'))
    
@login_required
def profile_display(request):
    username=request.session.get('username')
    UO=User.objects.get(username=username)
    PO=Profile.objects.get(username=UO)
    d={'UO':UO,'PO':PO}
    return render(request,'profile_display.html',d)


@login_required
def change_password(request):
    if request.method=='POST':
        username=request.session.get('username')
        UO=User.objects.get(username=username)
        nw=request.POST['nw']
        UO.set_password(nw)
        UO.save()
        return HttpResponse('password changed successfully')

    return render(request,'change_password.html')
    