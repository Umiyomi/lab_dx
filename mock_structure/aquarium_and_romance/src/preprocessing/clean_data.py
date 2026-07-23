"""Clean and validate survey response data."""

from __future__ import annotations

import csv
from pathlib import Path

VALID_RATINGS = {1, 2, 3, 4, 5}
VALID_INTENSITY = {1, 2, 3, 4, 5}


def load_csv(path: Path) -> list[dict[str, str]]:
    with path.open(encoding="utf-8") as f:
        return list(csv.DictReader(f))


def clean_rows(rows: list[dict[str, str]]) -> list[dict[str, str | int | bool]]:
    cleaned: list[dict[str, str | int | bool]] = []

    for row in rows:
        rating = int(row["experience_rating"])
        intensity = int(row["emotion_intensity"])
        if rating not in VALID_RATINGS or intensity not in VALID_INTENSITY:
            continue

        purpose = row["visit_purpose"]
        companion = row["companion"]
        cleaned.append(
            {
                "respondent_id": row["respondent_id"],
                "age_group": row["age_group"],
                "visit_purpose": purpose,
                "companion": companion,
                "memorable_exhibit": row["memorable_exhibit"],
                "experience_rating": rating,
                "primary_emotion": row["primary_emotion"],
                "emotion_intensity": intensity,
                "revisit_intention": row["revisit_intention"],
                "is_romantic_context": purpose == "デート" or companion == "恋人・配偶者",
            }
        )

    return cleaned


def write_csv(path: Path, rows: list[dict], fieldnames: list[str]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(rows)
