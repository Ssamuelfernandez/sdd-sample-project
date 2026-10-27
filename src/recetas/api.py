from rest_framework.authentication import TokenAuthentication
from rest_framework.generics import ListCreateAPIView, RetrieveAPIView
from rest_framework.permissions import AllowAny, IsAdminUser

from .models import Receta
from .serializers import RecetaSerializer


class RecetaListCreateAPIView(ListCreateAPIView):
    serializer_class = RecetaSerializer
    # Solo token: sin sesión no hay CSRF que gestionar y un POST sin token da 401.
    authentication_classes = [TokenAuthentication]
    # Los borradores nunca salen en la API pública (CA-33).
    queryset = Receta.objects.filter(publicada=True)

    def get_permissions(self):
        # Leer es público; crear exige un administrador de Django con token.
        permiso = IsAdminUser if self.request.method == 'POST' else AllowAny
        return [permiso()]

    def perform_create(self, serializer):
        # La API solo crea borradores; se publican desde la web o el admin.
        serializer.save(publicada=False)


class RecetaRetrieveAPIView(RetrieveAPIView):
    serializer_class = RecetaSerializer
    authentication_classes = [TokenAuthentication]
    permission_classes = [AllowAny]
    queryset = Receta.objects.filter(publicada=True)
