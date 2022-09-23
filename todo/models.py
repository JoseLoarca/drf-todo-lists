from django.db import models


class Todo(models.Model):
    id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=255, null=True, blank=True)
    is_complete = models.BooleanField(null=True, blank=True)
    parent = models.ForeignKey(
        'Todo',
        related_name='children',
        on_delete=models.SET_NULL,
        null=True,
        blank=True
    )

    class Meta:
        db_table = "todo"

    def __str__(self):
        return "{} - (Is Complete: {}) [{}]".format(self.name, self.is_complete, self.id)

    def get_children(self, direct_descendants: bool = False) -> dict:
        """
        Get all the children for a TODO list

        :param direct_descendants: If True, only the direct descendants will be returned
        """
        result = {'has_children': False, 'children': [], 'all_children_complete': True}
        stack = [self]
        while stack:
            current = stack.pop()

            for child in current.children.all():
                if not child.is_complete:
                    result['all_children_complete'] = False
                result['has_children'] = True
                result['children'].append(child)

                if not direct_descendants:
                    stack.append(child)

        return result

    def get_parents(self) -> dict:
        """
        Get all the parents for a TODO list
        """
        result = {'has_parents': False, 'parents': []}

        if self.parent:
            result['parents'].append(self.parent)
            result['has_parents'] = True
            parent_exists = True

            while parent_exists:
                current = result['parents'][-1]
                if current.parent:
                    result['parents'].append(current.parent)
                else:
                    parent_exists = False

        return result

    def update_parents(self) -> dict:
        """
        Update all its parent status(is_complete field) to be the same as the received TODO.
        """
        result = {'response': {'message': 'Todo has no parents!'}, 'status_code': 400}

        parents = self.get_parents()

        if parents['has_parents']:
            new_status = self.is_complete
            parents_ids = [parent.id for parent in parents['parents']]
            Todo.objects.filter(id__in=parents_ids).update(is_complete=new_status)

            result['response'] = {'message': 'Parents updated successfully'}
            result['status_code'] = 200

        return result

    def get_branch_status(self) -> dict:
        """
        For a branch to be complete, all the children TODO should be complete.
        """
        children = self.get_children()

        if not children['has_children']:
            return {'message': 'Todo has no children!'}

        return {'response': 'Branch is complete!' if children['all_children_complete'] else 'Branch is not complete!'}

    def mark_as_complete(self) -> None:
        """
        Mark a todo as complete, as a result all its direct descendants should be marked as completed
        """
        self.is_complete = True
        self.save()

        children = self.get_children(direct_descendants=True)
        if children['has_children']:
            children_ids = [child.id for child in children['children']]
            Todo.objects.filter(id__in=children_ids).update(is_complete=True)
