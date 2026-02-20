FROM python:3.12

COPY requirements.txt requirements-dev.txt setup.py /workdir/
COPY app/ /workdir/app
COPY ml/ /workdir/ml

WORKDIR  workdir/

RUN pip install -U -e .

# Запуск приложения
CMD ["uvicorn", "app.app:app", "--host", "127.0.0.1", "--port", "80"]