from django import forms
from phonenumber_field.formfields import PhoneNumberField

class ShippingAddressForm(forms.Form):
     house_address = forms.CharField(widget=forms.TextInput(attrs={
        'class' : 'form-control',
        'id' : 'floatingInput',
        'placeholder' : 'House Address'
     }))
     post_office =  forms.CharField(widget=forms.TextInput(attrs={
        'class' : 'form-control',
        'id' : 'floatingPostoffice',
        'placeholder' : 'Post Office'
     }))
     city =  forms.CharField(widget=forms.TextInput(attrs={
        'class' : 'form-control',
        'id' : 'floatingCity',
        'placeholder' : 'City'
     }))
     postal_code =  forms.CharField(widget=forms.TextInput(attrs={
        'class' : 'form-control',
        'id' : 'floatingPostal',
        'placeholder' : 'Postal Code'
     }))
     phone_number = PhoneNumberField(region="BD",widget=forms.TextInput(attrs={
        'class' : 'form-control',
        'id' : 'floatingPhone',
        'placeholder' : 'Phone Number'
     }))