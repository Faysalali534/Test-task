import django
from django.contrib.auth.models import User
from rest_framework import generics
from rest_framework import viewsets
from rest_framework import permissions
from rest_framework.decorators import action
from rest_framework.exceptions import ValidationError
from rest_framework.generics import ListAPIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework_simplejwt.exceptions import InvalidToken
from rest_framework_simplejwt.exceptions import TokenError
from rest_framework_simplejwt.settings import api_settings
from rest_framework_simplejwt.views import TokenViewBase

from product_manager.utils import create_json_response
from products.models import Product
from products.models import ProductSelection
from products.serializers import UserSerializer
from products.serializers import ProductSerializer
from products.serializers import ProductSelectionSerializer


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
        try:
            serializer = self.get_serializer(data=request.data)
            serializer.is_valid(raise_exception=True)
            self.perform_create(serializer)
            user = serializer.instance
            return Response(create_json_response(status=True, message="user created", data=UserSerializer(user).data),
                            status=status.HTTP_201_CREATED)
        except ValidationError as e:
            return Response(create_json_response(status=False, message=e),
                            status=status.HTTP_400_BAD_REQUEST)
        except Exception as e:
            return Response(create_json_response(status=False, message=e),
                            status=status.HTTP_400_BAD_REQUEST)


class TokenObtainPairView(TokenViewBase):
    """
    Takes a set of user credentials and returns an access and refresh JSON web
    token pair to prove the authentication of those credentials.
    """

    _serializer_class = api_settings.TOKEN_OBTAIN_SERIALIZER

    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)

        try:
            serializer.is_valid(raise_exception=True)
        except TokenError as e:
            raise InvalidToken(e.args[0])

        return Response(create_json_response(status=True, message="Token Created", data=serializer.validated_data),
                        status=status.HTTP_200_OK)


