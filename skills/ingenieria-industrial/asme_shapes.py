"""
asme_shapes.py — Generador de DOPs y DAPs con simbologia ASME via drawpyo

Uso:
    from asme_shapes import generate_dap, generate_dop

Tipos de actividad validos:
    "operacion"      — circulo (O)
    "transporte"     — flecha singleArrow (=>)
    "inspeccion"     — cuadrado (□)
    "demora"         — forma D (D)
    "almacenamiento" — triangulo invertido (▽)
    "op_insp"        — operacion + inspeccion combinada (circulo con cuadrado)

Fuente: drawpyo 0.2.5 — https://github.com/MerrimanInd/drawpyo
"""

import os
import drawpyo
import drawpyo.diagram

# ---------------------------------------------------------------------------
# Constantes de layout
# ---------------------------------------------------------------------------
COL_TIEMPO   = 130   # x de la columna "Tiempo"
COL_SIMBOLO  = 300   # x centro de la columna de simbolos ASME
COL_DESC     = 510   # x de la columna "Descripcion"
ROW_HEIGHT   = 110   # separacion vertical entre pasos
ROW_MARGIN   = 80    # margen superior (primer paso)
HEADER_Y     = 30    # y del encabezado
NUM_OFFSET   = 42    # px por encima del centro del simbolo para el numero de paso

COLORES_TIPO = {
    "operacion":      "#DAE8FC",   # azul claro
    "transporte":     "#D5E8D4",   # verde claro
    "inspeccion":     "#FFF2CC",   # amarillo claro
    "demora":         "#FFE6CC",   # naranja claro
    "almacenamiento": "#E1D5E7",   # violeta claro
    "op_insp":        "#F8CECC",   # rojo claro
}

# ---------------------------------------------------------------------------
# Helpers internos
# ---------------------------------------------------------------------------

