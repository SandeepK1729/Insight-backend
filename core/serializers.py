from rest_framework     import serializers
from .models            import ModelFile, User


class ModelFileSerializer(serializers.ModelSerializer):
    """ 
        ModelFile Object Serializer, ablt to convert model obj into dictionaryw
    """
    created_by_user = serializers.SerializerMethodField()

    class Meta:
        model = ModelFile 
        fields = [
            'project_name',
            'model_name',
            'is_public',
            'model_obj',
            'created_on',
            'last_trained_on',
            'created_by_user'
        ]

    def get_created_by_user(self, obj):
        return obj.created_by.username
    
class UserSerializer(serializers.ModelSerializer):
    """User Model Serilizer"""
    class Meta:
        model = User
        fields = "__all__"


    def create_user(self, data):
        user = User.objects.create_user(
            username    = data.get("username"),
            password    = data.get("password"),
            email       = data.get("email"),
            first_name  = data.get("first_name"),
            last_name   = data.get("last_name"), 
            is_active   = True,
            is_staff    = False,
            mobile_number = data.get("mobile_number"),
            dob = data.get("dob"),
        )

        return user