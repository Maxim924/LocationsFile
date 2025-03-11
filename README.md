1. Создать виртуальное окружение: python -m venv venv
2. Прописать команду: deactivate для выхода из окружения
3. Прописать команду: venv\Scripts\activate для активации виртуального окружения
4. Выбираем интерпретатор виртуального окружения (python 3.10)
5. Установить нужные библиотеки командой: pip install -r requirements.txt
6. Если потребуется, обновить pip: pip install --upgrade pip
7. Запускаем: uvicorn main:app --reload
