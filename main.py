from fastapi import FastAPI, Request, Form
from fastapi.responses import HTMLResponse, StreamingResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
import openpyxl
from io import BytesIO
from datetime import datetime

app = FastAPI()

app.mount("/static", StaticFiles(directory="app/static"), name="static")
templates = Jinja2Templates(directory="app/templates")

TEST_METHODS = ["Ручне тестування", "Автоматизоване тестування", "ШІ тестування"]
CRITERIA_COUNT = 5
VALUES_PER_CRITERION = 3

CRITERIA_NAMES = [
    "Час виконання тестування (у годинах)",
    "Кількість виконаних тест-кейсів (за 1 сесію)",
    "Кількість знайдених багів",
    "Відсоток покриття функціоналу",
    "Стабільність результатів (% успішних повторних запусків)"
]


analysis_history = []

def calculate_scores(criteria_values):
    scores = [0, 0, 0]  # Бали для кожного методу
    
    # Критерій 1: Час виконання (годин)
    time = criteria_values[0]
    if time[0] > 3:   scores[0] += 1
    elif 2 <= time[0] <= 3: scores[0] += 2
    elif 1 <= time[0] < 2: scores[0] += 3
    elif 0.5 <= time[0] < 1: scores[0] += 4
    elif time[0] < 0.5: scores[0] += 5
    
    if time[1] > 3:   scores[1] += 1
    elif 2 <= time[1] <= 3: scores[1] += 2
    elif 1 <= time[1] < 2: scores[1] += 3
    elif 0.5 <= time[1] < 1: scores[1] += 4
    elif time[1] < 0.5: scores[1] += 5
    
    if time[2] > 3:   scores[2] += 1
    elif 2 <= time[2] <= 3: scores[2] += 2
    elif 1 <= time[2] < 2: scores[2] += 3
    elif 0.5 <= time[2] < 1: scores[2] += 4
    elif time[2] < 0.5: scores[2] += 5
    
    # Критерій 2: Тест-кейси
    cases = criteria_values[1]
    for i, val in enumerate(cases):
        if val <= 5: scores[i] += 1
        elif 6 <= val <= 10: scores[i] += 2
        elif 11 <= val <= 20: scores[i] += 3
        elif 21 <= val <= 30: scores[i] += 4
        elif val > 30: scores[i] += 5
    
    # Критерій 3: Баги
    bugs = criteria_values[2]
    for i, val in enumerate(bugs):
        if val <= 1: scores[i] += 1
        elif 2 <= val <= 3: scores[i] += 2
        elif val == 4: scores[i] += 3
        elif val == 5: scores[i] += 4
        elif val >= 6: scores[i] += 5
    
    # Критерій 4: Покриття
    coverage = criteria_values[3]
    for i, val in enumerate(coverage):
        if val < 20: scores[i] += 1
        elif 20 <= val < 40: scores[i] += 2
        elif 40 <= val < 60: scores[i] += 3
        elif 60 <= val < 80: scores[i] += 4
        elif val >= 80: scores[i] += 5
    
    # Критерій 5: Стабільність
    stability = criteria_values[4]
    for i, val in enumerate(stability):
        if val < 60: scores[i] += 1
        elif 60 <= val < 75: scores[i] += 2
        elif 75 <= val < 85: scores[i] += 3
        elif 85 <= val < 95: scores[i] += 4
        elif val >= 95: scores[i] += 5
    
    return scores
