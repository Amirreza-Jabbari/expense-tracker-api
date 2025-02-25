from django.contrib.auth import get_user_model
from rest_framework import serializers
from core.models import PasswordResetToken
from django.utils.http import urlsafe_base64_decode, urlsafe_base64_encode
from django.contrib.auth.tokens import default_token_generator
from django.utils.encoding import force_bytes


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = get_user_model()
        fields = ('email', 'password', 'f_name', 'l_name')
        extra_kwargs = {
            'password': {'min_length':8, 'write_only':True, 'required': True}
        }
    def create(self, validated_data):
        return get_user_model().objects.create_user(**validated_data)
    
class UserDetailSerializer(serializers.ModelSerializer):
    class Meta:
        model = get_user_model()
        exclude = ['password']

class UserUpdateSerializer(serializers.ModelSerializer):
    class Meta:
        model = get_user_model()
        exclude = ['password']
    
    def update(self, instance, validated_data):
        password = validated_data.pop('password', None)
        user = super().update(instance, validated_data)

        if password:
            user.set_password(password)
            user.save()

        return user
        
class PasswordResetRequestSerializer(serializers.Serializer):
    email = serializers.EmailField()

    def validate_email(self, value):
        if not get_user_model().objects.filter(email=value).exists():
            raise serializers.ValidationError("User  with this email does not exist.")
        return value

class PasswordResetSerializer(serializers.Serializer):
    token = serializers.CharField()  # Treat token as a CharField
    new_password1 = serializers.CharField(write_only=True, min_length=8)
    new_password2 = serializers.CharField(write_only=True, min_length=8)

    def validate(self, data):
        # Ensure the new passwords match
        if data['new_password1'] != data['new_password2']:
            raise serializers.ValidationError("Passwords do not match.")
        return data

    def validate_token(self, value):
        try:
            # Get the token from the URL parameters
            uidb64 = self.context['request'].parser_context['kwargs']['uidb64']
            token = self.context['request'].parser_context['kwargs']['token']

            # Check if the token is valid
            user = get_user_model().objects.get(pk=urlsafe_base64_decode(uidb64).decode())
            if not default_token_generator.check_token(user, token):
                raise serializers.ValidationError("Invalid token.")
        except (TypeError, ValueError, OverflowError, get_user_model().DoesNotExist):
            raise serializers.ValidationError("Invalid token.")
        return value

    def save(self, **kwargs):
        # Get the token from the URL parameters
        uidb64 = self.context['request'].parser_context['kwargs']['uidb64']
        token = self.context['request'].parser_context['kwargs']['token']

        # Update the user's password
        user = get_user_model().objects.get(pk=urlsafe_base64_decode(uidb64).decode())
        new_password = self.validated_data['new_password1']
        user.set_password(new_password)
        user.save()

        return user