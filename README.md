# FIXU AI Skills — Claude Code

Skills y agentes reutilizables para Claude Code, construidos por la comunidad de **FIXU AI**.

Diseñados para profesionales, ingenieros industriales y tesistas que quieren potenciar su flujo de trabajo con IA.

---

## Skills disponibles

| Skill | Descripción | Requiere |
|-------|-------------|----------|
| [`skills/ingenieria-industrial/`](skills/ingenieria-industrial/) | Genera DOPs y DAPs con simbología ASME | Python + drawpyo |

---

## ¿Cómo usar una skill?

1. Copia `asme_shapes.py` a tu proyecto (o a tu carpeta `.claude/skills/`)
2. Instala la dependencia: `pip install drawpyo`
3. Pídele a Claude que genere el diagrama — o ejecuta el script de ejemplo directamente

Ejemplo con Claude Code:
```
Genera un DOP del proceso de atención al cliente con estas actividades:
1. Recibir solicitud
2. Verificar datos del cliente
3. Procesar pedido
4. Confirmar al cliente
```

Claude leerá la skill y generará el archivo `.drawio` listo para abrir en [draw.io](https://app.diagrams.net).

---

## Comunidad

¿Construiste algo con estas skills? Abre un PR o comparte en la comunidad de FIXU AI.

- Instagram: [@fixuai](https://instagram.com/fixuai)

---

> Construido con [Claude Code](https://claude.ai/code) por Santiago Zavaleta / FIXU AI
