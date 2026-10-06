# 🎵 midi-orquesta

> **⚠️ STATUS: WORK IN PROGRESS ⚠️**
> 
> This project is actively under development. The API, structure, and compositions may change without prior notice. Do not use in production.

---

## Description

Advanced music composer with full orchestra. Generates MIDI and audio (OGG) files using FluidSynth.

## Features

- **Full orchestra:** 7-10 tracks per composition
- **Varied instruments:** Strings, woodwinds, brass, percussion, harp, choir
- **Advanced techniques:** Counterpoint, orchestration, dynamics
- **3 included compositions:**
  - `01_sad_orchestra` — Sad concert (D minor, 70 BPM)
  - `02_romeo_julieta` — Romantic theme (C major, 80 BPM)
  - `03_requiem` — Funeral march (E minor, 60 BPM)

## Requirements

- Python 3.8+
- FluidSynth (`sudo apt install fluidsynth fluid-soundfont-gm`)
- ffmpeg (`sudo apt install ffmpeg`)

## Usage

```bash
python compositor_avanzado.py
```

Files are generated in the current directory:
- `.mid` — Editable MIDI files
- `.ogg` — Rendered audio
- `.wav` — Uncompressed audio

## Structure

```
midi-orquesta/
├── compositor_avanzado.py   # Main script
└── README.md
```

## License

MIT

---

**Last updated:** 2026-10-06
