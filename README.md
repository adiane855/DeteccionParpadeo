# Proyecto Click por Parpadeo de Ojos 👁️🖱️

Este proyecto permite controlar el ratón de tu computadora (clic izquierdo, clic derecho, doble clic) mediante la detección del parpadeo de tus ojos, utilizando únicamente la cámara web.

## 🌟 Características

* **Clic Izquierdo:** Se activa con un parpadeo deliberado del ojo izquierdo.
* **Clic Derecho:** Se activa con un parpadeo deliberado del ojo derecho.
* **Doble Clic:** Se activa con un parpadeo simultáneo de ambos ojos.
* **Feedback Visual en Pantalla:** Proporciona mensajes claros en la ventana de la cámara para confirmar el tipo de parpadeo/clic detectado.

## 📋 Requisitos

* Python 3.x (se recomienda Python 3.8 o superior)
* Una cámara web funcional

## 🚀 Instalación y Configuración

Sigue estos pasos para poner en marcha el proyecto:

1.  **Clonar el Repositorio:**
    Abre tu terminal y clona el repositorio de GitHub:
    ```bash
    git clone https://github.com/adiane855/DeteccionParpadeo.git
    cd DeteccionParpadeo
    ```
    (Asegúrate de reemplazar `DeteccionParpadeo` por el nombre real de tu carpeta si es diferente).

2.  **Crear y Activar un Entorno Virtual (Recomendado):**
    Es una buena práctica crear un entorno virtual para aislar las dependencias del proyecto.
    ```bash
    python3 -m venv venv
    source venv/bin/activate
    ```
    Notarás `(venv)` al inicio de tu línea de comandos, indicando que el entorno virtual está activo.

3.  **Instalar Dependencias de Python:**
    Asegúrate de tener un archivo `requirements.txt` en la raíz de tu proyecto con todas las librerías listadas (si no lo tienes, puedes crearlo con `pip freeze > requirements.txt` después de instalar las librerías manualmente, o simplemente instala las librerías una por una).
    ```bash
    pip install -r requirements.txt
    ```

4.  **Instalar Dependencias del Sistema (para Ubuntu/Debian):**
    Para que `pyautogui` pueda controlar el ratón en entornos Linux (como Ubuntu/Debian), necesitas algunas librerías adicionales del sistema.
    ```bash
    sudo apt update
    sudo apt install scrot python3-tk python3-dev xsel xclip
    ```
    *Es altamente recomendable reiniciar tu sistema después de instalar estas dependencias para que los cambios surtan efecto.*

5.  **Descargar el Predictor de Forma Facial de Dlib:**
    Este proyecto requiere el archivo de modelo `shape_predictor_68_face_landmarks.dat` para la detección de puntos de referencia faciales.
    Puedes descargarlo desde este enlace:
    http://dlib.net/files/shape_predictor_68_face_landmarks.dat.bz2
    * Descomprime el archivo `.bz2` (puedes usar `bunzip2 shape_predictor_68_face_landmarks.dat.bz2` en Linux).
    * Coloca el archivo `shape_predictor_68_face_landmarks.dat` **directamente en la misma carpeta que `blink_detector_dlib.py`**.

## 💻 Uso

1.  **Activar el Entorno Virtual y Configurar Permisos XHost (Solo Linux GUI):**
    Asegúrate de que tu entorno virtual esté activo:
    ```bash
    source venv/bin/activate
    ```
    Para que las aplicaciones gráficas (como la ventana de la cámara de OpenCV) puedan interactuar con tu servidor X (el sistema gráfico de Linux) y permitir que `pyautogui` controle la interfaz, es posible que necesites otorgar permisos si estás en un entorno específico (ej. SSH con reenvío X, contenedores Docker, o a veces entornos virtuales si hay configuraciones de seguridad restrictivas). Ejecuta:
    ```bash
    xhost +local:
    ```
    *Este comando permite que los clientes X locales (tu aplicación Python) se conecten al servidor X. Puede que no sea estrictamente necesario en todas las configuraciones de escritorio estándar, pero es útil para solucionar problemas de permisos gráficos.*

2.  **Ejecutar el Script Principal:**
    Desde el mismo directorio y con el entorno virtual activo, ejecuta:
    ```bash
    python blink_detector_dlib.py
    ```

3.  **Control y Salida:**
    * Una ventana mostrando la transmisión de tu cámara web se abrirá.
    * **Asegúrate de que el cursor de tu ratón esté en la ventana o aplicación que deseas controlar.** Si la ventana de la cámara está activa, los clics se registrarán dentro de ella. Para controlar el escritorio o una aplicación externa, haz clic manualmente fuera de la ventana de la cámara para darle el foco.
    * **Realiza los parpadeos:**
        * Parpadea solo con el ojo izquierdo para un **clic izquierdo**.
        * Parpadea solo con el ojo derecho para un **clic derecho**.
        * Parpadea con ambos ojos simultáneamente para un **doble clic**.
    * Para salir del programa, presiona la tecla `q` en la ventana de la cámara.

## ⚠️ Notas Importantes

-   **Precisión de la Detección:** La exactitud de la detección de parpadeo puede variar significativamente según la iluminación de tu entorno, la calidad de tu cámara y la forma natural en que parpadeas. Puedes ajustar los valores de `EYE_AR_THRESH` y `EYE_AR_CONSEC_FRAMES` en el código para afinar la sensibilidad y adaptarla mejor a tus condiciones.
-   **Control del Ratón (Clics vs. Movimiento):**
    * Este proyecto se enfoca en simular **solo los eventos de clic** del ratón (izquierdo, derecho, doble clic) en la **posición actual del cursor**.
    * **No incluye funcionalidad de movimiento del cursor.** Un sistema completo de control ocular que mueva el cursor requeriría la implementación de seguimiento de la mirada (gaze tracking) o control de la posición de la cabeza, lo cual es una extensión más compleja que no forma parte de este proyecto minimalista.
-   **Foco de la Ventana para los Clics:**
    * El programa utiliza la librería `pyautogui` para simular los clics. Estos clics siempre se envían a la **ventana que tiene el foco** (la ventana activa) en tu sistema operativo.
    * Cuando el programa inicia, la ventana de la cámara (`Control de Clic por Parpadeo`) a menudo toma el foco automáticamente. Si quieres que los clics funcionen en tu escritorio, un navegador, un explorador de archivos u otra aplicación, debes **hacer clic manualmente fuera de la ventana de la cámara** (por ejemplo, en el escritorio o en la aplicación deseada) para darle el foco antes de intentar un parpadeo.
-   **Dependencias de `pyautogui` en Linux (Ubuntu):**
    * Para que `pyautogui` funcione correctamente en sistemas Linux como Ubuntu, es **esencial instalar librerías adicionales del sistema** (como se detalla en la sección de Instalación).
    * A menudo, es recomendable **reiniciar tu sistema** después de instalar estas dependencias para que los cambios surtan efecto por completo.
-   **Entorno de Desarrollo:** Este proyecto ha sido desarrollado y probado principalmente en el sistema operativo **Linux (Ubuntu)**. Las instrucciones de instalación y las dependencias específicas están orientadas a este entorno.


---
