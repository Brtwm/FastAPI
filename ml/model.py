from dataclasses import dataclass
from pathlib import Path
from typing import Callable

import yaml
from transformers import pipeline


@dataclass
class SentimentPrediction:
    """Результат предсказания тональности."""
    label: str
    score: float


def _load_config() -> dict:
    """
    Загружает конфиг из ml/config.yaml или ml/config.yml.
    Бросает понятную ошибку, если файла нет или он пустой/битый.
    """
    base_dir = Path(__file__).resolve().parent
    candidates = [base_dir / "config.yaml", base_dir / "config.yml"]

    config_path = next((p for p in candidates if p.exists()), None)
    if config_path is None:
        raise FileNotFoundError(
            f"Не найден конфиг. Ожидался один из файлов: {candidates[0].name} или {candidates[1].name} "
            f"в папке {base_dir}"
        )

    with config_path.open("r", encoding="utf-8") as f:
        config = yaml.safe_load(f)

    if not isinstance(config, dict):
        raise ValueError(f"Конфиг {config_path} пустой или имеет неверный формат (ожидался YAML mapping).")

    for key in ("task", "model"):
        if key not in config or not config[key]:
            raise ValueError(f"В конфиге {config_path} отсутствует или пустой ключ '{key}'.")

    return config


def load_model(device: int = -1) -> Callable[[str], SentimentPrediction]:
    """
    Загружает модель для анализа тональности текста.

    :param device: -1 для CPU, 0 для первой CUDA GPU и т.д.
    :return: функция, которая принимает text и возвращает SentimentPrediction
    """
    config = _load_config()

    model_hf = pipeline(
        task=config["task"],
        model=config["model"],
        device=device,
    )

    def model(text: str) -> SentimentPrediction:
        pred = model_hf(text)
        best = pred[0]
        return SentimentPrediction(
            label=best["label"],
            score=float(best["score"]),
        )

    return model