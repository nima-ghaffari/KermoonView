from django import forms
from .models import Tour, User, Hotel

class TourForm(forms.ModelForm):
    class Meta:
        model = Tour
        fields = ['title', 'hotel', 'price', 'capacity', 'start_date', 'duration_text', 'location', 'category', 'description', 'image']
        widgets = {
            'title': forms.TextInput(attrs={'class': 'soft-input', 'placeholder': 'مثلا: کویر گردی شهداد'}),
            'hotel': forms.Select(attrs={'class': 'soft-input'}),
            'price': forms.NumberInput(attrs={'class': 'soft-input'}),
            'capacity': forms.NumberInput(attrs={'class': 'soft-input'}),
            'start_date': forms.DateInput(attrs={'class': 'soft-input', 'type': 'date'}),
            'duration_text': forms.TextInput(attrs={'class': 'soft-input', 'placeholder': 'مثلا: ۲ روزه'}),
            'location': forms.TextInput(attrs={'class': 'soft-input'}),
            'category': forms.Select(attrs={'class': 'soft-input'}),
            'description': forms.Textarea(attrs={'class': 'soft-input', 'rows': 4}),
            'image': forms.FileInput(attrs={'class': 'soft-input'}),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['hotel'].queryset = Hotel.objects.filter(is_approved=True)
        self.fields['hotel'].empty_label = "انتخاب هتل (اگر در لیست نیست، ابتدا در داشبورد معرفی کنید)"

class HotelSuggestionForm(forms.ModelForm):
    class Meta:
        model = Hotel
        fields = ['name', 'location', 'capacity']
        widgets = {
            'name': forms.TextInput(attrs={'class': 'soft-input', 'placeholder': 'نام هتل'}),
            'location': forms.TextInput(attrs={'class': 'soft-input', 'placeholder': 'آدرس دقیق هتل'}),
            'capacity': forms.NumberInput(attrs={'class': 'soft-input', 'placeholder': 'ظرفیت نفرات'}),
        }

class ProfileUpdateForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ['first_name', 'last_name', 'email', 'phone_number', 'avatar']
        widgets = {
            'first_name': forms.TextInput(attrs={'class': 'soft-input'}),
            'last_name': forms.TextInput(attrs={'class': 'soft-input'}),
            'email': forms.EmailInput(attrs={'class': 'soft-input'}),
            'phone_number': forms.TextInput(attrs={'class': 'soft-input'}),
            'avatar': forms.FileInput(attrs={'class': 'soft-input'}),
        }