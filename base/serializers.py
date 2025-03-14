from rest_framework import serializers
from django.contrib.auth import authenticate
from django.contrib.auth.password_validation import validate_password
from django.contrib.auth import get_user_model

User = get_user_model()  # Correct variable naming convention


class RegistrationSerializer(serializers.ModelSerializer):
    password2 = serializers.CharField(style={'input_type': 'password'}, write_only=True)

    class Meta:
        model = User
        fields = ('id', 'email', 'first_name', 'last_name', 'password', 'password2')
        extra_kwargs = {'password': {'write_only': True}}



    def validate_email(self, value):
        value = value.lower()  # Normalize email
        if User.objects.filter(email__iexact=value).exists():
            raise serializers.ValidationError("A user with this email already exists.")
        return value


    
    def validate(self, attrs):
        if attrs['password'] != attrs['password2']:
            raise serializers.ValidationError("Password and Confirm Password do not match.")
        
        validate_password(attrs['password'])  # Django's built-in password validation
        return attrs
    
    
    def create(self, validated_data):
        validated_data.pop('password2')  # Remove confirm password
        validated_data['email'] = validated_data['email'].lower()  # Normalize email
        return User.objects.create_user(**validated_data)  # Uses Django’s built-in method



class LoginSerializer(serializers.Serializer):
    email = serializers.EmailField()
    password = serializers.CharField(write_only=True)

    def validate(self, attrs):
        email = attrs.get('email').lower()  # Normalize email
        password = attrs.get('password')

        user = authenticate(email=email, password=password)  # Authenticate user

        if not user:
            raise serializers.ValidationError("Invalid email or password.")

        if not user.is_active:
            raise serializers.ValidationError("This account is inactive.")

        attrs['user'] = user  # Store user object in validated data
        return attrs
