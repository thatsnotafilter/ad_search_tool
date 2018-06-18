from django import forms

class SearchForm(forms.Form):
    search_criteria = forms.CharField(
        label='',
        max_length=100,
        widget = forms.TextInput(attrs = {
            'class':'w3-input w3-center w3-border',
            'style':'width:100%',
            }
        )
    )
