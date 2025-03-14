from django.dispatch import receiver
from django.db.models.signals import post_save
from django.contrib.auth import get_user_model
from django.contrib.auth.models import Group
from .models import UserProfile

User = get_user_model()

@receiver(post_save, sender=User)
def create_user_profile(sender, instance, created, *args, **kwargs):
    """
    Signal to create a UserProfile and assign default groups when a new user is created.
    """
    if created:
        # Get or create the 'Reader' and 'Blog Manager' groups
        reader_group, _ = Group.objects.get_or_create(name='Reader')
        blog_manager_group, _ = Group.objects.get_or_create(name='Blog Manager')

        # Assign groups based on user role
        instance.groups.add(reader_group)  # All users are Readers by default

        if instance.is_staff:  # Staff users should be in 'Blog Manager'
            instance.groups.add(blog_manager_group)

        # Create a UserProfile for the new user
        UserProfile.objects.create(
            user=instance,
            first_name=instance.first_name,
            last_name=instance.last_name,
            email=instance.email
        )