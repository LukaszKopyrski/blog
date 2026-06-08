from rest_framework import serializers
from api.models.user import CustomUser
import re
from django.contrib.auth.password_validation import validate_password

class CustomUserSerializer(serializers.ModelSerializer):
    last_login = serializers.DateTimeField(format="%Y/%m/%d %H:%M", read_only=True)
    date_joined = serializers.DateTimeField(format="%Y/%m/%d %H:%M", read_only=True)

    class Meta:
        model = CustomUser
        fields = ['id','email','username','password','answer','is_staff','is_demo','last_login','date_joined']
        extra_kwargs = {
            'password': {'write_only': True},
            'is_staff':{'read_only':True},
            'is_demo':{'read_only':True},
            'last_login':{'read_only':True},
            'date_joined':{'read_only':True}
        }

    def validate_username(self, value):
        regex = r'^[a-zA-Z0-9_.@]{2,16}$'
        if not re.match(regex, value):
            raise serializers.ValidationError("Username must contain uppercase letters, lowercase letters numbers and the following characters :_.@. Length must be between 2 and 16 characters.")
        
        if CustomUser.objects.filter(username=value).exists():
            raise serializers.ValidationError("Username is already taken")
        
        return value
    
    def validate_password(self, value):
        validate_password(value)
        regex = r'^(?=.*?[A-Z])(?=.*?[a-z])(?=.*?[0-9])(?=.*?[!@#$^&*-]).{8,64}$'
        if not re.match(regex, value):
            raise serializers.ValidationError("Password must contain uppercase letters, lowercase letters numbers and the following characters :!@$^&*-. Length must be between 8 and 16 characters.")
        return value    
    
    def validate_answer(self, value):
        regex = r'^[a-zA-Z]{2,16}$'
        if not re.match(regex, value):
            raise serializers.ValidationError("Answer must contain uppercase letters, lowercase letters. Length must be between 2 and 16 characters.")
        return value

    def create(self, validated_data):
        password = validated_data.pop('password', None)
        user_count = CustomUser.objects.all().count()
        if user_count == 0:
            validated_data['is_staff'] = True
            validated_data['is_superuser'] = True

        user = self.Meta.model(**validated_data)
        if password is not None:
            user.set_password(password)
        user.save()
        return user