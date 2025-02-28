from django.shortcuts import render
from django.shortcuts import render,redirect
from . import forms
from . import models
from django.contrib.auth.models import User
from django.contrib.auth.models import Group
from django.http import HttpResponseRedirect
from django.shortcuts import render, get_object_or_404
from django.contrib.auth.decorators import login_required
from . models import Worker,Consumer,Chatmodel
from .forms import PaymentForm,WorkerUserForm,WorkerForm,ContractorForm
from django.http import HttpResponse

# from . forms import ServiceForm



from django.core.mail import EmailMultiAlternatives
from django.template.loader import render_to_string
from django.utils.html import strip_tags
from django.conf import settings

def send_email(template, subject, content, recipients, bulk=False):
    sender = settings.EMAIL_HOST_USER
    try:
        # Render HTML content using the provided template
        html_content = render_to_string(template, content)
        text_content = strip_tags(html_content)

        # Handle sending in bulk or individual email
        if bulk:
            msg = EmailMultiAlternatives(subject, text_content, from_email=sender, to=recipients)
            msg.attach_alternative(html_content, 'text/html')
            msg.bcc = recipients  # Blind carbon copy for bulk sending
        else:
            msg = EmailMultiAlternatives(subject, text_content, from_email=sender, to=[recipients])
            msg.attach_alternative(html_content, 'text/html')

            # Send the email
            msg.send()
            print('Mail sent successfully')
            return True
    except Exception as e:
        print(e, 'Mail not sent')
        return False


# Create your views here.
def worker_signup_view(request):
    userform = WorkerUserForm()
    workerform = WorkerForm()
    mydict = {'userform': userform, 'workerform': workerform}

    if request.method == 'POST':
        userform = WorkerUserForm(request.POST)
        workerform = WorkerForm(request.POST, request.FILES)  # Pass request.FILES
        if userform.is_valid() and workerform.is_valid():
            user = userform.save()
            user.set_password(user.password)
            user.save()
            worker = workerform.save(commit=False)
            worker.user = user
            worker.save()
            my_patient_group = Group.objects.get_or_create(name='WORKER')
            my_patient_group[0].user_set.add(user)
            return HttpResponseRedirect('workerlogin')

    return render(request, 'worker/worker_signup.html', context=mydict)

def worker_dashboard_view(request):
    serviceform = forms.ServiceForm()
    worker = models.Worker.objects.get(user_id=request.user.id)  # Get the worker associated with the logged-in user
    
    payments = models.Payment.objects.filter(booking__worker=worker, status='Completed')

    if request.method == 'POST':
        serviceform = forms.ServiceForm(request.POST, request.FILES)
        if serviceform.is_valid():
            services = serviceform.save(commit=False)
            services.worker = worker  # Assign the worker to the service
            services.save()
            return HttpResponseRedirect('services')

    return render(request, 'worker/worker_dashboard.html', {
        'serviceform': serviceform,
        'worker': worker,
        'payments': payments,  # Pass the payments list to the template
    })

def worker_profile_view(request):
    worker = models.Worker.objects.get(user_id=request.user.id)
    return render(request,'worker/profile.html',{'worker':worker})

def services_view(request):
    worker = models.Worker.objects.get(user_id=request.user.id)
    services = models.Services.objects.filter(worker=worker)
    return render(request,'worker/services.html',{'worker':worker, 'services':services})

def update_services_view(request, pk):
    service = get_object_or_404(models.Services, id=pk)
    if request.method == 'POST':
        serviceform = forms.ServiceForm(request.POST, request.FILES, instance=service)
        if serviceform.is_valid():
            serviceform.save()
            return redirect('services')  # Redirect to the services list
    else:
        serviceform = forms.ServiceForm(instance=service)
    
    return render(request, 'worker/update_service.html', {'serviceform': serviceform, 'service': service})

def delete_service_view(request,pk):
    services = models.Services.objects.get(id=pk)
    services.delete()
    return redirect('services')
def bookings_view(request):
    # Get the worker associated with the logged-in user
    worker = models.Worker.objects.filter(user=request.user).first()
    
    if not worker:
        return render(request, 'worker/bookings.html', {'data': [], 'worker': None})

    # Get the services offered by the worker
    worker_services = models.Services.objects.filter(worker=worker)

    # Fetch bookings for the services provided by the worker
    bookings = models.Booking.objects.filter(service__in=worker_services)

    booked_services = []
    booked_bys = []

    for booking in bookings:
        booked_service = booking.service
        booked_by = models.Consumer.objects.filter(id=booking.consumer.id).first()

        booked_services.append(booked_service)
        booked_bys.append(booked_by)

    # Zip the booked services, consumers, and bookings together for rendering
    data = zip(booked_services, booked_bys, bookings)

    # Pass worker explicitly in the context
    return render(request, 'worker/bookings.html', {'data': data, 'worker': worker})


def approve_booking_view(request,pk):
    booking = models.Booking.objects.get(id=pk)
    booking.status = 'Approved'
    booking.save()
    return redirect('bookings')

def reject_booking_view(request,pk):
    booking = models.Booking.objects.get(id=pk)
    booking.status = 'Rejected'
    booking.save()
    return redirect('bookings')


from django.shortcuts import render,redirect,reverse
from django.contrib.auth.models import User
from django.shortcuts import render, get_object_or_404

# Create your views here.


from django.shortcuts import render
from .models import Feedback

from django.shortcuts import render
from .models import Feedback, Advertisement

def home_view(request):
    # Fetch all feedback from the database, ordered by most recent
    feedbacks = Feedback.objects.all().order_by('-created_at')

    # Fetch all approved advertisements
    approved_ads = Advertisement.objects.filter(is_approved=True)

    # Pass both feedbacks and advertisements to the template
    return render(request, 'owner/home.html', {
        'feedbacks': feedbacks,
        'approved_ads': approved_ads
    })

def register_view(request):
    return render(request,'owner/register.html')

from .models import Contractor
from django.contrib.auth import authenticate,login
def login_view(request):
    username=request.POST.get('username')
    password=request.POST.get('password')

    user=authenticate(username=username,password=password)
    if user:
        login(request,user)
        if Worker.objects.filter(user=user).exists():
            return redirect('worker-dashboard')
        elif Contractor.objects.filter(user=user).exists():
            return redirect('contractor-dashboard')
        elif user.is_superuser == True:
            return redirect('admin-dashboard')
        elif Consumer.objects.filter(user=user).exists():
            return redirect('consumer-dashboard')

    return redirect('consumerlogin')

def is_consumer(user):
    return user.groups.filter(name='CONSUMER').exists()

def is_worker(user):
    return user.groups.filter(name='WORKER').exists()


# def afterlogin_view(request):
#     if is_consumer(request.user):
#         return redirect('consumer-dashboard')
#     elif is_worker(request.user):
#         account_approval = wmodels.Worker.objects.filter(user_id=request.user.id).first()
#         if account_approval and account_approval.status:  # Check if the worker is approved
#             return redirect('worker-dashboard')
#         else:
#             return render(request, 'owner/waiting_for_approval.html')  # Show waiting page if not approved
#     else:
#         return redirect('admin-dashboard')
from django.shortcuts import redirect, render
from django.contrib.auth import authenticate
from django.shortcuts import redirect, render
from django.contrib.auth import authenticate

def afterlogin_view(request):
    if is_consumer(request.user):
        return redirect('consumer-dashboard')

    elif is_worker(request.user):
        account_approval = wmodels.Worker.objects.filter(user_id=request.user.id).first()
        if account_approval:
            if account_approval.is_approved:  
                return redirect('worker-dashboard')  # Redirect if approved
            else:
                return render(request, 'owner/waiting_for_approval.html')  # Show waiting page
        else:
            return redirect('some_error_page')  # Handle missing worker profile

    else:
        # Check if the logged-in user is 'urban'
        if request.user.username == "urban":
            return redirect('admin-dashboard')  # Redirect to admin dashboard

        return redirect('contractor-dashboard')  # Redirect to contractor dashboard if not admin

