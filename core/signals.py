from django.db.models.signals   import post_save, post_delete
from django.dispatch            import receiver
from django.core.cache          import cache

from .models import Dataset, ModelFile
from .serializers import DatasetSerializer

@receiver(post_save, sender=Dataset)
@receiver(post_delete, sender=Dataset)
def datasets_update(sender, instance, **kwargs):
    """informs the backend that the dataset list has changed

    Args:
        sender (Model): name of the model that triggered the signal
        instance (Model obj): instance of the model that triggered the signal
    """

    instance.path.delete(save=False)
    cache.delete('datasets')
    cache.set('datasets', DatasetSerializer(Dataset.objects.all(), many=True).data, 60*60*2)


@receiver(post_save, sender=ModelFile)
@receiver(post_delete, sender=ModelFile)
def model_files_update(sender, instance, **kwargs):
    """informs the backend that the dataset list has changed

    Args:
        sender (Model): name of the model that triggered the signal
        instance (Model obj): instance of the model that triggered the signal
    """

    instance.model_obj.delete(save=False)
    cache.delete('model_files')
    cache.set('model_files', ModelFile.objects.all(), 60*60*2)
