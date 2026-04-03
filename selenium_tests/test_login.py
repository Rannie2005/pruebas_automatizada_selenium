import pytest
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time

def test_login_camino_feliz(driver):
    """
    HISTORIA 1 - PRUEBA FELIZ
    Como usuario quiero iniciar sesión con credenciales correctas
    """
    print("\n📝 Prueba: Login exitoso")
    
    driver.get("http://localhost:8000/login/")
    time.sleep(1)
    
    driver.find_element(By.NAME, "username").send_keys("testuser")
    driver.find_element(By.NAME, "password").send_keys("Chamon1234")
    driver.find_element(By.CSS_SELECTOR, "button[type='submit']").click()
    time.sleep(2)
    

    assert "notas" in driver.current_url or "dashboard" in driver.current_url or "bienvenido" in driver.page_source.lower()
    
    print("✅ Login exitoso verificado")

def test_login_negativo(driver):
    """
    HISTORIA 1 - PRUEBA NEGATIVA
    Usuario con contraseña incorrecta NO debe entrar
    """
    print("\n📝 Prueba: Login con contraseña incorrecta")
    
    driver.get("http://localhost:8000/login/")
    time.sleep(1)
    
    driver.find_element(By.NAME, "username").send_keys("testuser")
    driver.find_element(By.NAME, "password").send_keys("contraseña_mala")
    driver.find_element(By.CSS_SELECTOR, "button[type='submit']").click()
    time.sleep(1)
    
    # Debe mostrar mensaje de error
    pagina = driver.page_source.lower()
    assert "error" in pagina or "inválido" in pagina or "incorrecto" in pagina
    

    assert "notas" not in driver.current_url
    
    print("✅ Error mostrado correctamente")

def test_login_limites(driver):
    """
    HISTORIA 1 - PRUEBA DE LÍMITES
    Usuario con nombre demasiado largo (más de 150 caracteres)
    """
    print("\n📝 Prueba: Login con usuario muy largo")
    
    driver.get("http://localhost:8000/login/")
    time.sleep(1)
    
    
    usuario_largo = "a" * 151
    driver.find_element(By.NAME, "username").send_keys(usuario_largo)
    driver.find_element(By.NAME, "password").send_keys("Chamon1234")
    driver.find_element(By.CSS_SELECTOR, "button[type='submit']").click()
    time.sleep(1)
    
    
    pagina = driver.page_source.lower()
    assert "error" in pagina or "inválido" in pagina
    
    print("✅ Límite de caracteres manejado correctamente")