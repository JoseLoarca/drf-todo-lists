import json
from datetime import datetime

import factory
from django.core import management
from django.test import TestCase
from django.urls import reverse
from faker import Factory
from rest_framework import status
from rest_framework.test import APIClient

from ..models import Todo
from .factories import TodoFactory, CompleteTodoFactory, IncompleteTodoFactory

faker = Factory.create()

class InterviewTodoListFactory():
    def build(self):
        root = IncompleteTodoFactory(name="TODO List")
        todo_a = IncompleteTodoFactory(parent=root, name="TODO A")
        todo_a1 = CompleteTodoFactory(parent=todo_a, name="TODO A1")
        todo_a2 = IncompleteTodoFactory(parent=todo_a, name="TODO A2")
        todo_a2_1 = CompleteTodoFactory(parent=todo_a2, name="TODO A2.1")
        todo_a2_2 = IncompleteTodoFactory(parent=todo_a2, name="TODO A2.2")
        todo_a2_3 = CompleteTodoFactory(parent=todo_a2, name="TODO A2.3")
        todo_a3 = IncompleteTodoFactory(parent=todo_a, name="TODO A3")
        todo_a3_1 = IncompleteTodoFactory(parent=todo_a3, name="TODO A3.1")
        todo_a3_1_1 = IncompleteTodoFactory(parent=todo_a3_1, name="TODO A3.1.1")
        todo_a3_1_2 = CompleteTodoFactory(parent=todo_a3_1, name="TODO A3.1.2")
        todo_a3_1_3 = IncompleteTodoFactory(parent=todo_a3_1, name="TODO A3.1.3")
        todo_a3_2 = CompleteTodoFactory(parent=todo_a3, name="TODO A3.2")
        todo_b = CompleteTodoFactory(parent=root, name="TODO B")
        todo_b1 = CompleteTodoFactory(parent=todo_b, name="TODO B1")
        todo_b2 = CompleteTodoFactory(parent=todo_b, name="TODO B2")
        return root


class Interview_Test(TestCase):
    def setUp(self):
        self.api_client = APIClient()
        self.todo_list = InterviewTodoListFactory().build()

    def test_get_parents(self) -> None:
        """
        Ensure get parents return the correct objects.
        """
        no_parents = self.todo_list.get_parents()
        assert no_parents['has_parents'] is False
        assert no_parents['parents'] == []

        todo_b = Todo.objects.get(name="TODO B")
        todo_b_parents = todo_b.get_parents()
        assert todo_b_parents['has_parents'] is True
        assert len(todo_b_parents['parents']) == 1

    def test_get_children(self) -> None:
        """
        Ensure get children (all children) return the correct objects.
        """
        root_list = self.todo_list
        all_children = root_list.get_children()
        assert all_children['has_children'] is True
        assert len(all_children['children']) == 15

        todo_b = Todo.objects.get(name="TODO B")
        todo_b_children = todo_b.get_children()
        assert todo_b_children['has_children'] is True
        assert len(todo_b_children['children']) == 2

        todo_a1 = Todo.objects.get(name="TODO A1")
        todo_a1_children = todo_a1.get_children()
        assert todo_a1_children['has_children'] is False
        assert todo_a1_children['children'] == []

    def test_get_direct_descendants(self) -> None:
        """
        Ensure get children return just the direct descendants when specified
        """
        root_list = self.todo_list
        direct_descendants = root_list.get_children(direct_descendants=True)
        assert direct_descendants['has_children'] is True
        assert len(direct_descendants['children']) == 2

    def test_children_cascade_delete(self) -> None:
        """
        Ensure (using DELETE request) all children get deleted when a todo is removed
        """
        todo_b = Todo.objects.get(name="TODO B")
        self.api_client.delete(reverse('todo-detail', kwargs={'pk': todo_b.id}))
        assert Todo.objects.filter(name="TODO B").count() == 0
        assert Todo.objects.filter(name="TODO B1").count() == 0
        assert Todo.objects.filter(name="TODO B2").count() == 0

        root_list = self.todo_list
        self.api_client.delete(reverse('todo-detail', kwargs={'pk': root_list.id}))
        assert Todo.objects.all().count() == 0

    def test_branch_completion(self) -> None:
        """
        Ensure all direct descendants get marked as complete when using the "complete" endpoint
        """
        todo_a3 = Todo.objects.get(name="TODO A3")
        self.api_client.put(reverse('todo-complete', kwargs={'pk': todo_a3.id}))
        assert Todo.objects.filter(name="TODO A3", is_complete=1).count() == 1
        assert Todo.objects.filter(name="TODO A3.1", is_complete=1).count() == 1
        assert Todo.objects.filter(name="TODO A3.2", is_complete=1).count() == 1

        root_list = self.todo_list
        self.api_client.put(reverse('todo-complete', kwargs={'pk': root_list.id}))
        assert Todo.objects.filter(name="TODO A", is_complete=1).count() == 1
        assert Todo.objects.filter(name="TODO B", is_complete=1).count() == 1

    def test_branch_status(self) -> None:
        """
        Ensure the status of a branch is returned correctly
        """
        todo_a1 = Todo.objects.get(name="TODO A1")
        res = self.api_client.get(reverse('todo-status', kwargs={'pk': todo_a1.id}))
        assert res.status_code == 200
        assert res.data['message'] == 'Todo has no children!'

        todo_a3 = Todo.objects.get(name="TODO A3")
        res = self.api_client.get(reverse('todo-status', kwargs={'pk': todo_a3.id}))
        assert res.status_code == 200
        assert res.data['message'] == 'Branch is not complete!'

        todo_b = Todo.objects.get(name="TODO B")
        res = self.api_client.get(reverse('todo-status', kwargs={'pk': todo_b.id}))
        assert res.status_code == 200
        assert res.data['message'] == 'Branch is complete!'

    def test_parent_update(self) -> None:
        """
        Test the endpoint to update all parents status
        """
        root_list = self.todo_list
        res = self.api_client.put(reverse('todo-parents', kwargs={'pk': root_list.id}))
        assert res.status_code == 400
        assert res.data['message'] == 'Todo has no parents!'

        todo_a1 = Todo.objects.get(name="TODO A1")
        res = self.api_client.put(reverse('todo-parents', kwargs={'pk': todo_a1.id}))
        assert res.status_code == 200
        assert res.data['message'] == 'Parents updated successfully'
        todo_a = Todo.objects.get(name="TODO A")
        assert todo_a.is_complete == 1
        root_list = Todo.objects.get(name="TODO List")
        assert root_list.is_complete == 1