from .models import Consumer, Worker, Advertisement, Payment
from decimal import Decimal
from django.shortcuts import render
from .models import Consumer, Worker, Advertisement, Payment

def admin_dashboard_view(request):
    # Consumer and Worker count
    consumer_count = Consumer.objects.count()
    approved_worker_count = Worker.objects.filter(status='Confirmed').count()
    not_approved_worker_count = Worker.objects.filter(status='Pending').count()

    # Add advertisements (if needed)
    advertisements = Advertisement.objects.all()

    # Query payment details (assuming you want all payments, not just for a specific consumer or worker)
    payments = Payment.objects.all()

    # Define the commission rate as Decimal (to avoid float issues)
    commission_rate = Decimal('0.10')

    # Calculate the commission for each payment (10% of the amount)
    payments_with_commission = []
    for payment in payments:
        commission = payment.amount * commission_rate  # Calculate commission as Decimal
        payments_with_commission.append({
            'payment': payment,
            'commission': commission
        })

    # Pass data to the template
    context = {
        'consumer_count': consumer_count,
        'approved_worker_count': approved_worker_count,
        'not_approved_worker_count': not_approved_worker_count,
        'advertisements': advertisements,
        'payments_with_commission': payments_with_commission,  # Pass payments with commission details
    }

    return render(request, 'owner/admin_dashboard.html', context)

def worker_request_view(request):
    workers = wmodels.Worker.objects.filter(is_approved=False)
    return render(request, 'owner/worker_request.html', {'worker': workers})

# def approve_worker_view(request, pk):
#     worker = wmodels.Worker.objects.get(id=pk)
#     worker.is_approved = True  # Set is_approved to True
#     worker.save()
#     return redirect('admin-approve-worker')

def admin_approve_worker(request):
    workers = wmodels.Worker.objects.all()  # Fetch all workers including approved
    return render(request, 'owner/manage_worker.html', {'worker': workers})

# def reject_worker_view(request, pk):
#     worker = wmodels.Worker.objects.get(id=pk)
#     user = User.objects.get(id=worker.user_id)
#     worker.delete()
#     user.delete()
#     return redirect('worker-request')


def approve_worker_view(request, pk):
    worker = wmodels.Worker.objects.get(id=pk)
    worker.is_approved = True  # Set is_approved to True when admin approves the worker
    worker.save()
    return redirect('admin-approve-worker')  # Redirect to admin worker approval page

def reject_worker_view(request, pk):
    worker = wmodels.Worker.objects.get(id=pk)
    user = User.objects.get(id=worker.user_id)
    worker.delete()  # Delete worker record
    user.delete()  # Delete the user associated with the worker
    return redirect('worker-request')  # Redirect to a page showing worker requests

def manage_worker_view(request):
    workers = wmodels.Worker.objects.filter(is_approved=True)
    return render(request, 'owner/manage_worker.html', {'worker': workers})

def update_worker_view(request, pk):
    worker = get_object_or_404(wmodels.Worker, id=pk)
    user = get_object_or_404(User, id=worker.user_id)
    
    if request.method == 'POST':
        workerForm = forms.WorkerForm(request.POST, request.FILES, instance=worker)
        userform = forms.WorkerUserForm(request.POST, instance=user)

        if workerForm.is_valid() and userform.is_valid():
            userform.save()  # Save the updated user instance
            workerForm.save()  # Save the updated worker instance
            return redirect('manage-worker')
        else:
            print(workerForm.errors)  # Debugging line
            print(userform.errors)  # Debugging line
    else:
        userform = forms.WorkerUserForm(instance=user)
        workerForm = forms.WorkerForm(instance=worker)

    return render(request, 'owner/update_worker.html', {
        'workerform': workerForm,
        'userform': userform
    })
def delete_worker_view(request,pk):
    worker=wmodels.Worker.objects.get(id=pk)
    user=User.objects.get(id=worker.user_id)
    worker.delete()
    user.delete()
    return redirect('manage-worker')

def manage_consumer_view(request):
    consumer = models.Consumer.objects.all()
    return render(request,'owner/manage_consumer.html',{'consumer':consumer})

def update_consumer_view(request, pk):
    consumer = get_object_or_404(models.Consumer, id=pk)
    user = get_object_or_404(User, id=consumer.user_id)
    
    if request.method == 'POST':
        consumerform = forms.ConsumerForm(request.POST, request.FILES, instance=consumer)
        userform = forms.ConsumerUserForm(request.POST, request.FILES, instance=user)  # Note: should use 'user' instead of 'consumer'

        if consumerform.is_valid() and userform.is_valid():
            user = userform.save()  # Save the user instance
            consumer = consumerform.save(commit=False)
            consumer.user = user  # Associate the user with the consumer
            consumer.save()
            return redirect('manage-consumer')
    else:
        userform = forms.ConsumerUserForm(instance=user)  # Initialize user form with user instance
        consumerform = forms.ConsumerForm(instance=consumer)  # Initialize consumer form with consumer instance

    return render(request, 'owner/update_consumer.html', {
        'consumerform': consumerform, 
        'consumer': consumer, 
        'userform': userform
    })

def delete_consumer_view(request,pk):
    is_consumer=models.Consumer.objects.get(id=pk)
    user=User.objects.get(id=is_consumer.user_id)
    is_consumer.delete()
    user.delete()
    return redirect('manage-consumer')

from django.shortcuts import render,reverse
from . import forms,models
from django.db.models import Sum,Q
from django.contrib.auth.models import Group
from django.http import HttpResponseRedirect,Http404
from django.contrib.auth.decorators import login_required,user_passes_test
from django.conf import settings
from datetime import date, timedelta
from django.contrib import messages
from django.shortcuts import get_object_or_404, redirect
from django.contrib import messages
from . models import Booking
# Create your views here.

def consumer_signup_view(request):
    userform=forms.ConsumerUserForm()
    consumerform=forms.ConsumerForm()
    mydict={'userform':userform,'consumerform':consumerform}
    if request.method == 'POST':
        userform=forms.ConsumerUserForm(request.POST)
        consumerform=forms.ConsumerForm(request.POST,request.FILES)
        if userform.is_valid() and consumerform.is_valid():
            user=userform.save()
            user.set_password(user.password)
            user.save()
            consumer=consumerform.save(commit=False)
            consumer.user=user
            consumer.save()
            my_consumer_group = Group.objects.get_or_create(name='CONSUMER')
            my_consumer_group[0].user_set.add(user)
        return HttpResponseRedirect('consumerlogin')
    return render(request,'consumer/consumer_signup.html',context=mydict)

def consumer_dashboard_view(request):
    services = wmodels.Services.objects.all()
    contractor = wmodels.Contractor.objects.all()

    
    bookings = Booking.objects.filter(user=request.user)

    payments = models.Payment.objects.filter(booking__in=bookings)

    return render(request, 'consumer/consumer_dashboard.html', {
        'services': services,
        'payments': payments,
        'contractor':contractor  # Pass payments to the template
    })
def consumer_profile_view(request):
    consumer = models.Consumer.objects.get(user_id=request.user.id)
    return render(request,'consumer/profile.html',{'consumer':consumer})
from django.shortcuts import render
from django.db.models import Q
from itertools import chain
from django.db.models import Q




