"""Run mock data generation, preprocessing, analysis, and figure export."""

from __future__ import annotations

import csv
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))

from src.analysis.analyze_experience import (  # noqa: E402
    emotion_counts,
    group_mean,
    romantic_comparison,
    revisit_by_rating,
)
from src.preprocessing.clean_data import clean_rows, load_csv, write_csv  # noqa: E402
from src.visualization.plot_results import (  # noqa: E402
    plot_exhibit_ratings,
    plot_romantic_comparison,
)

RAW_PATH = ROOT / "data" / "mock" / "survey_responses_mock.csv"
PROCESSED_PATH = ROOT / "data" / "processed" / "analysis_dataset.csv"
RESULTS_DIR = ROOT / "results"
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
    if RAW_PATH.exists():
        return
    from scripts.generate_mock_data import main as generate_main

    generate_main()


def write_summary_tables(rows: list[dict]) -> None:
    tables_dir = RESULTS_DIR / "tables"
    tables_dir.mkdir(parents=True, exist_ok=True)

    exhibit_means = group_mean(rows, "memorable_exhibit")
    with (tables_dir / "exhibit_ratings.csv").open("w", newline="", encoding="utf-8") as f:
        writer = csv.writer(f)
        writer.writerow(["memorable_exhibit", "mean_experience_rating"])
        for key, value in exhibit_means.items():
            writer.writerow([key, value])

    romantic = romantic_comparison(rows)
    with (tables_dir / "romantic_context_comparison.csv").open("w", newline="", encoding="utf-8") as f:
        writer = csv.writer(f)
        writer.writerow(["metric", "value"])
        for key, value in romantic.items():
            writer.writerow([key, value])

    emotions = emotion_counts(rows)
    with (tables_dir / "emotion_counts.csv").open("w", newline="", encoding="utf-8") as f:
        writer = csv.writer(f)
        writer.writerow(["primary_emotion", "count"])
        for key, value in sorted(emotions.items(), key=lambda x: -x[1]):
            writer.writerow([key, value])

    revisit = revisit_by_rating(rows)
    with (tables_dir / "revisit_by_rating.csv").open("w", newline="", encoding="utf-8") as f:
        writer = csv.writer(f)
        writer.writerow(["rating_bucket", "revisit_intention", "count"])
        for bucket, counts in revisit.items():
            for intention, count in counts.items():
                writer.writerow([bucket, intention, count])


def main() -> None:
    ensure_mock_data()

    raw_rows = load_csv(RAW_PATH)
    processed = clean_rows(raw_rows)
    write_csv(PROCESSED_PATH, processed, FIELDNAMES)

    exhibit_means = group_mean(processed, "memorable_exhibit")
    romantic = romantic_comparison(processed)

    figures_dir = RESULTS_DIR / "figures"
    plot_exhibit_ratings(exhibit_means, figures_dir / "exhibit_ratings.svg")
    plot_romantic_comparison(romantic, figures_dir / "romantic_context_comparison.svg")
    write_summary_tables(processed)

    print(f"Processed dataset: {PROCESSED_PATH}")
    print(f"Figures: {figures_dir}")
    print(f"Tables: {RESULTS_DIR / 'tables'}")


if __name__ == "__main__":
    main()
