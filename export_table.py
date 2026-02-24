from typing import Any
import csv
import os

from fetch_courses import fetch_course_data


def build_table_rows(data: dict[str, Any]) -> list[list[str]]:
    available = data.get("available_courses") or []
    rows: list[list[str]] = []
    rows.append(["Code", "Course Name", "GE Field", "Lecturer", "Credit", "Time & Venue", "Quota", "Apply"])

    for c in available:
        rows.append([
            str(c.get("code", "")),
            str(c.get("name", "")),
            str(c.get("field", "")),
            str(c.get("lecturer", "")),
            str(c.get("credit", "")),
            str(c.get("time_venue", "")),
            str(c.get("quota", "")),
            str(c.get("applicant", "")),
        ])

    return rows


def save_csv_file(rows: list[list[str]], filename: str = "courses_table.csv") -> str:
    output_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), filename)
    with open(output_path, "w", encoding="utf-8", newline="") as f:
        writer = csv.writer(f)
        writer.writerows(rows)
    return output_path


def main() -> None:
    data = fetch_course_data()
    rows = build_table_rows(data)
    output_path = save_csv_file(rows)
    print(f"CSV 表格已生成：{output_path}")


if __name__ == "__main__":
    main()
