from dataclasses import dataclass
from pathlib import Path
import yaml
from transformers import pipeline

# Загрузка файла конфига
config_path = Path(__file__).parent / "config.yml"
with open(config_path, 'r') as f:
    config = yaml.load(f, Loader=yaml.FullLoader)

@dataclass
class SentimentPrediction:
    '''Класс представляющий результат предсказания настроения'''

    label: str
    score: float

def load_model():
    '''
    Загружает предобученную модель для анализа тональности текста
    :return:
        model (function): Функция которая берет текстовый ввод  и возвращает объект SentimentPrediction
    '''

    model_hf = pipeline(config["task"], model=config["model"], device=-1)

    def  model(text: str) -> SentimentPrediction:
        pred = model_hf(text)
        pred_best_class = pred[0]
        return SentimentPrediction(
            label=pred_best_class['label'],
            score=pred_best_class['score'],
        )

    return model