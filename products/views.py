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


class ProductSearchView(generics.ListAPIView):
    """
    API endpoint for searching and sorting products.

    Allows users to search for products based on a query string and sort the search results.

    Request method: GET
    Endpoint: /api/product/search/

    Query Parameters:
    - query (optional): The search query string.
    - sort_by (optional): The field to sort the search results by. Defaults to 'name'.
    - sort_order (optional): The sort order for the search results. 'asc' for ascending (default), 'desc' for descending.

    Returns a list of serialized products based on the search query and sorting parameters.

    Returns:
        200 OK: Successful search operation.
            Response Payload:
            [
                {
                    "id": "integer",
                    "name": "string",
                    "description": "string",
                    "price": "decimal",
                    "stock": "integer",
                    "selected": "boolean"
                },
                ...
            ]

        400 BAD REQUEST: Invalid query or sorting parameters.
    """
    serializer_class = ProductSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        query = self.request.query_params.get('query', '')
        sort_by = self.request.query_params.get('sort_by', 'name')
        sort_order = self.request.query_params.get('sort_order', 'asc')

        products = Product.objects.filter(name__icontains=query)
        fields = ProductSerializer.Meta.fields

        # Apply sorting based on the sort_by and sort_order parameters
        if sort_by in fields:
            # Construct the sort field based on sort_by and sort_order
            sort_field = sort_by if sort_order == 'asc' else f"-{sort_by}"
            products = products.order_by(sort_field)

        return products

    def list(self, request, *args, **kwargs):
        queryset = self.get_queryset()
        serializer = self.get_serializer(queryset, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)
