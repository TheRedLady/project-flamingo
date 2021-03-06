from rest_framework.serializers import (
    ModelSerializer,
    HyperlinkedIdentityField,
    SerializerMethodField,
    ValidationError,
)


from profiles.models import MyUser, Profile


class MyUserCreateSerializer(ModelSerializer):
    class Meta:
        model = MyUser
        fields = [
            'email',
            'password',
            'first_name',
            'last_name',
        ]
        extra_kwargs = {'password': {'write_only': True}}

    def create(self, validated_data):
        new_user = MyUser.objects.create_user(
            email = validated_data['email'],
            first_name = validated_data['first_name'],
            last_name = validated_data['last_name'],
        )
        new_user.set_password(validated_data['password'])
        new_user.save()
        return new_user


class MyUserDetailSerializer(ModelSerializer):
    class Meta:
        model = MyUser
        fields = [
            'id',
            'email',
            'first_name',
            'last_name',
        ]


class MyUserUpdateSerializer(ModelSerializer):
    class Meta:
        model = MyUser
        fields = [
            'id',
            'email',
            'first_name',
            'last_name',
        ]
        extra_kwargs = {'id': {'read_only': True}, 'email': {'read_only': True}}


class FollowSerializer(ModelSerializer):

    url = HyperlinkedIdentityField(view_name = 'profile-detail')

    class Meta:
        model = Profile
        fields = ['url', 'user_id']


class ProfileCreateSerializer(ModelSerializer):

    user = MyUserCreateSerializer()

    class Meta:
        model = Profile
        fields = [
            'user',
            'birthdate',
            'follows',
        ]

    def create(self, validated_data):
        new_user = MyUserCreateSerializer().create(validated_data.pop('user'))
        new_profile = Profile.objects.get(user_id=new_user.id)
        new_profile.birthdate = validated_data['birthdate']
        new_profile.follows = validated_data['follows']
        new_profile.save()
        return new_profile


class ProfileDetailSerializer(ModelSerializer):

    user = MyUserDetailSerializer(read_only=True)
    follows = FollowSerializer(read_only=True, many=True)
    url = HyperlinkedIdentityField(view_name='profile-detail')

    class Meta:
        model = Profile
        fields = [
            'url',
            'user',
            'birthdate',
            'follows',
        ]
        extra_kwargs = {'birthdate': {'read_only': True}}


class ProfileUpdateSerializer(ModelSerializer):

    user = MyUserUpdateSerializer()

    class Meta:
        model = Profile
        fields = [
            'user',
            'birthdate',
            'follows',
        ]

    def update(self, instance, validated_data):
        MyUserUpdateSerializer().update(instance.user, validated_data.pop('user'))
        instance.birthdate = validated_data.get('birthdate', instance.birthdate)
        if instance in validated_data['follows']:
            raise ValidationError("User cannot follow self.")
        for profile in validated_data['follows']:
            instance.follows.add(profile)
        instance.save()
        return instance


class PostedBySerializer(ModelSerializer):

    url = SerializerMethodField()
    full_name = SerializerMethodField()

    class Meta:
        model = MyUser
        fields = [
            'id',
            'url',
            'email',
            'full_name',
        ]

    def get_full_name(self, obj):
        return obj.get_full_name()

    def get_url(self, obj):
        return obj.get_absolute_url()
