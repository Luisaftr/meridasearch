# 🍓 Module D: History

| Requirement | Our answer | File |
|---|---|---|
| A stack for undo/redo of queries | ✅ `Stack` on our `DynamicArray`; `QueryHistory` keeps an undo stack and a redo stack | `stack.py`, `history.py` |
| A queue for a batch of pending queries | ✅ `Queue`, a circular queue that doubles when full; `run_pending` runs the batch oldest first | `pending_queue.py`, `history.py` |

## How undo and redo work
- `run(query)` executes the query, pushes it on the **undo stack**, and clears the **redo stack** (like a text editor: a new action ends the old "future").
- `undo()` moves the top of the undo stack onto the redo stack and shows the previous query again.
- `redo()` moves it back.
- Undoing the very first query returns an empty screen; undoing with nothing left returns `None`.

## How the batch works
`add_pending(query)` enqueues. `run_pending()` dequeues in arrival order, runs each query, and records it in the history, so batch queries can also be undone.

The history does not know how to search: it receives an `executor` function, so the full engine plugs in later without changing this module.

## Run it
From the repo root:
```
python -m module_d_history.demo
python -m unittest discover -t . -s . -v
```

## Complexity
| Operation | Time |
|---|---|
| Stack push / pop / peek | O(1) amortized |
| Queue enqueue / dequeue | O(1) amortized |
| run / undo / redo | O(1) plus the cost of the query itself |
