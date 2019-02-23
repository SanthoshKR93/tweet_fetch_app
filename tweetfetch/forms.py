from django import forms

class IndexForm(forms.Form):
   Twitter_Handle = forms.CharField(widget=forms.TextInput(
      attrs = {
      'class':'form-control','placeholder':'Enter User Handle..',
      }
   ))
