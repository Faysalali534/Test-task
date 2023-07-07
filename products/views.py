from .models import User
from rest_framework import status
from rest_framework.response import Response
from .serializers import UserSerializer
from rest_framework import viewsets, permissions, generics
from .models import Product
from .serializers import ProductSerializer


class SignupView(generics.CreateAPIView):
    """
    API endpoint for user signup.

    Allows new users to create an account by providing the required user data.

    Request method: POST
    Endpoint: /api/signup/

    Request Payload:
    {
        "username": "string",
        "email": "string",
        "password": "string"
    }

    Returns the serialized user data upon successful signup.

    Returns:
        201 CREATED: User account created successfully.
            Response Payload:
            {
                "id": "integer",
                "username": "string",
                "email": "string"
            }

        400 BAD REQUEST: Invalid request payload or user data.
    """

    queryset = User.objects.all()
    serializer_class = UserSerializer

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)
        user = serializer.instance

        return Response(UserSerializer(user).data, status=status.HTTP_201_CREATED)


class ProductViewSet(viewsets.ModelViewSet):
    """
    API endpoint for Creating products.

    Provides CRUD (Create) operations for products.

    Allowed HTTP methods: POST
    Endpoint: /api/product/create/

    POST:
        Creates a new product with the provided data.

    Returns:
        - POST : The serialized data of the created product.

    Permissions:
        - Only authenticated users can access this endpoint.
    """
    queryset = Product.objects.all()
    serializer_class = ProductSerializer
    permission_classes = [permissions.IsAuthenticated]

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)
        headers = self.get_success_headers(serializer.data)
        return Response(serializer.data, status=status.HTTP_201_CREATED, headers=headers)
