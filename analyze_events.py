#!/usr/bin/env python3
"""
Анализ и визуализация распределения событий информационной безопасности
по их типам (поле "signature") из файла events.json.

Используемые библиотеки: Pandas, Matplotlib, Seaborn.
"""

import json
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns


# ---------------------------------------------------------------------------
# Этап 2. Загрузка данных из JSON в датафрейм
# ---------------------------------------------------------------------------

def load_events(path: str = "events.json") -> pd.DataFrame:
    """Загружает события из JSON-файла в pandas DataFrame."""
    with open(path, "r", encoding="utf-8") as f:
        data = json.load(f)
    df = pd.DataFrame(data)

    # Приводим timestamp к типу datetime для удобства дальнейшего анализа
    if "timestamp" in df.columns:
        df["timestamp"] = pd.to_datetime(df["timestamp"])

    return df


def analyze_signatures(df: pd.DataFrame) -> pd.Series:
    """
    Анализирует распределение событий по полю 'signature':
    возвращает количество событий каждого типа, отсортированное по убыванию.
    """
    counts = df["signature"].value_counts()
    return counts


# ---------------------------------------------------------------------------
# Этап 3. Визуализация распределения типов событий
# ---------------------------------------------------------------------------

def plot_signature_distribution(counts: pd.Series, out_file: str = "signature_distribution.png"):
    """Строит горизонтальную столбчатую диаграмму распределения событий по типам (Seaborn)."""
    sns.set_theme(style="whitegrid")

    plt.figure(figsize=(12, 7))
    ax = sns.barplot(
        x=counts.values,
        y=counts.index,
        hue=counts.index,
        palette="viridis",
        legend=False,
    )
    ax.set_title("Распределение событий ИБ по типам (signature)", fontsize=14, pad=15, loc="left")
    ax.set_xlabel("Количество событий")
    ax.set_ylabel("Тип события (signature)")

    # Подписываем значения рядом со столбцами
    for i, v in enumerate(counts.values):
        ax.text(v + max(counts.values) * 0.01, i, str(v), va="center", fontsize=9)

    plt.tight_layout()
    plt.savefig(out_file, dpi=150)
    print(f"График сохранён в {out_file}")
    plt.show()


def main():
    df = load_events("events.json")

    print(f"Всего загружено событий: {len(df)}")
    print(f"Столбцы датафрейма: {list(df.columns)}")
    print()

    counts = analyze_signatures(df)
    print("Распределение событий по типам (signature):")
    print(counts)
    print()
    print("Доля каждого типа событий (%):")
    print((counts / counts.sum() * 100).round(2))

    plot_signature_distribution(counts)


if __name__ == "__main__":
    main()
