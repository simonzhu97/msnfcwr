from django import forms
from liu_yan_ban.models import *

class FormPlus(forms.Form):
    def __init__(self, *args, **kwargs):
        super(FormPlus, self).__init__(*args, **kwargs)
        for field in self.fields:
            self.fields[field].widget.attrs.update({
                'class':'form-control',
        })