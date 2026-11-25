"""Unit tests for Module D. Run from the repo root:  python -m unittest discover -t . -s . -v"""
import unittest

from module_d_history.stack import Stack
from module_d_history.pending_queue import Queue
from module_d_history.history import Query, QueryHistory


class TestStack(unittest.TestCase):
    def test_last_in_first_out(self):
        s = Stack()
        for i in (1, 2, 3):
            s.push(i)
        self.assertEqual([s.pop(), s.pop(), s.pop()], [3, 2, 1])
        self.assertTrue(s.is_empty())

    def test_empty_errors(self):
        with self.assertRaises(IndexError):
            Stack().pop()
        with self.assertRaises(IndexError):
            Stack().peek()


class TestQueue(unittest.TestCase):
    def test_first_in_first_out(self):
        q = Queue()
        for i in range(5):
            q.enqueue(i)
        self.assertEqual([q.dequeue() for _ in range(5)], [0, 1, 2, 3, 4])

    def test_wraps_around_and_grows(self):
        q = Queue(capacity=4)
        for i in range(3):
            q.enqueue(i)
        q.dequeue()
        q.dequeue()                      # head has moved, so the ring must wrap
        for i in range(3, 20):           # forces several growths
            q.enqueue(i)
        self.assertEqual([q.dequeue() for _ in range(len(q))], list(range(2, 20)))

    def test_empty_errors(self):
        with self.assertRaises(IndexError):
            Queue().dequeue()


class TestHistory(unittest.TestCase):
    def setUp(self):
        self.calls = []

        def executor(query):
            self.calls.append(query.argument)
            return "result of " + query.argument

        self.history = QueryHistory(executor)
        self.a, self.b, self.c = Query("code", "A"), Query("code", "B"), Query("code", "C")

    def test_undo_and_redo_walk_the_history(self):
        for q in (self.a, self.b, self.c):
            self.history.run(q)
        self.assertEqual(self.history.undo()[0], self.b)
        self.assertEqual(self.history.undo()[0], self.a)
        self.assertEqual(self.history.redo()[0], self.b)
        self.assertEqual(self.history.current(), self.b)

    def test_new_query_clears_redo(self):
        self.history.run(self.a)
        self.history.run(self.b)
        self.history.undo()
        self.assertTrue(self.history.can_redo())
        self.history.run(self.c)
        self.assertFalse(self.history.can_redo())
        self.assertIsNone(self.history.redo())

    def test_undoing_the_first_query_gives_empty_screen(self):
        self.history.run(self.a)
        self.assertEqual(self.history.undo(), (None, None))
        self.assertIsNone(self.history.undo())          # nothing left to undo
        self.assertEqual(self.history.redo()[0], self.a)

    def test_batch_runs_in_arrival_order(self):
        for q in (self.a, self.b, self.c):
            self.history.add_pending(q)
        self.assertEqual(self.history.pending_count(), 3)
        done = self.history.run_pending()
        self.assertEqual([q.argument for q, _ in done], ["A", "B", "C"])
        self.assertEqual(self.history.pending_count(), 0)
        self.assertEqual(self.history.current(), self.c)   # batch queries enter the history


if __name__ == "__main__":
    unittest.main()
