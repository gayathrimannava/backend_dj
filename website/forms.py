from django import forms
from django.contrib.auth.forms import UserCreationForm
# Import the actual models
from website.models import Product
# Import the custom user model defined in your app (as indicated by the error trace)
from .models import AuthUser as CustomUser 

# --- Product Form (Kept for completeness) ---

class ProductForm(forms.ModelForm):
    """Form to handle creation and editing of Products."""
    class Meta:
        model = Product
        fields = ['name', 'price', 'description','stock'] 
        widgets = {
            'name': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Enter product name'}),
            'price': forms.NumberInput(attrs={'class': 'form-control', 'placeholder': 'Enter price'}),
            'description': forms.Textarea(attrs={'class': 'form-control', 'placeholder': 'Enter product description', 'rows': 4}),
            # 'stock': forms.NumberInput(attrs={'class': 'form-control', 'placeholder': 'Enter stock quantity'}),
        }


class CustomUserCreationForm(UserCreationForm):
    """
    A custom form for creating new users that uses the custom user model (AuthUser).
    Explicitly adds the email field and applies Bootstrap styling to all fields,
    including specific placeholders.
    """
    
    # 1. Email Field Definition (Explicitly added and styled)
    email = forms.EmailField(
        label="Email Address",
        max_length=254,
        required=True,
        widget=forms.EmailInput(attrs={'class': 'form-control', 'placeholder': 'Enter your email'})
    )

    class Meta(UserCreationForm.Meta):
        model = CustomUser 
        fields = UserCreationForm.Meta.fields + ('email',)

    # 2. Styling and Placeholders for Inherited Fields (username, password1, password2)
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        
        # Define a dictionary for placeholders to keep the code clean
        placeholders = {
            'username': 'Enter username',
            'password1': 'Enter a strong password',
            'password2': 'Confirm your password',
            # Add other custom field placeholders here if needed
        }
        
        # Apply styling and placeholders to all fields
        for field_name, field in self.fields.items():
            field.widget.attrs.update({'class': 'form-control'})
            
            # Apply placeholders using the dictionary, checking if the key exists
            if field_name in placeholders:
                field.widget.attrs.update({'placeholder': placeholders[field_name]})
                