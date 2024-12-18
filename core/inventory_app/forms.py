# forms.py
from .models import Transaction, Product, ProductCategory, ReceiverEmail
from django import forms
from django.contrib.auth import get_user_model
from .models import CustomUser


class TransactionForm(forms.ModelForm):
    class Meta:
        model = Transaction
        fields = ['quantity', 'transaction_type']


class EmployeeCreationForm(forms.ModelForm):
    password = forms.CharField(widget=forms.PasswordInput)
    confirm_password = forms.CharField(widget=forms.PasswordInput)
    first_name = forms.CharField(max_length=30, required=True,
                                 widget=forms.TextInput(attrs={'placeholder': 'First Name'}))
    last_name = forms.CharField(max_length=30, required=True,
                                widget=forms.TextInput(attrs={'placeholder': 'Last Name'}))
    role = forms.ChoiceField(choices=CustomUser.ROLE_CHOICES, required=True, widget=forms.Select)

    class Meta:
        model = CustomUser
        fields = ['first_name', 'last_name', 'role', 'username', 'password']

    def clean(self):
        cleaned_data = super().clean()
        password = cleaned_data.get("password")
        confirm_password = cleaned_data.get("confirm_password")

        if password and confirm_password and password != confirm_password:
            self.add_error('confirm_password', "Passwords do not match.")

        return cleaned_data


class ProductForm(forms.ModelForm):
    class Meta:
        model = Product
        fields = ['name', 'category', 'price', 'quantity', 'low_stock_threshold']


class CategoryForm(forms.ModelForm):
    class Meta:
        model = ProductCategory
        fields = ['name', ]



class TransactionFilterForm(forms.Form):
    start_date = forms.DateField(required=False, widget=forms.DateInput(attrs={'type': 'date'}))
    end_date = forms.DateField(required=False, widget=forms.DateInput(attrs={'type': 'date'}))
    product = forms.ModelChoiceField(queryset=Product.objects.all(), required=False)
    employee = forms.ModelChoiceField(queryset=get_user_model().objects.all(), required=False)

    def filter_transactions(self):
        queryset = Transaction.objects.all()

        if self.cleaned_data.get('start_date'):
            queryset = queryset.filter(timestamp__gte=self.cleaned_data['start_date'])

        if self.cleaned_data.get('end_date'):
            queryset = queryset.filter(timestamp__lte=self.cleaned_data['end_date'])

        if self.cleaned_data.get('product'):
            queryset = queryset.filter(product=self.cleaned_data['product'])

        if self.cleaned_data.get('employee'):
            queryset = queryset.filter(employee=self.cleaned_data['employee'])

        return queryset


class EmailForm(forms.ModelForm):
    admin_email = forms.EmailField(max_length=30,
                                   required=True,
                                   widget=forms.EmailInput(attrs={'placeholder': 'Email'}))

    class Meta:
        model = ReceiverEmail
        fields = ['admin_email', ]