def search_view(request):
    query = request.GET.get('query', '').strip()  # Get and trim the search query
    
    services = []
    if query:
        # Perform a case-insensitive OR search on skills and city
        services = models.Services.objects.filter(
            Q(skills__icontains=query) | Q(city__icontains=query)
        )
    
    # Check for service count in cart
    service_count_in_cart = 0
    service_ids = request.COOKIES.get('service_ids', '')
    if service_ids:
        service_count_in_cart = len(set(service_ids.split('|')))

    # Message to show in the template
    word = "Searched Result:" if query else "No search query provided"

    context = {
        'services': services,
        'word': word,
        'service_count_in_cart': service_count_in_cart
    }

    return render(request, 'consumer/consumer_dashboard.html', context)

def csearch_view(request):
    query = request.GET.get('query', '').strip()  # Get and trim the search query
    
    services = []
    if query:
        # Perform a case-insensitive OR search on skills and city
        services = models.CServices.objects.filter(
            Q(skills__icontains=query) | Q(city__icontains=query)
        )
    
    # Check for service count in cart
    service_count_in_cart = 0
    service_ids = request.COOKIES.get('service_ids', '')
    if service_ids:
        service_count_in_cart = len(set(service_ids.split('|')))

    # Message to show in the template
    word = "Searched Result:" if query else "No search query provided"

    context = {
        'services': services,
        'word': word,
        'service_count_in_cart': service_count_in_cart
    }

    return render(request, 'consumer/consumer_dashboard.html', context)



from django.http import JsonResponse, HttpResponseRedirect
from django.urls import reverse
from django.contrib import messages

def consumer_address_view(request):
    # Check whether services are present in the cart
    service_in_cart = False
    if 'service_ids' in request.COOKIES:
        service_ids = request.COOKIES['service_ids']
        if service_ids != "":
            service_in_cart = True

    # Count the number of services in the cart
    if 'service_ids' in request.COOKIES:
        service_ids = request.COOKIES['service_ids']
        counter = service_ids.split('|')
        service_count_in_cart = len(set(counter))
    else:
        service_count_in_cart = 0

    addressForm = forms.AddressForm()
    if request.method == 'POST':
        addressForm = forms.AddressForm(request.POST)
        if addressForm.is_valid():
            # Get address data from the form
            name = addressForm.cleaned_data['name']
            mobile = addressForm.cleaned_data['mobile']
            address = addressForm.cleaned_data['address']

            # Save consumer details in the Booking model
            consumer = Booking.objects.create(name=name, mobile=mobile, address=address)

            # Store the consumer ID in session for future use
            request.session['consumer_id'] = consumer.id

            # Calculate total service cost
            total = 0
            if 'service_ids' in request.COOKIES:
                service_ids = request.COOKIES['service_ids']
                if service_ids != "":
                    service_id_in_cart = service_ids.split('|')
                    services = wmodels.Services.objects.filter(id__in=service_id_in_cart)
                    for s in services:
                        total += float(s.service_rate)

            # Proceed to the payment page with the total amount
            response = render(request, 'consumer/payment.html', {'total': total})
            response.set_cookie('name', name)
            response.set_cookie('mobile', mobile)
            response.set_cookie('address', address)
            return response

    return render(request, 'consumer/consumer_address.html', {
        'addressForm': addressForm,
        'service_in_cart': service_in_cart,
        'service_count_in_cart': service_count_in_cart
    })


def payment_success_view(request):
    print('hkgb')
    consumer = models.Consumer.objects.get(id=request.user.id)
    services = None
    name = None
    mobile = None
    address = None

    if 'service_ids' in request.COOKIES:
        service_ids = request.COOKIES['service_ids']
        if service_ids:
            service_id_in_cart = service_ids.split('|')
            services = wmodels.Services.objects.filter(id__in=service_id_in_cart)

    # Accessing customer details from cookies
    if 'name' in request.COOKIES:
        name = request.COOKIES['name']
    if 'mobile' in request.COOKIES:
        mobile = request.COOKIES['mobile']
    if 'address' in request.COOKIES:
        address = request.COOKIES['address']

    # Check if services is not None or empty before iterating
    if services:
        for service in services:
            models.Booking.objects.get_or_create(
                consumer=consumer,
                service=service,
                status='Pending',
                name=name,
                mobile=mobile,
                address=address,
            )

 

    # Deleting cookies after order is placed
    response = render(request, 'consumer/payment_success.html')
    response.delete_cookie('service_ids')
    response.delete_cookie('name')
    response.delete_cookie('mobile')
    response.delete_cookie('address')
    return response


def my_bookings_view(request):
    # Get the consumer associated with the logged-in user
    consumer = models.Consumer.objects.get(user_id=request.user.id)
    
    # Fetch all bookings for the logged-in consumer
    bookings = models.Booking.objects.filter(consumer=consumer)
    
    booked_services = []
    
    for booking in bookings:
        # Fetch the service associated with each booking
        booked_service = booking.service  # Directly access the service related to the booking
        booked_services.append(booked_service)

    # Zip the booked services and bookings together for rendering
    data = zip(booked_services, bookings)

    return render(request, 'consumer/my_bookings.html', {'data': data})

def delete_booking_from_mybookings(request,pk):
    consumer = models.Consumer.objects.get(user_id=request.user.id)

    # Get the booking object to delete
    booking = get_object_or_404(models.Booking, id=pk, consumer=consumer)

    # Delete the booking
    booking.delete()
    
    # Show a success message
    messages.success(request, "Booking deleted successfully.")

    # Redirect back to the My Bookings page
    return redirect('my-bookings') 


# def customer_address_view(request):
#     # this is for checking whether product is present in cart or not
#     # if there is no product in cart we will not show address form
#     product_in_cart=False
#     if 'product_ids' in request.COOKIES:
#         product_ids = request.COOKIES['product_ids']
#         if product_ids != "":
#             product_in_cart=True
#     #for counter in cart
#     if 'product_ids' in request.COOKIES:
#         product_ids = request.COOKIES['product_ids']
#         counter=product_ids.split('|')
#         product_count_in_cart=len(set(counter))
#     else:
#         product_count_in_cart=0

#     addressForm = forms.AddressForm()
#     if request.method == 'POST':
#         addressForm = forms.AddressForm(request.POST)
#         if addressForm.is_valid():
#             # here we are taking address, email, mobile at time of order placement
#             # we are not taking it from customer account table because
#             # these thing can be changes
#             email = addressForm.cleaned_data['Email']
#             mobile=addressForm.cleaned_data['Mobile']
#             address = addressForm.cleaned_data['Address']
#             #for showing total price on payment page.....accessing id from cookies then fetching  price of product from db
#             total=0
#             if 'product_ids' in request.COOKIES:
#                 product_ids = request.COOKIES['product_ids']
#                 if product_ids != "":
#                     product_id_in_cart=product_ids.split('|')
#                     products=models.Product.objects.all().filter(id__in = product_id_in_cart)
#                     print(products)
#                     for p in products:
#                         total=total+p.price

#             response = render(request, 'consumer/payment.html',{'total':total})
#             response.set_cookie('email',email)
#             response.set_cookie('mobile',mobile)
#             response.set_cookie('address',address)
#             return response
#     return render(request,'consumer/consumer_address.html',{'addressForm':addressForm,'product_in_cart':product_in_cart,'product_count_in_cart':product_count_in_cart})




# # here we are just directing to this view...actually we have to check whther payment is successful or not
# #then only this view should be accessed
# def payment_success_view(request):
#     # Here we will place order | after successful payment
#     # we will fetch customer  mobile, address, Email
#     # we will fetch product id from cookies then respective details from db
#     # then we will create order objects and store in db
#     # after that we will delete cookies because after order placed...cart should be empty
#     customer=models.Customer.objects.get(user_id=request.user.id)
#     products=None
#     email=None
#     mobile=None
#     address=None
#     if 'product_ids' in request.COOKIES:
#         product_ids = request.COOKIES['product_ids']
#         if product_ids != "":
#             product_id_in_cart=product_ids.split('|')
#             products=models.Product.objects.all().filter(id__in = product_id_in_cart)
#             # Here we get products list that will be ordered by one customer at a time

