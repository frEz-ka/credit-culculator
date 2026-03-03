from django import forms
from .models import Credit

class CreditForm(forms.ModelForm):
    class Meta:
        model = Credit
        fields = ['name', 'total_amount', 'interest_rate', 'term_months', 'start_date']
        widgets = {
            'start_date': forms.DateInput(attrs={'type': 'date'}),
            'name': forms.TextInput(attrs={'class': 'form-control'}),
            'total_amount': forms.NumberInput(attrs={'class': 'form-control', 'step': '0.01'}),
            'interest_rate': forms.NumberInput(attrs={'class': 'form-control', 'step': '0.01'}),
            'term_months': forms.NumberInput(attrs={'class': 'form-control'}),
        }
        labels = {
            'name': 'Название кредита',
            'total_amount': 'Общая сумма кредита (руб)',
            'interest_rate': 'Годовая процентная ставка (%)',
            'term_months': 'Срок кредита (месяцев)',
            'start_date': 'Дата первого платежа',
        }