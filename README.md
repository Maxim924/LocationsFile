1. Создать виртуальное окружение: python -m venv venv (Можно создать вручную, выбрав интерпретатор) 
2. Прописать команду: deactivate для выхода из окружения
3. Прописать команду: venv\Scripts\activate для активации виртуального окружения
4. Обновить pip: python.exe -m pip install --upgrade pip
5. Установить нужные библиотеки командой: pip install -r requirements.txt
6. Выполняем команду для создания контейнера Docker: docker-compose up --build
Таблицы вручную создавать не нужно, все выполнится автоматически sql скриптом.
7. Запускаем: uvicorn main:app --reload

Тестовый кошелек Tron: TMzoZ7iRvSJhi47Fygp47MQbVPbsezdqZV
