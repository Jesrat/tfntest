from .models import User
from django import forms

class ModelFormControl(forms.ModelForm):
    form_control_exclude = []

    def __init__(self, *args, **kwargs):
        self.request = kwargs.pop('request', None)
        allowed_fields = kwargs.pop('fields', [])
        readonly_fields = kwargs.pop('readonly_fields', [])
        super().__init__(*args, **kwargs)
        for field in set(self.fields):
            if field not in allowed_fields:
                print(f'popping field {field}')
                self.fields.pop(field)

        for field in self.fields.keys():
            if field in readonly_fields:
                self.fields[field].widget.attrs['readonly'] = True
            if field in self.form_control_exclude:
                continue
            self.fields[field].widget.attrs.update({'class': 'form-control'})

    class Meta:
        model = User
        fields = '__all__'

