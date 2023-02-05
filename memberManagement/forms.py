from django import forms
from phonenumber_field.formfields import PhoneNumberField

from memberManagement.models import Membership


class MemberForm(forms.Form):
    first_name = forms.CharField(label='First name', max_length=100)
    last_name = forms.CharField(label='Last name', max_length=100)
    email = forms.EmailField()
    phone_number = PhoneNumberField()
    # role = forms.CharField(max_length=2, widget=forms.Select(choices=Membership.Role))
    role = forms.ChoiceField(widget=forms.RadioSelect, choices=Membership.Role.choices, label='role')
