

import pytest
import os
import sys

# Configurar Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'blog_notas.settings')

# Crear carpetas necesarias
os.makedirs("selenium_tests/screenshots", exist_ok=True)
os.makedirs("selenium_tests/reports", exist_ok=True)

print("=" * 60)
print("🚀 INICIANDO PRUEBAS AUTOMATIZADAS CON SELENIUM")
print("=" * 60)
print(f"📂 Proyecto: {os.getcwd()}")
print(f"📸 Capturas: selenium_tests/screenshots/")
print(f"📊 Reporte: selenium_tests/reports/report.html")
print("=" * 60)

# Ejecutar pruebas
exit_code = pytest.main([
    "selenium_tests/",
    "--html=selenium_tests/reports/report.html",
    "--self-contained-html",
    "-v",
    "-s",
    "--tb=short"
])

print("\n" + "=" * 60)
if exit_code == 0:
    print("✅ TODAS LAS PRUEBAS PASARON")
else:
    print("❌ ALGUNAS PRUEBAS FALLARON")
    print("📸 Revisa las capturas en: selenium_tests/screenshots/")
print(f"📊 Abre el reporte: selenium_tests/reports/report.html")
print("=" * 60)

sys.exit(exit_code)