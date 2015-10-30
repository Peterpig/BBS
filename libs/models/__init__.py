#coding: utf-8
from django.db.models.query import QuerySet
from django.db.models.manager import Manager

def first(self):
    """
    Returns the first object of a query, returns None if no match is found.
    """
    qs = self if self.ordered else self.order_by('pk')
    try:
        return qs[0]
    except IndexError:
        return None

def last(self):
    """
    Returns the last object of a query, returns None if no match is found.
    """
    qs = self.reverse() if self.ordered else self.order_by('-pk')
    try:
        return qs[0]
    except IndexError:
        return None

def seek(self, *args, **kwargs):
    """
    Safely get. Performs the query and returns a single object matching the given
    keyword arguments.
    """
    clone = self.filter(*args, **kwargs)
    if self.query.can_filter():
        clone = clone.order_by()
    num = len(clone)
    if num > 0:
        return clone._result_cache[0]

def m_seek(self, *args, **kwargs):
    return self.get_query_set().seek(*args, **kwargs)

QuerySet.first = first
QuerySet.last = last
QuerySet.seek = seek

Manager.seek = m_seek
