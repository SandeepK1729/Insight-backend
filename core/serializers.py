from rest_framework     import serializers

from .models            import Dataset, ModelFile

class DatasetSerializer(serializers.ModelSerializer):
    """
        Dataset Model Objects Serializer, able to convert obj to dict
    """
    class Meta:
        model = Dataset
        fields = "__all__"

class ModelFileSerializer(serializers.ModelSerializer):
    """ 
        ModelFile Object Serializer, ablt to convert model obj into dictionaryw
    """
    class Meta:
        model = ModelFile 
        fields = "__all__"