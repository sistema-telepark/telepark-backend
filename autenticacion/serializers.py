from rest_framework import serializers


class LoginSerializer(serializers.Serializer):
    username = serializers.CharField()
    password = serializers.CharField(write_only=True)


class CreateUserSerializer(serializers.Serializer):
    user = serializers.CharField(required=True)
    email = serializers.CharField(required=True)
    first_name = serializers.CharField(required=True)
    last_name = serializers.CharField(required=True)
    password = serializers.CharField(write_only=True, required=True)

    def validate(self, attrs):
        if self.initial_data:
            for field in ('is_superuser', 'is_staff', 'is_active'):
                if field in self.initial_data:
                    raise serializers.ValidationError({field: 'No puedes modificar este campo'})
        return attrs


class UpdateUserSerializer(serializers.Serializer):
    user = serializers.CharField(required=False, help_text="Obsoleto — el username se toma de la URL")
    email = serializers.CharField(required=False)
    first_name = serializers.CharField(required=False)
    last_name = serializers.CharField(required=False)
    password = serializers.CharField(write_only=True, required=False)
    is_active = serializers.BooleanField(required=False)

    def validate(self, attrs):
        if self.initial_data:
            for field in ('is_superuser', 'is_staff'):
                if field in self.initial_data:
                    raise serializers.ValidationError({field: 'No puedes modificar este campo'})
        return attrs


class RoleChangeSerializer(serializers.Serializer):
    is_superuser = serializers.BooleanField()


class UserListOutputSerializer(serializers.Serializer):
    username = serializers.CharField()
    first_name = serializers.CharField()
    last_name = serializers.CharField()
    is_superuser = serializers.BooleanField()
    is_active = serializers.BooleanField()