class TokenRefreshView(TokenViewBase):
    """
    Takes a refresh type JSON web token and returns an access type JSON web
    token if the refresh token is valid.
    """

    _serializer_class = api_settings.TOKEN_REFRESH_SERIALIZER

    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)

        try:
            serializer.is_valid(raise_exception=True)
        except TokenError as e:
            raise InvalidToken(e.args[0])

        return Response(create_json_response(status=True, message="Token Created", data=serializer.validated_data),
                        status=status.HTTP_200_OK)


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

    def create(self, request, *args, **kwargs):
        try:
            serializer = self.get_serializer(data=request.data)
            serializer.is_valid(raise_exception=True)
            self.perform_create(serializer)
            return Response(create_json_response(status=True, message="Product Created", data=serializer.data))
        except Exception as e:
            return Response(create_json_response(status=False, message=e), status=status.HTTP_400_BAD_REQUEST)


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
                },
                ...
            ]

        400 BAD REQUEST: Invalid query or sorting parameters.
    """
    serializer_class = ProductSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        try:
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
        except Exception as e:
            return Product.objects.none()

    def list(self, request, *args, **kwargs):
        try:
            queryset = self.get_queryset()
            serializer = self.get_serializer(queryset, many=True)
            return Response(create_json_response(status=True, message=f"Products Overview", data=serializer.data))
        except Exception as e:
            return Response(dict(error=str(e)), status=status.HTTP_400_BAD_REQUEST)


class ProductSelectViewSet(viewsets.ModelViewSet):
    permission_classes = [permissions.IsAuthenticated]

    @action(detail=True, methods=['post'])
    def select(self, request, pk=None):
        """
        API endpoint to select a product.

        Marks the specified product as selected.

        Request method: POST
        Endpoint: /api/product/{id}/select/

        Parameters:
            - {id}: The ID of the product to be selected.

        Returns:
            - 200 OK: Product selected successfully.
                Response Payload:
                            {
                "status": true,
                "message": "Product Selected by user aastasaayyassb",
                "data": [
                    {
                        "user": 1,
                        "product": 1,
                        "selected": true
                    }
                ]
            }

            - 404 NOT FOUND: Product with the specified ID not found.

        Raises:
            - HTTPError: If there is a general error on the Select API.

        """
        try:

            serializer = ProductSelectionSerializer(
                data=dict(user=request.user.id, product=pk, selected=True))
            if serializer.is_valid(raise_exception=True):
                serializer.save()
                return Response(
                    create_json_response(status=True, message=f"Product Selected by user {request.user.username}",
                                         data=serializer.data))
        except django.db.utils.IntegrityError as e:
            return Response(
                create_json_response(status=True, message=f"Product Selected by user {request.user.username} again"),
                status=status.HTTP_200_OK)
        except ValidationError as e:
            error_detail = e.detail
            error_message = error_detail.get('non_field_errors', None)
            if str(error_message[0]).__contains__('unique'):
                return Response(
                    create_json_response(status=True,
                                         message=f"Product Selected by user {request.user.username} again"),
                    status=status.HTTP_200_OK)
            return Response(create_json_response(status=False, message=e),
                            status=status.HTTP_400_BAD_REQUEST)
        except Product.DoesNotExist:
            return Response(create_json_response(status=False, message="Product doesnt exist"),
                            status=status.HTTP_404_NOT_FOUND)
        except Exception:
            return Response(create_json_response(status=False, message="General Error on Select API"),
                            status=status.HTTP_400_BAD_REQUEST)

    @action(detail=True, methods=['put'])
    def deselect(self, request, pk=None):
        """
        API endpoint to deselect a product.

        Marks the specified product as not selected.

        Request method: PUT
        Endpoint: /api/product/{id}/deselect/

        Parameters:
            - {id}: The ID of the product to be deselected.

        Returns:
            - 200 OK: Product deselected successfully.
                Response Payload:
                {
                    "status": true,
                    "message": "Product Deselected by user aastasaayyassb",
                    "data": [
                        {
                            "user": 1,
                            "product": 1,
                            "selected": false
                        }
                    ]
                }

            - 404 NOT FOUND: Product with the specified ID not found.

        Raises:
            - HTTPError: If there is a general error on the Deselect API.

        """
        try:
            product_selection = ProductSelection.objects.get(user_id=request.user.id, product_id=pk)
            serializer = ProductSelectionSerializer(product_selection, data={'selected': False}, partial=True)
            if serializer.is_valid():
                serializer.save()
                return Response(
                    create_json_response(status=True, message=f"Product Deselected by user {request.user.username}",
                                         data=serializer.data))
        except ProductSelection.DoesNotExist:
            return Response(create_json_response(status=False, message="Product selection doesn't exist"),
                            status=status.HTTP_404_NOT_FOUND)
        except Exception:
            return Response(create_json_response(status=False, message="General Error on Deselect API"),
                            status=status.HTTP_400_BAD_REQUEST)


class UserProductListView(ListAPIView):
    serializer_class = ProductSelectionSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        user = self.request.user
        return ProductSelection.objects.filter(user=user)

    def get_serializer_context(self):
        context = super().get_serializer_context()
        context.update({"depth": 1})
        return context

    def list(self, request, *args, **kwargs):
        """
                API endpoint to retrieve products of a user.

                Returns the list of products selected by the user.

                Request method: GET
                Endpoint: /api/user/products/

                Returns:
                    - 200 OK: Products retrieved successfully.
                        Response Payload:
                                        {
                    "status": true,
                    "message": "Products Overview",
                    "data": [
                        [
                            {
                                "id": 4,
                                "name": "adada",
                                "description": "This is a sample product description.",
                                "price": "121.00",
                                "stock": 2
                            },
                            {
                                "id": 1,
                                "name": "amazon",
                                "description": "This is a sample product description.",
                                "price": "121.00",
                                "stock": 2
                            },
                            {
                                "id": 3,
                                "name": "some",
                                "description": "This is a sample product description.",
                                "price": "121.00",
                                "stock": 2
                            },
                            {
                                "id": 2,
                                "name": "wwd",
                                "description": "This is a sample product description.",
                                "price": "121.00",
                                "stock": 2
                            }
                        ]
                    ]
                    }
                """
        queryset = self.filter_queryset(self.get_queryset())

        page = self.paginate_queryset(queryset)
        if page is not None:
            serializer = self.get_serializer(page, many=True)
            return self.get_paginated_response(serializer.data)

        serializer = self.get_serializer(queryset, many=True)
        return Response(create_json_response(status=True, message=f"Products of user {request.user.username}",
                                             data=serializer.data))
