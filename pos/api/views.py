from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework import permissions
from pos_app.models import (
    User, TableResto, Profile, Category, MenuResto, 
    OrderMenu, OrderMenuDetail,
)
from api.serializers import (
    TableRestoSerializer, LoginSerializer, ProfileSerializer, ProfileSerializerII,
    RegisterWaitressSerializer, CategorySerializer, 
    MenuRestoSerializer, OrderMenuCreateSerializer, OrderMenuViewSerializer,
    OrderMenuDetailSerializer, OrderMenuDetailViewSerializer,
)
from rest_framework import generics
from rest_framework.generics import GenericAPIView
from rest_framework.authentication import TokenAuthentication
from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework.authtoken.models import Token
from django.contrib.auth import login as django_login, logout as django_logout
from django.http import HttpResponse, JsonResponse
from rest_framework import filters

# Start Controller TableResto
class TableRestoListApiView(APIView):
    permission_classes = [IsAuthenticated]   

    def get(self, request, *args, **kwargs):
        table_restos = TableResto.objects.all()
        serializer = TableRestoSerializer(table_restos, many = True)
        response = {
            'status' : status.HTTP_200_OK,
            'message' : 'Retrive all data success...',
            'data' : serializer.data
        }
        return Response(response, status = status.HTTP_200_OK)
        # return Response(serializer.data, status = status.HTTP_200_OK)       

    def post(self, request, *args,**kwargs):
        data = {
            'code' : request.data.get('code'),
            'name' : request.data.get('name'),
            'capacity' : request.data.get('capacity'),            
        }
        serializer = TableRestoSerializer(data = data)
        if serializer.is_valid():
            serializer.save()
            response = {
                'status' : status.HTTP_201_CREATED,
                'message' : 'Data created successfully...',
                'data' : serializer.data
            }
            return Response(response, status = status.HTTP_201_CREATED)            

        return Response(serializer.errors, status = status.HTTP_400_BAD_REQUEST)
    
class TableRestoDetailApiView(APIView):
    permission_classes = [IsAuthenticated]

    def get_object(self, id):
        try:
            return TableResto.objects.get(id = id)
        except TableResto.DoesNotExist:
            return None
        
    def get(self, request, id, *args, **kwargs):
        table_resto_instance = self.get_object(id)
        if not table_resto_instance:
            return Response(
                {
                    'status' : status.HTTP_400_BAD_REQUEST,
                    'message' : 'Data does not exists...',
                    'data' : {}
                }, status = status.HTTP_400_BAD_REQUEST 
            )

        serializer = TableRestoSerializer(table_resto_instance)
        response = {
            'status' : status.HTTP_200_OK, 
            'message' : 'Data retrieve successfully...',
            'data' : serializer.data 
        }
        return Response(response, status = status.HTTP_200_OK)

    def put(self, request, id, *args, **kwargs):
        table_resto_instance = self.get_object(id)
        if not table_resto_instance:
            return Response(
                {
                    'status' : status.HTTP_400_BAD_REQUEST, 
                    'message' : 'Data does not exists...',
                    'data' : {} 
                }, status = status.HTTP_400_BAD_REQUEST
            )
        
        data = {
            'code' : request.data.get('code'),
            'name' : request.data.get('name'),
            'capacity' : request.data.get('capacity'),
            'table_status' : request.data.get('table_status'),
            'status' : request.data.get('status'),
        }
        serializer = TableRestoSerializer(instance = table_resto_instance, data = data, partial = True)
        if serializer.is_valid():
            serializer.save()
            response = {
                'status' : status.HTTP_200_OK,
                'message' : 'Data updated successfully...',
                'data' : serializer.data
            }
            return Response(response, status = status.HTTP_200_OK)
       
        return Response(serializer.errors, status = status.HTTP_400_BAD_REQUEST)

    def delete(self, request, id, *args, **kwargs):
        table_resto_instance = self.get_object(id)
        if not table_resto_instance:
            return Response(
                {
                    'status' : status.HTTP_400_BAD_REQUEST, 
                    'message' : 'Data does not exists...',
                    'data' : {} 
                }, status = status.HTTP_400_BAD_REQUEST
            )
                    
        table_resto_instance.delete()
        response = {
            'status' : status.HTTP_200_OK,
            'message' : 'Data deleted successfully...'
        }
        return Response(response, status = status.HTTP_200_OK)
# End Controller TableResto

