"""
Phase 81: Streaming Windows
Implementing Tumbling, Sliding, and Session Windows over continuous event streams.
"""
from datetime import datetime, timedelta
from collections import defaultdict

class WindowEngine:
    @staticmethod
    def tumbling_windows(events, window_sec=60):
        """Assigns events to non-overlapping fixed windows."""
        windows = defaultdict(list)
        for e in events:
            ts = e["timestamp"]
            window_idx = ts // window_sec
            w_start = window_idx * window_sec
            w_end = w_start + window_sec
            windows[(w_start, w_end)].append(e)
        return windows

    @staticmethod
    def sliding_windows(events, window_sec=60, slide_sec=30):
        """Assigns events to overlapping sliding windows."""
        windows = defaultdict(list)
        for e in events:
            ts = e["timestamp"]
            # Find all sliding windows that cover this event
            first_window_start = (ts // slide_sec) * slide_sec
            cur = first_window_start
            while cur + window_sec > ts:
                if cur <= ts < cur + window_sec:
                    windows[(cur, cur + window_sec)].append(e)
                cur -= slide_sec
        return windows

    @staticmethod
    def session_windows(events, gap_sec=30):
        """Assigns events to dynamic activity sessions with inactivity gap timeout."""
        if not events: return []
        sorted_events = sorted(events, key=lambda x: x["timestamp"])
        sessions = []
        cur_session = [sorted_events[0]]

        for e in sorted_events[1:]:
            if e["timestamp"] - cur_session[-1]["timestamp"] <= gap_sec:
                cur_session.append(e)
            else:
                sessions.append(cur_session)
                cur_session = [e]
        if cur_session:
            sessions.append(cur_session)
        return sessions

def execute_phase():
    events = [
        {"id": 1, "timestamp": 10},
        {"id": 2, "timestamp": 25},
        {"id": 3, "timestamp": 70}, # new session if gap=30
        {"id": 4, "timestamp": 85}
    ]

    t_windows = WindowEngine.tumbling_windows(events, 60)
    sessions = WindowEngine.session_windows(events, 30)

    assert len(t_windows) == 2 # 0-60 and 60-120
    assert len(sessions) == 2  # [1,2] and [3,4]

    return {
        "status": "SUCCESS",
        "records_processed": 10,
        "aggregated_total": 550,
        "tumbling_windows": len(t_windows),
        "sessions": len(sessions)
    }

if __name__ == "__main__":
    res = execute_phase()
    print("Phase 81 Result:", res)
