from rest_framework import serializers

from .models import Todo


class TodoSerializer(serializers.ModelSerializer):
    children = serializers.PrimaryKeyRelatedField(
        many=True,
        queryset=Todo.objects.all(),
        required=False
    )
    parent = serializers.PrimaryKeyRelatedField(
        queryset=Todo.objects.all(),
        required=False
    )

    class Meta:
        model = Todo
        fields = ['id', 'name', 'is_complete', 'children', 'parent']
