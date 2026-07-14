"""Project paths (single source of truth)."""

from __future__ import annotations

from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]

DATA_DIR = ROOT / "data"
MOCK_DIR = DATA_DIR / "mock"
PROCESSED_DIR = DATA_DIR / "processed"
DOCS_DIR = ROOT / "docs"
RESULTS_DIR = ROOT / "results"
FIGURES_DIR = RESULTS_DIR / "figures"
TABLES_DIR = RESULTS_DIR / "tables"

VISITOR_DATA_MOCK = MOCK_DIR / "visitor_data_mock.csv"
SURVEY_RESPONSES_MOCK = MOCK_DIR / "survey_responses_mock.csv"
ANALYSIS_DATASET = PROCESSED_DIR / "analysis_dataset.csv"

EXHIBIT_RATINGS_FIGURE = FIGURES_DIR / "exhibit_ratings.svg"
ROMANTIC_CONTEXT_FIGURE = FIGURES_DIR / "romantic_context_comparison.svg"

EXHIBIT_RATINGS_TABLE = TABLES_DIR / "exhibit_ratings.csv"
ROMANTIC_CONTEXT_TABLE = TABLES_DIR / "romantic_context_comparison.csv"
EMOTION_COUNTS_TABLE = TABLES_DIR / "emotion_counts.csv"
REVISIT_BY_RATING_TABLE = TABLES_DIR / "revisit_by_rating.csv"