#     # these things can be change so accessing at the time of order...
#     if 'email' in request.COOKIES:
#         email=request.COOKIES['email']
#     if 'mobile' in request.COOKIES:
#         mobile=request.COOKIES['mobile']
#     if 'address' in request.COOKIES:
#         address=request.COOKIES['address']

#     # here we are placing number of orders as much there is a products
#     # suppose if we have 5 items in cart and we place order....so 5 rows will be created in orders table
#     # there will be lot of redundant data in orders table...but its become more complicated if we normalize it
#     for product in products:
#         models.Orders.objects.get_or_create(customer=customer,product=product,status='Pending',email=email,mobile=mobile,address=address)

#     # after order placed cookies should be deleted
#     response = render(request,'consumer/payment_success.html')
#     response.delete_cookie('product_ids')
#     response.delete_cookie('email')
#     response.delete_cookie('mobile')
#     response.delete_cookie('address')
#     return response

from django.shortcuts import render,reverse
from . import forms,models
from django.db.models import Sum,Q
from django.contrib.auth.models import Group
from django.http import HttpResponseRedirect,Http404
from django.contrib.auth.decorators import login_required,user_passes_test
from django.conf import settings
from datetime import date, timedelta
from django.contrib import messages
from django.shortcuts import get_object_or_404, redirect
from django.contrib import messages
from . models import Booking
# Create your views here.

def consumer_signup_view(request):
    userform=forms.ConsumerUserForm()
    consumerform=forms.ConsumerForm()
    mydict={'userform':userform,'consumerform':consumerform}
    if request.method == 'POST':
        userform=forms.ConsumerUserForm(request.POST)
        consumerform=forms.ConsumerForm(request.POST,request.FILES)
        if userform.is_valid() and consumerform.is_valid():
            user=userform.save()
            user.set_password(user.password)
            user.save()
            consumer=consumerform.save(commit=False)
            consumer.user=user
            consumer.save()
            my_consumer_group = Group.objects.get_or_create(name='CONSUMER')
            my_consumer_group[0].user_set.add(user)
        return HttpResponseRedirect('consumerlogin')
    return render(request,'consumer/consumer_signup.html',context=mydict)

from django.shortcuts import render
from .models import Services, CServices

def consumer_dashboard_view(request):
    services = Services.objects.all()
    c_services = CServices.objects.all()
    
    # If you're trying to display the contractors related to these services
    contractors = Contractor.objects.all()  # Assuming Contractor is the model with `id`

    return render(request, 'consumer/consumer_dashboard.html', {
        'services': services,
        'c_services': c_services,
        'contractors': contractors,  # Ensure contractors are passed if needed in the template
    })


def consumer_profile_view(request):
    consumer = models.Consumer.objects.get(user_id=request.user.id)
    return render(request,'consumer/profile.html',{'consumer':consumer})


def add_to_cart_view(request, pk):
    services = wmodels.Services.objects.all()
    if 'service_ids' in request.COOKIES:
        service_ids = request.COOKIES['service_ids']
        counter = service_ids.split('|')
        service_count_in_cart = len(set(counter))
    else:
        service_count_in_cart = 0
    if not request.user.is_authenticated:
        return HttpResponseRedirect(reverse('consumerlogin'))
    if 'service_ids' in request.COOKIES:
        service_ids = request.COOKIES['service_ids']
        if service_ids == "":
            service_ids = str(pk)
        else:
            service_ids += "|" + str(pk)
    else:
        service_ids = str(pk)
    response = render(request, 'consumer/consumers_dashboard.html', {
        'services': services,
        'service_count_in_cart': service_count_in_cart + 1 
    })
    response.set_cookie('service_ids', service_ids)
    service = models.Services.objects.get(id=pk)
    print(f"Service added to cart: {service.skills}")  
    return response


def cart_view(request):
    #for cart counter
    if 'service_ids' in request.COOKIES:
        service_ids = request.COOKIES['service_ids']
        counter=service_ids.split('|')
        service_count_in_cart=len(set(counter))
    else:
        service_count_in_cart=0

    # fetching product details from db whose id is present in cookie
    services=None
    total=0
    if 'service_ids' in request.COOKIES:
        service_ids = request.COOKIES['service_ids']
        if service_ids != "":
            service_id_in_cart=service_ids.split('|')
            services=wmodels.Services.objects.all().filter(id__in = service_id_in_cart)

            #for total price shown in cart
            for s in services:
                total += float(s.service_rate)
    return render(request,'consumer/cart.html',{'services':services,'total':total,'service_count_in_cart':service_count_in_cart})

def remove_service_from_cart(request,pk):
    if 'service_ids' in request.COOKIES:

        service_ids = request.COOKIES['service_ids']
        counter=service_ids.split('|')
        service_count_in_cart=len(set(counter))
    else:
        service_count_in_cart=0

    # removing product id from cookie
    total=0
    if 'service_ids' in request.COOKIES:
        service_ids = request.COOKIES['service_ids']
        service_id_in_cart=service_ids.split('|')
        service_id_in_cart=list(set(service_id_in_cart))
        service_id_in_cart.remove(str(pk))
        services=wmodels.Services.objects.all().filter(id__in = service_id_in_cart)
        #for total price shown in cart after removing product
        for s in services:
            total += float(s.service_rate)

        #  for update coookie value after removing product id in cart
        value=""
        for i in range(len(service_id_in_cart)):
            if i==0:
                value=value+service_id_in_cart[0]
            else:
                value=value+"|"+service_id_in_cart[i]
        response = render(request, 'consumer/cart.html',{'services':services,'total':total,'service_count_in_cart':service_count_in_cart})
        if value=="":
            response.delete_cookie('service_ids')
        response.set_cookie('service_ids',value)
        return response
    

# def cart_view(request):
#     #for cart counter
#     if 'product_ids' in request.COOKIES:
#         product_ids = request.COOKIES['product_ids']
#         counter=product_ids.split('|')
#         product_count_in_cart=len(set(counter))
#     else:
#         product_count_in_cart=0

#     # fetching product details from db whose id is present in cookie
#     products=None
#     total=0
#     if 'product_ids' in request.COOKIES:
#         product_ids = request.COOKIES['product_ids']
#         if product_ids != "":
#             product_id_in_cart=product_ids.split('|')
#             products=models.Product.objects.all().filter(id__in = product_id_in_cart)

#             #for total price shown in cart
#             for p in products:
#                 total=total+p.price
#     return render(request,'consumer/cart.html',{'products':products,'total':total,'product_count_in_cart':product_count_in_cart})


# def remove_service_from_cart(request,pk):
#     #for counter in cart
#     if 'product_ids' in request.COOKIES:
#         product_ids = request.COOKIES['product_ids']
#         counter=product_ids.split('|')
#         product_count_in_cart=len(set(counter))
#     else:
#         product_count_in_cart=0

#     # removing product id from cookie
#     total=0
#     if 'product_ids' in request.COOKIES:
#         product_ids = request.COOKIES['product_ids']
#         product_id_in_cart=product_ids.split('|')
#         product_id_in_cart=list(set(product_id_in_cart))
#         product_id_in_cart.remove(str(pk))
#         products=models.Product.objects.all().filter(id__in = product_id_in_cart)
#         #for total price shown in cart after removing product
#         for p in products:
#             total=total+p.price

#         #  for update coookie value after removing product id in cart
#         value=""
#         for i in range(len(product_id_in_cart)):
#             if i==0:
#                 value=value+product_id_in_cart[0]
#             else:
#                 value=value+"|"+product_id_in_cart[i]
#         response = render(request, 'consumer/cart.html',{'products':products,'total':total,'product_count_in_cart':product_count_in_cart})
#         if value=="":
#             response.delete_cookie('product_ids')
#         response.set_cookie('product_ids',value)
#         return response


