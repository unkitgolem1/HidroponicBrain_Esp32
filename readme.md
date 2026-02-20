# 🏺 Proyecto Macedonia: Sistema de Riego Inteligente IoT

Sistema de control asíncrono basado en **ESP32** y **MicroPython** para la gestión automatizada de riego con reporte a backend FastAPI.

## 🏗️ Arquitectura del Sistema
El proyecto sigue un patrón de **Estado Compartido** mediante un DTO (`Contexto`), permitiendo concurrencia real entre sensores, lógica y red.
Priorizamos un codigo limpio y legible, perfectamente modificable y ajustable. Listo para la adversidad.

- **models.py**: Definición del Estado del Sistema y Máquina de Estados.
- **sensores.py (Infra)**: Drivers de bajo nivel (DS18B20 y Relés).
- **logic.py**: Orquestación de reglas de negocio y comunicaciones HTTP.
- **main.py**: Punto de entrada y gestión del Event Loop de `uasyncio`.

## 🔌 Conexiones (Pinout)
| Componente | Pin ESP32 | Función |
| :--- | :--- | :--- |
| DS18B20 | GPIO 12 | Sensor de Temperatura (OneWire) |
| Relé Bomba | GPIO 4 | Actuador de potencia |

## 🚀 Instalación y Uso
1. Configurar los endpoints en `logic.py` con la IP de tu servidor FastAPI. (La ip es ficticia)
2. Cargar los archivos a la ESP32
3. El sistema iniciará automáticamente el `gather` de tareas.
Recomendamos que la ip del backend sea fija (dentro del rango permitido por el DHCP)
## 🧠 Lógica de Control
El sistema opera bajo un modelo híbrido(autonomus way & DrivenByUser):
- **Automático**: Activación si Temp >= 29°C.
- **Manual**: Override remoto desde el backend (prioridad alta).

## ⚖️ Licencia

Este proyecto está bajo la **Licencia Apache 2.0**.

Eres libre de usar, modificar y distribuir este software, incluso para fines comerciales, siempre que se mantenga el aviso de copyright y la atribución original. 

Consulta el archivo [LICENSE](LICENSE) para ver el texto completo de la licencia.