class LoginView(GenericAPIView):
    serializer_class = LoginSerializer

    def post(self, request):
        serializer = LoginSerializer(data = request.data)
        serializer.is_valid(raise_exception = True)
        user = serializer.validated_data['user']
        django_login(request, user)
        token, created = Token.objects.get_or_create(user = user)
        return JsonResponse({
            'data' : {
                'token' : token.key,
                'id' : user.id,
                'username' : user.username,
                'first_name' : user.first_name,
                'last_name' : user.last_name,
                'email' : user.email,
                'is_active' : user.is_active,            
                'is_waitress' : user.is_waitress,
            },
            'status' : 200,
            'message' : 'You are login right now...'
        })

class LogoutView(APIView):
    authenticate_classes = (TokenAuthentication, )
    
    def post(self, request):
        django_logout(request)
        return JsonResponse({'message' : 'You have been logout...'})

# class RegisterWaitressAPI(generics.CreateAPIView):
#     queryset = User.objects.all()
#     serializer_class = RegisterWaitressSerializer

class RegisterWaitressAPI(APIView):
    serializer_class = RegisterWaitressSerializer
    
    def post(self, request, format = None):
        serializer = self.serializer_class(data = request.data)
        if serializer.is_valid():
            user = serializer.save()

            response_data = {
                'status' : status.HTTP_201_CREATED,
                'message' : 'Selamat anda telah terdaftar...',
                'data' : serializer.data,                
            }
            return Response(response_data, status = status.HTTP_201_CREATED)        
        return Response({
            'status' : status.HTTP_400_BAD_REQUEST,
            'message' : 'Terjadi error...',
            'data' : serializer.errors,
        }, status = status.HTTP_400_BAD_REQUEST)

# Start Controller Profile
class ProfileDetailApiView(APIView):
    permission_classes = [IsAuthenticated]

    def get_object(self, user_id):
        try:            
            return Profile.objects.get(user = user_id)                    
        except Profile.DoesNotExist:
            return None            
    
    # Retrieve data in Profile model
    def get(self, request, user_id, *args, **kwargs):
        profile_instance = self.get_object(user_id)
        if not profile_instance:
            return Response(
                {
                    'status' : status.HTTP_400_BAD_REQUEST,
                    'message' : 'Data does not exists...',
                    'data' : {}
                }, status = status.HTTP_400_BAD_REQUEST
            )
        
        serializer = ProfileSerializer(profile_instance, context = {'request' : request})
        response = {
                'status' : status.HTTP_200_OK,
                'message' : 'Data retrieve successfully...',
                'data' : serializer.data
            }
        return Response(response, status = status.HTTP_200_OK)

    # Update data in Profile model
    def put(self, request, user_id, *args, **kwargs):
        profile_instance = self.get_object(user_id)
        if not profile_instance:
            return Response(
                {
                    'status' : status.HTTP_400_BAD_REQUEST, 
                    'message' : 'Data does not exists...',
                    'data' : {} 
                }, status = status.HTTP_400_BAD_REQUEST
            )
        
        data = {
            'avatar' : request.data.get('avatar'),
            'bio' : request.data.get('bio'),
            'user_update' : request.data.get('user_update'),
        }
        serializer = ProfileSerializer(instance = profile_instance, 
            data = data, partial = True, 
            context = {'request' : request})
        if serializer.is_valid():
            serializer.save()
            response = {
                'status' : status.HTTP_200_OK,
                'message' : 'Data updated successfully...',
                'data' : serializer.data
            }
            return Response(response, status = status.HTTP_200_OK)
       
        return Response(serializer.errors, status = status.HTTP_400_BAD_REQUEST)    
# End Controller Profile

# Start Controller Category
class CategoryListApiView(APIView):
    permission_classes = [IsAuthenticated]   

    def get(self, request, *args, **kwargs):
        categories = Category.objects.all()
        serializer = CategorySerializer(categories, many = True)
        response = {
            'status' : status.HTTP_200_OK,
            'message' : 'Retrive all data success...',
            'data' : serializer.data
        }
        return Response(response, status = status.HTTP_200_OK)        

class CategoryDetailApiView(APIView):
    permission_classes = [IsAuthenticated]

    def get_object(self, id):
        try:
            return Category.objects.get(id = id)
        except Category.DoesNotExist:
            return None
        
    def get(self, request, id, *args, **kwargs):
        category_instance = self.get_object(id)
        if not category_instance:
            return Response(
                {
                    'status' : status.HTTP_400_BAD_REQUEST,
                    'message' : 'Data does not exists...',
                    'data' : {}
                }, status = status.HTTP_400_BAD_REQUEST 
            )

        serializer = CategorySerializer(category_instance)
        response = {
            'status' : status.HTTP_200_OK, 
            'message' : 'Data retrieve successfully...',
            'data' : serializer.data 
        }
        return Response(response, status = status.HTTP_200_OK)
