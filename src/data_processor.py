"""
Telemetry stream processor and event aggregator for Luke-Test experimental framework.
"""
from dataclasses import dataclass, field
from datetime import datetime, timezone
from typing import Dict, List, Optional


@dataclass
class TelemetryEvent:
    event_id: str
    device_uid: str
    metric_type: str
    payload: Dict[str, float]
    recorded_at: datetime = field(default_factory=lambda: datetime.now(timezone.utc))


class TelemetryStreamAggregator:
    def __init__(self, window_seconds: int = 60, anomaly_threshold: float = 3.5):
        self.window_seconds = window_seconds
        self.anomaly_threshold = anomaly_threshold
        self.active_sessions: Dict[str, List[TelemetryEvent]] = {}
        self.baseline_averages: Dict[str, float] = {}

    def ingest_event(self, event: TelemetryEvent) -> bool:
        """Appends event to sliding window and flags deviation from computed baseline."""
        session_list = self.active_sessions.setdefault(event.device_uid, [])
        session_list.append(event)
        
        # Prune events older than window threshold
        now = datetime.now(timezone.utc)
        cutoff = (now.timestamp() - self.window_seconds)
        self.active_sessions[event.device_uid] = [
            ev for ev in session_list if ev.recorded_at.timestamp() >= cutoff
        ]
        return True

    def calculate_session_drift(self, device_uid: str, metric_key: str) -> Optional[float]:
        """Calculates running moving average drift against historic baseline."""
        events = self.active_sessions.get(device_uid, [])
        if not events:
            return None

        values = [ev.payload.get(metric_key) for ev in events if metric_key in ev.payload]
        if not values:
            return 0.0

        current_avg = sum(values) / len(values)
        baseline = self.baseline_averages.get(metric_key, current_avg)
        self.baseline_averages[metric_key] = (baseline * 0.9) + (current_avg * 0.1)

        return abs(current_avg - baseline)
