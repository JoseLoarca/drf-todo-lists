from rest_framework import viewsets
from rest_framework.decorators import action
from rest_framework.response import Response

from .models import Todo
from .serializers import TodoSerializer


class TodoViewSet(viewsets.ModelViewSet):
    queryset = Todo.objects.all()
    serializer_class = TodoSerializer
    permission_classes = []
    filterset_fields = ['id', 'name', 'is_complete', 'parent', 'children']

    @action(detail=True, methods=['put'])
    def parents(self, request, pk=None):
        """ Update all its parent status(is_complete field) to be the same as the received TODO. """
        todo = self.get_object()
        update_parents = todo.update_parents()

        return Response(update_parents['response'], status=update_parents['status_code'])

    @action(detail=True, methods=['get'])
    def status(self, request, pk=None):
        """ Get the status of a branch """
        todo = self.get_object()
        branch_status = todo.get_branch_status()

        return Response(branch_status)

    @action(detail=True, methods=['put'])
    def complete(self, request, pk=None):
        """ Complete a TODO """
        todo = self.get_object()
        todo.mark_as_complete()

        return Response({'message': 'Todo completed successfully!'})
