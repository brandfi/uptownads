from rest_framework import serializers
from ads.models import Impression


class ImpressionSerializer(serializers.ModelSerializer):
    ad = serializers.StringRelatedField()

    class Meta:
        model = Impression
        fields = '__all__'
