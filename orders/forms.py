from django import forms

class PaymentForm(forms.Form):
    MONTH_CHOICES = [
        ('', 'MM'),
        ('1', '01'), ('2', '02'), ('3', '03'),
        ('4', '04'), ('5', '05'), ('6', '06'),
        ('7', '07'), ('8', '08'), ('9', '09'),
        ('10', '10'), ('11', '11'), ('12', '12'),
    ]
    YEAR_CHOICES = [(i, i) for i in range(17, 26)]
    YEAR_CHOICES.insert(0,('','YY'))

    address_line1 = forms.CharField(max_length=50, label='House number/name', label_suffix=' *')
    address_line2 = forms.CharField(max_length=50, label='Street', label_suffix=' *')
    address_city = forms.CharField(max_length=20, label='Town', label_suffix=' *')
    address_zip = forms.CharField(max_length=10, label='Postcode', label_suffix=' *')
    name = forms.CharField(max_length=50, label='Name on card', label_suffix=' *')
    card_number = forms.CharField(label='Card number', label_suffix=' *')
    expiry_month = forms.ChoiceField(widget=forms.Select(attrs={'placeholder': 'MM'}), label='Expiry Date', label_suffix=' *', choices=MONTH_CHOICES)
    expiry_year = forms.ChoiceField(widget=forms.Select(attrs={'placeholder': 'YY'}), label='', choices=YEAR_CHOICES)
    cvv = forms.CharField(label='CVV', label_suffix=' *')
    stripe_id = forms.CharField(widget=forms.HiddenInput, required=False)

