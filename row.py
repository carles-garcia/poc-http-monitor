import datetime
from typing import Any, List


class Row:
    """
    Row representation built from a csv row
    """

    def __init__(self, csv_row) -> None:
        self.host: str = csv_row["remotehost"]
        self.rfc931: str = csv_row["rfc931"]
        self.authuser: str = csv_row["authuser"]
        self.date: str = csv_row["date"]
        self.request: str = csv_row["request"]
        self.status: str = csv_row["status"]
        self.bytes: str = csv_row["bytes"]

    @property
    def section(self) -> str:
        """
        Get the section in a row request.
        Example request:
            GET /api/user HTTP/1.0
        The section is /api
        """
        path = self.request.split(" ")[1]
        section = "/" + path.split("/")[1]
        return section

    @property
    def datetime(self) -> Any:
        return datetime.datetime.fromtimestamp(float(self.date))


class RowCache:
    """
    Cache that stores rows for a given window.
    Assumes rows are added chronologically.
    """

    def __init__(self, window_in_secs: int) -> None:
        self.window: int = window_in_secs
        self.rows: List[Row] = []
        self._window_delta: Any = datetime.timedelta(seconds=self.window)

    def add(self, new_row: Row) -> None:
        """
        Add a row to the cache.
        Remove the oldest rows so the window is respected.
        """
        self.rows.append(new_row)
        self._prune_cache()

    def requests_per_second(self) -> float:
        hits = len(self.rows)
        requests_per_second = hits / self.window
        return requests_per_second

    def _prune_cache(self) -> None:
        """
        Remove the oldest rows that don't fit in the window.
        """
        if self.rows:
            delta_between_first_and_last_row = (
                self.rows[-1].datetime - self.rows[0].datetime
            )
            if delta_between_first_and_last_row > self._window_delta:
                oldest_row_index_inside_window = 0
                for i, row in enumerate(self.rows):
                    if self.rows[-1].datetime - row.datetime <= self._window_delta:
                        oldest_row_index_inside_window = i
                        break
                self.rows = self.rows[oldest_row_index_inside_window:]
