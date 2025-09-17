from django import forms

class MovieSearchForm(forms.Form):
    prompt = forms.CharField(
        label='Buscar película',
        max_length=200,
        widget=forms.TextInput(attrs={'placeholder': 'Escribe tu búsqueda...'})
    )
