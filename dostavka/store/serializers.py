from rest_framework import serializers
from .models import *
from rest_framework_simplejwt.tokens import RefreshToken
from django.contrib.auth import authenticate


class ProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserProfile
        fields = ['username', 'email', 'password', 'first_name', 'last_name']
        extra_kwargs = {'password': {'write_only': True}}

    def create(self, validated_data):
        user = UserProfile.objects.create_user(**validated_data)
        return user

    def to_representation(self, instance):
        # Проверяем, был ли вызван create
        if self.context.get('is_registration', False):
            refresh = RefreshToken.for_user(instance)
            return {
                'user': {
                    'username': instance.username,
                    'email': instance.email,
                },
                'access': str(refresh.access_token),
                'refresh': str(refresh)
            }
        return super().to_representation(instance)


class LoginSerializers(serializers.Serializer):
    username = serializers.CharField()
    password = serializers.CharField(write_only=True)

    def validate(self, data):
        user = authenticate(**data)
        if user and user.is_active:
            return user
        raise serializers.ValidationError("Неверные учетные данные или пользователь неактивен.")

    def to_representation(self, instance):
        refresh = RefreshToken.for_user(instance)
        return {
            'user': {
                'username': instance.username,
                'email': instance.email,
            },
            'access': str(refresh.access_token),
            'refresh': str(refresh)
        }


class LogoutSerializer(serializers.Serializer):
    refresh = serializers.CharField()

    def validate(self, data):
        self.token = data['refresh']
        return data

    def save(self, **kwargs):
        try:
            token = RefreshToken(self.token)
            token.blacklist()
        except Exception as e:
            raise serializers.ValidationError({'detail': 'Недействительный или уже отозванный токен'})



class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserProfile
        fields =  '__all__'

class UserNameSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserProfile
        fields = ['last_name', 'first_name', 'username']


class UserReviewSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserProfile
        fields = ['user']


class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = ['category_name',]


class ContactsSerializer(serializers.ModelSerializer):
    class Meta:
        model=Contacts
        fields=['contact_info']

class StoreNameSerializer(serializers.ModelSerializer):
    class Meta:
        model=Store
        fields=['store_name',]


class StoreSerializer(serializers.ModelSerializer):
    get_avg_rating = serializers.SerializerMethodField()
    get_count_people = serializers.SerializerMethodField()
    category=CategorySerializer(read_only=True)
    class Meta:
        model = Store
        fields = ['id', 'store_name','category', 'image', 'get_avg_rating', 'get_count_people',]

    def get_avg_rating(self, obj):
        return obj.get_avg_rating()

    def get_count_people(self, obj):
        return obj.get_count_people()


class StoreEditSerializer(serializers.ModelSerializer):
    class Meta:
        model=Store
        fields='__all__'


class CategoryDetailSerializer(serializers.ModelSerializer):
    store_category=StoreSerializer(many=True, read_only=True)
    class Meta:
        model = Category
        fields = ['category_name', 'store_category']


class ProductSerializer(serializers.ModelSerializer):
    store=StoreNameSerializer(read_only=True)
    class Meta:
        model = Product
        fields = ['id', 'product_name', 'description', 'price',  'store']


class ProductCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model=Product
        fields=['id', 'product_name', 'description', 'price',  'store', 'user']


class ComboSerializer(serializers.ModelSerializer):
    class Meta:
        model = Combo
        fields = ['id', 'product_name', 'description', 'price',  'store']


class ComboCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Combo
        fields = ['id', 'product_name', 'description', 'price',  'store', 'user']


class ReviewSerializer(serializers.ModelSerializer):
    datetime=serializers.DateTimeField(format='%d-%m-%Y  %H:%M')
    user=UserNameSerializer()
    store=StoreNameSerializer()
    class Meta:
        model = Review
        fields = ['id', 'user', 'store',  'stars', 'parent','text','datetime']



class StoreDetailSerializer(serializers.ModelSerializer):
    products=ProductSerializer(read_only=True, many=True)
    user=UserNameSerializer(read_only=True)
    category=CategorySerializer(read_only=True)
    reviews=ReviewSerializer(read_only=True, many=True)
    get_count_people=serializers.SerializerMethodField()
    contacts=ContactsSerializer(many=True, read_only=True)
    product_combo=ComboSerializer(many=True, read_only=True)
    class Meta:
        model=Store
        fields=['id', 'store_name', 'description','user', 'contacts','category','address', 'image','products','product_combo','get_count_people', 'reviews',]

    def get_count_people(self, obj):
        return obj.get_count_people()



class SaveSerializer(serializers.ModelSerializer):
    class Meta:
        model = ProductsCart
        fields = '__all__'


class SavePostSerializer(serializers.ModelSerializer):
    class Meta:
        model = ProductsItem
        fields = '__all__'


class OrderSerializer(serializers.ModelSerializer):
    created_date = serializers.DateTimeField(format='%d-%m-%Y  %H:%M')
    client = UserNameSerializer(read_only=True)
    cart = SavePostSerializer(read_only=True)
    courier = UserNameSerializer(read_only=True)

    class Meta:
        model = Order
        fields = ['id', 'client', 'cart', 'status', 'address', 'courier', 'created_date']


class OrderCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Order
        fields = '__all__'


class CourierReviewSerializer(serializers.ModelSerializer):
    datetime=serializers.DateTimeField(format='%d-%m-%Y  %H:%M')
    user=UserNameSerializer(read_only=True)
    class Meta:
        model = Review
        fields = ['id', 'user', 'store',  'stars', 'parent','text','datetime']


class CourierSerializer(serializers.ModelSerializer):
    rating=CourierReviewSerializer(read_only=True, many=True)
    class Meta:
        model=Courier
        fields=['user', 'current_orders', 'status', 'rating']
