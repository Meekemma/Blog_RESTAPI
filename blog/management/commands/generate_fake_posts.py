from django.core.management.base import BaseCommand
from faker import Faker
from blog.models import Post, Category, Tag, Comment
from django.contrib.auth import get_user_model
import random

User = get_user_model()
fake = Faker()

class Command(BaseCommand):
    help = "Generate fake blog posts with comments"

    def handle(self, *args, **kwargs):
        # Get or create categories
        categories = ['Tech', 'Health', 'Finance', 'Lifestyle']
        category_objs = [Category.objects.get_or_create(name=cat)[0] for cat in categories]

        # Get or create tags
        tags = ['Django', 'Python', 'React', 'AI', 'Web Development']
        tag_objs = [Tag.objects.get_or_create(name=tag)[0] for tag in tags]

        # Get a random author (ensure you have users in your DB)
        authors = User.objects.all()
        if not authors.exists():
            self.stdout.write(self.style.ERROR("No users found! Create at least one user."))
            return

        # Generate 30 fake posts
        for _ in range(30):
            author = random.choice(authors)
            category = random.choice(category_objs)
            title = fake.sentence()
            content = fake.paragraph(nb_sentences=10)

            post = Post.objects.create(
                title=title,
                slug=fake.slug(title),
                content=content,
                author=author,
                category=category,
                status='published',
                is_published=True
            )

            # Assign random tags
            post.tags.set(random.sample(tag_objs, k=random.randint(1, 3)))

            # Add random comments to each post (1 to 5 comments per post)
            num_comments = random.randint(1, 5)
            for _ in range(num_comments):
                comment_author = random.choice(authors)
                Comment.objects.create(
                    post=post,
                    user=comment_author,
                    body=fake.sentence(),
                )

            self.stdout.write(self.style.SUCCESS(f"Created post: {post.title} with {num_comments} comments"))
