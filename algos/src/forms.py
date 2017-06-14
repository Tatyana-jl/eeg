from django import forms

class SForm(forms.Form):
    s_len = forms.CharField(label='Signal length', max_length=100)
    file = forms.FileField(widget=forms.ClearableFileInput(attrs={'multiple': True}))
