"""
ejemplo_dap.py — Genera un DAP de ejemplo con los 5 símbolos ASME.

Instalación:
    pip install drawpyo

Ejecutar:
    python ejemplo_dap.py

Resultado: DAP_Proceso_de_Pedidos.drawio — abrir en https://app.diagrams.net
"""
from asme_shapes import generate_dap

pasos = [
    {"tipo": "operacion",      "descripcion": "Recibir pedido del cliente",      "tiempo_min": 2},
    {"tipo": "transporte",     "descripcion": "Trasladar orden a almacén",        "tiempo_min": 5},
    {"tipo": "demora",         "descripcion": "Espera en cola de preparación",    "tiempo_min": 30},
    {"tipo": "inspeccion",     "descripcion": "Verificar disponibilidad en stock","tiempo_min": 3},
    {"tipo": "operacion",      "descripcion": "Preparar y empacar pedido",        "tiempo_min": 15},
    {"tipo": "inspeccion",     "descripcion": "Inspeccionar calidad del pedido",  "tiempo_min": 5},
    {"tipo": "operacion",      "descripcion": "Registrar salida en sistema",       "tiempo_min": 2},
    {"tipo": "transporte",     "descripcion": "Trasladar a zona de despacho",     "tiempo_min": 3},
    {"tipo": "almacenamiento", "descripcion": "Aguardar recolección del courier", "tiempo_min": 60},
    {"tipo": "operacion",      "descripcion": "Entregar al courier / cliente",    "tiempo_min": 5},
]

path = generate_dap(
    nombre_proceso="Proceso de Pedidos — As-Is",
    pasos=pasos,
    output_dir=".",
    filename="DAP_Proceso_de_Pedidos",
)

print(f"DAP generado: {path}")
print("Abre el archivo en: https://app.diagrams.net")
