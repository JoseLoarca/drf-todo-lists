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

    def test_test_function(self):
        pass