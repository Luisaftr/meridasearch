"""Module D, part 3: query history with undo/redo, and a batch of pending queries.

UNDO / REDO   Two stacks. `undo_stack` holds every query we ran (the top is the
              current one). Undo moves the top onto `redo_stack`; redo moves it
              back. Running a brand-new query clears the redo stack, exactly like
              a text editor.

BATCH         A queue of pending queries. `run_pending` takes them out in the order
              they arrived, runs each one and records it in the history.

The history does not know HOW to search. We give it an `executor`, a function
that receives a Query and returns its result, so any engine can plug in.
"""

from .stack import Stack
from .pending_queue import Queue


class Query:
    """A search request, for example Query('code', '97000')."""

    __slots__ = ("kind", "argument")

    def __init__(self, kind, argument):
        self.kind = kind            # 'code', 'range' or 'prefix'
        self.argument = argument

    def __repr__(self):
        return f"{self.kind}: {self.argument}"


class QueryHistory:
    def __init__(self, executor):
        self._executor = executor
        self._undo_stack = Stack()   # queries already run, current one on top
        self._redo_stack = Stack()   # queries we stepped back from
        self._pending = Queue()

    # ----- single queries -----
    def run(self, query):
        result = self._executor(query)
        self._undo_stack.push(query)
        self._redo_stack.clear()     # a new query ends the old "future"
        return result

    def current(self):
        return None if self._undo_stack.is_empty() else self._undo_stack.peek()

    def can_undo(self):
        return len(self._undo_stack) > 0

    def can_redo(self):
        return len(self._redo_stack) > 0

    def undo(self):
        """Step back. Returns (query now current, its result), or None if nothing to undo."""
        if not self.can_undo():
            return None
        self._redo_stack.push(self._undo_stack.pop())
        return self._replay_current()

    def redo(self):
        """Step forward again. Returns (query, result), or None if nothing to redo."""
        if not self.can_redo():
            return None
        self._undo_stack.push(self._redo_stack.pop())
        return self._replay_current()

    def _replay_current(self):
        query = self.current()
        if query is None:
            return (None, None)      # we undid the very first query: empty screen
        return (query, self._executor(query))

    # ----- batch of pending queries -----
    def add_pending(self, query):
        self._pending.enqueue(query)

    def pending_count(self):
        return len(self._pending)

    def run_pending(self):
        """Run every pending query, oldest first. Returns a list of (query, result)."""
        done = []
        while not self._pending.is_empty():
            query = self._pending.dequeue()
            done.append((query, self.run(query)))
        return done
