from rest_framework import serializers

from .models import User, Permission, Role


class PermisionSerializers(serializers.ModelSerializer):
    class Meta:
        model = Permission
        fields = '__all__'


class PermissionRelatedField(serializers.StringRelatedField):
    def to_representation(self, value):
        return PermisionSerializers(value).data

    def to_internal_value(self, data):
        return data


class RoleSerializers(serializers.ModelSerializer):
    permission = PermissionRelatedField(many=True)

    class Meta:
        model = Role
        fields = '__all__'

    def create(self, validated_data):
        permission = validated_data.pop('permission', None)
        instance = self.Meta.model(**validated_data)
        instance.save()
        instance.permission.add(*permission)
        instance.save()
        return instance


class RoleRelatedField(serializers.RelatedField):
    def to_representation(self, instance):
        return RoleSerializers(instance).data

    def to_internal_value(self, data):
        return self.queryset.get(pk=data)


class UserSerializers(serializers.ModelSerializer):
    role = RoleRelatedField(many=False, queryset=Role.objects.all())

    class Meta:
        model = User
        fields = ['id', 'first_name', 'last_name', 'email', 'password', 'role']
        extra_kwargs = {
            'password': {'write_only': True}
        }

    def create(self, validated_data):
        password = validated_data.pop('password', None)
        instance = self.Meta.model(**validated_data)
        if password is not None:
            instance.set_password(password)
        instance.save()
        return instance

    def update(self, instance, validated_data):
        password = validated_data.pop('password', None)
        last_name = validated_data.pop('last_name', None)
        first_name = validated_data.pop('first_name', None)
        role = validated_data.pop('role', None)
        if password is not None:
            instance.set_password(password)
        if last_name is not None:
            instance.last_name = last_name
        if first_name is not None:
            instance.first_name = first_name
        if role is not None:
            instance.role = role

        instance.save()
        return instance
