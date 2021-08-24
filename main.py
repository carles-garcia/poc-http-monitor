import argparse
import csv
import datetime
import sys
from statistics import Statistics
from typing import Optional

from alert import Alert
from row import Row, RowCache


def print_statistics(stats: Statistics, base_date, last_date, interval: int) -> None:
    print(f"\nSection hits in the last ~{interval} seconds")
    print(f"(from {base_date} to {last_date})")
    for section, nhits in sorted(stats.section_hits.items(), key=lambda item: item[1]):
        print(f"{section} {nhits}")


def monitor(
    filename: Optional[str], threshold: int, window: int, interval: int
) -> None:
    """
    Read the log file row by row, printing statistics every interval and
    alerting if the requests/second in the window crosses the threshold.
    """
    if filename is not None:
        csv_input = open(filename, "r")
    else:
        csv_input = sys.stdin
    reader = csv.DictReader(csv_input)

    row_cache = RowCache(window)
    stats = Statistics()
    alert = Alert(threshold)

    first_row = Row(next(reader))
    row_cache.add(first_row)
    stats.update_hits(first_row)

    base_datetime = first_row.datetime
    last_datetime = base_datetime
    delta_interval = datetime.timedelta(seconds=interval)
    for csv_row in reader:
        row = Row(csv_row)
        row_cache.add(row)
        delta = row.datetime - base_datetime
        if delta > delta_interval:
            # more than 10 seconds passed since the base row and the current
            # print collected stats until now and reset
            print_statistics(stats, base_datetime, last_datetime, interval)
            stats.clear()
            base_datetime = row.datetime
        last_datetime = row.datetime

        stats.update_hits(row)
        alert.check(row_cache.requests_per_second())
        if alert.raised():
            print(
                f"\nHigh traffic generated an alert - hits = {row_cache.requests_per_second():.2f}, triggered at {row.datetime}"
            )
        elif alert.recovered():
            print(f"\nAlert recovered at {row.datetime}")

    csv_input.close()


def main() -> None:
    parser = argparse.ArgumentParser(
        prog="httpmonit", description="HTTP log monitoring utility"
    )
    parser.add_argument(
        "-i", "--input-file", nargs="?", type=str, help="log file to read"
    )
    parser.add_argument(
        "-t",
        "--threshold",
        type=int,
        nargs="?",
        default=10,
        help="requests per second threshold for the high traffic alert",
    )
    parser.add_argument(
        "-w",
        "--window",
        type=int,
        nargs="?",
        default=120,
        help="window in seconds for the high traffic alert",
    )
    parser.add_argument(
        "-s",
        "--statistics-interval",
        type=int,
        nargs="?",
        default=10,
        help="interval in seconds for printing request statistics",
    )
    args = parser.parse_args()

    monitor(args.input_file, args.threshold, args.window, args.statistics_interval)


if __name__ == "__main__":
    main()
