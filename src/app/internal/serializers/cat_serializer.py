from rest_framework import serializers

from app.internal.models.cat_model import Cat, CatBreed


class CatBreedSerializer(serializers.ModelSerializer):
    class Meta:
        model = CatBreed
        fields = "__all__"


class CatSerializer(serializers.ModelSerializer):
    breed_info = CatBreedSerializer(read_only=True, source='breed')

    class Meta:
        model = Cat
        fields = "__all__"
        read_only_fields = ["owner", "breed_info"]
        extra_kwargs = {"name": {"required": True}, "breed": {"required": True}}

    def create(self, validated_data):
        validated_data['owner'] = self.context["request"].user
        return super().create(validated_data)
