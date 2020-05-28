from user.models import CustomUser
from .models import Event, Pass
from django import forms

class PassCreationForm(forms.ModelForm):
    event = forms.CharField(widget = forms.HiddenInput())
    class Meta:
        model = Pass
        fields = ['event', 'name', 'cost']

class RegistrationForm(forms.Form):
    def __init__(self, event, *args, **kwargs):
        PASSES = [(P.id, P.name) for P in Pass.objects.filter(event = event)]
        super(RegistrationForm, self).__init__(*args, **kwargs)
        self.fields['pass_type'] = forms.ChoiceField( choices = PASSES)
        for visible in self.visible_fields():
            visible.field.widget.attrs['class'] = 'form-control bg-light'
    
    pass_type = forms.ChoiceField()
    name = forms.CharField(max_length = 20, required = False)
    email = forms.EmailField()
    count = forms.IntegerField()
    
class AddUserForm(forms.Form):
    def __init__(self, *args, **kwargs):
        users = [(U.email, (U.name + " - " + U.email)) for U in CustomUser.objects.all()]
        super(AddUserForm, self).__init__(*args, **kwargs)
        self.fields['users'] = forms.ChoiceField( choices = users)
