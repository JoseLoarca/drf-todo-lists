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

    def print_tree(self):
        stack = [(self, 1)]
        while stack:
            current, depth = stack.pop()
            print("*" * depth, current)
            for child in current.children.all():
                stack.append((child, depth + 1))
