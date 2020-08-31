from django.db import models

# Create your models here.


class UserInfo(models.Model):
    # 用户表
    nid = models.BigAutoField(primary_key=True)
    username = models.CharField(verbose_name='用户名', max_length=32, unique=True)
    password = models.CharField(verbose_name='密码', max_length=64)
    nickname = models.CharField(verbose_name='昵称', max_length=32)
    email = models.EmailField(verbose_name='邮箱', unique=True)
    avatar = models.ImageField(verbose_name='头像', upload_to='./static/img/touxiang')
    create_time = models.DateTimeField(verbose_name='创建时间', auto_now_add=True)
    fans = models.ManyToManyField(verbose_name='粉丝们',
                                  to='UserInfo',
                                  through='UserFans',
                                  related_name='f',
                                  through_fields=('user', 'follower'))

    class Meta:
        verbose_name_plural = '用户表'

    def __str__(self):
        return self.username


class Blog(models.Model):
    # 博客信息
    nid = models.BigAutoField(primary_key=True)
    title = models.CharField(verbose_name='个人博客标题', max_length=64)
    site = models.CharField(verbose_name='个人博客前缀', max_length=32, unique=True)
    theme = models.CharField(verbose_name='博客主题', max_length=32)
    user = models.OneToOneField(to='UserInfo', to_field='nid', on_delete=models.CASCADE)

    class Meta:
        verbose_name_plural = '博客信息'

    def __str__(self):
        return self.title


class UserFans(models.Model):
    # 互粉关系表
    user = models.ForeignKey(
        verbose_name='博主',
        to='UserInfo',
        to_field='nid',
        related_name='users',
        on_delete=models.CASCADE
    )
    follower = models.ForeignKey(
        verbose_name='粉丝',
        to='UserInfo',
        to_field='nid',
        related_name='followers',
        on_delete=models.CASCADE
    )

    class Meta:
        unique_together = [
            ('user', 'follower'),
        ]
        verbose_name_plural = '互粉关系表'


class Category(models.Model):
    # 博主个人文章分类表
    nid = models.AutoField(primary_key=True)
    title = models.CharField(verbose_name='分类标题', max_length=32)
    blog = models.ForeignKey(
        verbose_name='所属博客',
        to='Blog',
        to_field='nid',
        on_delete=models.CASCADE)

    class Meta:
        verbose_name_plural = '个人文章分类'

    def __str__(self):
        return self.title


class Tag(models.Model):
    # 博主个人文章标签表
    nid = models.AutoField(primary_key=True)
    title = models.CharField(verbose_name='标签名称', max_length=32)
    blog = models.ForeignKey(
        verbose_name='所属博客',
        to='Blog',
        to_field='nid',
        on_delete=models.CASCADE)

    class Meta:
        verbose_name_plural = '文章标签'

    def __str__(self):
        return self.title


class UpDown(models.Model):
    """
    文章顶或踩
    """
    article = models.ForeignKey(
        verbose_name='文章',
        to='Article',
        to_field='nid',
        on_delete=models.CASCADE)
    user = models.ForeignKey(
        verbose_name='赞或踩用户',
        to='UserInfo',
        to_field='nid',
        on_delete=models.CASCADE)
    up = models.BooleanField(verbose_name='是否赞')

    class Meta:
        unique_together = [
            ('article', 'user'),
        ]
        verbose_name_plural = '文章踩赞表'


class Comment(models.Model):
    """
    评论表
    """
    nid = models.BigAutoField(primary_key=True)
    content = models.CharField(verbose_name='评论内容', max_length=255)
    create_time = models.DateTimeField(verbose_name='创建时间', auto_now_add=True)

    reply = models.ForeignKey(
        verbose_name='回复评论',
        to='self',
        related_name='back',
        null=True,
        blank=True,
        on_delete=models.CASCADE)
    article = models.ForeignKey(
        verbose_name='评论文章',
        to='Article',
        to_field='nid',
        on_delete=models.CASCADE)
    user = models.ForeignKey(
        verbose_name='评论者',
        to='UserInfo',
        to_field='nid',
        on_delete=models.CASCADE)

    class Meta:
        verbose_name_plural = '评论表'


class ArticleDetail(models.Model):
    # 文章详细表
    content = models.TextField(verbose_name='文章详细',)
    article = models.OneToOneField(
        verbose_name='所属文章',
        to='Article',
        to_field='nid',
        on_delete=models.CASCADE)

    class Meta:
        verbose_name_plural = '文章详细'


class Article(models.Model):
    nid = models.BigAutoField(primary_key=True)
    title = models.CharField(verbose_name='文章标题', max_length=128)
    summary = models.CharField(verbose_name='文章简介', max_length=255)
    read_count = models.IntegerField(default=0)
    comment_count = models.IntegerField(default=0)
    up_count = models.IntegerField(default=0)
    down_count = models.IntegerField(default=0)
    create_time = models.DateTimeField(verbose_name='创建时间', auto_now_add=True)
    blog = models.ForeignKey(
        verbose_name='所属博客',
        to='Blog',
        to_field='nid',
        on_delete=models.CASCADE)
    category = models.ForeignKey(
        verbose_name='文章类型',
        to='Category',
        to_field='nid',
        null=True,
        on_delete=models.CASCADE)

    type_choices = [
        (1, "Python"),
        (2, "Linux"),
        (3, "OpenStack"),
        (4, "GoLang"),
    ]
    article_type_id = models.IntegerField(choices=type_choices, default=None)
    tags = models.ManyToManyField(
        to="Tag",
        through="Article2Tag",
        through_fields=('article', 'tag'),
    )

    class Meta:
        verbose_name_plural = '文章表'

    def __str__(self):
        return self.title


class Article2Tag(models.Model):
    # 文章标签关系表
    article = models.ForeignKey(
        verbose_name='文章',
        to="Article",
        to_field='nid',
        on_delete=models.CASCADE)
    tag = models.ForeignKey(
        verbose_name='标签',
        to="Tag",
        to_field='nid',
        on_delete=models.CASCADE)

    class Meta:
        unique_together = [
            ('article', 'tag'),
        ]
        verbose_name_plural = '文章标签关系'


class Trouble(models.Model):
    title = models.CharField(max_length=32)
    detail = models.TextField()
    user = models.ForeignKey(
        UserInfo,
        related_name='u',
        on_delete=models.CASCADE)  # 报障者
    ctime = models.DateTimeField()  # 提交时间
    status_choice = (
        (1, '未处理'),
        (2, '处理中'),
        (3, '已处理'),
    )
    status = models.IntegerField(choices=status_choice, default=1)
    processer = models.ForeignKey(
        UserInfo,
        related_name='p',
        on_delete=models.CASCADE,
        null=True,
        blank=True)  # 处理者
    solution = models.TextField(null=True)
    ptime = models.DateTimeField(null=True, blank=True)  # 处理时间
    pj_choices = (
        (1, '不满意'),
        (2, '一般'),
        (3, '活很好'),
    )  # 评价
    pj = models.IntegerField(choices=pj_choices, null=True, default=2)
