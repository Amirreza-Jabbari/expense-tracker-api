from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework_simplejwt.authentication import JWTAuthentication
from .permissions import IsOwner
from rest_framework import generics, status
from rest_framework.response import Response
from django.core.mail import EmailMultiAlternatives
from django.conf import settings
from django.shortcuts import render
from django.utils.http import urlsafe_base64_encode
from django.contrib.auth.tokens import default_token_generator
from django.contrib.auth import get_user_model
from rest_framework.views import APIView
from .serializers import UserSerializer, UserDetailSerializer, UserUpdateSerializer, PasswordResetSerializer, PasswordResetRequestSerializer
from django.utils.encoding import force_bytes
from django.contrib.auth.models import User
from django.views.decorators.csrf import csrf_exempt
from django.utils.decorators import method_decorator
from django.template.loader import render_to_string
from django.utils.html import strip_tags


User = get_user_model()

@method_decorator(csrf_exempt, name='dispatch')
class CreateUserView(generics.CreateAPIView):
    serializer_class = UserSerializer
    permission_classes = [AllowAny]

@method_decorator(csrf_exempt, name='dispatch')
class RetrieveUserView(generics.RetrieveAPIView):
    serializer_class = UserDetailSerializer
    queryset = User.objects.all()
    lookup_field = 'email'
    permission_classes = [IsAuthenticated]

@method_decorator(csrf_exempt, name='dispatch')
class ListUserView(generics.ListAPIView):
    serializer_class = UserDetailSerializer
    queryset = User.objects.all()
    permission_classes = [IsAuthenticated]

@method_decorator(csrf_exempt, name='dispatch')
class UpdateUserView(generics.UpdateAPIView):
    serializer_class = UserUpdateSerializer
    queryset = User.objects.all()
    lookup_field = 'email'
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated, IsOwner]

@method_decorator(csrf_exempt, name='dispatch')
class DeleteUserView(generics.DestroyAPIView):
    queryset = User.objects.all()
    lookup_field = 'email'
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated, IsOwner]

    def destroy(self, request, *args, **kwargs):
        instance = self.get_object()
        self.perform_destroy(instance)
        return Response(
            {'message': f'User "{instance.email}" has been successfully deleted.'},
            status=status.HTTP_200_OK
        )

# View to request password reset
@method_decorator(csrf_exempt, name='dispatch')
class PasswordResetRequestView(generics.GenericAPIView):
    serializer_class = PasswordResetRequestSerializer
    permission_classes = [AllowAny]

    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        email = serializer.validated_data['email']
        user = get_user_model().objects.get(email=email)
        token = default_token_generator.make_token(user)
        uidb64 = urlsafe_base64_encode(force_bytes(user.pk))
        # Construct URL using path parameters to match the URL pattern
        password_reset_url = f"{request.scheme}://{request.get_host()}/api/user/reset-password/{uidb64}/{token}/"
        
        # Render HTML email template
        html_content = render_to_string('password_reset_email.html', {'password_reset_url': password_reset_url})
        text_content = strip_tags(html_content)  # Plain text version
        
        # Send email with both HTML and plain text
        email_message = EmailMultiAlternatives(
            subject="Password Reset Request",
            body=text_content,
            from_email=settings.EMAIL_HOST_USER,
            to=[email]
        )
        email_message.attach_alternative(html_content, "text/html")
        email_message.send()
        
        return Response({"message": "Password reset email sent successfully."}, status=status.HTTP_200_OK)
    
@csrf_exempt
def password_reset(request,):
    return render(request, 'password_reset_confirm.html')

@method_decorator(csrf_exempt, name='dispatch')
class PasswordResetConfirmView(APIView):
    permission_classes = [AllowAny]

    def get(self, request, uidb64, token):
        # Render a simple form to allow the user to enter the new password
        context = {'uidb64': uidb64, 'token': token}
        return render(request, 'password_reset_confirm.html', context)

    def post(self, request, uidb64, token):
        serializer = PasswordResetSerializer(data=request.data, context={'request': request})
        if serializer.is_valid():
            serializer.save()
            return Response({'message': 'Password has been reset successfully!'}, status=status.HTTP_200_OK)

        return Response({'errors': serializer.errors}, status=status.HTTP_400_BAD_REQUEST)
