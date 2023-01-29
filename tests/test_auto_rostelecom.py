import pytest

from pages.auth_page import AuthPage
from pages.registration_page import RegPage


# Тест-кейс TK-001
# Регистрация пользователя с пустым полем "Имя", появления текста с подсказкой об ошибке
def test_registration_page_with_empty_name_field(web_browser):
    auth_page = AuthPage(web_browser)
    auth_page.registration_link.click()
    reg_page = RegPage(web_browser, auth_page.get_current_url())
    reg_page.name_field.send_keys('')
    reg_page.last_name_field.send_keys("Иванов")
    reg_page.email_or_mobile_phone_field.send_keys("sergey.kholopkin@yandex.ru")
    reg_page.password_field.send_keys("Qwerty123456")
    reg_page.password_confirmation_field.send_keys("Qwert123456")
    reg_page.continue_button.click()
    reg_page.error_message_name.is_visible()
    assert reg_page.error_message_name.get_text() == "Необходимо заполнить поле кириллицей. От 2 до 30 символов."


# Тест-кейс ТК-002
# Регистрация пользователя с некорректным значением в поле "Имя"(< 2 символов), появление текста с подскаской об ошибке
def test_registration_with_an_incorrect_value_in_the_name_field(web_browser):
    auth_page = AuthPage(web_browser)
    auth_page.registration_link.click()
    reg_page = RegPage(web_browser, auth_page.get_current_url())
    reg_page.name_field.send_keys('С')
    reg_page.last_name_field.send_keys("Иванов")
    reg_page.email_or_mobile_phone_field.send_keys("sergey.kholopkin@yandex.ru")
    reg_page.password_field.send_keys("Qwerty123456")
    reg_page.password_confirmation_field.send_keys("Qwerty123456")
    reg_page.continue_button.click()
    reg_page.error_message_name.is_visible()
    assert reg_page.error_message_name.get_text() == "Необходимо заполнить поле кириллицей. От 2 до 30 символов."


# Тест-кейс ТК-003
# Регистрация пользователя с некорректным значением в поле "Фамилия"(>30 символов), появление текста с подскаской об ошибке
def test_registration_with_an_incorrect_value_in_the_last_name_field(web_browser):
    auth_page = AuthPage(web_browser)
    auth_page.registration_link.click()
    reg_page = RegPage(web_browser, auth_page.get_current_url())
    reg_page.name_field.send_keys("Сергей")
    reg_page.last_name_field.send_keys("ккккккккккккккккккккккккккккккк")
    reg_page.email_or_mobile_phone_field.send_keys("sergey.kholopkin@yandex.ru")
    reg_page.password_field.send_keys("Qwerty123456")
    reg_page.password_confirmation_field.send_keys("Qwerty123456")
    reg_page.continue_button.click()
    reg_page.error_message_name.is_visible()
    assert reg_page.error_message_last_name.get_text() == "Необходимо заполнить поле кириллицей. От 2 до 30 символов."


# Тест-кейс ТК-004
# Регистрация пользователя с уже зарегистрированным номером, отображается оповещающая форма
def test_registration_of_an_already_registered_user(web_browser):
    auth_page = AuthPage(web_browser)
    auth_page.registration_link.click()
    reg_page = RegPage(web_browser, auth_page.get_current_url())
    reg_page.name_field.send_keys("Сергей")
    reg_page.last_name_field.send_keys("Иванов")
    reg_page.email_or_mobile_phone_field.send_keys("+79192630021")
    reg_page.password_field.send_keys("Qwerty123456")
    reg_page.password_confirmation_field.send_keys("Qwerty123456")
    reg_page.continue_button.click()
    assert reg_page.notification_form.is_visible



# Тест-кейс ТК-005
# Некорректный пароль при регистрации пользователя (< 8 символов), появления текста с подсказкой об ошибке
def test_incorrect_password_during_registration(web_browser):
    auth_page = AuthPage(web_browser)
    auth_page.registration_link.click()
    reg_page = RegPage(web_browser, auth_page.get_current_url())
    reg_page.name_field.send_keys("Сергей")
    reg_page.last_name_field.send_keys("Иванов")
    reg_page.email_or_mobile_phone_field.send_keys("sergey.kholopkin@yandex.ru")
    reg_page.password_field.send_keys("123")
    reg_page.password_confirmation_field.send_keys("123")
    reg_page.continue_button.click()
    assert reg_page.error_message_password.get_text() == "Длина пароля должна быть не менее 8 символов"


# Тест-кейс ТК-006
# Проверка Авторизации с неправильным паролем в форме "Авторизация" уже зарегистрированного пользователя, надпись "Забыл пароль"
# перекрашивается в оранжнвый цвет
def test_authorization_of_a_user_with_an_invalid_password(web_browser):
    page = AuthPage(web_browser)
    page.phone.send_keys('+79192630021')
    page.password.send_keys("123")
    page.btn_login.click()
    assert page.message_invalid_username_or_password.get_text() == "Неверный логин или пароль"
    assert "rt-link--orange" in page.the_element_forgot_the_password.get_attribute('class')


