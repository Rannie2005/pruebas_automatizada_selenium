import pytest
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time

# ============ PRUEBAS DE CREAR NOTA (HISTORIA 2) ============

def test_crear_nota_camino_feliz(logged_driver):
    """
    HISTORIA 2 - CREAR: Camino feliz
    Usuario autenticado crea una nota correctamente
    """
    print("\n📝 Prueba: Crear nota exitosamente")
    
    logged_driver.get("http://localhost:8000/crear/")
    time.sleep(2)
    
    # Usar los IDs correctos de los campos
    titulo_field = logged_driver.find_element(By.ID, "id_titulo")
    titulo_field.send_keys("Mi nota de prueba")
    
    contenido_field = logged_driver.find_element(By.ID, "id_contenido")
    contenido_field.send_keys("Este es el contenido de mi nota de prueba")
    
    # Hacer clic en el botón Guardar
    logged_driver.find_element(By.CSS_SELECTOR, ".btn-submit").click()
    time.sleep(2)
    
    assert "Mi nota de prueba" in logged_driver.page_source
    print("✅ Nota creada exitosamente")

def test_crear_nota_negativo(logged_driver):
    """
    HISTORIA 2 - CREAR: Prueba negativa
    Intentar crear nota sin título (campo obligatorio)
    """
    print("\n📝 Prueba: Crear nota sin título (debe fallar)")
    
    logged_driver.get("http://localhost:8000/crear/")
    time.sleep(2)
    
    # Solo llenar contenido, dejar título vacío
    contenido_field = logged_driver.find_element(By.ID, "id_contenido")
    contenido_field.send_keys("Contenido sin título")
    
    logged_driver.find_element(By.CSS_SELECTOR, ".btn-submit").click()
    time.sleep(2)
    
    pagina = logged_driver.page_source.lower()
    assert "error" in pagina or "obligatorio" in pagina or "requerido" in pagina
    print("✅ Validación funcionó correctamente")

def test_crear_nota_limite(logged_driver):
    """
    HISTORIA 2 - CREAR: Prueba de límites
    Título con 200 caracteres (máximo del campo)
    """
    print("\n📝 Prueba: Crear nota con título en el límite (200 caracteres)")
    
    logged_driver.get("http://localhost:8000/crear/")
    time.sleep(2)
    
    titulo_200 = "A" * 200
    titulo_field = logged_driver.find_element(By.ID, "id_titulo")
    titulo_field.send_keys(titulo_200)
    
    contenido_field = logged_driver.find_element(By.ID, "id_contenido")
    contenido_field.send_keys("Contenido normal")
    
    logged_driver.find_element(By.CSS_SELECTOR, ".btn-submit").click()
    time.sleep(2)
    
    assert titulo_200 in logged_driver.page_source or "error" not in logged_driver.page_source.lower()
    print("✅ Límite de 200 caracteres funcionando")

# ============ PRUEBAS DE LEER/LISTAR NOTAS (HISTORIA 3) ============

def test_listar_notas_camino_feliz(logged_driver):
    """
    HISTORIA 3 - LEER: Ver listado de notas
    """
    print("\n📝 Prueba: Ver listado de notas")
    
    logged_driver.get("http://localhost:8000/")
    time.sleep(2)
    
    assert "nota" in logged_driver.page_source.lower() or "titulo" in logged_driver.page_source.lower()
    print("✅ Listado de notas visible")

def test_listar_notas_negativo(logged_driver):
    """
    HISTORIA 3 - LEER: Intentar ver nota que no existe
    """
    print("\n📝 Prueba: Ver nota con ID inexistente")
    
    logged_driver.get("http://localhost:8000/99999/")
    time.sleep(2)
    
    pagina = logged_driver.page_source.lower()
    assert "404" in pagina or "no encontrada" in pagina or "no existe" in pagina
    print("✅ Error 404 manejado correctamente")

def test_listar_notas_limite(logged_driver):
    """
    HISTORIA 3 - LEER: Página de listado con número de página extremo
    """
    print("\n📝 Prueba: Página de listado con número muy alto")
    
    logged_driver.get("http://localhost:8000/?page=9999")
    time.sleep(2)
    
    pagina = logged_driver.page_source.lower()
    assert "error" not in pagina or "no existe" in pagina
    print("✅ Página extrema manejada correctamente")

# ============ PRUEBAS DE EDITAR NOTA (HISTORIA 4) ============

def test_editar_nota_camino_feliz(logged_driver):
    """
    HISTORIA 4 - EDITAR: Modificar nota existente
    """
    print("\n📝 Prueba: Editar nota existente")
    
    # Crear una nota para editar
    logged_driver.get("http://localhost:8000/crear/")
    time.sleep(2)
    
    titulo_field = logged_driver.find_element(By.ID, "id_titulo")
    titulo_field.send_keys("Nota original")
    
    contenido_field = logged_driver.find_element(By.ID, "id_contenido")
    contenido_field.send_keys("Contenido original")
    
    logged_driver.find_element(By.CSS_SELECTOR, ".btn-submit").click()
    time.sleep(2)
    
    # Buscar y hacer clic en editar
    try:
        boton_editar = logged_driver.find_element(By.CSS_SELECTOR, ".edit-btn")
        boton_editar.click()
    except:
        # Si no encuentra, intentar con el enlace
        boton_editar = logged_driver.find_element(By.CSS_SELECTOR, "a[href*='editar']")
        boton_editar.click()
    
    time.sleep(2)
    
    # Editar el título
    titulo_field = logged_driver.find_element(By.ID, "id_titulo")
    titulo_field.clear()
    titulo_field.send_keys("Nota EDITADA")
    
    logged_driver.find_element(By.CSS_SELECTOR, ".btn-submit").click()
    time.sleep(2)
    
    assert "EDITADA" in logged_driver.page_source
    print("✅ Nota editada exitosamente")

