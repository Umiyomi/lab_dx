"""Project entry point: run analysis with research asset logging."""

from __future__ import annotations

from src.config import RESULTS_DIR, SURVEY_RESPONSES_MOCK
from src.logger import ResearchRun
from scripts.run_analysis import run_analysis


def main() -> None:
    with ResearchRun(entrypoint="main.py") as run:
        run.input(SURVEY_RESPONSES_MOCK)
        run.output(RESULTS_DIR)
        run_analysis()


if __name__ == "__main__":
    main()
