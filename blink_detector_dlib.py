# importar los paquetes necesarios
from scipy.spatial import distance as dist
from imutils.video import VideoStream
from imutils import face_utils
import numpy as np
import imutils
import time
import dlib
import cv2
import pyautogui

# Función para calcular la relación de aspecto del ojo (EAR)


def eye_aspect_ratio(eye):
    A = dist.euclidean(eye[1], eye[5])
    B = dist.euclidean(eye[2], eye[4])
    C = dist.euclidean(eye[0], eye[3])
    ear = (A + B) / (2.0 * C)
    return ear


# --- Configuración del modelo y constantes ---
# La ruta al predictor de forma facial pre-entrenado
SHAPE_PREDICTOR_PATH = "shape_predictor_68_face_landmarks.dat"

# Constantes para la detección de parpadeo
EYE_AR_THRESH = 0.24
EYE_AR_CONSEC_FRAMES = 3

# Constante para el tiempo de "cooldown" después de un clic (en segundos)
CLICK_COOLDOWN_TIME = 1.5
# Duración en segundos que el mensaje de clic permanecerá en pantalla
MESSAGE_DISPLAY_DURATION = 1.0  # 1 segundo

# inicializar contadores y variables de estado
left_COUNTER = 0
right_COUNTER = 0
TOTAL_BLINKS = 0

last_click_time = time.time()
current_blink_type = "Ninguno"

# Variables para controlar el mensaje en pantalla
display_message_until = 0  # El mensaje se mostrará hasta este tiempo
current_on_screen_message = ""  # El texto del mensaje actual

# inicializar el detector de rostros de dlib y el predictor de puntos de referencia
print("[INFO] cargando el predictor de puntos de referencia faciales...")
detector = dlib.get_frontal_face_detector()
predictor = dlib.shape_predictor(SHAPE_PREDICTOR_PATH)

# obtener los índices de los puntos de referencia faciales para los ojos izquierdo y derecho
(lStart, lEnd) = face_utils.FACIAL_LANDMARKS_IDXS["left_eye"]
(rStart, rEnd) = face_utils.FACIAL_LANDMARKS_IDXS["right_eye"]

# iniciar el flujo de video desde la webcam
print("[INFO] iniciando el hilo del flujo de video de la webcam...")
vs = VideoStream(src=0).start()
time.sleep(1.0)

# ajustar la velocidad de pyautogui (opcional, pero recomendado)
pyautogui.PAUSE = 0.01

# recorrer los fotogramas del flujo de video
while True:
    frame = vs.read()
    frame = imutils.resize(frame, width=600)
    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

    # detectar rostros
    rects = detector(gray, 0)

    # procesar cada rostro detectado
    for rect in rects:
        shape = predictor(gray, rect)
        shape = face_utils.shape_to_np(shape)

        leftEye = shape[lStart:lEnd]
        rightEye = shape[rStart:rEnd]
        leftEAR = eye_aspect_ratio(leftEye)
        rightEAR = eye_aspect_ratio(rightEye)

        # visualizar los ojos
        leftEyeHull = cv2.convexHull(leftEye)
        rightEyeHull = cv2.convexHull(rightEye)
        cv2.drawContours(frame, [leftEyeHull], -1, (0, 255, 0), 1)
        cv2.drawContours(frame, [rightEyeHull], -1, (0, 255, 0), 1)

        # --- Lógica de Detección de Parpadeo y Clic ---
        current_time = time.time()

        # Actualizar contadores si el ojo está cerrado
        if leftEAR < EYE_AR_THRESH:
            left_COUNTER += 1
        else:
            left_COUNTER = 0

        if rightEAR < EYE_AR_THRESH:
            right_COUNTER += 1
        else:
            right_COUNTER = 0

        # Verificar si se cumple la condición de parpadeo para realizar un clic, respetando el cooldown
        if (current_time - last_click_time) > CLICK_COOLDOWN_TIME:

            # Priorizar doble clic si ambos ojos parpadean simultáneamente
            if left_COUNTER >= EYE_AR_CONSEC_FRAMES and right_COUNTER >= EYE_AR_CONSEC_FRAMES:
                TOTAL_BLINKS += 1
                # DESCOMENTADO PARA CLIC REAL
                pyautogui.doubleClick(interval=0.1)
                current_blink_type = "Doble Clic"
                print("¡Doble Clic detectado y realizado!")
                current_on_screen_message = "!!! DOBLE CLIC !!!"  # Mensaje para mostrar
                display_message_until = current_time + MESSAGE_DISPLAY_DURATION  # Temporizador
                last_click_time = current_time
                left_COUNTER = 0
                right_COUNTER = 0

            # Si no es doble clic, verificar parpadeo del ojo izquierdo
            elif left_COUNTER >= EYE_AR_CONSEC_FRAMES:
                TOTAL_BLINKS += 1
                pyautogui.leftClick()  # DESCOMENTADO PARA CLIC REAL
                current_blink_type = "Clic Izquierdo"
                print("¡Clic Izquierdo detectado y realizado!")
                current_on_screen_message = "!!! CLIC IZQUIERDO !!!"  # Mensaje para mostrar
                display_message_until = current_time + MESSAGE_DISPLAY_DURATION  # Temporizador
                last_click_time = current_time
                left_COUNTER = 0

            # Si no es doble ni izquierdo, verificar parpadeo del ojo derecho
            elif right_COUNTER >= EYE_AR_CONSEC_FRAMES:
                TOTAL_BLINKS += 1
                pyautogui.rightClick()  # DESCOMENTADO PARA CLIC REAL
                current_blink_type = "Clic Derecho"
                print("¡Clic Derecho detectado y realizado!")
                current_on_screen_message = "!!! CLIC DERECHO !!!"  # Mensaje para mostrar
                display_message_until = current_time + MESSAGE_DISPLAY_DURATION  # Temporizador
                last_click_time = current_time
                right_COUNTER = 0

        # --- Fin de la Lógica de Detección de Parpadeo y Clic ---

        # Dibujar información en el fotograma
        cv2.putText(frame, "Parpadeos Total: {}".format(TOTAL_BLINKS), (10, 30),
                    cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 0, 255), 2)
        cv2.putText(frame, "EAR Izq: {:.2f}".format(leftEAR), (10, 60),
                    cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 0, 255), 2)
        cv2.putText(frame, "EAR Der: {:.2f}".format(rightEAR), (10, 90),
                    cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 0, 255), 2)
        cv2.putText(frame, "Ultimo Clic: {}".format(current_blink_type), (10, 120),
                    cv2.FONT_HERSHEY_SIMPLEX, 0.7, (255, 0, 0), 2)

        # Mostrar tiempo de cooldown restante
        if (time.time() - last_click_time) < CLICK_COOLDOWN_TIME:
            remaining_cooldown = int(
                CLICK_COOLDOWN_TIME - (time.time() - last_click_time)) + 1
            cv2.putText(frame, "Cooldown: {}s".format(remaining_cooldown), (400, 30),
                        cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 255, 255), 2)

        # Mostrar el mensaje de clic si el temporizador está activo
        if current_time < display_message_until and current_on_screen_message:
            cv2.putText(frame, current_on_screen_message, (150, 250),
                        cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 0, 255), 3)

    # mostrar el fotograma
    cv2.imshow("Control de Clic por Parpadeo", frame)
    key = cv2.waitKey(1) & 0xFF

    # si la tecla `q` fue presionada, salir del bucle
    if key == ord("q"):
        break

# limpiar
cv2.destroyAllWindows()
vs.stop()
