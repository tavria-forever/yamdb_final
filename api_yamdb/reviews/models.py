from django.core.validators import MaxValueValidator, MinValueValidator
from django.db import models
from users.models import User


class Category(models.Model):
    name = models.CharField(max_length=256)
    slug = models.SlugField(max_length=50, unique=True)

    class Meta:
        verbose_name_plural = 'categories'

    def __str__(self):
        return (
            f'Category(id={self.id}, name={self.name[:15]}, slug'
            f'={self.slug})'
        )


class Genre(models.Model):
    name = models.TextField()
    slug = models.SlugField(max_length=50, unique=True)

    def __str__(self):
        return (
            f'Genre(id={self.id}, name={self.name[:15]}, slug' f'={self.slug})'
        )


class Title(models.Model):
    name = models.TextField()
    year = models.PositiveSmallIntegerField()
    category = models.ForeignKey(
        Category, on_delete=models.SET_NULL, related_name='title', null=True
    )
    genre = models.ManyToManyField(Genre)
    description = models.TextField(blank=True)

    def __str__(self):
        return (
            f'Title(id={self.id}, name={self.name[:15]}, category'
            f'={self.category}, genre={self.genre}, description='
            f'{self.description[:15]})'
        )


class Review(models.Model):
    text = models.TextField()
    score = models.IntegerField(
        validators=[MinValueValidator(1), MaxValueValidator(10)]
    )
    pub_date = models.DateTimeField(auto_now_add=True)
    author = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name='reviews'
    )
    title = models.ForeignKey(
        Title, on_delete=models.CASCADE, related_name='reviews'
    )

    class Meta:
        ordering = ('-pub_date',)
        constraints = [
            models.UniqueConstraint(
                fields=['author', 'title'], name='unique_review'
            )
        ]

    def __str__(self):
        return (
            f'Review(id={self.id}, text={self.text[:15]}, score'
            f'={self.score}, author={self.author}, title={self.title})'
        )


class Comment(models.Model):
    author = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name='comments'
    )
    review = models.ForeignKey(
        Review, on_delete=models.CASCADE, related_name='comments'
    )
    text = models.TextField()
    pub_date = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return (
            f'Comment(id={self.id}, text={self.text[:15]}, pub_date'
            f'={self.pub_date}, author={self.author}, review={self.review})'
        )
