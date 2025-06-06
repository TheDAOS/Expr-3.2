# own
# forms.py
from django import forms
from .models import Users, Expenses_Table

# insert form
from datetime import datetime


class SignUpForm(forms.ModelForm):
    class Meta:
        model = Users
        fields = ['name', 'email', 'password']  # Include all the fields you want to display in the form

    # Add Bootstrap classes to the form fields
    def __init__(self, *args, **kwargs):
        super(SignUpForm, self).__init__(*args, **kwargs)
        for field in self.fields:
            # self.fields[field].widget.attrs.update({'class': 'form-control'})
            self.fields[field].widget.attrs.update({'class': 'form-control', 'placeholder': self.fields[field].label})
            
            

class LoginForm(forms.Form):
        
    email = forms.EmailField(label='Email', max_length=254)
    password = forms.CharField(label='Password', widget=forms.PasswordInput)
    
    # Add Bootstrap classes to the form fields
    def __init__(self, *args, **kwargs):
        super(LoginForm, self).__init__(*args, **kwargs)
        for field in self.fields:
            # self.fields[field].widget.attrs.update({'class': 'form-control'})
            self.fields[field].widget.attrs.update({'class': 'form-control', 'placeholder': self.fields[field].label})


class InsertForm(forms.Form):

    categories_name = forms.CharField(
        label='Catagories',
        max_length=254,
        widget=forms.TextInput(attrs={'class': 'form-control'}),
    )

    amount = forms.DecimalField(
        label='Amount',
        max_digits=10,
        decimal_places=2,
        widget=forms.NumberInput(attrs={'class': 'form-control'}),
    )

    date = forms.DateField(
        label='Date',
        widget=forms.DateInput(attrs={'class': 'form-control'}),
    )

    description = forms.CharField(
        label='Description',
        max_length=254,
        widget=forms.TextInput(attrs={'class': 'form-control'}),
        required=False,
    )

    INCOME_CHOICES = [
        (True, 'Income'),
        (False, 'Expense'),
    ]

    income = forms.ChoiceField(
        label='Type',
        choices=INCOME_CHOICES,
        # widget=forms.RadioSelect(attrs={'class': 'form-check-input'}),
        widget=forms.Select(attrs={'class': 'form-select'}),
        initial=True,
    )

class EditForm(forms.Form):
    
    categories_name     = forms.CharField(
        label           = 'Catagories',
        max_length      = 254,
        widget          = forms.TextInput(attrs={'class': 'form-control'}),
        required        = False,
    )

    amount              = forms.DecimalField(
        label           = 'Amount',
        max_digits      = 10,
        decimal_places  = 2,
        widget          = forms.NumberInput(attrs={'class': 'form-control'}),
        required        = False,
    )

    date                = forms.DateField(
        label           = 'Date',
        widget          = forms.DateInput(attrs={'class': 'form-control'}),
        required        = False,
    )

    description         = forms.CharField(
        label           = 'Description',
        max_length      = 254,
        widget          = forms.TextInput(attrs={'class': 'form-control'}),
        required        = False,
    )

    INCOME_CHOICES = [
        (True, 'Income'),
        (False, 'Expense'),
    ]

    income              = forms.ChoiceField(
        label           = 'Type',
        choices         = INCOME_CHOICES,
        widget          = forms.RadioSelect(attrs={'class': 'form-check-input'}),
        required        = False,
    )
    

class EditProfileForm(forms.Form): 
    
    name            = forms.CharField(
        label       = 'Name',
        max_length  = 254,
        required    = False,
        )
    
    email           = forms.EmailField(
        label       ='Email',
        max_length  = 254,
        required    = False,
        )
    
    password        = forms.CharField(
        label       = 'Password',
        widget      = forms.PasswordInput,
        required    = False,
        )
    
    # class Meta:
    #     model = Users
    #     fields = ['name', 'email', 'password']  # List the fields you want to be editable in the form

    # def clean_email(self):
    #     email = self.cleaned_data.get('email')
    #     user_id = self.instance.user_id  # Get the user_id of the instance being updated
    #     if Users.objects.exclude(user_id=user_id).filter(email=email).exists():
    #         raise forms.ValidationError("This email is already in use.")
    #     return email