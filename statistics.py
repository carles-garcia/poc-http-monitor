from typing import Dict

from row import Row


class Statistics:
    """
    Store log statistics
    """

    def __init__(self) -> None:
        self.section_hits: Dict[str, int] = {}

    def update_hits(self, row: Row) -> None:
        if row.section in self.section_hits:
            self.section_hits[row.section] += 1
        else:
            self.section_hits[row.section] = 1

    def clear(self) -> None:
        self.section_hits.clear()
