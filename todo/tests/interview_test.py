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
