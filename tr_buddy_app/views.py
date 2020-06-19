from django.shortcuts import render, redirect
from django.contrib import messages
from django.contrib.messages import error
from .models import *
import bcrypt 



def index(request):
    return render(request, "index.html")

def create_user(request): #PASS
    # pass the post data to the method we wrote and save the response in a variable called errors
    if request.method == "POST":
        errors = User.objects.basic_validator(request.POST)
        # check if the errors dictionary has anything in it
        if errors:
        # if the errors dictionary contains anything, loop through each key-value pair and make a flash message
            for e in errors:
                error(request, e)
        # redirect the user back to the form to fix the errors
            return redirect('/')
        # if the errors object is empty, that means there were no errors!

        else:  #PASS THIS HELPS HASH THE PASSWORD
            hashed_pw = bcrypt.hashpw(request.POST['psw'].encode(),bcrypt.gensalt()).decode()   # ADD DECODE METHOD TO THE END
            user = User.objects.create( 
                first_name = request.POST['first_name'], 
                last_name = request.POST['last_name'],
                email = request.POST['email'],
                password = hashed_pw,
            )
            request.session['userid']=user.id

        return redirect('/dashboard')




    

def login(request): #PASS 
    email = User.objects.filter(email=request.POST['email'])

    if len(email) > 0:
        logged_user = email[0]

        if bcrypt.checkpw(request.POST['psw'].encode(),logged_user.password.encode()): # COMPARES THE EXISTED PSW MATCH
            request.session['userid'] = logged_user.id
            return redirect('/dashboard')
        else:
           messages.error(request,"Email and Password did not match")
    else:
        messages.error(request,"This email has not been registered yet!")
    return redirect('/')


def log_out(request):
    request.session.clear()    #pass delete the current session    
    return render(request, "index.html")



def create_trip(request):
    current_user = User.objects.get(id = request.session['userid'])
    if request.method == "POST":
        errors = Trip.objects.basic_validator(request.POST)
        if errors:
            for e in errors:
                error(request, e)

            return redirect('/trips/new')
        
        else:
            the_trip = Trip.objects.create(
                destination = request.POST['destination'], 
                start_date = request.POST['start_date'],
                end_date = request.POST['end_date'],
                plan = request.POST['plan'],
                travels_by = current_user
            )

            request.session['tripid'] = the_trip.id

        return redirect('/dashboard')



def dashboard(request):   #PASS

    Context ={
        'all_trips': Trip.objects.all().order_by("-created_at"),
        'a_user': User.objects.get(id=request.session['userid']),
    }
    return render(request,"dashboard.html", Context)




def delete(request, id):   #PASS delete a post by creator 
    to_delete = Trip.objects.get(id=id)
    to_delete.delete()
    return redirect('/dashboard')




def add_trip_page(request): 
    Context ={
        'a_user': User.objects.get(id=request.session['userid']),
    }

    return render(request,'add_trip.html', Context)

def join(request, id):
    join_trip = Trip.objects.get(id=id)
    this_user = User.objects.get(id=request.session['userid'])
    this_user.has_trips.add(join_trip)
    return redirect('/dashboard')




def editpage(request, id):  #pass
    Context ={
        'a_user': User.objects.get(id=request.session['userid']),
        'a_trip' : Trip.objects.get(id = id)
    }
    return render(request,'edit_trip.html', Context)



def edit_trip(request, id):

    if request.method == "POST":
        errors = Trip.objects.basic_validator(request.POST)
        if errors:
            for e in errors:
                error(request, e)
            return redirect(f'/trips/edit/{id}')
    
        update = Trip.objects.get(id =id)
        update.destination = request.POST["destination"]
        update.start_date = request.POST['start_date']
        update.end_date =request.POST['end_date']
        update.plan = request.POST['plan']
        update.save()

    return redirect(f"/trips/edit/{id}")


def trip_info(request,id):   #PASS
    Context ={
        'a_trip': Trip.objects.get(id=id),
        'a_user': User.objects.get(id=request.session['userid']),
        'all_trips': Trip.objects.all(),

        }
    
    return render(request, "trip_page.html",Context)