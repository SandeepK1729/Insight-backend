from django.db.models.signals   import post_save, post_delete
from django.dispatch            import receiver
from django.core.cache          import cache

@receiver(post_save)
def instance_created_or_updated(sender, **kwargs):
    cache.clear()