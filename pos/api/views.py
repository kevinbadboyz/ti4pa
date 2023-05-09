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
    MenuRestoSerializer,
)
from rest_framework import generics
from rest_framework.generics import GenericAPIView
from rest_framework.authentication import TokenAuthentication
from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework.authtoken.models import Token
from django.contrib.auth import login as django_login, logout as django_logout
from django.http import HttpResponse, JsonResponse

# Start Controller TableResto
class TableRestoListApiView(APIView):    

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

class RegisterWaitressAPI(generics.CreateAPIView):
    queryset = User.objects.all()
    serializer_class = RegisterWaitressSerializer

# Start Controller Profile
class ProfileDetailApiView(APIView):
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
class CategoryList(generics.ListAPIView):
    queryset = Category.objects.all().order_by('id')
    serializer_class =  CategorySerializer

    # def list(self, request, *args, **kwargs):
    #     queryset = self.get_queryset()
    #     serializer = CategorySerializer(queryset, many = True, 
    #         context = {'request' : request})
    #     response = {
    #         'status' : status.HTTP_200_OK,
    #         'message' : 'Retrive all data success...',
    #         'data' : serializer.data
    #     }
    #     return Response(response, status = status.HTTP_200_OK)

class CategoryDetail(generics.RetrieveAPIView):
    queryset = Category.objects.all().order_by('id')
    serializer_class =  CategorySerializer

    # def get_object(self):
    #     return super().get_object()

    # def get(self, request, *args, **kwargs):
    #     return super().get(request, *args, **kwargs)
# End Controller Category

# Start Controller MenuResto
class MenuRestoList(generics.ListAPIView):
    queryset = MenuResto.objects.all().order_by('id')
    serializer_class =  MenuRestoSerializer
    permission_classes = [IsAuthenticated]

    def list(self, request, *args, **kwargs):
        queryset = self.get_queryset()
        serializer = MenuRestoSerializer(queryset, many = True, 
            context = {'request' : request})
        response = {
            'status' : status.HTTP_200_OK,
            'message' : 'Retrive all data success...',
            'data' : serializer.data
        }
        return Response(response, status = status.HTTP_200_OK)

# class MenuRestoList(APIView) run successfully
# class MenuRestoList(APIView):    

#     def get(self, request, *args, **kwargs):
#         menu_restos = MenuResto.objects.all()
#         serializer = MenuRestoSerializer(menu_restos, many = True,
#             context = {'request' : request})
#         response = {
#             'status' : status.HTTP_200_OK,
#             'message' : 'Retrive all data success...',
#             'data' : serializer.data
#         }
#         return Response(response, status = status.HTTP_200_OK)

class MenuRestoDetail(generics.RetrieveUpdateAPIView):
    queryset = MenuResto.objects.all().order_by('id')
    serializer_class =  MenuRestoSerializer
    permission_classes = [IsAuthenticated]

    # def get_object(self, pk):
    #     try:            
    #         return MenuResto.objects.get(pk = pk)                    
    #     except MenuResto.DoesNotExist:
    #         return None            
    
    # # Retrieve data in Profile model
    # def get(self, request, pk, *args, **kwargs):
    #     menu_resto_instance = self.get_object(pk)
    #     if not menu_resto_instance:
    #         return Response(
    #             {
    #                 'status' : status.HTTP_400_BAD_REQUEST,
    #                 'message' : 'Data does not exists...',
    #                 'data' : {}
    #             }, status = status.HTTP_400_BAD_REQUEST
    #         )
        
    #     serializer = MenuRestoSerializer(menu_resto_instance, context = {'request' : request})
    #     response = {
    #             'status' : status.HTTP_200_OK,
    #             'message' : 'Data retrieve successfully...',
    #             'data' : serializer.data
    #         }
    #     return Response(response, status = status.HTTP_200_OK)
# End Controller MenuResto
