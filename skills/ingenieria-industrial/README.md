# Skill: Diagramas de Ingeniería Industrial (DOP / DAP)

Genera **Diagramas de Operaciones del Proceso (DOP)** y **Diagramas de Análisis del Proceso (DAP)** con simbología ASME, listos para abrir en [draw.io](https://app.diagrams.net) y exportar a PDF o PNG.

Funciona con Claude Code: descríbele tu proceso en lenguaje natural y él genera el archivo `.drawio` automáticamente.

## ¿Qué genera?

- Archivos `.drawio` con símbolos ASME correctos (abre en draw.io / diagrams.net)
- Número de paso encima de cada símbolo
- Cuadro de resumen automático (conteo por tipo + tiempo total)
- Colores diferenciados por tipo de actividad

## Símbolos ASME soportados

| Símbolo | Tipo en código | Descripción |
|---------|---------------|-------------|
| ○ | `operacion` | Operación |
| □ | `inspeccion` | Inspección |
| ○□ | `op_insp` | Operación + Inspección combinada |
| ➜ | `transporte` | Transporte *(solo DAP)* |
| D | `demora` | Demora / Espera *(solo DAP)* |
| ▽ | `almacenamiento` | Almacenamiento *(solo DAP)* |

## Instalación

```bash
pip install drawpyo
```

Copia `asme_shapes.py` a tu proyecto. No requiere instalación adicional.

## Uso con Claude Code

Abre Claude Code en tu proyecto y escribe:

```
Genera un DOP del proceso de admisión de pacientes. Los pasos son:
1. Recibir al paciente en recepción
2. Verificar si tiene cita previa
3. Registrar datos en el sistema
4. Asignar número de atención
5. Derivar al área correspondiente
6. Confirmar registro al paciente

Usa la skill asme_shapes.py que está en .claude/skills/
```

Claude generará el `.drawio` directamente.

## Uso directo en Python

```python
from asme_shapes import generate_dop, generate_dap

# DOP — solo operaciones e inspecciones
pasos_dop = [
    {"tipo": "operacion",  "descripcion": "Recibir pedido del cliente",       "tiempo_min": 2},
    {"tipo": "inspeccion", "descripcion": "Verificar disponibilidad en stock", "tiempo_min": 3},
    {"tipo": "operacion",  "descripcion": "Preparar y empacar pedido",         "tiempo_min": 15},
    {"tipo": "inspeccion", "descripcion": "Inspeccionar calidad del pedido",   "tiempo_min": 5},
    {"tipo": "operacion",  "descripcion": "Despachar al cliente",              "tiempo_min": 3},
]

path = generate_dop(
    nombre_producto="Gestión de Pedidos",
    materiales=["Pedido del cliente"],
    operaciones=pasos_dop,
    output_dir="./figuras",
)
print(f"DOP generado: {path}")
```

```python
# DAP — incluye los 5 símbolos ASME
pasos_dap = [
    {"tipo": "operacion",      "descripcion": "Recibir pedido",           "tiempo_min": 2},
    {"tipo": "transporte",     "descripcion": "Trasladar a almacén",       "tiempo_min": 5},
    {"tipo": "demora",         "descripcion": "Espera en cola",            "tiempo_min": 30},
    {"tipo": "inspeccion",     "descripcion": "Verificar stock",           "tiempo_min": 3},
    {"tipo": "operacion",      "descripcion": "Preparar pedido",           "tiempo_min": 15},
    {"tipo": "inspeccion",     "descripcion": "Control de calidad",        "tiempo_min": 5},
    {"tipo": "almacenamiento", "descripcion": "Registrar salida",          "tiempo_min": 2},
    {"tipo": "operacion",      "descripcion": "Entregar al courier",       "tiempo_min": 3},
]

path = generate_dap(
    nombre_proceso="Proceso de Pedidos — As-Is",
    pasos=pasos_dap,
    output_dir="./figuras",
)
print(f"DAP generado: {path}")
```

## Abrir el resultado

1. Ve a **[app.diagrams.net](https://app.diagrams.net)**
2. Abre el archivo `.drawio` generado
3. Exporta a PNG, PDF o SVG

## Archivos

| Archivo | Descripción |
|---------|-------------|
| `asme_shapes.py` | Librería principal — importar en tus scripts |
| `ejemplo_dop.py` | Ejemplo listo para ejecutar — DOP |
| `ejemplo_dap.py` | Ejemplo listo para ejecutar — DAP |

---

> Skill construida con [Claude Code](https://claude.ai/code) · FIXU AI