# Тест-кейс ТК-007
# Регистрация пользователя в форме "Регистрации" в поле ввода "Фамилия" вместо кириллицы недопустимые символы
def test_instead_of_cyrillic_invalid_characters(web_browser):
    auth_page = AuthPage(web_browser)
    auth_page.registration_link.click()
    reg_page = RegPage(web_browser, auth_page.get_current_url())
    reg_page.name_field.send_keys("Сергей")
    reg_page.last_name_field.send_keys("!!!?")
    reg_page.email_or_mobile_phone_field.send_keys("sergey.kholopkin@yandex.ru")
    reg_page.password_field.send_keys("Qwerty123456")
    reg_page.password_confirmation_field.send_keys("Qwerty123456")
    reg_page.continue_button.click()
    assert reg_page.message_must_be_filled_in_cyrillic.get_text() == "Необходимо заполнить поле кириллицей. От 2 до 30 символов."


# Тест-кейс ТК-008
# Проверка регистрации с некорректным подтверждением пароля(Поле ввода "Пароль" и поле ввода "Подтверждение пароля" не совпадают)
def test_password_and_password_confirmation_do_not_match(web_browser):
    auth_page = AuthPage(web_browser)
    auth_page.registration_link.click()
    reg_page = RegPage(web_browser, auth_page.get_current_url())
    reg_page.name_field.send_keys("Сергей")
    reg_page.last_name_field.send_keys("Иванов")
    reg_page.email_or_mobile_phone_field.send_keys("sergey.kholopkin@yandex.ru")
    reg_page.password_field.send_keys("Qwerty123456")
    reg_page.password_confirmation_field.send_keys("Qwerty")
    reg_page.continue_button.click()
    assert reg_page.message_passwords_dont_match.get_text() == "Пароли не совпадают"


# Тест-кейс TK-009
# Регистрация с некорректным email в поле ввода "Email или мобильный телефон"
def test_invalid_email_or_mobile_phone(web_browser):
    auth_page = AuthPage(web_browser)
    auth_page.registration_link.click()
    reg_page = RegPage(web_browser, auth_page.get_current_url())
    reg_page.name_field.send_keys("Сергей")
    reg_page.last_name_field.send_keys("Иванов")
    reg_page.email_or_mobile_phone_field.send_keys("ааааааааа")
    reg_page.password_field.send_keys("Qwerty123456")
    reg_page.password_confirmation_field.send_keys("Qwerty123456")
    reg_page.continue_button.click()
    assert reg_page.message_enter_the_phone_in_the_format.get_text() == "Введите телефон в формате +7ХХХХХХХХХХ или" \
                                                                        " +375XXXXXXXXX, или email в формате example@email.ru"

# Тест-кейс ТК-010
# Тестирование аутентификации зарегистрированного пользователя
def test_authorisation_valid(web_browser):
    page = AuthPage(web_browser)
    page.phone.send_keys('+79192630021')
    page.password.send_keys("January2023")
    page.btn_login.click()

    assert 'https://b2c.passport.rt.ru/account_b2c/page?state=' in page.get_current_url() \
           and '&client_id=account_b2c#/' in page.get_current_url()


# Тест-кейс ТК-011
# Тестирование аутентификации зарегистрированного пользователя ввод в поле почта
def test_authorisation_valid(web_browser):
    page = AuthPage(web_browser)
    page.mail_tab.click()
    page.email.send_keys('serjant82@rambler.ru')
    page.password.send_keys("January2023")
    page.btn_login.click()

    assert 'https://b2c.passport.rt.ru/account_b2c/page?state=' in page.get_current_url() \
           and '&client_id=account_b2c#/' in page.get_current_url()

# Тест-кейс ТК-012
# При вводе почты в поле "номер телефона"- таб выбора аутентификации меняется автоматически.
def test_authorisation_valid(web_browser):
    page = AuthPage(web_browser)
    page.phone.send_keys('+serjant82@rambler.ru')
    page.password.send_keys("January2023")
    mail_tab_class = page.mail_tab.get_attribute("class")
    assert mail_tab_class == "rt-tab rt-tab--small rt-tab--active"

# Тест-кейс ТК-013
# При вводе латинских букв в поле "номер телефона"- таб выбора аутентификации меняется автоматически.
def test_authorisation_valid(web_browser):
    page = AuthPage(web_browser)
    page.phone.send_keys('abcdeefg')
    page.password.send_keys("January2023")
    login_tab_class = page.login_tab.get_attribute("class")
    assert login_tab_class == "rt-tab rt-tab--small rt-tab--active"

# Тест-кейс ТК-014
# При вводе цифр- в поле "номер телефона"таб выбора аутентификации меняется автоматически.
def test_authorisation_valid(web_browser):
    page = AuthPage(web_browser)
    page.phone.send_keys('123456789')
    page.password.send_keys("January2023")
    ls_tab_class = page.ls_tab.get_attribute("class")
    assert ls_tab_class == "rt-tab rt-tab--small rt-tab--active"

# Тест-кейс ТК-015
# Проверка Авторизации с пустым номером телефона
def test_authorization_of_a_user_with_an_invalid_password(web_browser):
    page = AuthPage(web_browser)
    page.phone.send_keys('')
    page.password.send_keys("January2023")
    page.btn_login.click()

    assert "rt-link--orange" in page.the_element_forgot_the_password.get_attribute('class')