def _text(page, value, x, y, w=100, h=25, align="center", bold=False):
    """Crea un objeto de solo texto."""
    style = f"text;html=1;align={align};verticalAlign=middle;whiteSpace=wrap;"
    if bold:
        style += "fontStyle=1;"
    obj = drawpyo.diagram.Object(page=page, value=value)
    obj.apply_style_string(style)
    obj.width = w
    obj.height = h
    obj.position = (x - w // 2, y - h // 2)
    return obj


def _encabezado(page, titulo):
    """Dibuja el encabezado del DAP/DOP con titulo y columnas."""
    titulo_obj = drawpyo.diagram.Object(page=page, value=f"<b>{titulo}</b>")
    titulo_obj.apply_style_string(
        "text;html=1;align=center;fontSize=14;fontStyle=1;whiteSpace=wrap;"
    )
    titulo_obj.width = 600
    titulo_obj.height = 35
    titulo_obj.position = (COL_SIMBOLO - 270, HEADER_Y)

    headers = [
        (COL_TIEMPO,  "Tiempo (min)"),
        (COL_SIMBOLO, "Simbolo ASME"),
        (COL_DESC,    "Descripcion"),
    ]
    for x, label in headers:
        _text(page, label, x, HEADER_Y + 45, w=150, h=25, bold=True)


def _simbolo_operacion(page, y, color):
    obj = drawpyo.diagram.object_from_library(
        library="general", obj_name="circle",
        fillColor=color, strokeColor="#000000",
        width=55, height=55
    )
    obj.page = page
    obj.center_position = (COL_SIMBOLO, y)
    return obj


def _simbolo_inspeccion(page, y, color):
    obj = drawpyo.diagram.object_from_library(
        library="general", obj_name="square",
        fillColor=color, strokeColor="#000000",
        width=55, height=55
    )
    obj.page = page
    obj.center_position = (COL_SIMBOLO, y)
    return obj


def _simbolo_transporte(page, y, color):
    obj = drawpyo.diagram.Object(page=page, value="")
    obj.apply_style_string(
        f"shape=singleArrow;whiteSpace=wrap;html=1;"
        f"fillColor={color};strokeColor=#000000;"
        f"arrowWidth=0.4;arrowSize=0.35;"
    )
    obj.width = 80
    obj.height = 45
    obj.center_position = (COL_SIMBOLO, y)
    return obj


def _simbolo_demora(page, y, color):
    obj = drawpyo.diagram.object_from_library(
        library="flowchart", obj_name="delay",
        fillColor=color, strokeColor="#000000",
        width=80, height=50
    )
    obj.page = page
    obj.center_position = (COL_SIMBOLO, y)
    return obj


def _simbolo_almacenamiento(page, y, color):
    obj = drawpyo.diagram.Object(page=page, value="")
    obj.apply_style_string(
        f"triangle;whiteSpace=wrap;html=1;"
        f"direction=south;fillColor={color};strokeColor=#000000;"
    )
    obj.width = 55
    obj.height = 55
    obj.center_position = (COL_SIMBOLO, y)
    return obj


def _simbolo_op_insp(page, y, color):
    """Circulo con cuadrado inscrito (operacion + inspeccion combinada)."""
    circ = drawpyo.diagram.Object(page=page, value="")
    circ.apply_style_string(
        f"ellipse;whiteSpace=wrap;html=1;"
        f"fillColor={color};strokeColor=#000000;"
    )
    circ.width = 60
    circ.height = 60
    circ.center_position = (COL_SIMBOLO, y)

    sq = drawpyo.diagram.Object(page=page, value="")
    sq.apply_style_string(
        "whiteSpace=wrap;html=1;"
        "fillColor=#ffffff;strokeColor=#000000;opacity=0;"
    )
    sq.width = 30
    sq.height = 30
    sq.center_position = (COL_SIMBOLO, y)
    return circ


_BUILDERS = {
    "operacion":      _simbolo_operacion,
    "transporte":     _simbolo_transporte,
    "inspeccion":     _simbolo_inspeccion,
    "demora":         _simbolo_demora,
    "almacenamiento": _simbolo_almacenamiento,
    "op_insp":        _simbolo_op_insp,
}

# ---------------------------------------------------------------------------
# API publica
# ---------------------------------------------------------------------------

def add_step(page, row_n, tipo, descripcion, tiempo_min=None):
    """
    Agrega un paso ASME al diagrama y retorna el nodo principal.

    Args:
        page:          drawpyo.Page donde se dibuja
        row_n:         indice de fila (0, 1, 2, ...)
        tipo:          str — ver tipos validos en el modulo
        descripcion:   str — texto de la actividad
        tiempo_min:    float | None — tiempo en minutos

    Returns:
        El objeto drawpyo del simbolo ASME creado.
    """
    tipo = tipo.lower().strip()
    if tipo not in _BUILDERS:
        raise ValueError(
            f"Tipo '{tipo}' no valido. Validos: {list(_BUILDERS.keys())}"
        )

    y = ROW_MARGIN + HEADER_Y + 60 + ROW_HEIGHT * row_n
    color = COLORES_TIPO.get(tipo, "#ffffff")

    nodo = _BUILDERS[tipo](page, y, color)

    # Numero de paso encima del simbolo
    _text(page, str(row_n + 1), COL_SIMBOLO, y - NUM_OFFSET, w=30, h=20)

    # Descripcion
    _text(page, descripcion, COL_DESC, y, w=240, h=50, align="left")

    # Tiempo
    if tiempo_min is not None:
        _text(page, str(tiempo_min), COL_TIEMPO, y, w=100)

    return nodo


def connect_steps(page, source, target):
    """Conecta dos pasos con linea vertical."""
    return drawpyo.diagram.Edge(
        page=page,
        source=source,
        target=target,
        exitX=0.5, exitY=1,
        entryX=0.5, entryY=0,
    )


def _resumen(page, pasos, y_final):
    """Agrega cuadro de resumen de totales al final del diagrama."""
    conteo = {t: 0 for t in _BUILDERS}
    total_tiempo = 0

    for p in pasos:
        t = p.get("tipo", "").lower().strip()
        if t in conteo:
            conteo[t] += 1
        total_tiempo += p.get("tiempo_min") or 0

    simbolos = {
        "operacion":      "O",
        "transporte":     "=>",
        "inspeccion":     "□",
        "demora":         "D",
        "almacenamiento": "▽",
        "op_insp":        "O+□",
    }

    lines = ["<b>RESUMEN</b>"]
    for tipo, sym in simbolos.items():
        if conteo[tipo] > 0:
            lines.append(f"{sym} {tipo.capitalize()}: {conteo[tipo]}")
    lines.append(f"Tiempo total: {total_tiempo} min")

    resumen = drawpyo.diagram.Object(
        page=page, value="<br>".join(lines)
    )
    resumen.apply_style_string(
        "whiteSpace=wrap;html=1;align=left;verticalAlign=top;"
        "fillColor=#f5f5f5;strokeColor=#666666;fontColor=#333333;"
    )
    resumen.width = 220
    resumen.height = 30 + len(lines) * 18
    resumen.position = (COL_SIMBOLO + 120, y_final + 20)


def generate_dap(nombre_proceso, pasos, output_dir, filename=None, _tipo="DAP"):
    """
    Genera un DAP completo con simbologia ASME y lo guarda como .drawio.

    Args:
        nombre_proceso: str — nombre del proceso (aparece como titulo)
        pasos:          list[dict] — lista de pasos, cada uno con:
                          tipo        (str, obligatorio)
                          descripcion (str, obligatorio)
                          tiempo_min  (float, opcional)
        output_dir:     str — directorio donde guardar el archivo
        filename:       str | None — nombre del archivo sin extension

    Returns:
        str — ruta completa del archivo .drawio generado
    """
    os.makedirs(output_dir, exist_ok=True)

    fname = filename or f"{_tipo}_{nombre_proceso.replace(' ', '_')}"
    file = drawpyo.File()
    file.file_name = f"{fname}.drawio"
    file.file_path = output_dir
    page = drawpyo.Page(file=file)
    page.name = nombre_proceso

    _encabezado(page, f"{_tipo} — {nombre_proceso}")

    nodos = []
    for i, paso in enumerate(pasos):
        nodo = add_step(
            page=page,
            row_n=i,
            tipo=paso["tipo"],
            descripcion=paso["descripcion"],
            tiempo_min=paso.get("tiempo_min"),
        )
        nodos.append(nodo)
        if i > 0:
            connect_steps(page, nodos[i - 1], nodos[i])

    y_final = ROW_MARGIN + HEADER_Y + 60 + ROW_HEIGHT * len(pasos)
    _resumen(page, pasos, y_final)

    file.write()
    return os.path.join(output_dir, file.file_name)


def generate_dop(nombre_producto, materiales, operaciones, output_dir, filename=None):
    """
    Genera un DOP (Diagrama de Operaciones del Proceso).
    Solo incluye Operaciones (O), Inspecciones (□) y Combinadas (O+□).

    Args:
        nombre_producto: str — nombre del producto o servicio
        materiales:      list[str] — lista de materiales/entradas (referencia)
        operaciones:     list[dict] — pasos del proceso
        output_dir:      str — directorio de salida
        filename:        str | None

    Returns:
        str — ruta del archivo .drawio generado
    """
    pasos_validos = []
    for p in operaciones:
        t = p.get("tipo", "").lower().strip()
        if t not in ("operacion", "inspeccion", "op_insp"):
            raise ValueError(
                f"DOP solo acepta 'operacion', 'inspeccion' u 'op_insp'. Recibido: '{t}'"
            )
        pasos_validos.append(p)

    return generate_dap(
        nombre_proceso=nombre_producto,
        pasos=pasos_validos,
        output_dir=output_dir,
        filename=filename or f"DOP_{nombre_producto.replace(' ', '_')}",
        _tipo="DOP",
    )


# ---------------------------------------------------------------------------
# CLI minimo para prueba rapida
# ---------------------------------------------------------------------------
if __name__ == "__main__":
    import sys

    output = sys.argv[1] if len(sys.argv) > 1 else "."

    pasos_demo = [
        {"tipo": "operacion",  "descripcion": "Lead ingresa por WhatsApp",        "tiempo_min": 0},
        {"tipo": "operacion",  "descripcion": "Agente IA recibe y procesa",        "tiempo_min": 0.5},
        {"tipo": "inspeccion", "descripcion": "Verificar interes real del lead",   "tiempo_min": 1},
        {"tipo": "demora",     "descripcion": "Espera disponibilidad asesor",      "tiempo_min": 15},
        {"tipo": "operacion",  "descripcion": "Asesor atiende al lead",            "tiempo_min": 20},
        {"tipo": "inspeccion", "descripcion": "Calificar como prospecto",          "tiempo_min": 5},
        {"tipo": "operacion",  "descripcion": "Registrar en CRM",                  "tiempo_min": 2},
    ]

    ruta = generate_dap(
        nombre_proceso="Atencion de Lead — Cumbres (As-Is)",
        pasos=pasos_demo,
        output_dir=output,
    )
    print(f"DAP generado: {ruta}")
