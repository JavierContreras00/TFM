import cv2
import json
import numpy as np
from ultralytics import YOLO

print("🔵 Programa iniciado")

# Cargar la imagen
ruta_imagen = "ejemplo.jpg"
imagen = cv2.imread(ruta_imagen)
imagen_rgb = cv2.cvtColor(imagen, cv2.COLOR_BGR2RGB)

# Cargar modelo YOLOv8
modelo = YOLO("yolov8n.pt")
resultados = modelo.predict(source=imagen_rgb, conf=0.3)[0]

# Leer anotaciones del JSON (formato COCO modificado)
with open("labels_my-project-name_2025-04-03-08-39-57.json", "r") as f:
    data = json.load(f)
anotaciones = data["annotations"]

# Inicializar contadores
total = len(anotaciones)
ocupadas = 0
libres = 0

# Dibujar vehículos detectados
for box in resultados.boxes:
    x1, y1, x2, y2 = map(int, box.xyxy[0])
    clase = int(box.cls[0])
    if clase == 2:  # coche
        cv2.rectangle(imagen, (x1, y1), (x2, y2), (0, 255, 0), 2)
        cv2.putText(imagen, "Vehículo", (x1, y1 - 5), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 255, 0), 1)

# Crear nueva imagen con espacio a la derecha
ancho_extra = 300
imagen_ampliada = np.zeros((imagen.shape[0], imagen.shape[1] + ancho_extra, 3), dtype=np.uint8)
imagen_ampliada[:, :imagen.shape[1]] = imagen

# Evaluar ocupación plaza por plaza
for plaza in anotaciones:
    puntos = plaza["segmentation"][0]
    coords = [(int(puntos[i]), int(puntos[i + 1])) for i in range(0, len(puntos), 2)]

    # Dibujar contorno
    cv2.polylines(imagen_ampliada, [np.array(coords)], isClosed=True, color=(255, 0, 0), thickness=2)

    # Crear máscara binaria
    mascara = np.zeros(imagen.shape[:2], dtype=np.uint8)
    cv2.fillPoly(mascara, [np.array(coords)], 255)

    ocupada = False
    for box in resultados.boxes:
        if int(box.cls[0]) == 2:
            x1, y1, x2, y2 = map(int, box.xyxy[0])
            centro_x = (x1 + x2) // 2
            centro_y = (y1 + y2) // 2
            if mascara[centro_y, centro_x] == 255:
                ocupada = True
                break

    color = (0, 0, 255) if ocupada else (0, 255, 0)
    texto = "Ocupada" if ocupada else "Libre"
    cv2.putText(imagen_ampliada, texto, coords[0], cv2.FONT_HERSHEY_SIMPLEX, 0.5, color, 2)

    if ocupada:
        ocupadas += 1
    else:
        libres += 1

# Mostrar resumen a la derecha
start_x = imagen.shape[1] + 10
cv2.putText(imagen_ampliada, "Resumen:", (start_x, 30), cv2.FONT_HERSHEY_SIMPLEX, 0.8, (0, 0, 0), 2)
cv2.putText(imagen_ampliada, f"Total plazas: {total}", (start_x, 70), cv2.FONT_HERSHEY_SIMPLEX, 0.7, (50, 50, 50), 2)
cv2.putText(imagen_ampliada, f"Ocupadas: {ocupadas}", (start_x, 110), cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 0, 255), 2)
cv2.putText(imagen_ampliada, f"Libres: {libres}", (start_x, 150), cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 128, 0), 2)

# Mostrar imagen y logs finales
print(f"✅ Total plazas: {total}")
print(f"🚗 Ocupadas: {ocupadas}")
print(f"🅿️ Libres: {libres}")
print("✅ Programa finalizado")

cv2.imshow("Detección de plazas", imagen_ampliada)
cv2.waitKey(0)
cv2.destroyAllWindows()
