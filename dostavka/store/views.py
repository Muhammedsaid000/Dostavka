from rest_framework.pagination import PageNumberPagination
from rest_framework.permissions import IsAuthenticatedOrReadOnly
from .pagination import LargeResultsSetPagination
from .permissions import *
from .serializers import *
from rest_framework import viewsets, generics, status
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.filters import SearchFilter, OrderingFilter
from .filters import *
from rest_framework.response import Response
from rest_framework_simplejwt.views import TokenObtainPairView


class RegisterView(generics.CreateAPIView):
    serializer_class = ProfileSerializer

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data, context={'is_registration': True})
        serializer.is_valid(raise_exception=True)
        user = serializer.save()
        return Response(serializer.data, status=status.HTTP_201_CREATED)


class CustomLoginView(TokenObtainPairView):
    serializer_class = LoginSerializers

    def post(self, request, *args, **kwargs):
        serializer=self.get_serializer(data=request.data)
        try:
            serializer.is_valid(raise_exception=True)
        except Exception:
            return Response({"detail: Неверные учетные данные"}, status=status.HTTP_401_UNAUTHORIZED)

        user=serializer.validated_data
        return Response(serializer.data, status=status.HTTP_200_OK)


class LogoutView(generics.GenericAPIView):
    serializer_class = LogoutSerializer
    def post(self, request, *args, **kwargs):
        refresh_token = request.data.get("refresh")
        if not refresh_token:
            return Response({"detail": "Refresh токен отсутствует."}, status=status.HTTP_400_BAD_REQUEST)
        try:
            token = RefreshToken(refresh_token)
            token.blacklist()
            return Response({"detail": "Вы вышли из системы."}, status=status.HTTP_205_RESET_CONTENT)
        except Exception as e:
            return Response({"detail": "Ошибка обработки токена."}, status=status.HTTP_400_BAD_REQUEST)




class UserProfileListAPIView(generics.ListAPIView):
    queryset = UserProfile.objects.all()
    serializer_class = UserSerializer

    def get_queryset(self):
        return UserProfile.objects.filter(id=self.request.user.id)


class UserProfileDetailAPIView(generics.RetrieveUpdateDestroyAPIView):
    queryset = UserProfile.objects.all()
    serializer_class = UserSerializer

    def get_queryset(self):
        return UserProfile.objects.filter(id=self.request.user.id)


class CategoryListAPIView(generics.ListAPIView):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer


class CategoryDetailAPIView(generics.RetrieveAPIView):
    queryset = Category.objects.all()
    serializer_class = CategoryDetailSerializer


class StoreListAPIView(generics.ListAPIView):
    queryset = Store.objects.all()
    serializer_class = StoreSerializer
    filter_backends = [DjangoFilterBackend, SearchFilter]
    filterset_class = StoreFilter
    search_fields = ['store_name']
    permission_classes = (IsAuthenticatedOrReadOnly,)


class StoreDetailAPIView(generics.RetrieveAPIView):
    queryset = Store.objects.all()
    serializer_class = StoreDetailSerializer


class StoreCreateAPIView(generics.CreateAPIView):
    serializer_class = StoreEditSerializer
    permission_classes = [CheckUserCreate, IsAuthenticatedOrReadOnly]


    def get_queryset(self):
        return Store.objects.filter(user=self.request.user)

class StoreEDITAPIView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Store.objects.all()
    serializer_class = StoreEditSerializer
    permission_classes = [IsAuthenticatedOrReadOnly]

    def get_queryset(self):
        return Store.objects.filter(user=self.request.user)


class ProductListAPIView(generics.ListAPIView):
    queryset = Product.objects.all()
    serializer_class = ProductSerializer
    filter_backends = [DjangoFilterBackend, SearchFilter, OrderingFilter]
    filterset_class = ProductFilter
    search_fields = ['product_name',]
    pagination_class = LargeResultsSetPagination
    ordering_fields = ['price']



class ProductCreateAPIView(generics.CreateAPIView):
    serializer_class = ProductCreateSerializer
    permission_classes = [CheckUserCreate, IsAuthenticatedOrReadOnly]


    def get_queryset(self):
        return Product.objects.filter(user=self.request.user)


class ProductEDITAPIView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Product.objects.all()
    serializer_class = ProductSerializer

    def get_queryset(self):
        return Product.objects.filter(user=self.request.user)


class ComboListAPIView(generics.ListAPIView):
    queryset = Combo.objects.all()
    serializer_class = ComboSerializer


class ComboDetailAPIView(generics.RetrieveAPIView):
    queryset = Combo.objects.all()
    serializer_class = ComboSerializer


class ComboCreateAPIView(generics.CreateAPIView):
    serializer_class = ComboCreateSerializer
    permission_classes = [CheckUserCreate,IsAuthenticatedOrReadOnly]

    def get_queryset(self):
        return Combo.objects.filter(user=self.request.user)


class ComboEDITAPIView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Combo.objects.all()
    serializer_class = ComboCreateSerializer

    def get_queryset(self):
        return Combo.objects.filter(user=self.request.user)


class ReviewViewSet(viewsets.ModelViewSet):
    queryset = Review.objects.all()
    serializer_class = ReviewSerializer
    permission_classes = [CheckReviewCreate, CheckReviewEdit, IsAuthenticatedOrReadOnly]


class CourierReviewViewSet(viewsets.ModelViewSet):
    queryset = CourierReview.objects.all()
    serializer_class = CourierReviewSerializer
    permission_classes = [IsAuthenticatedOrReadOnly]


class SaveListAPIView(generics.ListAPIView):
    queryset = ProductsCart.objects.all()
    serializer_class = SaveSerializer
    permission_classes = [IsAuthenticatedOrReadOnly]

    def get_queryset(self):
        return ProductsCart.objects.filter(id=self.request.user.id)


class SavePostAPIView(generics.RetrieveUpdateDestroyAPIView):
    queryset = ProductsItem.objects.all()
    serializer_class = SavePostSerializer
    permission_classes = [IsAuthenticatedOrReadOnly]
    def get_queryset(self):
        return ProductsItem.objects.filter(id=self.request.user.id)


class OrderListAPIView(generics.ListAPIView):
    queryset = Order.objects.all()
    serializer_class = OrderSerializer


class OrderEDITAPIView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Order.objects.all()
    serializer_class = OrderSerializer
    permission_classes = [CheckReviewEdit]

    def get_queryset(self):
        return Combo.objects.filter(user=self.request.user)

class OrderCreateAPIView(generics.CreateAPIView):
    serializer_class = OrderCreateSerializer
    permission_classes = [CheckOrderCreate, IsAuthenticatedOrReadOnly]


class OrderCourierAPIView(generics.ListAPIView):
    queryset = Order.objects.all()
    serializer_class = OrderSerializer
    permission_classes = [CheckCourierReview]


class CourierViewSet(viewsets.ModelViewSet):
    queryset = Courier.objects.all()
    serializer_class = CourierSerializer
