from django.contrib.auth.models import User, Group
from django.contrib.auth import authenticate
from .views import Song
from rest_framework import serializers
from rest_framework.authtoken.models import Token


#Serializer example(General)
class GeneralSongSerializer(serializers.Serializer):
    #you dont have to include all fields
    #read only in id means it only shows up in get request
    id = serializers.IntegerField(read_only=True)
    name = serializers.CharField(max_length=100)
    album = serializers.CharField(max_length=100)
    logo = serializers.FileField()
    isFavorite = serializers.BooleanField()

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


class UserRegisterSerializer(serializers.ModelSerializer):

    #any extra fields not in User I will include here :
    password2 = serializers.CharField(style= {'input_type' : 'password'},write_only=True)

    class Meta:
        model = User
        fields = ['email','username','password', 'password2']

        #password should only be posted
        extra_kwargs = {
            'password' : {'write_only' : True}
        }


    def save(self):

        try:
            temp_user = User.objects.get( email = self.validated_data['email'])
        except User.MultipleObjectsReturned :
            raise serializers.ValidationError({'email': 'email already exists'})
        except User.DoesNotExist:
            user = User(
                username = self.validated_data['username'],
                email = self.validated_data['email']
            )
            password = self.validated_data['password']
            password2 = self.validated_data['password2']

            if password != password2:
                raise serializers.ValidationError({'password':'Passwords Dont match !'})
            user.set_password(password)
            user.save()

        else:
            raise serializers.ValidationError({'email': 'email already exists'})


class UserLoginSerializer(serializers.Serializer):

    username = serializers.CharField(max_length=255)
    password = serializers.CharField(max_length=128 , write_only= True)
    token = serializers.CharField(max_length=255, read_only=True)

    # class Meta:
    #     model = User
    #     fields = ['username','password','token']
    #
    #     #password should only be posted
    #     extra_kwargs = {
    #         'password' : {'write_only' : True}
    #     }



    def validate(self,data):

        try:
            temp_user = User.objects.get( username = data.get('username',None) )
        except User.DoesNotExist :
            raise serializers.ValidationError({'username': 'username does not exist'})

        else:

            username = data.get("username", None)
            password = data.get("password", None)
            # Now we authenticate the user

            user = authenticate(username=username, password=password)
            # this will return None if user in not authenticated
            # if it returned a value
            if user is not None:
                if user.is_active:  # if it's not banned/deleted ....
                    token = Token.objects.get_or_create(user = user)
                    #convention- wise : this is not correct, I should update token in update() not in validate, validate should only check parameters
                    data['token'] = token[0]
                    #return {'username' : username , 'token' : token[0]}
                    return data
            raise serializers.ValidationError({'username' : 'username or password is incorrect ! '})