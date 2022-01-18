from rest_framework import serializers
from transactions.models import User
from transactions.models import AccountDetails
from transactions.models import UserBalance


class RegisterSerializer(serializers.ModelSerializer):
    password = serializers.CharField(max_length=68, min_length=6, write_only=True)

    class Meta:
        model = User
        fields = ['email', 'username', 'password']

    def validate(self, attrs):
        attrs.get('email', '')
        username = attrs.get('username', '')
        if not username.isalnum():
            raise serializers.ValidationError('The username should only contain alphanumeric characters')
        return attrs
        return super().validate(attrs)

    def create(self, validated_data):
        return User.objects.create_user(**validated_data)


class VerifyEmailSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['email', 'otp']


class LoginSerializer(serializers.ModelSerializer):
    password = serializers.CharField(max_length=68, min_length=8, write_only=True)

    class Meta:
        model = User
        fields = ['email', 'password']


class ForgotPasswordSerializer(serializers.ModelSerializer):
    email = serializers.EmailField()

    class Meta:
        model = User

        fields = ('email',)


class ResetPasswordSerializer(serializers.ModelSerializer):
    email = serializers.EmailField(min_length=2)
    otp = serializers.CharField(max_length=6)
    password = serializers.CharField(max_length=68, min_length=6, write_only=True)
    confirm_password = serializers.CharField(min_length=6)

    class Meta:
        model = User
        fields = ['email', 'otp', 'password', 'confirm_password']


class CreateAccountSerializer(serializers.ModelSerializer):
    class Meta:
        model = AccountDetails
        fields = ['account_type', 'fullname', 'age', 'employment_status']


class AccountBalanceSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserBalance
        fields = ['account_balance']
