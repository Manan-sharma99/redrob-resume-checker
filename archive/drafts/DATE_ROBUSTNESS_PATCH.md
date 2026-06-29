# Date Robustness Patch Report

## Objective
The goal of this patch was to make the feature extraction pipeline robust to realistic resume date formats without altering the mathematical architecture of the ranking system. Previously, the system strictly required `YYYY-MM-DD` formatted dates, penalising or ignoring jobs with other valid chronological information.

## Patch 1: Date Parser (`_parse_date`)
The `_parse_date()` function in `extract_candidate_features.py` was extended to safely support common real-world resume formats.
*   **`YYYY-MM-DD`**: Parsed directly to the exact date.
*   **`YYYY-MM`**: Normalized to the first day of the month (`YYYY-MM-01`).
*   **`YYYY`**: Normalized to the first day of the year (`YYYY-01-01`).
*   **`Present`, `Current`, `Ongoing`**: Mapped to the `as_of_date` to correctly represent current employment without silent failures.
*   **Missing/Invalid**: Deterministically mapped to `None` without inventing dates.

## Patch 2: Career Features Integration
The `career_features()` function was updated to prevent jobs from being dropped if their exact ISO date strings were missing.
*   **Dual-path accumulation**: Jobs with valid start/end intervals are processed via `_union_months()` to handle concurrent overlapping roles. Jobs lacking exact dates but having a supplied `duration_months` are now accumulated independently as standalone durations.
*   **No lost experience**: `total_months_experience` now equals the sum of unified interval months plus all standalone duration months.

## Patch 3: Contradiction Scoring Fix
The `contradiction_score()` function was updated to remove arbitrary penalties.
*   **Removed missing-date penalties**: The hardcoded 8-point and 5-point penalties for simply lacking a start date or an end date were removed.
*   **Removed descriptive-string penalties**: `Present` and `Current` no longer trigger missing end-date penalties.
*   **Strict chronological checking**: Penalties are now strictly reserved for objective timeline violations (e.g., `end_date < start_date` or `start_date > as_of_date`).
