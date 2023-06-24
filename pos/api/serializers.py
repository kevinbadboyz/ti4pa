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
from django.db.models import Avg, Max, Min, Sum

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
                    msg = 'You have no access...'
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

class MenuRestoViewSerializer(serializers.ModelSerializer):    
    class Meta:        
        model = MenuResto
        fields = ['name', 'price', 'description', 'image_menu', 'menu_resto' ]

class OrderMenuCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = OrderMenu
        fields = '__all__'        
    
    def create(self, validated_data):
        req_table = validated_data.get('table_resto', None)        
        print('Result : ' + str(req_table))
        table_val = validated_data['table_resto'].id
        print(table_val)    
        current_order = OrderMenu.objects.filter(table_resto = table_val, 
            order_status = 'Belum Bayar')    
        if current_order.exists():
            om_id = current_order.values('id').get()['id']
            order_menu_details = list(OrderMenuDetail.objects.select_related('order_menu').\
                filter(order_menu__id = om_id).defer('subtotal').aggregate(Sum('subtotal')).values())[0]
            if(order_menu_details == None):
                total = 0
                ppn = 0
                tot_payment = 0
            else:
                total = order_menu_details
                ppn = 0.11 * float(order_menu_details)
                tot_payment = float(total) + ppn
            
            print('----- Found current OrderMenu -----')
            OrderMenu.objects.filter(id = om_id).update(total_order = total, tax_order = ppn, total_payment = tot_payment)
            return current_order[0]
        else:
            print('----- Create New OrderMenu -----')
            order_menu_instance = OrderMenu.objects.create(**validated_data)
            TableResto.objects.filter(id = order_menu_instance.table_resto.id).update(table_status = 'Terisi')
            return order_menu_instance

class OrderMenuViewSerializer(serializers.ModelSerializer):
    table_resto = TableRestoSerializer(many = False)

    class Meta:
        model = OrderMenu
        fields = ('id', 'code', 'table_resto', 'cashier', 'waitress', 'order_status', 'status')

class OrderMenuDetailSerializer(serializers.ModelSerializer):
    class Meta:
        model = OrderMenuDetail                
        fields = ('id', 'order_menu', 'menu_resto', 'quantity', 'subtotal', 'description', 'order_menu_detail_status', 'status', 'user_create')        

    def create(self, validated_data):        
        order_menu_detail = OrderMenuDetail.objects.create(**validated_data)
        order_menu_detail.subtotal = order_menu_detail.quantity * order_menu_detail.menu_resto.price
        order_menu_detail.save()
        return order_menu_detail
    
    def update(self, instance, validated_data):
        instance.menu_resto = validated_data.get('menu_resto', instance.menu_resto)
        instance.quantity = validated_data.get('quantity', instance.quantity)
        instance.description = validated_data.get('description', instance.description)
        instance.order_menu_detail_status = validated_data.get('order_menu_detail_status', instance.order_menu_detail_status)
        instance.subtotal = instance.quantity * instance.menu_resto.price
        instance.subtotal = validated_data.get('subtotal', instance.subtotal)
        instance.save()
        return instance
      
class OrderMenuDetailViewSerializer(serializers.ModelSerializer):
    menu_resto_id = serializers.CharField(source = 'menu_resto.id', read_only = True)
    menu_resto_name = serializers.CharField(source = 'menu_resto.name', read_only = True)
    menu_resto_price = serializers.DecimalField(source = 'menu_resto.price', read_only = True, max_digits = 10, decimal_places = 2)
    menu_resto_image_menu = serializers.ImageField(source = 'menu_resto.image_menu', read_only = True)
    menu_resto_description = serializers.CharField(source = 'menu_resto.description', read_only = True)
    
    class Meta:                        
        model = OrderMenuDetail        
        fields = ('id', 'menu_resto_id', 'menu_resto_name', 'menu_resto_price', 'menu_resto_image_menu', 'menu_resto_description', 'order_menu', 'quantity', 'subtotal', 'description', 'order_menu_detail_status', 'status')
        