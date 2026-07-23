"""Analysis pipeline (library). Invoke via project root main.py."""

from __future__ import annotations

import csv

from src.analysis.analyze_experience import (
    emotion_counts,
    group_mean,
    romantic_comparison,
    revisit_by_rating,
)
from src.config import (
    ANALYSIS_DATASET,
    EMOTION_COUNTS_TABLE,
    EXHIBIT_RATINGS_FIGURE,
    EXHIBIT_RATINGS_TABLE,
    FIGURES_DIR,
    REVISIT_BY_RATING_TABLE,
    ROMANTIC_CONTEXT_FIGURE,
    ROMANTIC_CONTEXT_TABLE,
    SURVEY_RESPONSES_MOCK,
    TABLES_DIR,
)
from src.preprocessing.clean_data import clean_rows, load_csv, write_csv
from src.visualization.plot_results import (
    plot_exhibit_ratings,
    plot_romantic_comparison,
)

FIELDNAMES = [
    "respondent_id",
    "age_group",
    "visit_purpose",
    "companion",
    "memorable_exhibit",
    "experience_rating",
    "primary_emotion",
    "emotion_intensity",
    "revisit_intention",
    "is_romantic_context",
]


def ensure_mock_data() -> None:
    if SURVEY_RESPONSES_MOCK.exists():
        return
    from scripts.generate_mock_data import generate_mock_data

    generate_mock_data()


def write_summary_tables(rows: list[dict]) -> None:
    TABLES_DIR.mkdir(parents=True, exist_ok=True)

    exhibit_means = group_mean(rows, "memorable_exhibit")
    with EXHIBIT_RATINGS_TABLE.open("w", newline="", encoding="utf-8") as f:
        writer = csv.writer(f)
        writer.writerow(["memorable_exhibit", "mean_experience_rating"])
        for key, value in exhibit_means.items():
            writer.writerow([key, value])

    romantic = romantic_comparison(rows)
    with ROMANTIC_CONTEXT_TABLE.open("w", newline="", encoding="utf-8") as f:
        writer = csv.writer(f)
        writer.writerow(["metric", "value"])
        for key, value in romantic.items():
            writer.writerow([key, value])

    emotions = emotion_counts(rows)
    with EMOTION_COUNTS_TABLE.open("w", newline="", encoding="utf-8") as f:
        writer = csv.writer(f)
        writer.writerow(["primary_emotion", "count"])
        for key, value in sorted(emotions.items(), key=lambda x: -x[1]):
            writer.writerow([key, value])

    revisit = revisit_by_rating(rows)
    with REVISIT_BY_RATING_TABLE.open("w", newline="", encoding="utf-8") as f:
        writer = csv.writer(f)
        writer.writerow(["rating_bucket", "revisit_intention", "count"])
        for bucket, counts in revisit.items():
            for intention, count in counts.items():
                writer.writerow([bucket, intention, count])


def run_analysis() -> None:
    ensure_mock_data()

    raw_rows = load_csv(SURVEY_RESPONSES_MOCK)
    processed = clean_rows(raw_rows)
    write_csv(ANALYSIS_DATASET, processed, FIELDNAMES)

    exhibit_means = group_mean(processed, "memorable_exhibit")
    romantic = romantic_comparison(processed)

    plot_exhibit_ratings(exhibit_means, EXHIBIT_RATINGS_FIGURE)
    plot_romantic_comparison(romantic, ROMANTIC_CONTEXT_FIGURE)
    write_summary_tables(processed)

    print(f"Processed dataset: {ANALYSIS_DATASET}")
    print(f"Figures: {FIGURES_DIR}")
    print(f"Tables: {TABLES_DIR}")
