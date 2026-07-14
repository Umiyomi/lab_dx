"""Exploratory analysis helpers for aquarium experience survey data."""

from __future__ import annotations

from collections import Counter, defaultdict
from statistics import mean


def group_mean(rows: list[dict], key: str, value: str = "experience_rating") -> dict[str, float]:
    buckets: dict[str, list[int]] = defaultdict(list)
    for row in rows:
        buckets[str(row[key])].append(int(row[value]))
    return {k: round(mean(v), 2) for k, v in sorted(buckets.items())}


def romantic_comparison(rows: list[dict]) -> dict[str, float]:
    romantic = [int(r["experience_rating"]) for r in rows if r["is_romantic_context"]]
    other = [int(r["experience_rating"]) for r in rows if not r["is_romantic_context"]]
    return {
        "romantic_context_mean": round(mean(romantic), 2) if romantic else 0.0,
        "other_context_mean": round(mean(other), 2) if other else 0.0,
        "romantic_n": len(romantic),
        "other_n": len(other),
    }


def emotion_counts(rows: list[dict]) -> dict[str, int]:
    return dict(Counter(str(r["primary_emotion"]) for r in rows))


def revisit_by_rating(rows: list[dict]) -> dict[str, dict[str, int]]:
    table: dict[str, dict[str, int]] = defaultdict(lambda: defaultdict(int))
    for row in rows:
        bucket = "high" if int(row["experience_rating"]) >= 4 else "low"
        table[bucket][str(row["revisit_intention"])] += 1
    return {k: dict(v) for k, v in table.items()}
