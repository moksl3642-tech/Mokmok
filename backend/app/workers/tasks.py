from __future__ import annotations

import json
import time
from dataclasses import dataclass


@dataclass
class TaskResult:
    summary: str
    data: dict

    def dumps(self) -> str:
        return json.dumps({"summary": self.summary, "data": self.data})


def train_logistic_regression(payload: dict) -> TaskResult:
    """CPU-heavy placeholder. Replace with real training pipeline."""
    records = payload.get("records", 50_000)
    penalty = payload.get("penalty", "l2")
    # simulate heavy compute
    for _ in range(3):
        time.sleep(1)

    return TaskResult(
        summary="logistic_regression_trained",
        data={"records": records, "penalty": penalty, "accuracy": 0.84},
    )


def batch_recompute_roadmap_stats(payload: dict) -> TaskResult:
    """I/O-heavy placeholder for recomputing aggregate data."""
    roadmap_ids = payload.get("roadmap_ids", [])
    chunk_size = payload.get("chunk_size", 100)
    for _ in range(max(1, len(roadmap_ids) // max(chunk_size, 1))):
        time.sleep(0.5)

    return TaskResult(
        summary="roadmap_statistics_recomputed",
        data={"roadmap_count": len(roadmap_ids), "chunk_size": chunk_size},
    )


TASK_REGISTRY = {
    "ml.logistic_regression.train": train_logistic_regression,
    "stats.roadmap.batch_recompute": batch_recompute_roadmap_stats,
}
