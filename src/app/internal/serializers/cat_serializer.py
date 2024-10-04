from rest_framework import serializers

from app.internal.models.cat_model import Cat, CatBreed


class CatBreedSerializer(serializers.ModelSerializer):
    class Meta:
        model = CatBreed
        fields = "__all__"


class CatSerializer(serializers.ModelSerializer):
    type = CatBreedSerializer(read_only=True)

    class Meta:
        model = Cat
        fields = "__all__"
        read_only_fields = ["owner"]

    def create(self, validated_data):
        validated_data['owner'] = self.context["request"].user
        return super().create(validated_data)
