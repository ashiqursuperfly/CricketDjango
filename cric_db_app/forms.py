from django import forms


class ContactForm(forms.Form):
    input_int = forms.IntegerField()
    input_char = forms.CharField(max_length=254)
    source = forms.CharField(  # A hidden input for internal use
        max_length=50,  # tell from which page the user sent the message
        widget=forms.HiddenInput()
    )

    def clean(self):
        cleaned_data = super(ContactForm, self).clean()
        input_int = cleaned_data.get('input_int')
        input_char = cleaned_data.get('input_char')

        if not input_int and not input_char:
            raise forms.ValidationError('You have to write something!')
