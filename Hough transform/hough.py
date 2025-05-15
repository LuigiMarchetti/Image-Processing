"""
Autores: Ari Elias da Silva Júnior e Luigi Garcia Marchetti
"""

import cv2
import os
import numpy as np
import shutil


def setup_output_directory(output_path):
    """Limpa e cria o diretório de saída."""
    if os.path.isdir(output_path):
        shutil.rmtree(output_path)
    os.makedirs(output_path, exist_ok=True)
    print(f"Diretório de saída configurado: {output_path}")


def detect_circle(gray_image, param1, param2, min_radius, max_radius):
    """
    Tenta detectar um círculo usando diferentes níveis de blur.
    Retorna as coordenadas e raio do círculo ou None.
    """
    for blur in [11, 9, 7, 5, 3, 1]:
        blurred = cv2.medianBlur(gray_image, blur)

        circles = cv2.HoughCircles(
            blurred, cv2.HOUGH_GRADIENT, dp=1, minDist=50,
            param1=param1, param2=param2,
            minRadius=min_radius, maxRadius=max_radius
        )

        if circles is not None:
            return np.uint16(np.around(circles))[0][0]

    return None


def process_image(image_path, output_path, filename):
    """Processa uma imagem para isolar a íris."""
    # Parâmetros para detecção
    iris_params = {"param1": 60, "param2": 60, "min_radius": 120, "max_radius": 210}
    pupil_params = {"param1": 40, "param2": 30, "min_radius": 22, "max_radius": 60}
    threshold_value = 50

    # Carrega e corta a imagem
    image = cv2.imread(image_path)
    if image is None:
        print(f"\033[31m[ERRO] {image_path}\033[0m")
        return False

    height, width = image.shape[:2]
    cropped = image[660:height-660, 800:width-800].copy()

    # Pré-processamento
    gray = cv2.cvtColor(cropped, cv2.COLOR_BGR2GRAY)
    _, threshold = cv2.threshold(gray, threshold_value, 255, cv2.THRESH_BINARY)

    # Destaca regiões claras
    dark = (cropped * 0.2).astype(np.uint8)
    enhanced = dark.copy()
    mask_bool = (threshold == 255)

    for c in range(3):
        enhanced[:, :, c] = np.where(mask_bool, cropped[:, :, c], dark[:, :, c])

    # Detecta íris
    processed_gray = cv2.cvtColor(enhanced, cv2.COLOR_BGR2GRAY)
    iris_circle = detect_circle(processed_gray, **iris_params)

    if iris_circle is None:
        return False

    # Cria máscara para a íris
    x, y, r = iris_circle
    iris_mask = np.zeros_like(processed_gray)
    cv2.circle(iris_mask, (x, y), r, 255, thickness=-1)

    # Isola a íris
    iris_result = cv2.bitwise_and(cropped, cropped, mask=iris_mask)

    # Detecta e remove a pupila
    result_gray = cv2.cvtColor(iris_result, cv2.COLOR_BGR2GRAY)
    pupil_circle = detect_circle(result_gray, **pupil_params)

    if pupil_circle is not None:
        x, y, r = pupil_circle
        cv2.circle(iris_mask, (x, y), r + 5, 0, thickness=-1)
        iris_result = cv2.bitwise_and(cropped, cropped, mask=iris_mask)

    # Salva o resultado
    result_path = os.path.join(output_path, filename)
    cv2.imwrite(result_path, iris_result)
    print(f"\033[32m[SUCESSO] {result_path}\033[0m")
    return True


input_path = './Iris'
output_path = './Resultados'

# Setup
setup_output_directory(output_path)

# Processa todas as imagens
processed = 0
total = 0

for filename in os.listdir(input_path):
    if filename.lower().endswith(('.jpg', '.jpeg', '.png')):
        total += 1
        image_path = os.path.join(input_path, filename)

        if process_image(image_path, output_path, filename):
            processed += 1

print(f"Processamento concluído: {processed}/{total} imagens processadas")