from django.shortcuts import render, redirect
from . import forms, models as wmodels
from .models import Booking
from django.shortcuts import render, redirect
from . import forms
from .models import Booking, Services  # Ensure to import your models

def consumer_address_view(request):
    # Check whether services are present in the cart
    service_in_cart = 'service_ids' in request.COOKIES and request.COOKIES['service_ids'] != ""
    
    # Count the number of services in the cart
    service_count_in_cart = 0
    if service_in_cart:
        service_ids = request.COOKIES['service_ids']
        counter = service_ids.split('|')
        service_count_in_cart = len(set(counter))

    addressForm = forms.AddressForm()
    if request.method == 'POST':
        lat=request.POST.get('lat')
        long=request.POST.get('long')
        addressForm = forms.AddressForm(request.POST)
        if addressForm.is_valid():
            # Get address data from the form
            name = addressForm.cleaned_data['name']
            mobile = addressForm.cleaned_data['mobile']

            # Save consumer details in the Booking model
            consumer = Booking.objects.create(name=name, mobile=mobile,lat=lat,long=long)
            request.session['lat']=lat
            request.session['long']=long

            # Store the consumer ID in session for future use
            request.session['consumer_id'] = consumer.id

            # Calculate total service cost
            total = 0
            if service_in_cart:
                service_id_in_cart = request.COOKIES['service_ids'].split('|')
                services = Services.objects.filter(id__in=service_id_in_cart)
                for s in services:
                    total += float(s.service_rate)

            # Set cookies for the consumer details
            response = redirect('payment')  # Assuming 'payment' is the name of the payment URL
            response.set_cookie('name', name)
            response.set_cookie('mobile', mobile)

            return response  # Redirect to payment page

        else:
            print(addressForm.errors)  # Log errors for debugging

    return render(request, 'consumer/consumer_address.html', {
        'addressForm': addressForm,
        'service_in_cart': service_in_cart,
        'service_count_in_cart': service_count_in_cart
    })




from django.shortcuts import render, get_object_or_404



from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from . import models

@login_required
def payment_success_view(request):
    print(f"Authenticated user: {request.user}")  # Debugging line

    try:
        consumer = get_object_or_404(models.Consumer, user=request.user)
    except ValueError as e:
        print(f"Error retrieving consumer: {e}")  # Debugging line
        return redirect('error-page')  # Redirect to an error page or handle the error

    services = None
    name = request.COOKIES.get('name')
    mobile = request.COOKIES.get('mobile')
    lat=request.session.get('lat')
    long=request.session.get('long')

    order_date=request.POST.get('order_date')
    print(order_date)

    service_ids = request.COOKIES.get('service_ids')
    if service_ids:
        service_id_in_cart = service_ids.split('|')
        services = wmodels.Services.objects.filter(id__in=service_id_in_cart)

    if services:
        for service in services:
            models.Booking.objects.get_or_create(
                consumer=consumer,
                service=service,
                status='Pending',
                name=name,
                mobile=mobile,
                lat=lat,
                long=long,
                order_date=order_date
            )


        template = 'mail.html'  
        subject = 'Welcome to Our Service!'
        content = {'username': 'John Doe'}  
        recipients =services.first().worker.email
        print(recipients)
        send_email(template, subject, content, recipients)


    response = render(request, 'consumer/payment_success.html')
    response.delete_cookie('service_ids')
    response.delete_cookie('name')
    response.delete_cookie('mobile')
    response.delete_cookie('address')
    return response

def my_bookings_view(request):
    consumer = models.Consumer.objects.get(user_id=request.user.id)
    
    # Fetch all bookings for the logged-in consumer
    bookings = models.Booking.objects.filter(consumer=consumer)
    
    booked_services = []
    
    for booking in bookings:
        # Fetch the service associated with each booking
        booked_service = booking.service  # Directly access the service related to the booking
        booked_services.append(booked_service)

    # Zip the booked services and bookings together for rendering
    data = zip(booked_services, bookings)

    return render(request, 'consumer/my_bookings.html', {'data': data})

def payment_view(request):
    return render(request,'consumer/payment.html')


from django.shortcuts import render, get_object_or_404, redirect
from .models import Booking, Payment, Worker, Consumer
from .forms import PaymentForm
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, get_object_or_404, redirect
from .models import Booking, Payment
from .forms import PaymentForm
from decimal import Decimal

def amountpay_view(request, booking_id):
    booking = get_object_or_404(Booking, id=booking_id)
    
    if request.method == "POST":
        form = PaymentForm(request.POST)
        if form.is_valid():
            payment = form.save(commit=False)
            payment.booking = booking

            # Use Decimal for precision when calculating the commission
            commission = payment.amount * Decimal('0.10')  # Use Decimal here
            print(commission)
            payment.save()

            # Redirect to the single payment page
            return redirect('singlepayment')
    else:
        form = PaymentForm()

    return render(request, 'consumer/amountpay.html', {
        'form': form,
        'booking': booking,
    })

def paysuccess_view(request, id):   
    booking = get_object_or_404(Booking, id=id)
    payment = Payment.objects.filter(booking=booking).first()
    if not payment:
        return render(request, 'consumer/success.html', {
            'message': 'No payment details found for this order'
        })
    return render(request, 'consumer/success.html', {
        'payment': payment,
        'booking': booking
    })

@login_required
def view_payment_details(request, user_id):
    payments = Payment.objects.filter(booking__user_id=user_id)
    if not payments.exists():
        return render(request, 'consumer/payment_details.html', {
            'message': 'No payment details found for this user'
        })
    return render(request, 'consumer/payment_details.html', {
        'payments': payments
    })

# def singlepayment_view(request):
#     consumer = get_object_or_404(Consumer, user=request.user)
#     user_bookings = Booking.objects.filter(consumer=consumer)
#     payments = Payment.objects.filter(booking__in=user_bookings)
#     return render(request, 'consumer/singlepayment.html', {
#         'payments': payments
#     })
from decimal import Decimal
from django.shortcuts import render
from .models import Payment

def singlepayment_view(request):
    payments = Payment.objects.all()
    payments_with_commission = []

    # Convert the commission rate to a Decimal
    commission_rate = Decimal('0.10')  # 10% commission

    # Calculate commission for each payment
    for payment in payments:
        commission = payment.amount * commission_rate  # Now using Decimal
        payments_with_commission.append({
            'payment': payment,
            'commission': commission
        })

    return render(request, 'consumer/singlepayment.html', {
        'payments_with_commission': payments_with_commission,
    })


@login_required
def worker_payment_details(request, worker_id):
    worker = get_object_or_404(Worker, id=worker_id)
    payments = Payment.objects.filter(worker=worker)
    return render(request, 'worker/payment_details.html', {
        'worker': worker,
        'payments': payments
    })



def chat(request,rec_id):
    if Worker.objects.filter(user=request.user).exists():
            message=Chatmodel.objects.filter(worker__user=request.user,consumer__id=rec_id)
            template='worker/workerchat.html'
    else:
        message=Chatmodel.objects.filter(consumer__user=request.user,worker__id=rec_id)
        template='consumer/chat.html'

    messages_with_dynamic_value = []

    for msg in message:
        messages_with_dynamic_value.append({
            'message': msg,
            'dynamic_value': True if msg.sender==request.user else False
        })
    return render(request,template,{'message':messages_with_dynamic_value,'rec_id':rec_id,})
 


