from __future__ import annotations

from pathlib import Path


class Prompt:
    def __init__(self, prompt_path: Path) -> None:
        self._prompt_path = prompt_path

    def load_system_prompt(self) -> str:
        try:
            return self._prompt_path.read_text(encoding="utf-8").strip()
        except OSError:
            return (
                "Ты — Ника, ассистентка по питанию и контексту диабета. "
                "Говори от первого лица в женском роде. "
                "Дай справочную информацию и напомни, что это не заменяет врача."
            )
