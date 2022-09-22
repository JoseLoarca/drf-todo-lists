from datetime import datetime

import factory
from django.test import TestCase
from django.urls import reverse
from rest_framework import serializers
from rest_framework.test import APIRequestFactory

from todo.serializers import TodoSerializer

from .factories import TodoFactory, TodoWithForeignFactory


class TodoSerializer_Test(TestCase):
    def setUp(self):
        self.factory = APIRequestFactory()
        self.todo = TodoWithForeignFactory.create()

    def test_that_a_todo_is_correctly_serialized(self):
        todo = self.todo
        serializer = TodoSerializer
        serialized_todo = serializer(todo).data

        assert serialized_todo['id'] == todo.id
        assert serialized_todo['name'] == todo.name
        assert serialized_todo['is_complete'] == todo.is_complete

        assert len(serialized_todo['children']) == todo.children.count()
