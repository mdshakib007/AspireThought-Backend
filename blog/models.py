from django.db import models
from django.template.defaultfilters import slugify
from users.models import CustomUser
from tag.models import Tag


class Blog(models.Model):
    author = models.ForeignKey(CustomUser, on_delete=models.CASCADE, related_name="blogs")
    title = models.CharField(max_length=250)
    image = models.ImageField(upload_to="blog_pics/", null=True, blank=True)
    body = models.TextField()
    slug = models.SlugField(max_length=300, unique=True, blank=True, primary_key=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    tags = models.ManyToManyField(Tag, related_name="blogs", blank=True)

    def save(self, *args, **kwargs):
        if not self.slug:
            base_slug = slugify(self.title)
            unique_slug = base_slug
            counter = 1
            while Blog.objects.filter(slug=unique_slug).exists():
                unique_slug = f"{base_slug}-{counter}"
                counter += 1
            self.slug = unique_slug
        super().save(*args, **kwargs)

    def like_count(self):
        return self.likes.count()

    def __str__(self):
        return self.title


class Like(models.Model):
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE, related_name="likes")
    blog = models.ForeignKey(Blog, on_delete=models.CASCADE, related_name="likes")
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ('user', 'blog')

    def __str__(self):
        return f"{self.user.username} likes {self.blog.title}"
