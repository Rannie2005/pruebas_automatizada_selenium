import pytest
import os
import django
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from datetime import datetime
import time

# === IMPORTANTE: webdriver-manager maneja la versión automáticamente ===
from webdriver_manager.chrome import ChromeDriverManager

# Configurar Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'blog_notas.settings')
django.setup()

from django.contrib.auth.models import User

@pytest.fixture
def driver():
    """Abre Chrome - webdriver-manager descarga el driver correcto automáticamente"""
    print("\n🚀 Abriendo navegador...")
    
    # === ESTA ES LA MAGIA: webdriver-manager detecta tu Chrome y descarga el driver correcto ===
    service = Service(ChromeDriverManager().install())
    
    options = webdriver.ChromeOptions()
    options.add_argument("--start-maximized")
    
    driver = webdriver.Chrome(service=service, options=options)
    driver.implicitly_wait(10)
    
    yield driver
    
    print("\n🔒 Cerrando navegador...")
    driver.quit()

@pytest.fixture
def usuario_prueba():
    """Crea un usuario de prueba en la base de datos"""
    user, creado = User.objects.get_or_create(
        username='testuser',
        defaults={'email': 'test@example.com'}
    )
    if creado:
        user.set_password('Chamon1234')
        user.save()
        print("✅ Usuario testuser creado")
    else:
        print("✅ Usuario testuser ya existe")
    return user

@pytest.fixture
def logged_driver(driver, usuario_prueba):
    """Driver con sesión iniciada automáticamente"""
    print("\n🔐 Iniciando sesión...")
    
    driver.get("http://localhost:8000/login/")
    time.sleep(2)
    
    username_field = WebDriverWait(driver, 10).until(
        EC.presence_of_element_located((By.NAME, "username"))
    )
    username_field.clear()
    username_field.send_keys("testuser")
    
    password_field = driver.find_element(By.NAME, "password")
    password_field.clear()
    password_field.send_keys("Chamon1234")
    
    submit_button = driver.find_element(By.CSS_SELECTOR, "button[type='submit']")
    submit_button.click()
    
    time.sleep(2)
    print("✅ Sesión iniciada")
    
    return driver

@pytest.hookimpl(tryfirst=True, hookwrapper=True)
def pytest_runtest_makereport(item, call):
    """Captura de pantalla automática si falla una prueba"""
    outcome = yield
    report = outcome.get_result()
    
    if report.when == "call" and report.failed:
        driver = item.funcargs.get("driver") or item.funcargs.get("logged_driver")
        if driver:
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            os.makedirs("selenium_tests/screenshots", exist_ok=True)
            filename = f"selenium_tests/screenshots/{item.name}_{timestamp}.png"
            driver.save_screenshot(filename)
            print(f"\n📸 Captura guardada: {filename}")