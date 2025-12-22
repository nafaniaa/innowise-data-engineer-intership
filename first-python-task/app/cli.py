import argparse


def parse_args():
    parser = argparse.ArgumentParser(description="Students & Rooms Analyzer")

    parser.add_argument(
        "--students",
        required=True,
        help="Path to students.json"
    )

    parser.add_argument(
        "--rooms",
        required=True,
        help="Path to rooms.json"
    )

    parser.add_argument(
        "--format",
        choices=["json", "xml"],
        required=True,
        help="Output format"
    )

    return parser.parse_args()
