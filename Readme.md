# Без установки(может работает а может и нет):

```
http://147.45.98.172:8501
```

# Установка и запуск:
Установка `uv` если еще не стоит:
```
curl -LsSf https://astral.sh/uv/install.sh | sh
```


Клоним репозиторий:
```
git clone https://github.com/andrushechka37/Qubit-Simulation.git
```

Переходим в репозиторий и подтягиваем зависимости:

```
cd Qubit-Simulation && uv sync
```
клон + uv + sync + run

Запуск:

```
uv run streamlit run main.py
```

Все использование и теория написаны в симуляторе

### Литература

1) https://vas3k.blog/blog/quantum_computing/

2) https://davidbkemp.github.io/QuantumComputingArticle/
3) https://github.com/Qiskit/textbook/blob/main/notebooks/ch-states/atoms-computation.ipynb
4) https://davidbkemp.github.io/QuantumComputingArticle/part2.html
4) https://arxiv.org/pdf/cond-mat/9904003v1
5) М. Нильсен, И. Чанг - Квантовые вычисления и квантовая информация
6) https://files.batistalab.com/teaching/attachments/chem584/Cooperpair.pdf
7) https://kpfu.ru/staff_files/F1966424564/Sverkhprovodyashhie_zaryadovye_kubity.pdf

