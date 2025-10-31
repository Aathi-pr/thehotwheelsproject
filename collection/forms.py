from django import forms
from .models import Car, Case, Series

class LoginForm(forms.Form):
    username = forms.CharField(
        max_length=150,
        widget=forms.TextInput(attrs={
            'class': 'form-input',
            'placeholder': 'USERNAME'
        })
    )
    password = forms.CharField(
        widget=forms.PasswordInput(attrs={
            'class': 'form-input',
            'placeholder': 'PASSWORD'
        })
    )

class CaseForm(forms.ModelForm):
    class Meta:
        model = Case
        fields = ['name', 'year', 'description', 'release_date']
        widgets = {
            'name': forms.Select(attrs={
                'class': 'form-control'
            }),
            'year': forms.NumberInput(attrs={
                'class': 'form-control',
                'min': '2000',
                'max': '2025'
            }),
            'description': forms.Textarea(attrs={
                'class': 'form-control',
                'rows': 3,
                'placeholder': 'Describe the cars in this case mix...'
            }),
            'release_date': forms.DateInput(attrs={
                'class': 'form-control',
                'type': 'date'
            }),
        }
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['description'].required = False
        self.fields['release_date'].required = False

class SeriesForm(forms.ModelForm):
    class Meta:
        model = Series
        fields = ['name', 'description', 'color_theme', 'is_active']
        widgets = {
            'name': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'e.g., HW J-Imports, Factory Fresh'
            }),
            'description': forms.Textarea(attrs={
                'class': 'form-control',
                'rows': 3,
                'placeholder': 'Describe this series...'
            }),
            'color_theme': forms.TextInput(attrs={
                'class': 'form-control',
                'type': 'color',
                'value': '#ff3d3d'
            }),
            'is_active': forms.CheckboxInput(attrs={
                'class': 'form-check-input',
                'checked': True
            }),
        }
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['description'].required = False
        self.fields['color_theme'].help_text = "Pick a color for this series"

class CarForm(forms.ModelForm):
    class Meta:
        model = Car
        fields = [
            'casting_name', 'number', 'year', 'color',
            'case', 'series', 'treasure_hunt',
            'manufacturer', 'scale', 'condition', 'quantity',
            'purchase_date', 'purchase_price', 'estimated_value',
            'image', 'notes', 'is_favorite', 'is_for_trade'
        ]
        widgets = {
            'casting_name': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'e.g., Nissan Skyline GT-R'
            }),
            'number': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'e.g., 1/250, 01/10'
            }),
            'year': forms.NumberInput(attrs={
                'class': 'form-control',
                'min': '1968',
                'max': '2025'
            }),
            'color': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'e.g., Red, Spectraflame Blue'
            }),
            'case': forms.Select(attrs={
                'class': 'form-select'
            }),
            'series': forms.Select(attrs={
                'class': 'form-select'
            }),
            'treasure_hunt': forms.Select(attrs={
                'class': 'form-select'
            }),
            'manufacturer': forms.TextInput(attrs={
                'class': 'form-control'
            }),
            'scale': forms.TextInput(attrs={
                'class': 'form-control'
            }),
            'condition': forms.Select(attrs={
                'class': 'form-select'
            }),
            'quantity': forms.NumberInput(attrs={
                'class': 'form-control',
                'min': '0'
            }),
            'purchase_date': forms.DateInput(attrs={
                'class': 'form-control',
                'type': 'date'
            }),
            'purchase_price': forms.NumberInput(attrs={
                'class': 'form-control',
                'step': '0.01',
                'min': '0'
            }),
            'estimated_value': forms.NumberInput(attrs={
                'class': 'form-control',
                'step': '0.01',
                'min': '0'
            }),
            'image': forms.FileInput(attrs={
                'class': 'form-control',
                'accept': 'image/*'
            }),
            'notes': forms.Textarea(attrs={
                'class': 'form-control',
                'rows': 3,
                'placeholder': 'Add any additional notes about this car...'
            }),
            'is_favorite': forms.CheckboxInput(attrs={
                'class': 'form-check-input'
            }),
            'is_for_trade': forms.CheckboxInput(attrs={
                'class': 'form-check-input'
            }),
        }
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        
        # Customize case field
        self.fields['case'].empty_label = "-- Select Case --"
        self.fields['case'].queryset = Case.objects.all().order_by('year', 'name')
        
        # Customize series field
        self.fields['series'].empty_label = "-- Select Series --"
        self.fields['series'].queryset = Series.objects.filter(is_active=True).order_by('name')
        
        # Add help text
        self.fields['casting_name'].help_text = "Official Hot Wheels casting name"
        self.fields['case'].help_text = "Which case mix is this car from?"
        self.fields['series'].help_text = "Which series does this car belong to?"
