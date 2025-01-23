from django import forms

from users.models import Company


from django import forms
from users.models import Company

class CreateNewService(forms.Form):
    name = forms.CharField(max_length=40)
    description = forms.CharField(widget=forms.Textarea, label='Description')
    price_hour = forms.DecimalField(decimal_places=2, max_digits=5, min_value=0.00)
    
    def __init__(self, *args, **kwargs):
        super(CreateNewService, self).__init__(*args, **kwargs)
        self.fields['field'] = forms.ChoiceField(
            choices=(
                ('Air Conditioner', 'Air Conditioner'),
                ('Carpentry', 'Carpentry'),
                ('Electricity', 'Electricity'),
                ('Gardening', 'Gardening'),
                ('Home Machines', 'Home Machines'),
                ('House Keeping', 'House Keeping'),
                ('Interior Design', 'Interior Design'),
                ('Locks', 'Locks'),
                ('Painting', 'Painting'),
                ('Plumbing', 'Plumbing'),
                ('Water Heaters', 'Water Heaters'),
            ),
            required=True
        )


class RequestServiceForm(forms.Form):
    pass
