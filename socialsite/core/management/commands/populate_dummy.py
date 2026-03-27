from django.core.management.base import BaseCommand
from django.contrib.auth.models import User
from core.models import Post, Like, Comment
import random

class Command(BaseCommand):
    help = 'Populate dummy users, posts, likes, and comments'

    def handle(self, *args, **kwargs):
        # Step 1: Create users
        users = []
        for i in range(1, 11):
            username = f'user{i}'
            if not User.objects.filter(username=username).exists():
                user = User.objects.create_user(username=username, password='password123')
                users.append(user)
                self.stdout.write(self.style.SUCCESS(f'Created user: {username}'))
            else:
                users.append(User.objects.get(username=username))

        # Step 2: Create posts
        posts = []
        for user in users:
            for j in range(2):  # each user makes 2 posts
                content = f"This is a post by {user.username}, post {j+1}"
                post = Post.objects.create(user=user, content=content)
                posts.append(post)
                self.stdout.write(self.style.SUCCESS(f'Created post: {content}'))

        # Step 3: Add random likes
        for post in posts:
            liked_users = random.sample(users, k=random.randint(0, len(users)))
            for u in liked_users:
                Like.objects.get_or_create(user=u, post=post)
            self.stdout.write(self.style.SUCCESS(f'Post {post.id} got {len(liked_users)} likes'))

        # Step 4: Add random comments
        comments_text = [
            "Nice post!", "I agree!", "Awesome!", "Interesting!", "Well said!"
        ]
        for post in posts:
            for _ in range(random.randint(0, 3)):  # 0-3 comments per post
                user = random.choice(users)
                text = random.choice(comments_text)
                Comment.objects.create(user=user, post=post, text=text)
            self.stdout.write(self.style.SUCCESS(f'Post {post.id} comments added'))

        self.stdout.write(self.style.SUCCESS('Dummy data population completed!'))