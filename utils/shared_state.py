"""Stato condiviso thread-safe tra tutte le sessioni Streamlit.

Usa st.cache_resource per creare un singleton in memoria condiviso
da tutte le sessioni browser collegate allo stesso server.
Perfetto per un workshop: dati visibili in tempo reale da tutti i PC.
"""

import threading
from datetime import datetime

import streamlit as st


class SharedState:
    """Dizionario thread-safe condiviso tra tutte le sessioni."""

    def __init__(self):
        self._lock = threading.Lock()
        self._data = {
            "groups": {},          # nome_gruppo -> dati del gruppo
            "quiz_responses": [],  # lista di risposte individuali al quiz
            "votes": {},           # voter_id -> {categoria: gruppo_votato}
            "reflections": {},     # voter_id -> {domanda: risposta}
        }

    # ── Gruppi ───────────────────────────────────────────────────────────

    def register_group(self, group_name: str, scenario: dict) -> bool:
        """Registra un nuovo gruppo. Ritorna False se il nome è già preso."""
        with self._lock:
            if group_name in self._data["groups"]:
                return False
            self._data["groups"][group_name] = {
                "scenario": scenario,
                "scenario_card": None,
                "card_classifications": {},
                "brainstorm_history": [],
                "coach_config": None,
                "coach_system_prompt": None,
                "coach_chat_history": [],
                "registered_at": datetime.now().isoformat(),
            }
            return True

    def get_group(self, group_name: str) -> dict | None:
        with self._lock:
            return self._data["groups"].get(group_name)

    def get_all_groups(self) -> dict:
        with self._lock:
            return dict(self._data["groups"])

    def get_group_names(self) -> list[str]:
        with self._lock:
            return list(self._data["groups"].keys())

    def update_group(self, group_name: str, **kwargs):
        """Aggiorna campi specifici di un gruppo."""
        with self._lock:
            if group_name in self._data["groups"]:
                self._data["groups"][group_name].update(kwargs)

    # ── Brainstorm chat history ──────────────────────────────────────────

    def add_brainstorm_message(self, group_name: str, role: str, content: str):
        with self._lock:
            if group_name in self._data["groups"]:
                self._data["groups"][group_name]["brainstorm_history"].append(
                    {"role": role, "content": content}
                )

    def get_brainstorm_history(self, group_name: str) -> list:
        with self._lock:
            group = self._data["groups"].get(group_name)
            return list(group["brainstorm_history"]) if group else []

    # ── Coach chat history ───────────────────────────────────────────────

    def set_coach_chat_history(self, group_name: str, history: list):
        with self._lock:
            if group_name in self._data["groups"]:
                self._data["groups"][group_name]["coach_chat_history"] = history

    def add_coach_message(self, group_name: str, role: str, content: str):
        with self._lock:
            if group_name in self._data["groups"]:
                self._data["groups"][group_name]["coach_chat_history"].append(
                    {"role": role, "content": content}
                )

    def get_coach_chat_history(self, group_name: str) -> list:
        with self._lock:
            group = self._data["groups"].get(group_name)
            return list(group["coach_chat_history"]) if group else []

    # ── Quiz ─────────────────────────────────────────────────────────────

    def add_quiz_response(self, student_id: str, answers: dict):
        """Aggiunge le risposte al quiz di uno studente."""
        with self._lock:
            # Rimuovi risposte precedenti dello stesso studente (se ri-compila)
            self._data["quiz_responses"] = [
                r for r in self._data["quiz_responses"]
                if r["student_id"] != student_id
            ]
            self._data["quiz_responses"].append({
                "student_id": student_id,
                "answers": answers,
                "submitted_at": datetime.now().isoformat(),
            })

    def get_quiz_responses(self) -> list:
        with self._lock:
            return list(self._data["quiz_responses"])

    # ── Voti ─────────────────────────────────────────────────────────────

    def cast_vote(self, voter_id: str, votes: dict):
        """Registra i voti di uno studente. votes = {categoria: gruppo_votato}"""
        with self._lock:
            self._data["votes"][voter_id] = votes

    def get_all_votes(self) -> dict:
        with self._lock:
            return dict(self._data["votes"])

    # ── Riflessioni ────────────────────────────────────────────────────

    def save_reflection(self, voter_id: str, answers: dict):
        """Salva le riflessioni finali di uno studente."""
        with self._lock:
            self._data["reflections"][voter_id] = answers

    def get_reflections(self) -> dict:
        with self._lock:
            return dict(self._data["reflections"])

    # ── Admin ────────────────────────────────────────────────────────────

    def reset_all(self):
        """Reset completo di tutti i dati."""
        with self._lock:
            self._data = {
                "groups": {},
                "quiz_responses": [],
                "votes": {},
                "reflections": {},
            }


@st.cache_resource
def get_shared_state() -> SharedState:
    """Ritorna il singleton dello stato condiviso."""
    return SharedState()
