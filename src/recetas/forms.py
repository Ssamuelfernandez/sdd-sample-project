from django import forms

# Formulario sin modelo mientras no existe Receta; pasará a ser un ModelForm.
# Los límites siguen el modelo de datos del PRD (sección 7).


def mensajes(campo):
    # Mensajes más claros que los que trae Django por defecto en español.
    return {
        'required': f'Falta {campo}.',
        'min_length': 'Debe tener al menos %(limit_value)d caracteres (ahora tiene %(show_value)d).',
        'max_length': 'Puede tener como máximo %(limit_value)d caracteres (ahora tiene %(show_value)d).',
    }


class RecetaForm(forms.Form):
    titulo = forms.CharField(
        label='Título',
        min_length=3,
        max_length=100,
        error_messages=mensajes('el título'),
        widget=forms.TextInput(attrs={'placeholder': 'Ej.: Tortilla de patatas'}),
    )
    autor = forms.CharField(
        label='Tu nombre',
        min_length=2,
        max_length=50,
        error_messages=mensajes('tu nombre'),
        widget=forms.TextInput(attrs={'placeholder': 'Ej.: Ana', 'autocomplete': 'name'}),
    )
    descripcion = forms.CharField(
        label='Descripción',
        required=False,
        max_length=300,
        error_messages=mensajes('la descripción'),
        help_text='Opcional. Una frase que invite a cocinarla.',
        widget=forms.Textarea(attrs={'rows': 2}),
    )
    ingredientes = forms.CharField(
        label='Ingredientes',
        max_length=3000,
        error_messages=mensajes('al menos un ingrediente'),
        help_text='Escribe un ingrediente por línea.',
        widget=forms.Textarea(attrs={'rows': 6, 'placeholder': '6 huevos\n4 patatas medianas\nSal'}),
    )
    pasos = forms.CharField(
        label='Preparación',
        max_length=5000,
        error_messages=mensajes('al menos un paso'),
        help_text='Escribe un paso por línea.',
        widget=forms.Textarea(attrs={'rows': 8, 'placeholder': 'Pela las patatas.\nFríelas a fuego medio.'}),
    )
