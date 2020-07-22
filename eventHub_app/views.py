from django.shortcuts import render, redirect, HttpResponse
from django.contrib import messages
from .models import User, Event, Cart
import bcrypt

# Create your views here.
def index(request):
    events= Event.objects.all()
    context = {
        'events':events
    }
    return render(request,'index.html', context)

def display_login(request):
    return render(request, 'signin.html')

def display_register(request):
    return render (request, 'register.html')

def dashboard(request):
    if 'uid' not in request.session:
        return redirect('/')
    events= Event.objects.all()
    user = User.objects.get(id = request.session['uid'])
    my_events = user.created_events.all()
    ordered_events = user.events.all()

    context = {
        'events':events,
        'my_events': my_events,
        'ordered_events': ordered_events
    }
    return render(request,'dashboard.html', context)

def display_category(request, category):
    events = Event.objects.filter(category=category)
    all_events = Event.objects.all()
    
    context = {
        'category_events': events,
        'events': all_events
    }
    return render(request,'events_category.html', context)

def display(request, event_id):
    event = Event.objects.get(id=event_id)
    
    context = {
        'event': event
    }
    return render(request,'display.html', context)

def add_to_cart(request, event_id):
    event = Event.objects.get(id=event_id)
    carts= Cart.objects.all().values()
    # return HttpResponse(len(event.cart.all().values()))
    if len(event.cart.all())==0:
        # return HttpResponse("po bon")
        cart = Cart.objects.create(event = event)
        if not "cart" in request.session:
            request.session['cart'] = 1
        else:
            request.session['cart'] +=1
    context =  {
        'event':event
    }
    return redirect(f'/display/{event.id}')

def cart(request):
    carts= Cart.objects.all()
    
    context = {
        'carts':carts
    }
    return render(request, 'cart.html', context)

def one_cart(request, event_id):
    event = Event.objects.get(id=event_id)
    context = {
        'event': event
    }
    return render(request, 'Onecart.html', context)

def buy(request, event_id):
    request.session['redirect'] = (f'oneCart/{event_id}')
    return redirect('/display_login')

def buyTicket(request, event_id):
    user = User.objects.get(id=request.session['uid'])
    event = Event.objects.get(id=event_id)
    cart = event.cart.get(event_id=event_id)
    
    # cart_event = cart.event.id
    
    tickets = request.POST['number']
    total_tickets = int(event.tickets)
    int_tickets = int(tickets)
    # return HttpResponse(total_tickets)
    if total_tickets>=int(tickets):
        # return HttpResponse("po bon")
        request.session['cart'] -= 1    
        total_tickets -=int_tickets
        user.events.add(event)
        cart.delete()
    return redirect('/dashboard')


def new_event(request):
    if 'uid' not in request.session:
        return redirect('/')
    return render(request, 'new_event.html')




def register(request):
    errors = User.objects.validator(request.POST)

    if len(errors)>0:
        for key, value in errors.items():
            messages.error(request,value)
        return redirect('/display_register')
    else:
        print(request.POST['first_name'])
        hash_pw = bcrypt.hashpw(request.POST["password"].encode(), bcrypt.gensalt()).decode()
        
        user = User.objects.create(first_name = request.POST['first_name'], last_name=request.POST['last_name'], email = request.POST['email'], password=hash_pw)

        request.session["uid"] = user.id
        if 'redirect' in request.session:
                redirect_url = request.session['redirect']
                del request.session['redirect']
                return redirect(f'/{redirect_url}')

        return redirect('/dashboard')


def login(request):
    user = User.objects.filter(email=request.POST['email'])
    if len(user)>0:
        logged_user = user[0]
        if bcrypt.checkpw(request.POST['password'].encode(), logged_user.password.encode()):
            request.session['uid'] = logged_user.id
            if 'redirect' in request.session:
                redirect_url = request.session['redirect']
                del request.session['redirect']
                return redirect(f'/{redirect_url}')
            return redirect('/dashboard')
        else:
            messages.error(request,"Email and password did not match")
    else:
        messages.error(request,"Email address is not registered yet.")
    return redirect('/display_login')


def create_event(request):
    
    errors = Event.objects.validator(request.POST)

    if len(errors)>0:
        for key, value in errors.items():
            messages.error(request,value)
        
        return redirect('/new_event')
    else:

        name = request.POST['name']
        location = request.POST['location']
        start_date= request.POST['start_date']
        category = request.POST["category"]
        tickets = request.POST['tickets']
        price = request.POST['price']
        about = request.POST['about']
        print("Category: " + category)
        
        if len(category)<1 or category=="Choose...":
            messages.error(request,"Your event must belong to a category")
            return redirect('/new_event')
        
        else:
            user = User.objects.get(id=request.session['uid'])
            event = Event.objects.create(name=name, location=location,start_date=start_date, category=category, tickets = tickets, price=price, about=about, creator=user)
        
        return redirect('/dashboard')

def logout(request):
    request.session.flush()
    
    return redirect('/')


def edit(request, event_id):
    if 'uid' not in request.session:
        return redirect('/')
    user = User.objects.get(id=request.session['uid'])
    event = Event.objects.get(id=event_id)
    context = {
        'event':event,
        'user':user
    }
    return render(request, 'edit.html', context)

def update(request,event_id):
    errors = Event.objects.validator(request.POST)

    if len(errors)>0:
        for key, value in errors.items():
            messages.error(request,value)
        
        return redirect(f'/edit/{event_id}')
    else:
        event = Event.objects.get(id=event_id)
        event.name = request.POST['name']
        event.location = request.POST['location']
        event.start_date= request.POST['start_date']
        event.category = request.POST["category"]
        event.tickets = request.POST['tickets']
        event.price = request.POST['price']
        event.about = request.POST['about']
        
        if len(category)<1 or category=="Choose...":
            messages.error(request,"Your event must belong to a category")
            return redirect(f'/edit/{event_id}')
        
        else:
            event.save()
        return redirect('/dashboard')
    # if request.method == "POST":
    #     errors = Event.objects.validator(request.POST)
    #     if len(errors)>0:
    #         for key, value in errors.items():
    #             messages.error(request, value)
    #             return redirect(f'/jobs/edit/{job_id}')
    #     job = Job.objects.get(id=job_id)
    #     job.title=request.POST['title']
    #     job.description=request.POST['description']
    #     job.location=request.POST['location']
    #     job.save()
    # return redirect('/dashboard')

def delete(request, event_id):
    user = User.objects.get(id=request.session['uid'])
    event = event.objects.get(id=event_id)
    event.delete()

    return redirect('/dashboard')