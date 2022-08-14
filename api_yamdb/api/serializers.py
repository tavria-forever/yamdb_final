import uuid

from rest_framework import serializers
from reviews.models import Category, Comment, Genre, Review, Title
from users.models import User


class SignUpSerializer(serializers.Serializer):
    email = serializers.EmailField(max_length=254, required=True)
    username = serializers.CharField(max_length=150, required=True)

    def save(self):
        if not User.objects.filter(**self.validated_data).exists():
            is_username_exist = User.objects.filter(
                username=self.validated_data['username']
            ).exists()
            is_email_exist = User.objects.filter(
                email=self.validated_data['email']
            ).exists()
            if is_username_exist or is_email_exist:
                error_field = 'username' if is_username_exist else 'email'
                raise serializers.ValidationError(
                    f'Пользователь с таким {error_field} уже существует.'
                )

        user = User.objects.create_user(**self.validated_data)
        user.confirmation_code = str(uuid.uuid4())
        user.save()
        message = f'Confirmation code: {user.confirmation_code}'
        user.email_user(
            from_email='admin@api_yamdb.com',
            subject='Confirmation code',
            message=message,
        )

    def validate_username(self, value):
        if value == 'me':
            raise serializers.ValidationError(
                'Использовать имя "me" в качестве username запрещено.'
            )
        return value


class TokenSerializer(serializers.Serializer):
    username = serializers.CharField(max_length=150, required=True)
    confirmation_code = serializers.CharField(required=True)


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = (
            'username',
            'email',
            'first_name',
            'last_name',
            'bio',
            'role',
        )


class MeSerializer(serializers.ModelSerializer):
    role = serializers.CharField(read_only=True)

    class Meta:
        model = User
        fields = (
            'username',
            'email',
            'first_name',
            'last_name',
            'bio',
            'role',
        )


class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = ('name', 'slug')


class GenreSerializer(serializers.ModelSerializer):
    class Meta:
        model = Genre
        fields = ('name', 'slug')


class TitleSerializer(serializers.ModelSerializer):
    category = serializers.SlugRelatedField(
        slug_field='slug',
        queryset=Category.objects.all(),
    )
    genre = serializers.SlugRelatedField(
        slug_field='slug',
        queryset=Genre.objects.all(),
        many=True,
    )
    rating = serializers.IntegerField(read_only=True)

    class Meta:
        model = Title
        fields = (
            'id',
            'name',
            'year',
            'category',
            'genre',
            'description',
            'rating',
        )

    def to_representation(self, instance):
        data = super().to_representation(instance)

        category = Category.objects.get(slug=data['category'])
        data['category'] = CategorySerializer(category).data

        genres = []
        for genre_slug in data['genre']:
            genre_obj = Genre.objects.get(slug=genre_slug)
            genre_data = GenreSerializer(genre_obj).data
            genres.append(genre_data)
        data['genre'] = genres
        return data


class ReviewSerializer(serializers.ModelSerializer):
    author = serializers.SlugRelatedField(
        read_only=True, slug_field='username'
    )
    title = serializers.PrimaryKeyRelatedField(read_only=True)

    class Meta:
        model = Review
        fields = '__all__'

    def to_representation(self, instance):
        data = super().to_representation(instance)
        del data['title']
        return data

    def validate(self, attrs):
        if self.context['request'].method == 'POST':
            title_id = self.context['view'].kwargs['title_id']
            username = self.context['request'].user
            if Review.objects.filter(title=title_id, author=username).exists():
                raise serializers.ValidationError(
                    {
                        'error': f'Пользователь {username} уже добавил свой '
                        f'отзыв к этому произведению.'
                    }
                )
        return attrs


class CommentSerializer(serializers.ModelSerializer):
    author = serializers.SlugRelatedField(
        read_only=True, slug_field='username'
    )
    review = serializers.PrimaryKeyRelatedField(read_only=True)

    class Meta:
        fields = '__all__'
        model = Comment

    def to_representation(self, instance):
        data = super().to_representation(instance)
        del data['review']
        return data
