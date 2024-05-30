import pytest
from selenium import webdriver


@pytest.fixture(scope="module")
def streamlit_app():
    options = webdriver.ChromeOptions()
    options.add_argument("--headless")
    driver = webdriver.Chrome(options=options)
    driver.get("http://localhost:8501")
    yield driver
    driver.quit()


def test_app_opening(streamlit_app):
    assert streamlit_app.title == "Помошник"  # Проверка наличия заголовка приложения
    assert (
        streamlit_app.find_element_by_xpath(
            "//input[@placeholder='Введите сообщение...']"
        )
        is not None
    )  # Проверка наличия поля ввода сообщения
    assert (
        streamlit_app.find_element_by_xpath("//button[contains(text(), 'Отправить')]")
        is not None
    )  # Проверка наличия кнопки отправки сообщения