def chat_message(request,receiverid):
    if request.method=='POST':
        message=request.POST.get('message')
        print(request.user)
        user=request.user
        worker=None
        consumer=None
        try:
            worker=Worker.objects.get(user=user)
            print(worker,receiverid,'test')
            consumer=get_object_or_404(Consumer,id=receiverid)
            Chatmodel.objects.create(message=message,worker=worker,consumer=consumer,sender=worker.user)
        except Exception as e:
            print(e,'sadfa')
            consumer=Consumer.objects.get(user=user)
            worker=get_object_or_404(Worker,id=receiverid)
            Chatmodel.objects.create(message=message,worker=worker,consumer=consumer,sender=consumer.user)
    return redirect('chat',rec_id=receiverid)   
     
                 
def contractor_view(request):
    userform = WorkerUserForm()
    ContractorForm = ContractorForm()
    mydict = {'userform': userform, 'workerform': workerform}

    if request.method == 'POST':
        userform = WorkerUserForm(request.POST)
        ContractorFormform = ContractorForm(request.POST, request.FILES)  # Pass request.FILES
        if userform.is_valid() and ContractorForm.is_valid():
            user = userform.save()
            user.set_password(user.password)
            user.save()
            contractor = ContractorForm.save(commit=False)
            contractor.user = user
            contractor.save()
            my_patient_group = Group.objects.get_or_create(name='CONTRACTOR')
            my_patient_group[0].user_set.add(user)
            return HttpResponseRedirect('workerlogin')

    return render(request, 'worker/worker_signup.html', context=mydict)


# from.forms import WorkeraboutForm
# def workerabout_view(request):
#     if request.method == 'POST':
#         worker=get_object_or_404(Worker,user=request.user)
#         form = WorkeraboutForm(request.POST, request.FILES)
#         if form.is_valid():
#             data=form.save(commit=False)  # Save the form data to the database
#             data.worker=worker
#             data.save()
#             return redirect('worker-dashboard')  # Redirect to a success page (replace 'success' with your desired route)
#     else:
#         form = WorkeraboutForm()
    
#     # Render the template with the form
#     return render(request, 'worker/workerabout.html', {'form': form})


from django.shortcuts import get_object_or_404, redirect, render
from .forms import WorkeraboutForm
from .models import Workerabout, Worker
from django.shortcuts import get_object_or_404, redirect, render
from .forms import WorkeraboutForm
from .models import Workerabout, Worker

def workerabout_view(request):
    # Get the worker object for the logged-in user
    worker = get_object_or_404(Worker, user=request.user)

    # Check if the worker already has a 'Workerabout' entry
    try:
        workerabout = Workerabout.objects.get(worker=worker)
    except Workerabout.DoesNotExist:
        workerabout = None  # If no entry exists, workerabout will be None
    
    if request.method == 'POST':
        form = WorkeraboutForm(request.POST, request.FILES, instance=workerabout)
        
        if form.is_valid():
            if workerabout:
                # Update existing Workerabout record
                form.save()  # Since `instance=workerabout`, this will update the existing record
            else:
                # Create a new Workerabout record
                workerabout = form.save(commit=False)
                workerabout.worker = worker  # Link the worker to the Workerabout
                workerabout.save()  # Save the new Workerabout record
            return redirect('worker-dashboard')  # Redirect after successful submission
    else:
        # If it's a GET request, prepopulate the form with the existing data (if available)
        form = WorkeraboutForm(instance=workerabout)

    # Render the template with the form (either new or pre-filled with existing data)
    return render(request, 'worker/workerabout.html', {'form': form})


from .models import Workerabout
from django.shortcuts import get_object_or_404, render
from .models import Worker, Workerabout

def aboutinfo_view(request, worker_id):
    # Get the worker object by ID (this could be passed dynamically)
    worker = get_object_or_404(Worker, id=worker_id)

    # Retrieve the latest Workerabout entry related to the worker (ordered by date, assuming there is a 'created_at' or 'updated_at' field)
    worker_about = Workerabout.objects.filter(worker=worker).last()  # Adjust 'created_at' to your model field name

    # Print the worker_about for debugging purposes (optional)
    print(worker_about)

    # Pass the latest worker_about object to the template
    return render(request, 'worker/aboutinfo.html', {'about': worker_about})

from django.shortcuts import render, redirect, get_object_or_404
from django.http import HttpResponseRedirect
from . import models, forms
from django.urls import reverse

def contractor_dashboard_view(request):
    serviceform = forms.CServiceForm()

    # Get the contractor associated with the logged-in user
    contractor = get_object_or_404(models.Contractor, user=request.user)  # Get the contractor (not worker)

    if request.method == 'POST':
        serviceform = forms.CServiceForm(request.POST, request.FILES)
        if serviceform.is_valid():
            services = serviceform.save(commit=False)
            services.contractor = contractor  # Assign the contractor to the service
            services.save()
            # Redirect to the 'cservices' URL
            return HttpResponseRedirect(reverse('cservices'))

    return render(request, 'contractor/contractor_dashboard.html', {
        'serviceform': serviceform,
        'contractor': contractor,  # Passing contractor instead of worker
    })



def contractor_register(request):
    if request.method == 'POST':
        username=request.POST.get('username')
        password=request.POST.get('password')
        print(username)
        email=request.POST.get('email')
        user = User.objects.create_user(username=username, email=email, password=password)

        form = ContractorForm(request.POST,request.FILES)
        if form.is_valid():
            # Extract user data from the form
            # Create a new User

            # Save the Contractor instance linked to the User
            contractor = form.save(commit=False)
            contractor.user = user  # Link the Contractor to the User
            contractor.save()  # Save the Contractor instance

            # Display a success message and redirect
            messages.success(request, "Registration successful!")
            return redirect('contractorlogin')  # Redirect to the contractor dashboard
        else:
            # Print form errors for debugging
            print(form.errors)
    else:
        # If it's a GET request, initialize an empty form
        form = ContractorForm()

    # Render the registration template with the form
    return render(request, 'contractor/contractor_register.html', {'form': form})



from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login
from django.contrib import messages
from .models import Contractor

