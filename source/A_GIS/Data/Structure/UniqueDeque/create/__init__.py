def create(*, maxlen=None):
    """Create a deque with uniqueness constraint.
    Whenever a non-unique value is added, the existing one is deleted.
    Useful to manage a finite list of commands for example.
    """
    import collections

    class _UniqueDeque(collections.deque):
        def __init__(self, *args, maxlen=None):
            super().__init__(*args, maxlen=maxlen)

        def append(self, item):
            """Append item, ensuring uniqueness."""
            if item in self:
                self.remove(item)
            super().append(item)

        def appendleft(self, item):
            """Append item to the left, ensuring uniqueness."""
            if item in self:
                self.remove(item)
            super().appendleft(item)

        def remove(self, item):
            """Remove item from deque."""
            super().remove(item)

        def pop(self):
            """Pop from the right."""
            return super().pop()

        def popleft(self):
            """Pop from the left."""
            return super().popleft()

        def __contains__(self, item):
            return super().__contains__(item)

        def __repr__(self):
            return f"UniqueDeque({list(self)})"

    return _UniqueDeque(maxlen=maxlen)
