from rest_framework import serializers
from pos_app.models import (
    User, TableResto, Profile, Category, MenuResto, 
    OrderMenu, OrderMenuDetail,
)
from django.contrib.auth import authenticate
from rest_framework import exceptions
from django.core.exceptions import ValidationError
from django.http import HttpResponse, JsonResponse
from rest_framework.validators import UniqueValidator
from django.contrib.auth.password_validation import validate_password

class TableRestoSerializer(serializers.ModelSerializer):
    class Meta:
        model = TableResto
        fields = ('id', 'code' ,'name', 'capacity', 'table_status', 'status')

class LoginSerializer(serializers.Serializer):
    username = serializers.CharField()
    password = serializers.CharField()

    def validate(self, data):
        username = data.get('username', '')
        password = data.get('password', '')

        if username and password:
            user = authenticate(username = username, 
                password = password)
            if user:
                # Check the user is_active and he/she is a waitress
                if user.is_active and user.is_waitress:
                    data['user'] = user
                else:
                    msg = 'User is deactivated...'
                    raise exceptions.ValidationError(msg)                    
                    # raise ValidationError({'message' : 'You have no access...'})                    
            else:
                msg = 'Unable to login with given credentials...'
                raise exceptions.ValidationError(msg)
        else:
            msg = 'Must provide username and password both...'
            raise exceptions.ValidationError(msg)
        return data

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('id', 'username', 'first_name', 'last_name', 'email')

class ProfileSerializer(serializers.ModelSerializer):
    user = UserSerializer(read_only = True)
    class Meta:
        model = Profile        
        fields = ('id', 'user', 'avatar', 'bio', 'status')

class ProfileSerializerII(serializers.ModelSerializer):
    user = UserSerializer(required = False)
    class Meta:
        model = Profile        
        fields = ('id', 'user', 'avatar', 'bio', 'status')

    def update(self, instance, validated_data):
        user_data = validated_data.pop('user')
        
        return super().update(instance, validated_data)

class RegisterWaitressSerializer(serializers.ModelSerializer):
    email = serializers.EmailField(required = True,
        validators = [UniqueValidator(queryset = User.objects.all())])
    password1 = serializers.CharField(write_only = True, 
        required = True, validators = [validate_password])
    password2 = serializers.CharField(write_only = True, 
        required = True)

    class Meta:
        model = User
        fields = ['username', 'email', 'password1', 'password2', 
            'is_active', 'is_waitress', 'first_name', 'last_name']
        extra_kwargs = {
            'first_name' : {'required' : True},
            'last_name' : {'required' : True}
        }

    def validate(self, attrs):
        if attrs['password1'] != attrs['password2']:
            raise serializers.ValidationError({
                'password' : 'Password field did not match...'
            })
        return attrs
    
    def create(self, validated_data):
        user = User.objects.create(
            username = validated_data['username'],
            email = validated_data['email'],            
            is_active = validated_data['is_active'],
            is_waitress = validated_data['is_waitress'],
            first_name = validated_data['first_name'],
            last_name = validated_data['last_name']
        )
        user.set_password(validated_data['password1'])
        user.save()
        profile = Profile.objects.create(user = user, 
            user_create = user)
        profile.save()
        return user
    
class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = ('id', 'name', 'status')

class MenuRestoSerializer(serializers.ModelSerializer):
    category = CategorySerializer(read_only = True)

    class Meta:
        model = MenuResto
        fields = ('id', 'code', 'name', 'price', 'description',
            'image_menu', 'category', 'menu_status', 'status',)
