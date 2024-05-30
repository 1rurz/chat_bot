import requests


def test_page_opening():
    response = requests.get(
        "http://localhost:8501"
    )  # Замените на URL вашего приложения
    assert response.status_code == 200, "Ошибка при открытии страницы"
