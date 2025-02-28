from django.db import models

# Create your models here.
from django.db import models
from django.contrib.auth.models import User

# Create your models here.
class Worker(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    phone = models.CharField(max_length=10, null=False)
    email = models.CharField(max_length=50, null=True)
    skills = models.CharField(max_length=30, null=False)
    work_experience = models.CharField(max_length=20)
    address = models.CharField(max_length=50,default='address' )
    pincode= models.CharField(max_length=6, default='pincode')
    city = models.CharField(max_length=25, null=False)
    district = models.CharField(max_length=25, default='district')
    aadhar_number = models.CharField(max_length=12, default='Pending')
    service_rate = models.CharField(max_length=30)
    status = models.CharField(max_length=20, default='Pending')
    profile_pic = models.FileField(
        upload_to='profile_files',
        default='profile_files/default.pdf',
        null=True,
        blank=True
    )
    is_approved = models.BooleanField(default=False)
    @property
    def get_name(self):
        return f"{self.user.first_name} {self.user.last_name}"

    def __str__(self):
        return self.get_name

class Services(models.Model):
    worker = models.ForeignKey(Worker, on_delete=models.CASCADE)
    service_pic = models.ImageField(upload_to='service_pic', null=True, blank=True)
    skills = models.CharField(max_length=40, null=False)
    city = models.CharField(max_length=25)
    service_rate = models.CharField(max_length=25)
    phone =models.CharField(max_length=10, null=False)
    def __str__(self):
        return f"{self.skills} by {self.worker.get_name}"



# Create your models here.

class Consumer(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    worker = models.ForeignKey(Worker, on_delete=models.CASCADE, null=True, blank=True)  # Optional relationship
    phone = models.CharField(max_length=10, null=False)
    email = models.CharField(max_length=50, null=True)
    address = models.CharField(max_length=50, default='address')
    pincode = models.CharField(max_length=6, default='pincode')
    city = models.CharField(max_length=25, null=False)
    district = models.CharField(max_length=25,default='district')
    profile_pic = models.ImageField(upload_to='profile_pic', null=True, blank=True)
    status = models.CharField(max_length=20,default='Pending')

    def get_name(self):
        return self.user.first_name+" "+self.user.last_name
    
    def __str__(self):
        return self.user.username
    







   

 

class Booking(models.Model):
    STATUS = (
        ('Order Confirmed', 'Order Confirmed'),
        ('Delivered', 'Delivered'),
    )
    consumer = models.ForeignKey(Consumer, on_delete=models.CASCADE, null=True)
    service = models.ForeignKey(Services, on_delete=models.CASCADE, null=True)
    worker = models.ForeignKey(Worker, on_delete=models.CASCADE, null=True)  # Add this line
    name = models.CharField(max_length=100, null=True)  # Add this line
    email = models.CharField(max_length=50, null=True)
    # location =models.CharField(max_length=20)
    lat=models.FloatField(default=0,null=True)
    long=models.FloatField(default=0,null=True) 
    mobile = models.CharField(max_length=10, null=True)
    order_date = models.DateField(null=True,blank=True)
    status = models.CharField(max_length=50, null=True, choices=STATUS)

# models.py

class Payment(models.Model):
    booking = models.ForeignKey('Booking', on_delete=models.CASCADE)  # Link to the booking
    worker = models.CharField(max_length=16,default="hai") # The worker being paid
    amount = models.DecimalField(max_digits=10, decimal_places=2)  # Amount paid
    card_number = models.CharField(max_length=16)  # Credit card number (for demo only)
    account_holder_name = models.CharField(max_length=100)  # Account holder name
    cvv = models.CharField(max_length=3)  # CVV code
    expiry_date = models.DateField()  # Expiry date
    status = models.CharField(max_length=20, default='Pending')  # Payment status
    created_at = models.DateTimeField(auto_now_add=True)  # Timestamp

    def __str__(self):
        return f"Payment for {self.booking} - {self.amount}"

    def is_paid(self):
        payment = Payment.objects.filter(booking=self.booking, status='Completed').first()
        return payment is not None

class Chatmodel(models.Model):
    message=models.TextField()
    consumer = models.ForeignKey(Consumer, on_delete=models.CASCADE, null=True)
    worker = models.ForeignKey(Worker, on_delete=models.CASCADE, null=True) 
    sender=models.ForeignKey(User,on_delete=models.CASCADE,null=True,blank=True)

    def __str__(self):
        return self.consumer.user.username 


class Contractor(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    name = models.CharField(max_length=100, null=True)  
    phone = models.CharField(max_length=10, null=False)
    email = models.CharField(max_length=200, null=False)
    professional_details = models.CharField(max_length=250)
    contractor_id_proof = models.FileField(max_length=20)
    address= models.CharField(max_length=50, default='address')
    pincode = models.CharField(max_length=6,default='pincode')
    city = models.CharField(max_length=25, null=False)
    district = models.CharField(max_length=25,default='district')
    status = models.BooleanField(default=False)
    workers=models.ManyToManyField(Worker,blank=True)
    is_approved = models.BooleanField(default=False) 

class Workerabout(models.Model):
    worker=models.ForeignKey(Worker,on_delete=models.CASCADE,null=True,blank=True)
    bio=models.TextField(null=True,blank=True)
    workimage1=models.ImageField(null=True,blank=True)
    workimage2=models.ImageField(null=True,blank=True)


from django.db import models

class Feedback(models.Model):
    name = models.CharField(max_length=255, help_text="Name of the person giving feedback")
    message = models.TextField(help_text="The feedback message")
    created_at = models.DateTimeField(auto_now_add=True, help_text="Date and time when feedback was created")

    def __str__(self):
        return f"Feedback from {self.name} on {self.created_at}"

    class Meta:
        ordering = ['-created_at']


from django.db import models

class Advertisement(models.Model):
    title = models.CharField(max_length=255)
    message = models.TextField()
    image = models.ImageField(upload_to='ads/', blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    is_approved = models.BooleanField(default=False)  # Field to track if the ad is approved

    def __str__(self):
        return self.title


from django.db import models
from django.utils import timezone

class Adpayment(models.Model):

    contractor = models.ForeignKey('Contractor', on_delete=models.CASCADE, related_name='payments')
    amount = models.DecimalField(max_digits=10, decimal_places=2)  # Store amount with two decimal places
    payment_date = models.DateTimeField(default=timezone.now)
  
class CServices(models.Model):
    contractor = models.ForeignKey(Contractor, on_delete=models.CASCADE)
    service_pic = models.ImageField(upload_to='service_pic', null=True, blank=True)
    skills = models.CharField(max_length=40, null=False)
    city = models.CharField(max_length=25)
    service_rate = models.CharField(max_length=25)
    phone =models.CharField(max_length=10, null=False)
from django.db import models
from django.contrib.auth.models import User  # To get User references
from django.utils import timezone

class Chats(models.Model):
    consumer = models.ForeignKey(Consumer, on_delete=models.CASCADE, null=True, blank=True)
    contractor = models.ForeignKey(Contractor, on_delete=models.CASCADE, null=True, blank=True)
    sender = models.ForeignKey(User, on_delete=models.CASCADE)
    message = models.TextField()

class Contractorabout(models.Model):
    contractor=models.ForeignKey(Contractor,on_delete=models.CASCADE,null=True,blank=True)
    bio=models.TextField(null=True,blank=True)
    workimage1=models.ImageField(null=True,blank=True)
    workimage2=models.ImageField(null=True,blank=True)


from django.db import models
from django.contrib.auth.models import User

class Notification(models.Model):
    consumer = models.ForeignKey(Consumer, on_delete=models.CASCADE)  # Consumer who is sending the notification
    contractor = models.ForeignKey(Contractor, on_delete=models.CASCADE)  # Contractor who will receive the notification
    message = models.TextField(help_text="Message from the consumer to the contractor")
    created_at = models.DateTimeField(auto_now_add=True, help_text="Timestamp when the notification was created")
    is_read = models.BooleanField(default=False, help_text="Flag to indicate whether the notification has been read by the contractor")

    def __str__(self):
        return f"Notification from {self.consumer.get_name()} to {self.contractor.name} at {self.created_at}"

    class Meta:
        ordering = ['-created_at']  # Order notifications by creation time (most recent first)


from django.db import models
from django.contrib.auth.models import User
from .models import Services  # Assuming the Services model is in the same app

class Cart(models.Model):
    consumer = models.ForeignKey('Consumer', on_delete=models.CASCADE)  # Link to the consumer
    service = models.ForeignKey(Services, on_delete=models.CASCADE)  # Link to the service
    added_at = models.DateTimeField(auto_now_add=True)  # When the service was added to the cart

    def __str__(self):
        return f"Cart item for {self.consumer.get_name()} - {self.service.skills}"

    class Meta:
        unique_together = ('consumer', 'service')  # Ensure that a consumer can't add the same service twice


class OTP(models.Model):
    otp = models.IntegerField(null=True,blank=True)
    email = models.EmailField()

    def __str__(self):
        return self.email
