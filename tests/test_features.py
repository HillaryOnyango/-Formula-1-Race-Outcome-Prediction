import pandas as pd

from src.features.build_features import build_model_table


def test_build_model_table_adds_required_features():
    df = pd.DataFrame(
        {
            "season": [2024, 2024, 2024, 2024],
            "round": [1, 1, 2, 2],
            "race_id": ["2024_1", "2024_1", "2024_2", "2024_2"],
            "race_name": ["Race A", "Race A", "Race B", "Race B"],
            "driver_id": ["driver_a", "driver_b", "driver_a", "driver_b"],
            "constructor_id": ["team_a", "team_b", "team_a", "team_b"],
            "grid": [1, 2, 3, 4],
            "finish_position": [1, 2, 3, 4],
            "points": [25.0, 18.0, 15.0, 12.0],
            "is_top3": [1, 1, 1, 0],
            "is_winner": [1, 0, 0, 0],
        }
    )
    result = build_model_table(df)
    assert "avg_finish_last_5" in result.columns
    assert "team_points_last_5" in result.columns
    assert len(result) == 4
