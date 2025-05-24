from django import forms


class SendCVEmailForm(forms.Form):
    """Form for sending CV via email."""

    email = forms.EmailField(
        max_length=254,
        widget=forms.EmailInput(
            attrs={
                'class': 'form-control',
                'placeholder': 'Enter email address...',
                'required': True,
            }
        ),
        help_text='Enter the email address to send the CV to',
    )
