from django.db import models
from django.core.validators import FileExtensionValidator
from profiles.models import Profile
# Create your models here.


class Post(models.Model):
    content = models.TextField(max_length=1000)
    image = models.ImageField(upload_to="posts", validators=[FileExtensionValidator(['jpg', 'png'])], blank=True)
    liked = models.ManyToManyField(Profile, default=None, related_name="likes", blank=True)
    updated = models.DateTimeField(auto_now=True)
    created = models.DateTimeField(auto_now_add=True)
    author = models.ForeignKey(Profile, on_delete=models.CASCADE, related_name="posts")

    def __str__(self):
        return str(self.content)

    class Meta:
        ordering = ('-created', )

class Comment(models.Model):
    user = models.ForeignKey(Profile, on_delete=models.CASCADE)
    post = models.ForeignKey(Post, on_delete=models.CASCADE)
    body = models.TextField(max_length=300)
    updated = models.DateTimeField(auto_now=True)
    created = models.DateTimeField(auto_now_add=True)


    def __str__(self):
        return str(self.pk)


LIKED_CHOICES = (
    ("Like", 'Like'),
    ("Unlike", "Unlike")
)

class Like(models.Model):
    user = models.ForeignKey(Profile, on_delete=models.CASCADE)
    post = models.ForeignKey(Post, on_delete=models.CASCADE)
    value = models.CharField(max_length=8, blank=True, choices=LIKED_CHOICES)
    updated = models.DateTimeField(auto_now=True)
    created = models.DateTimeField(auto_now_add=True)


    def __str__(self):
        return f"{self.user}-{self.post}-{self.value}"

