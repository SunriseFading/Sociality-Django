from django.contrib.auth import get_user_model
from django.db import models

User = get_user_model()


class Group(models.Model):
    title = models.CharField(
        max_length=200,
        verbose_name='Group name',
    )
    slug = models.SlugField(
        unique=True,
        max_length=20,
        verbose_name='Group URL part',
    )
    description = models.TextField(
        verbose_name='Group description',
        help_text='Write what this group is about, what posts will be in it',
    )
    active = models.BooleanField(
        default=True,
        verbose_name='Group visibility on the site',
    )

    class Meta:
        ordering = ('title',)
        verbose_name = 'Group'
        verbose_name_plural = 'Groups'

    def __str__(self):
        return self.title


class Post(models.Model):
    title = models.CharField(
        max_length=200,
        verbose_name='Post title',
        help_text='Name the post',
        null=False,
    )
    text = models.TextField(
        verbose_name='The text of your post',
    )
    pub_date = models.DateTimeField(
        verbose_name='Date of publication',
        auto_now_add=True,
    )
    author = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        verbose_name='Post author',
        null=False,
        related_name='posts',
    )
    group = models.ForeignKey(
        Group,
        blank=True,
        null=True,
        on_delete=models.SET_NULL,
        related_name='posts',
        verbose_name='Group to post',
        help_text='Select a group or leave blank',
    )
    image = models.ImageField(
        upload_to='posts/',
        blank=True,
        null=True,
        verbose_name='Image for post',
        help_text='Image files only',
    )
    active = models.BooleanField(default=True)

    class Meta:
        ordering = ('-pub_date',)
        verbose_name = 'Post'
        verbose_name_plural = 'Posts'

    def __str__(self):
        post_title = self.title
        post_pub_date = self.pub_date
        return f'Posy "{post_title}" from {post_pub_date:%d.%m.%Y}.'

    def default_title(self):
        words = self.text.split()
        return ' '.join(words[:4]) + '...'

    def save(self, *args, **kwargs):
        if not self.title:
            self.title = self.default_title()
        super(Post, self).save(*args, **kwargs)


class Comment(models.Model):
    post = models.ForeignKey(
        Post,
        blank=False,
        null=False,
        on_delete=models.CASCADE,
        related_name='comments',
        verbose_name='Post with comment',
    )
    author = models.ForeignKey(
        User,
        blank=False,
        null=False,
        on_delete=models.CASCADE,
        related_name='comments',
        verbose_name='Comment author',
    )
    text = models.TextField(
        verbose_name='Comment text',
    )
    created = models.DateTimeField(
        verbose_name='Date of publication',
        auto_now_add=True,
    )
    active = models.BooleanField(default=True)

    class Meta:
        ordering = ('-created',)
        verbose_name = 'Comment'
        verbose_name_plural = 'Comments'

    def __str__(self):
        comment_text = self.text[:20]
        comment_pub_date = self.created
        return f'Comment {comment_text}... from {comment_pub_date:%d.%m.%Y}.'


class Follow(models.Model):
    user = models.ForeignKey(
        User,
        verbose_name='Follower',
        related_name='follower',
        on_delete=models.CASCADE,
    )
    author = models.ForeignKey(
        User,
        verbose_name='Following',
        related_name='following',
        on_delete=models.CASCADE,
    )

    class Meta:
        verbose_name = 'Subscription'
        verbose_name_plural = 'Subscriptions'
        constraints = [
            models.UniqueConstraint(fields=['user', 'author'],
                                    name='twice_follow_impossible')]
