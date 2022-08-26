import django_tables2 as tables
from .models import todo

class TodaysTodoTable(tables.Table):
    class Meta:
        model = todo
        exclude = ("id", "person_fk")



