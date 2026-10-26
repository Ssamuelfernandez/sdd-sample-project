from django import forms

from .models import Receta

# Los límites de longitud vienen del modelo Receta (PRD, sección 7).


def mensajes(campo):
    # Mensajes más claros que los que trae Django por defecto en español.
    return {
        'required': f'Falta {campo}.',
        'min_length': 'Debe tener al menos %(limit_value)d caracteres (ahora tiene %(show_value)d).',
        'max_length': 'Puede tener como máximo %(limit_value)d caracteres (ahora tiene %(show_value)d).',
    }


class RecetaForm(forms.ModelForm):
    class Meta:
        model = Receta
        fields = ['titulo', 'autor', 'descripcion', 'ingredientes', 'pasos', 'imagen', 'publicada']
        labels = {
            'publicada': 'Publicar ahora',
            'titulo': 'Título',
            'autor': 'Tu nombre',
            'descripcion': 'Descripción',
            'ingredientes': 'Ingredientes',
            'pasos': 'Preparación',
            'imagen': 'Foto',
        }
        help_texts = {
            'descripcion': 'Opcional. Una frase que invite a cocinarla.',
            'ingredientes': 'Escribe un ingrediente por línea.',
            'pasos': 'Escribe un paso por línea.',
            'imagen': 'Opcional. JPG, PNG o WebP de hasta 2 MB. Si no subes ninguna, se usará la imagen genérica.',
            'publicada': 'Si la desmarcas, se guarda como borrador y no aparece en la portada hasta que se publique.',
        }
        error_messages = {
            'titulo': mensajes('el título'),
            'autor': mensajes('tu nombre'),
            'descripcion': mensajes('la descripción'),
            'ingredientes': mensajes('al menos un ingrediente'),
            'pasos': mensajes('al menos un paso'),
            'imagen': {
                'invalid_image': 'El archivo no es una imagen válida.',
                'invalid_extension': 'Solo se admiten fotos JPG, PNG o WebP.',
            },
        }
        widgets = {
            'titulo': forms.TextInput(attrs={'placeholder': 'Ej.: Tortilla de patatas'}),
            'autor': forms.TextInput(attrs={'placeholder': 'Ej.: Ana', 'autocomplete': 'name'}),
            'descripcion': forms.Textarea(attrs={'rows': 2}),
            'ingredientes': forms.Textarea(attrs={'rows': 6, 'placeholder': '6 huevos\n4 patatas medianas\nSal'}),
            'pasos': forms.Textarea(attrs={'rows': 8, 'placeholder': 'Pela las patatas.\nFríelas a fuego medio.'}),
            'imagen': forms.ClearableFileInput(attrs={'accept': 'image/jpeg,image/png,image/webp'}),
            # role="switch" hace que los lectores de pantalla lo anuncien como interruptor.
            'publicada': forms.CheckboxInput(attrs={'role': 'switch'}),
        }
