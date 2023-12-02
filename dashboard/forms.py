from django import forms


class SearchedValues(forms.Form):
    case = forms.CharField(
        label="",
        max_length=100,
        required=False,
        widget=forms.TextInput(
            attrs={
                'placeholder': 'Insert searched case',
            }
        ),
    )
