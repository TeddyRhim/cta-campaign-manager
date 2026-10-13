"""Limite des échecs de connexion, en mémoire du processus.

Suffisant pour un seul processus uvicorn. Avec plusieurs processus ou serveurs,
chaque processus a son propre compteur : passer alors par un stockage partagé (Redis).
"""
import time
from collections import defaultdict, deque
from threading import Lock

MAX_FAILURES = 5
WINDOW_SECONDS = 300

_failures: dict[str, deque[float]] = defaultdict(deque)
_lock = Lock()


def _recent(key: str, now: float) -> deque[float]:
    attempts = _failures[key]
    while attempts and now - attempts[0] > WINDOW_SECONDS:
        attempts.popleft()
    return attempts


def is_blocked(keys: list[str]) -> bool:
    now = time.monotonic()
    with _lock:
        return any(len(_recent(key, now)) >= MAX_FAILURES for key in keys)


def record_failure(keys: list[str]) -> None:
    now = time.monotonic()
    with _lock:
        for key in keys:
            _recent(key, now).append(now)


def reset(keys: list[str]) -> None:
    with _lock:
        for key in keys:
            _failures.pop(key, None)


def clear() -> None:
    with _lock:
        _failures.clear()
