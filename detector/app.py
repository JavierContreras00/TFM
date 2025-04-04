import os
import json
import cv2
import numpy as np
from flask import Flask, render_template, jsonify
from ultralytics import YOLO
from detectar import DetectorAparcamiento

app = Flask(__name__)

@app.route("/")
def index():
    return render_template("index.html")

@app.route("/estado_parking")
def estado_parking():
    # Rutas
    modelo_path = "yolov8n.pt"
    json_path = "labels_my-project-name_2025-04-03-08-39-57.json"
    imagen_path = "static/ejemplo.jpg"

    # Inicializar detector
    detector = DetectorAparcamiento(modelo_path, json_path, imagen_path)
    libres, ocupadas = detector.detectar_ocupacion()

    total = libres + ocupadas
    plazas = []

    for idx, plaza in enumerate(detector.plazas):
        x, y, w, h = cv2.boundingRect(plaza)
        ocupada = any(
            cv2.pointPolygonTest(plaza, (int((x1 + x2) / 2), int((y1 + y2) / 2)), False) >= 0
            for (x1, y1, x2, y2) in detector.coordenadas_coches
        )
        estado = "OCUPADA" if ocupada else "LIBRE"
        plazas.append({"id": idx + 1, "estado": estado})

    return jsonify({
        "total": total,
        "libres": libres,
        "ocupadas": ocupadas,
        "plazas": plazas
    })

if __name__ == "__main__":
    app.run(debug=True)
