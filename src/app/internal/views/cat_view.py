from rest_framework import generics
from rest_framework.permissions import AllowAny, IsAuthenticatedOrReadOnly, IsAuthenticated, SAFE_METHODS

from app.internal.models.cat_model import Cat, CatBreed
from app.internal.serializers.cat_serializer import CatBreedSerializer, CatSerializer


class CatBreedListAPIView(generics.ListAPIView):
    permission_classes = [AllowAny]
    serializer_class = CatBreedSerializer
    queryset = CatBreed.objects.all()


class CatListAPIView(generics.ListAPIView):
    permission_classes = [AllowAny]
    serializer_class = CatSerializer

    def get_queryset(self):
        queryset = Cat.objects.all()
        breed = self.request.query_params.get("breed")
        if breed is not None:
            queryset = Cat.objects.filter(breed=breed)
        return queryset


class CatDetailAPIView(generics.RetrieveUpdateDestroyAPIView):
    permission_classes = [IsAuthenticatedOrReadOnly]
    serializer_class = CatSerializer
    lookup_field = "id"

    def get_queryset(self):
        queryset = Cat.objects.all()
        if self.request.method in SAFE_METHODS:
            return queryset
        else:
            owner = self.request.user
            return queryset.filter(owner=owner)


# class CatUpdateDestroyAPIView(generics.UpdateAPIView, generics.DestroyAPIView):
#     permission_classes = [IsAuthenticatedOrReadOnly]
#     serializer_class = CatSerializer
#     lookup_field = "id"
#
#     def get_queryset(self):
#         owner = self.request.user
#         return Cat.objects.filter(owner=owner)


class CatCreateAPIView(generics.CreateAPIView):
    permission_classes = [IsAuthenticated]
    serializer_class = CatSerializer