def contractor_login(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(request, username=username, password=password)

        if user is not None:
            login(request, user)
            
            # Check if the user is a contractor
            try:
                contractor = Contractor.objects.get(user=user)
                if not contractor.is_approved:
                    return redirect('contractor_waiting')  # Redirect to waiting page
                return redirect('contractor-dashboard')  # Redirect to dashboard if approved
            except Contractor.DoesNotExist:
                messages.error(request, "You are not a registered contractor.")
                return redirect('contractorlogin')
        else:
            messages.error(request, "Invalid username or password.")
            return redirect('contractorlogin')
    
    return render(request, 'contractor/contractor_login.html')

def contractor_waiting(request):
    return render(request, 'contractor/contractor_waiting.html')


def contractor_request_view(request):
    contractors = wmodels.Contractor.objects.filter(is_approved=False)
    print(contractors,'fyujm')
    return render(request, 'owner/contractor_request.html', {'contractor': contractors})

def approve_contractor_view(request, pk):
    contractor = wmodels.Contractor.objects.get(id=pk)
    contractor.is_approved = True  # Set is_approved to True when admin approves the worker
    contractor.save()
    return redirect('manage-contractor')  # Redirect to admin worker approval page
    


def reject_contractor_view(request, pk):
    contractor = wmodels.Contractor.objects.get(id=pk)
    user = User.objects.get(id=contractor.user_id)
    contractor.delete()  # Delete worker record
    user.delete()  # Delete the user associated with the worker
    return redirect('contractor-request')  # Redirect to a page showing worker requests

def admin_approve_contractor(request):
    contractors = wmodels.Contractor.objects.filter(is_approved=False)
    return render(request, 'owner/manage_contractor.html', {'contractor': contractors})

def manage_contractor_view(request):
    contractors= wmodels.Contractor.objects.filter(is_approved=True)
    return render(request, 'owner/manage_contractor.html', {'contractor': contractors})

def update_contractor_view(request, pk):
    contractor = get_object_or_404(wmodels.Contractor, id=pk)
    user = get_object_or_404(User, id=contractor.user_id)
    
    if request.method == 'POST':
        print('hiiii')
        ContractorForm = forms.ContractorForm(request.POST, request.FILES, instance=contractor)
        userform = forms.WorkingUserForm(request.POST, instance=user)

        if ContractorForm.is_valid() and userform.is_valid():
            userform.save()  # Save the updated user instance
            ContractorForm.save()  # Save the updated worker instance
            return redirect('manage-contractor')
        else:
            print(ContractorForm.errors)  # Debugging line
            print(userform.errors)  # Debugging line
    else:
        userform = forms.WorkingUserForm(instance=user)
        ContractorForm = forms.ContractorForm(instance=contractor)

    return render(request, 'owner/update_contractor.html', {
        'Contractorform': ContractorForm,
        'userform': userform,
        'contractor':contractor
    })
def delete_contractor_view(request,pk):
    contractor=wmodels.Contractor.objects.get(id=pk)
    user=User.objects.get(id=contractor.user_id)
    contractor.delete()
    user.delete()
    return redirect('manage-contractor')

def location(request,re_id):
    report=get_object_or_404(Booking,id=re_id)
    print(report.lat,report.long)
    return render(request,'worker/location.html',{'lat':report.lat,'long':report.long})


from .forms import FeedbackForm

def feedback_view(request):
    if request.method == 'POST':
        form = FeedbackForm(request.POST)
        if form.is_valid():
            form.save()  # Save the feedback to the database
            return redirect('home')  # Redirect to the 'thank_you' page after submission
    else:
        form = FeedbackForm()

    return render(request, 'consumer/feedback_form.html', {'form': form})


from .models import Feedback

def feedback_list(request):
    feedbacks = Feedback.objects.all().order_by('-created_at')  # Order by the most recent feedback
    print(feedbacks)
    return render(request, 'feedback_list.html', {'feedbacks': feedbacks})


# views.py
from django.shortcuts import render, redirect
from .forms import AdvertisementForm

def advertisement_create(request):
    if request.method == 'POST':
        form = AdvertisementForm(request.POST, request.FILES)
        if form.is_valid():
            advertisement = form.save(commit=False)
            advertisement.save()  # Save the advertisement with the contractor
            return redirect('contractor-dashboard')  # Redirect to the contractor dashboard or another page
    else:
        form = AdvertisementForm()

    return render(request, 'contractor/advertisement_create.html', {'form': form})


# views.py
from django.shortcuts import render, get_object_or_404, redirect
from .models import Advertisement
from django.contrib.auth.decorators import login_required
def contractor_advertisement_list(request):
    # Get advertisements where is_approved is False
    advertisements = Advertisement.objects.all()
    print(advertisements)
    return render(request, 'contractor/contractor_advertisement_list.html', {
        'advertisements': advertisements
    })


from django.shortcuts import render, get_object_or_404, redirect
from .models import Advertisement

def approve_advertisement(request, pk):
    # Get the advertisement by its primary key (pk)
    ad = get_object_or_404(Advertisement, pk=pk)

    # Only allow approval if it's not already approved
    if not ad.is_approved:
        ad.is_approved = True
        ad.save()

    return redirect('contractor_advertisement_list')  # Redirect to the list of advertisements


from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from .forms import AdpaymentForm
from .models import Adpayment, Contractor

def add_payment(request):
    # Ensure the user is a contractor
    try:
        contractor = Contractor.objects.get(user=request.user)
    except Contractor.DoesNotExist:
        # If the user is not a contractor, redirect to an error or another page
        return redirect('some-error-page')

    if request.method == 'POST':
        form = AdpaymentForm(request.POST)
        if form.is_valid():
            # Save the payment with the current contractor
            payment = form.save(commit=False)
            payment.contractor = contractor  # Associate the payment with the contractor
            payment.save()
            return redirect('contractor-dashboard')  # Redirect to the contractor dashboard or another page after submission
    else:
        form = AdpaymentForm()  # Create an empty form if the request is GET
    
    return render(request, 'contractor/add_payment.html', {'form': form})


from django.contrib.admin.views.decorators import staff_member_required
from django.shortcuts import render
from .models import Adpayment

@staff_member_required  # Only accessible by staff members (admins)
def admin_payment_list(request):
    payments = Adpayment.objects.all()  # Fetch all payments
    return render(request, 'owner/payment_list.html', {'payments': payments})



def cservices_view(request):
    contractor = models.Contractor.objects.get(user_id=request.user.id)
    services = models.CServices.objects.filter(contractor=contractor)
    return render(request,'contractor/cservices.html',{'contractor':contractor, 'services':services})

def update_cservices_view(request, pk):
    service = get_object_or_404(models.CServices, id=pk)
    if request.method == 'POST':
        serviceform = forms.CServiceForm(request.POST, request.FILES, instance=service)
        if serviceform.is_valid():
            serviceform.save()
            return redirect('cservices')  # Redirect to the services list
    else:
        serviceform = forms.CServiceForm(instance=service)
    
    return render(request, 'contractor/update_cservice.html', {'serviceform': serviceform, 'service': service})

def delete_cservice_view(request,pk):
    services = models.CServices.objects.get(id=pk)
    services.delete()
    return redirect('cservices')


from . models import Chats
# View for rendering the chat page
def chats(request, chat_id):
    # Determine whether the user is a contractor or consumer
    if Contractor.objects.filter(user=request.user).exists():
        chat_details = Chats.objects.filter(contractor__user=request.user, consumer__id=chat_id)
        template = 'contractor/contractorchat.html'
    else:
        chat_details = Chats.objects.filter(consumer__user=request.user, contractor__id=chat_id)
        template = 'consumer/cchat.html'

    chats_with_dynamic_value = []

    # Add dynamic value based on whether the message is from the user
    for chat in chat_details:
        chats_with_dynamic_value.append({
            'message': chat,
            'dynamic_value': True if chat.sender == request.user else False
        })

    return render(request, template, {'chats': chats_with_dynamic_value, 'chat_id': chat_id})


# View for posting chat messages
def chats_message(request, receiver_id):
    if request.method == 'POST':
        message = request.POST.get('message')
        user = request.user
        contractor = None
        consumer = None

        try:
            # If the user is a contractor, create chat message for consumer
            contractor = Contractor.objects.get(user=user)
            consumer = get_object_or_404(Consumer, id=receiver_id)
            Chats.objects.create(message=message, contractor=contractor, consumer=consumer, sender=contractor.user)
        except Exception as e:
            # If the user is a consumer, create chat message for contractor
            consumer = Consumer.objects.get(user=user)
            contractor = get_object_or_404(Contractor, id=receiver_id)
            Chats.objects.create(message=message, contractor=contractor, consumer=consumer, sender=consumer.user)

    return redirect('chats', chat_id=receiver_id)



# views.py
from django.shortcuts import render
from .models import Consumer

# views.py
from django.shortcuts import render
from .models import Chats, Consumer, Contractor

def all_consumers(request, contractor_id):
    contractor = Contractor.objects.get(id=contractor_id)
    
    chats = Chats.objects.filter(contractor=contractor).distinct()
    
    consumers = Consumer.objects.filter(chats__in=chats).distinct()

    return render(request, 'contractor/all_consumers.html', {'consumers': consumers, 'contractor': contractor})


# views.py
from django.shortcuts import render, redirect, get_object_or_404
from .models import Contractorabout, Contractor
from .forms import ContractoraboutForm

def contractorabout_view(request):
    if request.method == 'POST':
        contractor = get_object_or_404(Contractor, user=request.user)  # Assuming Contractor model has a `user` field
        form = ContractoraboutForm(request.POST, request.FILES)
        if form.is_valid():
            data = form.save(commit=False)
            data.contractor = contractor
            data.save()
            return redirect('contractor-complete')  # Redirect to contractor's dashboard or desired route
    else:
        form = ContractoraboutForm()

    return render(request, 'contractor/contractorabout.html', {'form': form})

def contaboutinfo_view(request, contractor_id):
    contractor = get_object_or_404(Contractor, id=contractor_id)
    contractor_about = Contractorabout.objects.filter(contractor=contractor).first()
    print(contractor_about)  # For debugging purposes
    return render(request, 'contractor/aboutinfo.html', {'about': contractor_about})

from django.shortcuts import render
from .models import Advertisement

def approved_ads_view(request):
    # Filter advertisements that are approved
    approved_ads = Advertisement.objects.filter(is_approved=True)
    
    return render(request, 'ads/approved_ads.html', {'approved_ads': approved_ads})

# views.py
from django.contrib.auth.forms import PasswordResetForm
from django.contrib.auth import get_user_model
from django.shortcuts import render, redirect
from django.contrib.auth.tokens import default_token_generator
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode

def forgot_password_view(request):
    if request.method == 'POST':
        # Here we simulate password reset by taking the username and resetting the password directly
        username = request.POST.get('username')
        new_password = request.POST.get('new_password')

        # Find the user based on username
        user = get_user_model().objects.filter(username=username).first()

        if user:
            # Set the new password
            user.set_password(new_password)
            user.save()
            return redirect('home')  # Redirect to a success page
        else:
            # If user doesn't exist, you can show an error message
            return render(request, 'consumer/forgot_password.html', {'error': 'User not found'})

    return render(request, 'consumer/forgot_password.html')

def editinfo_view(request, pk):
    service = get_object_or_404(models.Workerabout, id=pk)
    if request.method == 'POST':
        serviceform = forms.WorkeraboutForm(request.POST, request.FILES, instance=service)
        if serviceform.is_valid():
            serviceform.save()
            return redirect('worker-dashboard')  # Redirect to the services list
    else:
        serviceform = forms.WorkeraboutForm(instance=service)
    
    return render(request, 'worker/editinfo.html', {'serviceform': serviceform, 'service': service})



from.forms import WorkeraboutForm
def workerabout_view(request):
    if request.method == 'POST':
        worker=get_object_or_404(Worker,user=request.user)
        form = WorkeraboutForm(request.POST, request.FILES)
        if form.is_valid():
            data=form.save(commit=False)  # Save the form data to the database
            data.worker=worker
            data.save()
            return redirect('complete')  # Redirect to a success page (replace 'success' with your desired route)
    else:
        form = WorkeraboutForm()
    
    # Render the template with the form
    return render(request, 'worker/workerabout.html', {'form': form})


from django.shortcuts import render, redirect
from .forms import NotificationForm

from django.shortcuts import render, redirect
from .forms import NotificationForm
from .models import Notification, Contractor

from django.shortcuts import render, redirect
from .forms import NotificationForm
from .models import Notification, Contractor

def add_notification(request):
    contractors = Contractor.objects.all()  # Get all contractors to display in the template

    if request.method == 'POST':
        form = NotificationForm(request.POST)
        if form.is_valid():
            # Ensure the consumer is automatically set
            notification = form.save(commit=False)  # Do not save to the database yet
            notification.consumer = request.user.consumer  # Set the consumer field to the logged-in user
            notification.save()  # Now save the notification

            return redirect('consumer-dashboard')  # Redirect to a success page after submission
    else:
        form = NotificationForm()  # Empty form for GET request

    # Pass both the form and the contractor details to the template
    return render(request, 'consumer/add_notification.html', {'form': form, 'contractors': contractors})


from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from .models import Notification, Contractor

def contractor_notifications(request):
    contractor = Contractor.objects.get(user=request.user)
    
    notifications = Notification.objects.filter(contractor=contractor)
    
    return render(request, 'contractor/notifications.html', {'notifications': notifications})


from django.urls import reverse

def completes(request):
    worker = models.Worker.objects.get(user_id=request.user.id)  # Get the worker associated with the logged-in user
    payments = models.Payment.objects.filter(booking__worker=worker, status='Completed')  # Fetch completed payments
    
    payment_details_url = reverse('payment_details', kwargs={'worker_id': worker.id})  # Ensure worker_id is passed

    return render(request, 'worker/complete.html', {
        'worker': worker,
        'payments': payments,
        'payment_details_url': payment_details_url  # Pass the URL to the template
    })

def contractor_complete(request):

    return render(request, 'contractor/contractor_complete.html')




import random
import string

def generate_otp(length=6):
    otp = ''.join(random.choices(string.digits, k=length))
    return otp


from django.conf import settings
from django.core.mail import EmailMultiAlternatives
from django.template.loader import render_to_string
from django.utils.html import strip_tags
from django.core.mail import EmailMultiAlternatives
from django.template.loader import render_to_string
from django.utils.html import strip_tags
from django.conf import settings

def send_email(template, subject, content, recipients, bulk=False):
    sender = settings.EMAIL_HOST_USER
    try:
        html_content = render_to_string(template, content)
        text_content = strip_tags(html_content)

        if bulk:
            msg = EmailMultiAlternatives(subject, text_content, from_email=sender, to=recipients)
            msg.attach_alternative(html_content, 'text/html')
            msg.bcc = recipients 
        else:
            msg = EmailMultiAlternatives(subject, text_content, from_email=sender, to=[recipients])
            msg.attach_alternative(html_content, 'text/html')

        msg.send()
        print('Mail sent successfully')
        return True
    except Exception as e:
        print(e, 'Mail not sent')
        return False

def password_reset(request):
    # Check if the request method is POST
    if request.method == 'POST':
        mail = request.POST.get('email')
        otp=generate_otp()
        
        recipient = mail
        subject = "Otp from crisis connect"
        content = {'content': 'content','otp':otp}
        template = "./smail.html"
        
        status=send_email(
            template=template,
            subject=subject,
            recipients=recipient,
            content=content,
            
        )
        if status == True:
            obj,_=models.OTP.objects.get_or_create(email=mail)
            obj.otp=otp
            obj.save()
            return redirect('verify_otp',otp_id=obj.id)
        
    return render(request, 'password_reset.html')


def verify_otp(request,otp_id):
    error_message=''
    if request.method=="POST":
        otp_obj=get_object_or_404(models.OTP,id=otp_id)
        enterd_otp=int(request.POST.get('otp')) if request.POST.get('otp') else 0

        if otp_obj.otp == enterd_otp:
            return redirect('set_new_password',pk=otp_obj.id)
        else:
            error_message = "Invalid OTP. Please try again."


    return render(request,'otp_verify.html',{'otp_id':otp_id,'error':error_message})

from django.contrib.auth.models import User

def set_new_password(request, pk):
    if request.method == 'POST':
        print(pk, 'ihu')
        otp_obj = get_object_or_404(models.OTP, id=pk)

        password = request.POST.get('password')
        print(password)

        # Try to find the user in both Worker and Consumer models
        user = None
        if Consumer.objects.filter(email=otp_obj.email).exists():
            user = get_object_or_404(Consumer, email=otp_obj.email)
        elif Worker.objects.filter(email=otp_obj.email).exists():
            user = get_object_or_404(Worker, email=otp_obj.email)
        elif Contractor.objects.filter(email=otp_obj.email).exists():
            user = get_object_or_404(Contractor, email=otp_obj.email)

        else:
            return HttpResponse("User not found", status=404)

        # Set the new password
        user.user.set_password(password)
        user.save()
        user.user.save()

        # Redirect to the login page after saving the new password
        return redirect('login')  # Update with correct login URL

    return render(request, 'new_password.html', {'pk': pk})

