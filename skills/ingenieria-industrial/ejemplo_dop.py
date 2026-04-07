"""
ejemplo_dop.py — Genera un DOP de ejemplo con simbología ASME.

Instalación:
    pip install drawpyo

Ejecutar:
    python ejemplo_dop.py

Resultado: DOP_Gestion_de_Pedidos.drawio — abrir en https://app.diagrams.net
"""
from asme_shapes import generate_dop

pasos = [
    {"tipo": "operacion",  "descripcion": "Recibir pedido del cliente",       "tiempo_min": 2},
    {"tipo": "inspeccion", "descripcion": "Verificar disponibilidad en stock", "tiempo_min": 3},
    {"tipo": "operacion",  "descripcion": "Preparar y empacar pedido",         "tiempo_min": 15},
    {"tipo": "inspeccion", "descripcion": "Inspeccionar calidad del pedido",   "tiempo_min": 5},
    {"tipo": "operacion",  "descripcion": "Registrar salida en sistema",        "tiempo_min": 2},
    {"tipo": "operacion",  "descripcion": "Despachar al cliente",              "tiempo_min": 3},
]

path = generate_dop(
    nombre_producto="Gestión de Pedidos",
    materiales=["Pedido del cliente"],
    operaciones=pasos,
    output_dir=".",
    filename="DOP_Gestion_de_Pedidos",
)

print(f"DOP generado: {path}")
print("Abre el archivo en: https://app.diagrams.net")
