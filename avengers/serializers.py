from django.utils.translation import ugettext_lazy as _
from django.db import transaction
from rest_framework import serializers

from avengers.models import Hero


class SignUpSerializer(serializers.ModelSerializer):

    class Meta:
        model = Hero
        fields = ('real_name', 'alias', 'super_powers', 'mobile', 'physical_id_marks', 'blood_type', 'email')

    def validate(self, data):
        heroes = Hero.objects.all()
        if heroes.filter(name=data["alias"], mode__in=['D', 'T']).exists():
            raise serializers.ValidationError({'message': _('Sorry, the alias which you have given exists already!')})
        return data

    @transaction.atomic()
    def create(self, validated_data):
        user = Hero.objects.create(
            email=validated_data['email'],
            real_name=validated_data['real_name'],
            alias=validated_data['alias'],
            super_powers=validated_data['super_powers'],
            mobile=validated_data['mobile'],
            physical_id_marks=validated_data['physical_id_marks'],
            blood_type=validated_data['blood_type'],
        )

        user.save()
        return user


class LoginSerializer(serializers.Serializer):
    username = serializers.EmailField(label=_('Username'), allow_blank=False)
    password = serializers.CharField(
        label=_('Password'),
        style={'input_type': 'password'},
        trim_whitespace=False
    )

    def validate(self, data):
        role = self.context.get('role', None)
        username = data.get('username')
        password = data.get('password')

        if username and password:
            user = authenticate(username=username, password=password)

            if not user:
                raise serializers.ValidationError({'password': [_('Unable to login with provided credentials.')]}, code='authorization')
            else:
                if user.mode == "D":
                    raise serializers.ValidationError({
                        'user': [_('You are not authorized by admin. Contact admin to revoke access')]},
                        code='authorization')

            if role == 'admin':
                if not user.is_superuser:
                    raise serializers.ValidationError({'authorization': [_('You are not authorized admin.')]}, code='authorization')

            user.last_login = now()
            user.save()

        else:
            raise serializers.ValidationError(_('Must include "username" and "password".'), code='authorization')

        return user