def test_editar_nota_negativo(logged_driver):
    """
    HISTORIA 4 - EDITAR: Editar nota que no existe
    """
    print("\n📝 Prueba: Editar nota inexistente")
    
    logged_driver.get("http://localhost:8000/editar/99999/")
    time.sleep(2)
    
    pagina = logged_driver.page_source.lower()
    assert "404" in pagina or "no encontrada" in pagina or "no existe" in pagina
    print("✅ Error al editar nota inexistente")

def test_editar_nota_limite(logged_driver):
    """
    HISTORIA 4 - EDITAR: Título con 200 caracteres
    """
    print("\n📝 Prueba: Editar nota con título en límite")
    
    # Primero crear una nota
    logged_driver.get("http://localhost:8000/crear/")
    time.sleep(2)
    
    titulo_field = logged_driver.find_element(By.ID, "id_titulo")
    titulo_field.send_keys("Nota para editar límite")
    
    contenido_field = logged_driver.find_element(By.ID, "id_contenido")
    contenido_field.send_keys("Contenido")
    
    logged_driver.find_element(By.CSS_SELECTOR, ".btn-submit").click()
    time.sleep(2)
    
    # Editar con título largo
    try:
        boton_editar = logged_driver.find_element(By.CSS_SELECTOR, ".edit-btn")
        boton_editar.click()
    except:
        boton_editar = logged_driver.find_element(By.CSS_SELECTOR, "a[href*='editar']")
        boton_editar.click()
    
    time.sleep(2)
    
    titulo_200 = "B" * 200
    titulo_field = logged_driver.find_element(By.ID, "id_titulo")
    titulo_field.clear()
    titulo_field.send_keys(titulo_200)
    
    logged_driver.find_element(By.CSS_SELECTOR, ".btn-submit").click()
    time.sleep(2)
    
    assert "error" not in logged_driver.page_source.lower() or titulo_200 in logged_driver.page_source
    print("✅ Edición con límite funcionando")

# ============ PRUEBAS DE ELIMINAR NOTA (HISTORIA 5) ============

def test_eliminar_nota_camino_feliz(logged_driver):
    """
    HISTORIA 5 - ELIMINAR: Eliminar nota existente
    """
    print("\n📝 Prueba: Eliminar nota existente")
    
    # Crear una nota temporal
    logged_driver.get("http://localhost:8000/crear/")
    time.sleep(2)
    
    titulo_field = logged_driver.find_element(By.ID, "id_titulo")
    titulo_field.send_keys("Nota PARA ELIMINAR")
    
    contenido_field = logged_driver.find_element(By.ID, "id_contenido")
    contenido_field.send_keys("Esta nota será eliminada")
    
    logged_driver.find_element(By.CSS_SELECTOR, ".btn-submit").click()
    time.sleep(2)
    
    assert "PARA ELIMINAR" in logged_driver.page_source
    
    # Buscar botón eliminar
    try:
        # El botón eliminar tiene clase delete-btn
        boton_eliminar = logged_driver.find_element(By.CSS_SELECTOR, ".delete-btn")
        boton_eliminar.click()
        time.sleep(1)
        
        # Aceptar el confirm de JavaScript
        alert = logged_driver.switch_to.alert
        alert.accept()
        time.sleep(1)
    except:
        # Si no encuentra, ir directamente a eliminar la primera nota
        logged_driver.get("http://localhost:8000/eliminar/1/")
    
    time.sleep(2)
    
    assert "PARA ELIMINAR" not in logged_driver.page_source
    print("✅ Nota eliminada exitosamente")

def test_eliminar_nota_negativo(logged_driver):
    """
    HISTORIA 5 - ELIMINAR: Eliminar nota que no existe
    """
    print("\n📝 Prueba: Eliminar nota inexistente")
    
    logged_driver.get("http://localhost:8000/eliminar/99999/")
    time.sleep(2)
    
    pagina = logged_driver.page_source.lower()
    assert "404" in pagina or "no encontrada" in pagina or "no existe" in pagina
    print("✅ Error al eliminar nota inexistente")

def test_eliminar_nota_limite(logged_driver):
    """
    HISTORIA 5 - ELIMINAR: Intentar eliminar la misma nota dos veces
    """
    print("\n📝 Prueba: Eliminar nota ya eliminada")
    
    # Crear una nota
    logged_driver.get("http://localhost:8000/crear/")
    time.sleep(2)
    
    titulo_field = logged_driver.find_element(By.ID, "id_titulo")
    titulo_field.send_keys("Nota doble eliminación")
    
    contenido_field = logged_driver.find_element(By.ID, "id_contenido")
    contenido_field.send_keys("Contenido")
    
    logged_driver.find_element(By.CSS_SELECTOR, ".btn-submit").click()
    time.sleep(2)
    
    # Primera eliminación
    try:
        boton_eliminar = logged_driver.find_element(By.CSS_SELECTOR, ".delete-btn")
        boton_eliminar.click()
        time.sleep(1)
        alert = logged_driver.switch_to.alert
        alert.accept()
        time.sleep(1)
    except:
        logged_driver.get("http://localhost:8000/eliminar/1/")
    
    time.sleep(2)
    
    # Intentar eliminar la misma nota (ya no existe)
    logged_driver.get("http://localhost:8000/eliminar/1/")
    time.sleep(2)
    
    pagina = logged_driver.page_source.lower()
    assert "404" in pagina or "no encontrada" in pagina or "no existe" in pagina
    print("✅ Error al eliminar nota ya eliminada")