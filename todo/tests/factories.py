from random import randint, uniform

import factory
from factory import LazyAttribute, LazyFunction, SubFactory, fuzzy
from factory.django import DjangoModelFactory
from faker import Factory

from todo.models import Todo

faker = Factory.create()


class TodoFactory(DjangoModelFactory):
    class Meta:
        model = Todo

    name = LazyAttribute(lambda o: faker.text(max_nb_chars=255))
    is_complete = LazyFunction(faker.boolean)

class CompleteTodoFactory(DjangoModelFactory):
    class Meta:
        model = Todo

    name = LazyAttribute(lambda o: faker.text(max_nb_chars=255))
    is_complete = True

class IncompleteTodoFactory(DjangoModelFactory):
    class Meta:
        model = Todo

    name = LazyAttribute(lambda o: faker.text(max_nb_chars=255))
    is_complete = False


class TodoWithForeignFactory(TodoFactory):
    @factory.post_generation
    def children(obj, create, extracted, **kwargs):
        if not create:
            return
        if extracted:
            for n in range(extracted):
                TodoFactory(parent=obj)
        else:
            number_of_units = randint(1, 10)
            for n in range(number_of_units):
                TodoFactory(parent=obj)
