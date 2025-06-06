from django.shortcuts import render

# own
from django.http import HttpResponse
from django.template import loader

# sign up
from django.shortcuts import redirect
from .forms import SignUpForm


# Login in
from .forms import LoginForm
from .models import Users, Expenses_Table

# page number
from django.core.paginator import Paginator

from .forms import InsertForm # insert
from .forms import EditForm # Edit

from .forms import EditProfileForm # Profile Edit

# Create your views here.

def home(request):
    user_id = request.session.get('user_id')
    user    = Users.objects.get(user_id= user_id)
    
    # for page dashboard
    expenses = Expenses_Table.objects.filter(user_id=user_id)
    
    income_sum  = 0
    expense_sum = 0
    food_sum    = 0
    bills_sum   = 0
    other_sum   = 0
    
    over_expense    = False
    food_exist      = False
    bills_exist     = False
    other_exist     = False
    
    for expense in expenses:
        
        if expense.categories_name.lower() == 'food':
            food_sum += expense.amount
            
        if expense.categories_name.lower() == 'bills':
            bills_sum += expense.amount
            
        if expense.categories_name.lower() == 'other':
            other_sum += expense.amount
        
        if expense.income:
            income_sum  += expense.amount
        else:
            expense_sum += expense.amount
    
    
    # calculation for dashboard
    
    # income percentage
    if income_sum == 0:
        percentage_amount = 0
    else:
        percentage_amount = round( (expense_sum / income_sum)*100, 2)
    
    # food/expense percentage
    if food_sum == 0:
        percentage_food = 0
    else:
        food_exist = True
        percentage_food = round( (food_sum / expense_sum)*100, 2)
        
    # bills/expense percentage
    if bills_sum == 0:
        percentage_bills = 0
    else:
        bills_exist = True
        percentage_bills = round( (bills_sum / expense_sum)*100, 2)
    
    # Others/expense percentage
    if other_sum == 0:
        percentage_other = 0
    else:
        other_exist = True
        percentage_other = round( (other_sum / expense_sum)*100, 2)
    
    
    if percentage_amount >= 100:
        over_expense        = True
    
    context = {
        'user'              : user,
        
        'income_sum'        : income_sum,
        'expense_sum'       : expense_sum,
        'percentage_amount' : percentage_amount,
        'over_expense'      : over_expense,
        
        'food_sum'          : food_sum,
        'percentage_food'   : percentage_food,
        'food_exist'        : food_exist,
        
        'bills_sum'         : bills_sum,
        'percentage_bills'  : percentage_bills,
        'bills_exist'       : bills_exist,
        
        'other_sum'         : other_sum,
        'percentage_other'  : percentage_other,
        'other_exist'       : other_exist,
    }
    
    return render(request, 'home.html', context)

def default_home(request):
    try:
        user_id = request.session.get('user_id')
        user = Users.objects.get(user_id= user_id)
        return redirect('home')
    except:
        return redirect('login')


def table(request):
    user_id = request.session.get('user_id')
    user    = Users.objects.get(user_id= user_id)
    
    # for page intentions
    expenses = Expenses_Table.objects.filter(user_id=user_id)
    
    # for page number and splitting 
    paginator = Paginator(expenses, 10)  # Display 10 items per page
    page_number = request.GET.get('page')
    expenses = paginator.get_page(page_number)
    
    context = {
        'user'              : user,
        'expenses'          : expenses,
    }
    
    return render(request, 'table.html', context)
    

def signup(request):
    if request.method == 'POST':
        form = SignUpForm(request.POST)
        if form.is_valid():
            form.save()  # This will save the data to the database
            return redirect('home') # Redirect to a success page after successful submission
    
    else:
        form = SignUpForm()
            
        
    return render(request, 'signup.html', {'form': form})    


def login_page(request):
    if request.method == 'POST':
        form = LoginForm(request.POST)

        if form.is_valid():
            
            email       = form.cleaned_data['email']
            password    = form.cleaned_data['password']
            
            try:
                user = Users.objects.get(email=email)
            except Users.DoesNotExist:
                error_message = 'Invalid Email.'
                return render(request, 'login.html', {'form': form, 'error_message': error_message})
            
            if user.password == password:
                    request.session['user_id'] = user.user_id
                    return redirect('home')
            else:
                error_message = 'Invalid Password.'
                return render(request, 'login.html', {'form': form, 'error_message': error_message})
        else:
            error_message = 'Invalid email or password.'
            return render(request, 'login.html', {'form': form, 'error_message': error_message})
    else:
        form = LoginForm()
    
    return render(request, 'login.html', {'form': form})


def logout(request):
    request.session.clear()
    return redirect('login')


