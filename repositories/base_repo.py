class BaseRepository:
    def __init__(self):
        self._items = []
        self._next_id = 1

    def _generate_id(self) -> int:
        new_id = self._next_id
        self._next_id += 1
        return new_id

    def list_all(self):
        return self._items

    def get_by_id(self, item_id: int):
        for item in self._items:
            if item.id == item_id:
                return item
        return None

    def add(self, item):
        if item.id == 0:
            item.id = self._generate_id()
        self._items.append(item)
        return item
