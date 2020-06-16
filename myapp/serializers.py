from django.contrib.auth.models import User, Group
from .views import Song
from rest_framework import serializers


#Serializer example(General)
class GeneralSongSerializer(serializers.Serializer):
    id = serializers.IntegerField(read_only=True)
    name = serializers.CharField(max_length=100)
    album = serializers.CharField(max_length=100)
    logo = serializers.FileField()
    isFavorite = serializers.BooleanField()

    # def validate(self, data):
    #
    #     if self.album == '123':
    #         raise serializers.ValidationError("Album can't be 123")
    #     return data


    #this is a field class based validator, you can make one for each field
    def validate_album(self,value):
        if value == '123':
            raise serializers.ValidationError("Album Can't be 123")
        return value



    def create(self, validated_data):
        """
        Create and return a new `Song` instance, given the validated data.
        """
        return Song.objects.create(**validated_data)

    def update(self, instance, validated_data):
        """
        Update and return an existing `Song` instance, given the validated data.
        """
        instance.name = validated_data.get('name', instance.name)
        instance.album = validated_data.get('album', instance.album)
        instance.logo = validated_data.get('logo', instance.logo)
        instance.isFavorite = validated_data.get('isFavorite', instance.isFavorite)
        instance.save()
        return instance


#Model Serializer example, this one and the one above are identical in functionality
class SongSerializer(serializers.ModelSerializer):
    class Meta:
        model = Song
        #which means all fields
        #fields = [field.name for field in Song._meta.get_fields()]
        fields = '__all__'
        #After this , you can add extra_kwargs to make some fields write or read only
        #extra_kwargs = []
        #you can also include validatos for your fields
        #validators = []