def insert(request):
    
    user_id = request.session.get('user_id')
    user    = Users.objects.get(user_id= user_id)
    
    if request.method == 'POST':
        form = InsertForm(request.POST)
        
        if form.is_valid():
            
            categories_name = form.cleaned_data['categories_name']
            amount          = form.cleaned_data['amount']
            date            = form.cleaned_data['date']
            description     = form.cleaned_data['description']
            income          = form.cleaned_data['income']
            
            Expenses_Table.objects.create(
                user_id=user,
                categories_name=categories_name,
                amount=amount,
                date=date,
                description=description,
                income=income 
                )
            
            return redirect('table')
            # Redirect to a success page or do something else
    else:
        form = InsertForm()
        
    
    context = {
        'user'  : user,
        'form'  : form
    }
    
    return render(request, 'insert.html', context)


def edit(request, edit_item_id):
    user_id = request.session.get('user_id')
    user    = Users.objects.get(user_id= user_id)
    
    expense = Expenses_Table.objects.get(user_id=user_id, expenses_id=edit_item_id)
    
    is_save = False
    edit_item_id = int()
    
    if request.method == 'POST':
        form = EditForm(request.POST)

        if form.is_valid():
            
            form_categories_name    = form.cleaned_data['categories_name']
            form_amount             = form.cleaned_data['amount']
            form_date               = form.cleaned_data['date']
            form_description        = form.cleaned_data['description']
            form_income             = form.cleaned_data['income']
            
            
            categories_name = expense.categories_name
            amount          = expense.amount
            date            = expense.date
            description     = expense.description
            income          = expense.income
            
            
            if categories_name != form_categories_name and form_categories_name != "":
                expense.categories_name = form_categories_name
                expense.save()
                is_save = True
            
            if amount != form_amount and form_amount is not None:
                expense.amount = form_amount
                expense.save()
                is_save = True
              
            # date temporally excluded  
            # if date != form_date and form_date is not None:
            #     expense.date = form_date
            #     expense.save()
            #     is_save = True
                
            if description != form_description and form_description != "":
                expense.description = form_description
                expense.save()
                is_save = True
                
            if income != form_income and form_income is not None:
                if form_income.lower() == "true":
                    expense.income = True
                    expense.save()
                    is_save = True
                
                if form_income.lower() == "false":
                    expense.income = False
                    expense.save()
                    is_save = True
            
            if is_save:
                return redirect('table')
            
    else:
        form = EditForm()
    
    context = {
        'edit_item_id'  : edit_item_id,
        'user'          : user,
        'expense'       : expense,
        'is_save'       : is_save,
        'form'          : form,
    }
    
    return render(request, 'edit.html', context)


def delete(request, delete_item_id):
    user_id = request.session.get('user_id')
    user    = Users.objects.get(user_id= user_id)
    
    expense = Expenses_Table.objects.get(user_id=user_id, expenses_id=delete_item_id)
    
    if request.method == 'POST':
        expense.delete()
        return redirect('table')
    
    context = {
        'delete_item_id'    : delete_item_id,
        'user'              : user,
        'expense'           : expense,
    }
    
    return render(request, 'delete.html', context)


def edit_profile(request):
    
    # user = get_object_or_404(Users, user_id=user_id)
    # if request.method == 'POST':
    #     form = UserUpdateForm(request.POST, instance=user)
    #     if form.is_valid():
    #         form.save()
    #         return redirect('user_detail', user_id=user_id)  # Redirect to user detail page or wherever you want
    # else:
    #     form = UserUpdateForm(instance=user)
    
    # context = {'form': form, 'user': user}
    # return render(request, 'update_user.html', context)
    
    user_id = request.session.get('user_id')
    user    = Users.objects.get(user_id= user_id)
    
    is_save = False
    
    if request.method == 'POST':
        form = EditProfileForm(request.POST)

        if form.is_valid():
            
            form_name       = form.cleaned_data['name']
            form_email      = form.cleaned_data['email']
            form_password   = form.cleaned_data['password']
            
            name        = user.name
            email       = user.email
            password    = user.password
            
            print(form)
            
            print(f"{form_name}, {form_email}, {form_password}\n")
            print(f"{name}, {email}, {password} \n")
            
            
            if name != form_name and form_name != "":
                user.name = form_name
                user.save()
                is_save = True
            
            if email != form_email and form_email != "":
                user.email = form_email
                user.save()
                is_save = True
            
            if password != form_password and form_password != "":
                user.password = form_password
                user.save()
                is_save = True
            
            if is_save:
                return redirect('home')
            
    else:
        form = EditProfileForm()
    
    context = {
        'form'      : form,
        'user'      : user,
        'is_save'   : is_save,
    }
    
    return render(request, 'edit_profile.html', context)

def delete_profile(request):
    user_id = request.session.get('user_id')
    user    = Users.objects.get(user_id= user_id)
    user.delete()
    
    return redirect('logout')
