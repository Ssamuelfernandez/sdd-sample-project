from rest_framework import serializers

from .models import Receta


class RecetaSerializer(serializers.ModelSerializer):
    # Mismas validaciones que el formulario web: vienen de los campos del modelo (PRD, sección 7).
    estado = serializers.SerializerMethodField()

    class Meta:
        model = Receta
        # 'publicada' no es un campo de entrada: cualquier valor que envíe el cliente se ignora (CL-21).
        fields = ['id', 'titulo', 'autor', 'descripcion', 'ingredientes', 'pasos', 'estado']

    def get_estado(self, receta):
        return 'publicada' if receta.publicada else 'borrador'
