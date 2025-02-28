from django import forms
from django.contrib.auth.models import User
from . import models


from django import forms
from django.contrib.auth.models import User

class WorkerUserForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ['first_name', 'username', 'password']
        widgets = {
            'password': forms.PasswordInput()
        }


class WorkerForm(forms.ModelForm):
    class Meta:
        model=models.Worker
        fields=['phone','email','skills','work_experience','address','pincode','city','district', 'aadhar_number','service_rate','profile_pic']


class ServiceForm(forms.ModelForm):
    class Meta:
        model=models.Services
        fields=['service_pic','skills','city','service_rate','phone']

from django import forms
from django.contrib.auth.models import User
from . import models

class ConsumerUserForm(forms.ModelForm):
    class Meta:
        model=User
        fields=['first_name','last_name','username','password']
        widgets= {
            'password':forms.PasswordInput()
        }

class ConsumerForm(forms.ModelForm):
    class Meta:
        model=models.Consumer
        fields=['profile_pic','phone','email','address','pincode','city','district']









class AddressForm(forms.Form):
    name = forms.CharField(max_length=30, required=True)
    mobile = forms.CharField(max_length=10, required=True)  # Change to CharField

# forms.py

from django import forms

# class PaymentForm(forms.ModelForm):
#     class Meta:
#         model = Payment
#         fields = ['amount', 'card_number', 'account_holder_name', 'cvv', 'expiry_date','worker']
#         widgets = {
#             'amount': forms.NumberInput(attrs={'placeholder': 'Amount'}),
#             'card_number': forms.TextInput(attrs={'placeholder': 'Card Number'}),
#             'account_holder_name': forms.TextInput(attrs={'placeholder': 'Account Holder Name'}),
#             'cvv': forms.PasswordInput(attrs={'placeholder': 'CVV'}),
#             'expiry_date': forms.DateInput(attrs={'placeholder': 'Expiry Date (YYYY-MM-DD)', 'type': 'date'}),
#         }


class PaymentForm(forms.ModelForm):
    worker = forms.ModelChoiceField(queryset=models.Worker.objects.all(), empty_label="Select a Worker")
    
    class Meta:
        model = models.Payment
        fields = ['worker', 'account_holder_name', 'card_number', 'cvv', 'expiry_date', 'amount']

class ContractorForm(forms.ModelForm):
   class Meta:
        model=models.Contractor
        fields=['name','phone','email','professional_details','contractor_id_proof','address','pincode','city','district']

        
from.models import Workerabout
class WorkeraboutForm(forms.ModelForm):
    class Meta:
        model = Workerabout
        fields = ['worker', 'bio', 'workimage1', 'workimage2']
        widgets = {
            'bio': forms.Textarea(attrs={'rows': 4, 'cols': 40}),
        }

from django import forms
from .models import Feedback

class FeedbackForm(forms.ModelForm):
    class Meta:
        model = Feedback
        fields = ['name', 'message']
        widgets = {
            'message': forms.Textarea(attrs={'rows': 4, 'placeholder': 'Enter your feedback here...'}),
        }
        
    
# forms.py
from django import forms
from .models import Advertisement

class AdvertisementForm(forms.ModelForm):
    class Meta:
        model = Advertisement
        fields = ['title', 'message', 'image']  # Specify fields to include in the form


from django import forms
from .models import Adpayment

class AdpaymentForm(forms.ModelForm):
    class Meta:
        model = Adpayment
        fields = ['amount', 'payment_date']  # Include the fields you want in the form

    amount = forms.DecimalField(max_digits=10, decimal_places=2, label='Payment Amount')
    payment_date = forms.DateTimeField(widget=forms.SelectDateWidget, label='Payment Date')


class CServiceForm(forms.ModelForm):
    class Meta:
        model=models.CServices
        fields=['service_pic','skills','city','service_rate','phone']


# forms.py
from django import forms
from .models import Contractorabout,Contractor

class ContractoraboutForm(forms.ModelForm):
    class Meta:
        model = Contractorabout
        fields = ['contractor', 'bio', 'workimage1', 'workimage2']
        
    contractor = forms.ModelChoiceField(queryset=Contractor.objects.all(), required=False)
    bio = forms.CharField(widget=forms.Textarea, required=False)
    workimage1 = forms.ImageField(required=False)
    workimage2 = forms.ImageField(required=False)


from django import forms
from .models import Notification, Contractor

class NotificationForm(forms.ModelForm):
    class Meta:
        model = Notification
        fields = ['contractor', 'message']  # These are the fields consumer can interact with
    
    # Customizing the form fields
    contractor = forms.ModelChoiceField(
        queryset=Contractor.objects.all(),
        empty_label="Select a contractor",
        widget=forms.Select(attrs={'class': 'form-control'}),
        help_text="Select a contractor to send the message to"
    )
    print(contractor)
    message = forms.CharField(
        widget=forms.Textarea(attrs={'class': 'form-control', 'rows': 4, 'placeholder': 'Enter your message'}),
        max_length=1000,
        help_text="Write the message you want to send to the contractor"
    )
    
