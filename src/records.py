#Module A, part 1: our own linear structure + catalog loader.


class DynamicArray:
    """A growable array built on a fixed block of slots."""

    def __init__(self):
        self._capacity = 8
        self._size = 0
        self._slots = [None] * self._capacity

    def __len__(self):
        return self._size

    def __getitem__(self, index):
        if index < 0 or index >= self._size:
            raise IndexError("DynamicArray index out of range")
        return self._slots[index]

    def __setitem__(self, index, value):
        if index < 0 or index >= self._size:
            raise IndexError("DynamicArray index out of range")
        self._slots[index] = value

    def __iter__(self):
        for i in range(self._size):
            yield self._slots[i]

    def append(self, item):
        if self._size == self._capacity:
            self._grow()
        self._slots[self._size] = item
        self._size += 1

    def pop(self):
        """Remove and return the last item (handy as a mini stack)."""
        if self._size == 0:
            raise IndexError("pop from empty DynamicArray")
        self._size -= 1
        item = self._slots[self._size]
        self._slots[self._size] = None
        return item

    def _grow(self):
        # Doubling gives O(1) amortized appends.
        self._capacity *= 2
        bigger = [None] * self._capacity
        for i in range(self._size):
            bigger[i] = self._slots[i]
        self._slots = bigger


class Record:
    """One neighborhood row of the Correos de Mexico catalog."""

    __slots__ = ("postal_code", "neighborhood", "kind",
                 "municipality", "state", "city", "zone")

    def __init__(self, postal_code, neighborhood, kind,
                 municipality, state, city, zone):
        self.postal_code = postal_code      # kept as text: '01000' keeps its zero
        self.neighborhood = neighborhood
        self.kind = kind
        self.municipality = municipality
        self.state = state
        self.city = city
        self.zone = zone

    def __repr__(self):
        return (f"Record({self.postal_code}, {self.neighborhood}, "
                f"{self.municipality}, {self.state})")


def load_catalog(path, limit=None):
    """Read CPdescarga.txt (pipe-separated, Latin-1) into a DynamicArray.

    The first line is a legal notice and the second is the header, so we skip both.
    """
    records = DynamicArray()
    with open(path, encoding="latin-1") as handle:
        handle.readline()   # legal notice
        handle.readline()   # column names
        for line in handle:
            parts = line.rstrip("\r\n").split("|")
            if len(parts) < 15:
                continue
            records.append(Record(parts[0], parts[1], parts[2], parts[3],
                                  parts[4], parts[5], parts[13]))
            if limit is not None and len(records) >= limit:
                break
    return records
