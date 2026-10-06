# 🎵 midi-orquesta

> **⚠️ ESTADO: EN DESARROLLO ⚠️**
> 
> Este proyecto está activamente en desarrollo. La API, la estructura y las composiciones pueden cambiar sin aviso previo. No usar en producción.

---

## Descripción

Compositor musical avanzado con orquesta completa. Genera archivos MIDI y audio (OGG) usando FluidSynth.

## Características

- **Orquesta completa:** 7-10 pistas por canción
- **Instrumentos variados:** Cuerdas, maderas, metales, percusión, arpa, coro
- **Técnicas avanzadas:** Contrapunto, orquestación, dinámica
- **3 composiciones incluidas:**
  - `01_sad_orchestra` — Concierto triste (D menor, 70 BPM)
  - `02_romeo_julieta` — Tema romántico (C mayor, 80 BPM)
  - `03_requiem` — Marcha fúnebre (E menor, 60 BPM)

## Requisitos

- Python 3.8+
- FluidSynth (`sudo apt install fluidsynth fluid-soundfont-gm`)
- ffmpeg (`sudo apt install ffmpeg`)

## Uso

```bash
python compositor_avanzado.py
```

Los archivos se generan en el directorio actual:
- `.mid` — Archivos MIDI editables
- `.ogg` — Audio renderizado
- `.wav` — Audio sin comprimir

## Estructura

```
midi-orquesta/
├── compositor_avanzado.py   # Script principal
└── README.md
```

## Licencia

MIT

---

**Última actualización:** 2026-10-06