# End Controller Category

# Start Controller MenuResto
class MenuRestoListApiView(APIView):    

    def get(self, request, *args, **kwargs):
        menu_restos = MenuResto.objects.all()
        serializer = MenuRestoSerializer(menu_restos, many = True,
            context = {'request' : request})
        response = {
            'status' : status.HTTP_200_OK,
            'message' : 'Retrive all data success...',
            'data' : serializer.data
        }
        return Response(response, status = status.HTTP_200_OK)

class MenuRestoDetailApiView(APIView):
    permission_classes = [IsAuthenticated]

    def get_object(self, id):
        try:
            return MenuResto.objects.get(id = id)
        except MenuResto.DoesNotExist:
            return None
        
    def get(self, request, id, *args, **kwargs):
        menu_resto_instance = self.get_object(id)
        if not menu_resto_instance:
            return Response(
                {
                    'status' : status.HTTP_400_BAD_REQUEST,
                    'message' : 'Data does not exists...',
                    'data' : {}
                }, status = status.HTTP_400_BAD_REQUEST 
            )

        serializer = MenuRestoSerializer(menu_resto_instance, context = {'request' : request})
        response = {
            'status' : status.HTTP_200_OK, 
            'message' : 'Data retrieve successfully...',
            'data' : serializer.data 
        }
        return Response(response, status = status.HTTP_200_OK)
# End Controller MenuResto

# Start Controller OrderMenu
class OrderMenuCreateApi(generics.CreateAPIView):
    queryset = OrderMenu.objects.all()
    serializer_class = OrderMenuCreateSerializer
    permission_classes = [permissions.IsAuthenticated]

class OrderMenuListApiView(APIView):
    permission_classes = [IsAuthenticated]   

    def get(self, request, *args, **kwargs):
        order_menus = OrderMenu.objects.all()
        serializer = OrderMenuCreateSerializer(order_menus, many = True)
        response = {
            'status' : status.HTTP_200_OK,
            'message' : 'Retrive all data success...',
            'data' : serializer.data
        }
        return Response(response, status = status.HTTP_200_OK)

    def post(self, request, *args,**kwargs):
        data = {
            'table_resto' : request.data.get('table_resto'),
            'waitress' : request.data.get('waitress'),
            'user_create' : request.data.get('user_create'),            
        }
        serializer = OrderMenuCreateSerializer(data = data)
        if serializer.is_valid():
            serializer.save()
            response = {
                'status' : status.HTTP_201_CREATED,
                'message' : 'Data created successfully...',
                'data' : serializer.data
            }
            return Response(response, status = status.HTTP_201_CREATED)            

        return Response(serializer.errors, status = status.HTTP_400_BAD_REQUEST)

class OrderMenuFilterApi(generics.ListAPIView):
    queryset = OrderMenu.objects.all()
    serializer_class = OrderMenuViewSerializer
    filter_backends = [filters.SearchFilter]
    search_fields = ['table_resto__id',]
# End Controller OrderMenu

# Start Controller OrderMenuDetail
class OrderMenuDetailListAPIView(generics.ListAPIView):
    serializer_class = OrderMenuDetailViewSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self, *args, **kwargs):
        query_list = OrderMenuDetail.objects.select_related('menu_resto').all().order_by('id')
        query = self.request.GET.get('q')
        if query:
            query_list = query_list.filter(order_menu__id = query).distinct()
        return query_list
    
# class OrderMenuDetailCreate(generics.CreateAPIView):
#     queryset = OrderMenuDetail.objects.all().order_by('id')
#     serializer_class = OrderMenuDetailSerializer
#     permission_classes = [IsAuthenticated]

class OrderMenuDetailCreateApiView(APIView):
    permission_classes = [IsAuthenticated]   

    def post(self, request, *args,**kwargs):
        data = {
            'order_menu' : request.data.get('order_menu'),
            'menu_resto' : request.data.get('menu_resto'),
            'user_create' : request.data.get('user_create'),     
            'quantity' : request.data.get('quantity'),       
        }
        serializer = OrderMenuDetailSerializer(data = data)
        if serializer.is_valid():
            serializer.save()
            response = {
                'status' : status.HTTP_201_CREATED,
                'message' : 'Data created successfully...',
                'data' : serializer.data
            }
            return Response(response, status = status.HTTP_201_CREATED)            

        return Response(serializer.errors, status = status.HTTP_400_BAD_REQUEST)

# End Controller OrderMenuDetail