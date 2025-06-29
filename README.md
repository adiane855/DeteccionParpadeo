# Proyecto Click por Parpadeo de Ojos 👁️🖱️

Este proyecto permite controlar el ratón de tu computadora (clic izquierdo, clic derecho, doble clic) mediante el parpadeo de tus ojos, utilizando la cámara web.

## Características
- **Clic Izquierdo:** Parpadeo del ojo izquierdo.
- **Clic Derecho:** Parpadeo del ojo derecho.
- **Doble Clic:** Parpadeo simultáneo de ambos ojos.
- Feedback visual en pantalla para la detección de parpadeo.

## Requisitos
- Python 3.x
- Cámara web

## Instalación

1.  **Clonar el repositorio:**
    ```bash
    git clone https://github.com/adiane855/DeteccionParpadeo.git
    cd nombre-del-repositorio
    ```

2.  **Crear y activar un entorno virtual (recomendado):**
    ```bash
    python3 -m venv venv
    source venv/bin/activate
    ```

3.  **Instalar dependencias de Python:**
    ```bash
    pip install -r requirements.txt
    ```

4.  **Instalar dependencias del sistema para pyautogui (para Ubuntu/Debian):**
    Para que `pyautogui` pueda controlar tu ratón, necesitas algunas librerías del sistema.
    ```bash
    sudo apt update
    sudo apt install scrot python3-tk python3-dev xsel xclip
    ```
    *(Es posible que necesites reiniciar tu sistema después de instalar estas dependencias para que surtan efecto.)*

5.  **Descargar el predictor de forma facial de Dlib:**
    Necesitarás el archivo `shape_predictor_68_face_landmarks.dat`. Puedes descargarlo desde este enlace:
    [http://dlib.net/files/shape_predictor_68_face_landmarks.dat.bz2](http://dlib.net/files/shape_predictor_68_face_landmarks.dat.bz2)
    Descomprime el archivo `.bz2` y coloca `shape_predictor_68_face_landmarks.dat` directamente en la misma carpeta que `blink_detector_dlib.py`.

## Uso

1.  **Asegúrate de que tu entorno virtual esté activado:**
    ```bash
    source venv/bin/activate
    ```

2.  **Ejecuta el script principal:**
    ```bash
    python blink_detector_dlib.py
    ```

3.  Una ventana de tu cámara web se abrirá. **Asegúrate de que el cursor de tu ratón esté en la ventana o aplicación que deseas controlar** (haz clic fuera de la ventana de la cámara si quieres controlar el escritorio).

4.  **Realiza los parpadeos:**
    - Parpadea solo con el ojo izquierdo para un **clic izquierdo**.
    - Parpadea solo con el ojo derecho para un **clic derecho**.
    - Parpadea con ambos ojos simultáneamente para un **doble clic**.

5.  Para salir del programa, presiona la tecla `q` en la ventana de la cámara.

## Notas Importantes
- La precisión de la detección de parpadeo puede variar según la iluminación y la configuración de tu cámara. Puedes ajustar `EYE_AR_THRESH` y `EYE_AR_CONSEC_FRAMES` en el código para mejorar la sensibilidad.
- Este proyecto demuestra el control del ratón; un sistema completo de control ocular requeriría también movimiento del cursor (ej. vía seguimiento de mirada).
- El desarrollo de este proyecto fue en Linux (Ubuntu)

---
