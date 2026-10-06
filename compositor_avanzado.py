#!/usr/bin/env python3
"""
Composición musical avanzada: 3 canciones con orquesta completa.
Estilos complejos, instrumentos variados, técnicas contrapuntísticas.
"""

import mido
from mido import MidiFile, MidiTrack, Message, MetaMessage
import os
import random
import subprocess
import shutil

# Configuración
TPQ = 480
OUTPUT_DIR = "/home/gerardo/Desktop"
SOUNDFONT = "/usr/share/sounds/sf3/MuseScore_General.sf3"

# Instrumentos GM
INST = {
    'piano': 0, 'violin': 40, 'viola': 41, 'cello': 42, 'contrabass': 43,
    'flute': 73, 'oboe': 68, 'clarinet': 71, 'bassoon': 70,
    'french_horn': 60, 'trumpet': 56, 'trombone': 57, 'tuba': 58,
    'timpani': 47, 'harp': 46, 'strings': 48, 'choir': 52,
    'glockensiel': 9, 'celesta': 8, 'vibraphone': 11,
}

def note_to_midi(note_str):
    """Convertir nota a número MIDI. Acepta 'D' (octava 4 por defecto) o 'D4'."""
    notes = {'C': 0, 'C#': 1, 'Db': 1, 'D': 2, 'D#': 3, 'Eb': 3,
             'E': 4, 'F': 5, 'F#': 6, 'Gb': 6, 'G': 7, 'G#': 8,
             'Ab': 8, 'A': 9, 'A#': 10, 'Bb': 10, 'B': 11}
    # Separar nota de octava
    if len(note_str) >= 2 and note_str[-1].isdigit():
        note = note_str[:-1]
        octave = int(note_str[-1])
    else:
        note = note_str
        octave = 4  # Octava por defecto
    if note not in notes:
        raise ValueError(f"Nota inválida: {note_str}")
    return (octave + 1) * 12 + notes[note]

def create_track(name, program, channel, notes_data):
    """Crear pista MIDI con notas"""
    track = MidiTrack()
    track.append(MetaMessage('track_name', name=name, time=0))
    track.append(Message('program_change', program=program, channel=channel, time=0))
    
    events = []
    for note, vel, start, dur in notes_data:
        start_tick = int(start * TPQ)
        end_tick = int((start + dur) * TPQ)
        events.append((start_tick, 'on', note, vel))
        events.append((end_tick, 'off', note, 0))
    
    events.sort(key=lambda e: (e[0], 0 if e[1] == 'off' else 1))
    
    current_tick = 0
    for tick, event_type, pitch, velocity in events:
        delta = max(0, tick - current_tick)
        if event_type == 'on':
            track.append(Message('note_on', note=pitch, velocity=velocity, channel=channel, time=delta))
        else:
            track.append(Message('note_off', note=pitch, velocity=0, channel=channel, time=delta))
        current_tick = tick
    
    track.append(MetaMessage('end_of_track', time=0))
    return track

def render_wav(mid_path):
    """Renderizar MIDI a WAV"""
    wav_path = mid_path.replace('.mid', '.wav')
    cmd = ['/usr/bin/fluidsynth', '-ni', '-F', wav_path, '-r', '44100', '-g', '0.4', '-z', '64', SOUNDFONT, mid_path]
    subprocess.run(cmd, capture_output=True, timeout=120)
    return wav_path

def convert_ogg(wav_path):
    """Convertir WAV a OGG"""
    ogg_path = wav_path.replace('.wav', '.ogg')
    cmd = ['/usr/bin/ffmpeg', '-y', '-i', wav_path, '-af', 'loudnorm=I=-16:TP=-1.5:LRA=11', '-c:a', 'libvorbis', '-q:a', '5', ogg_path]
    subprocess.run(cmd, capture_output=True, timeout=300)
    return ogg_path

print("Compositor avanzado listo.")
print(f"Salida: {OUTPUT_DIR}")

# ============================================================
# CANCIÓN 1: Concierto de orquesta — canción triste
# D menor, 70 BPM, orquesta completa con técnicas contrapuntísticas
# ============================================================

def compose_sad_orchestra():
    """Concierto triste con orquesta completa"""
    mid = MidiFile(ticks_per_beat=TPQ)
    bpm = 70
    beats_per_bar = 4
    total_bars = 24
    
    # Progresión: Dm - Bb - F - A - Dm - Gm - A - Dm
    progression = [
        ('D', 'minor'), ('Bb', 'major'), ('F', 'major'), ('A', 'major'),
        ('D', 'minor'), ('G', 'minor'), ('A', 'major'), ('D', 'minor'),
    ]
    
    # Escala D menor natural
    d_minor = [62, 64, 65, 67, 69, 70, 72]  # D E F G A Bb C
    
    # Pista 1: Violines I (melodía principal)
    violin1_notes = []
    # Intro: arpegio descendente lento
    melody_intro = [
        (74, 35, 0, 2), (72, 30, 2, 2), (70, 28, 4, 2), (69, 25, 6, 2),
        (67, 30, 8, 2), (65, 28, 10, 2), (64, 25, 12, 2), (62, 20, 14, 2),
    ]
    violin1_notes.extend(melody_intro)
    
    # Desarrollo: melodía con cromatismo expresivo
    melody_dev = [
        (62, 40, 16, 1), (64, 45, 17, 1), (65, 50, 18, 2), (67, 45, 20, 1),
        (69, 50, 21, 1), (70, 55, 22, 2), (72, 50, 24, 1), (74, 55, 25, 1),
        (72, 50, 26, 2), (70, 45, 28, 1), (69, 40, 29, 1), (67, 35, 30, 2),
        (65, 40, 32, 1), (67, 45, 33, 1), (69, 50, 34, 2), (70, 55, 36, 1),
        (72, 60, 37, 1), (74, 65, 38, 2), (76, 60, 40, 1), (77, 55, 41, 1),
        (76, 50, 42, 2), (74, 45, 44, 1), (72, 40, 45, 1), (70, 35, 46, 2),
    ]
    violin1_notes.extend(melody_dev)
    
    # Clímax: notas altas con intensidad
    melody_climax = [
        (74, 70, 48, 1), (76, 75, 49, 1), (77, 80, 50, 2), (79, 75, 52, 1),
        (77, 70, 53, 1), (76, 65, 54, 2), (74, 60, 56, 1), (72, 55, 57, 1),
        (70, 50, 58, 2), (69, 45, 60, 1), (67, 40, 61, 1), (65, 35, 62, 2),
    ]
    violin1_notes.extend(melody_climax)
    
    # Resolución: retorno a tónica
    melody_end = [
        (64, 30, 64, 2), (62, 25, 66, 2), (60, 20, 68, 4),
    ]
    violin1_notes.extend(melody_end)
    
    mid.tracks.append(create_track("Violin I", INST['violin'], 0, violin1_notes))
    
    # Pista 2: Violines II (armonía en terceras)
    violin2_notes = []
    for note, vel, start, dur in violin1_notes:
        if vel > 30:
            harmony_note = note + 4 if note + 4 <= 84 else note - 3
            violin2_notes.append((harmony_note, vel - 10, start, dur))
    mid.tracks.append(create_track("Violin II", INST['violin'], 1, violin2_notes))
    
    # Pista 3: Violas (quintas y octavas)
    viola_notes = []
    for note, vel, start, dur in violin1_notes[::2]:
        viola_notes.append((note - 7, vel - 15, start, dur))
    mid.tracks.append(create_track("Viola", INST['viola'], 2, viola_notes))
    
    # Pista 4: Cellos (bajo melódico)
    cello_notes = []
    for note, vel, start, dur in violin1_notes[::3]:
        cello_notes.append((note - 12, vel - 10, start, dur))
    mid.tracks.append(create_track("Cello", INST['cello'], 3, cello_notes))
    
    # Pista 5: Contrabajo (raíz de acordes)
    bass_notes = []
    for bar in range(total_bars):
        root_note = note_to_midi(progression[bar % len(progression)][0]) - 24
        bass_notes.append((root_note, 45, bar * 4, 2))
        bass_notes.append((root_note + 7, 40, bar * 4 + 2, 2))
    mid.tracks.append(create_track("Contrabass", INST['contrabass'], 4, bass_notes))
    
    # Pista 6: Oboe (contramelodía cromática)
    oboe_notes = [
        (69, 25, 0, 4), (70, 28, 4, 4), (72, 30, 8, 4), (74, 32, 12, 4),
        (72, 28, 16, 4), (70, 25, 20, 4), (69, 22, 24, 4), (67, 20, 28, 4),
        (65, 25, 32, 4), (67, 28, 36, 4), (69, 30, 40, 4), (70, 32, 44, 4),
        (72, 35, 48, 4), (70, 32, 52, 4), (69, 28, 56, 4), (67, 25, 60, 4),
    ]
    mid.tracks.append(create_track("Oboe", INST['oboe'], 5, oboe_notes))
    
    # Pista 7: Trompa francesa (sostenidos armónicos)
    horn_notes = []
    for bar in range(0, total_bars, 2):
        root = note_to_midi(progression[bar % len(progression)][0]) - 12
        horn_notes.append((root, 30, bar * 4, 8))
        horn_notes.append((root + 7, 25, bar * 4, 8))
    mid.tracks.append(create_track("French Horn", INST['french_horn'], 6, horn_notes))
    
    # Pista 8: Arpa (arpegios etéreos)
    harp_notes = []
    for bar in range(total_bars):
        root = note_to_midi(progression[bar % len(progression)][0]) + 12
        for beat in range(4):
            harp_notes.append((root, 20, bar * 4 + beat, 0.5))
            harp_notes.append((root + 4, 18, bar * 4 + beat + 0.5, 0.5))
            harp_notes.append((root + 7, 15, bar * 4 + beat + 1, 0.5))
    mid.tracks.append(create_track("Harp", INST['harp'], 7, harp_notes))
    
    # Pista 9: Timpani (golpes solemnes)
    timpani_notes = []
    for bar in range(0, total_bars, 4):
        timpani_notes.append((38, 50, bar * 4, 2))
        timpani_notes.append((38, 40, bar * 4 + 2, 2))
    mid.tracks.append(create_track("Timpani", INST['timpani'], 9, timpani_notes))
    
    # Pista 10: Glockenspiel (destellos celestiales)
    glock_notes = []
    for bar in range(2, total_bars, 4):
        glock_notes.append((86, 15, bar * 4, 1))
        glock_notes.append((84, 12, bar * 4 + 2, 1))
    mid.tracks.append(create_track("Glockenspiel", INST['glockensiel'], 8, glock_notes))
    
    # Tempo
    mid.tracks[0].insert(0, MetaMessage('set_tempo', tempo=mido.bpm2tempo(bpm), time=0))
    mid.tracks[0].insert(0, MetaMessage('time_signature', numerator=4, denominator=4, time=0))
    
    return mid, bpm

# ============================================================
# CANCIÓN 2: Romeo y Julieta — primer encuentro
# C mayor, 80 BPM, orquesta de cámara con dueto violín-piano
# ============================================================

def compose_romeo_julieta():
    """Tema romántico del primer encuentro con orquesta de cámara"""
    mid = MidiFile(ticks_per_beat=TPQ)
    bpm = 80
    total_bars = 20
    
    # Progresión: C - G - Am - F - C - F - G - C
    progression = ['C', 'G', 'A', 'F', 'C', 'F', 'G', 'C']
    
    # Pista 1: Piano (melodía principal - arpegios y melodía)
    piano_notes = []
    # Intro: arpegios suaves de C mayor
    for bar in range(4):
        root = note_to_midi('C') + 12
        piano_notes.extend([
            (root, 30, bar * 4, 0.5), (root + 4, 28, bar * 4 + 0.5, 0.5),
            (root + 7, 32, bar * 4 + 1, 0.5), (root + 12, 35, bar * 4 + 1.5, 0.5),
            (root + 7, 30, bar * 4 + 2, 0.5), (root + 4, 28, bar * 4 + 2.5, 0.5),
        ])
    
    # Desarrollo: melodía romántica con cromatismo
    melody = [
        (76, 45, 16, 1), (74, 40, 17, 0.5), (72, 45, 17.5, 0.5),
        (74, 50, 18, 1), (76, 55, 19, 1), (79, 60, 20, 2),
        (77, 55, 22, 1), (76, 50, 23, 0.5), (74, 45, 23.5, 0.5),
        (72, 40, 24, 1), (74, 45, 25, 1), (76, 50, 26, 2),
        (74, 45, 28, 1), (72, 40, 29, 0.5), (71, 35, 29.5, 0.5),
        (72, 40, 30, 1), (74, 45, 31, 1), (76, 50, 32, 2),
    ]
    piano_notes.extend(melody)
    
    # Clímax: notas altas con intensidad
    climax = [
        (84, 65, 34, 1), (83, 60, 35, 0.5), (81, 55, 35.5, 0.5),
        (79, 50, 36, 1), (81, 55, 37, 1), (83, 60, 38, 2),
        (84, 65, 40, 1), (86, 70, 41, 1), (84, 65, 42, 2),
        (83, 60, 44, 1), (81, 55, 45, 0.5), (79, 50, 45.5, 0.5),
        (77, 45, 46, 1), (79, 50, 47, 1), (81, 55, 48, 2),
    ]
    piano_notes.extend(climax)
    
    # Resolución suave
    end = [
        (79, 40, 50, 2), (76, 35, 52, 2), (74, 30, 54, 2), (72, 25, 56, 4),
    ]
    piano_notes.extend(end)
    mid.tracks.append(create_track("Piano", INST['piano'], 0, piano_notes))
    
    # Pista 2: Violín (dueto con piano - contramelodía)
    violin_notes = [
        (67, 35, 0, 4), (72, 40, 4, 4), (76, 45, 8, 4), (79, 50, 12, 4),
        (76, 45, 16, 2), (74, 40, 18, 2), (72, 35, 20, 2), (74, 40, 22, 2),
        (76, 45, 24, 2), (79, 50, 26, 2), (81, 55, 28, 2), (79, 50, 30, 2),
        (76, 45, 32, 2), (74, 40, 34, 2), (72, 35, 36, 2), (74, 40, 38, 2),
        (76, 45, 40, 2), (79, 50, 42, 2), (81, 55, 44, 2), (79, 50, 46, 2),
        (76, 45, 48, 2), (74, 40, 50, 2), (72, 35, 52, 2), (67, 30, 54, 4),
    ]
    mid.tracks.append(create_track("Violin", INST['violin'], 1, violin_notes))
    
    # Pista 3: Cello (bajo cálido)
    cello_notes = []
    for bar in range(total_bars):
        root = note_to_midi(progression[bar % len(progression)]) - 12
        cello_notes.append((root, 35, bar * 4, 2))
        cello_notes.append((root + 7, 30, bar * 4 + 2, 2))
    mid.tracks.append(create_track("Cello", INST['cello'], 2, cello_notes))
    
    # Pista 4: Arpa (toques etéreos)
    harp_notes = []
    for bar in range(total_bars):
        root = note_to_midi(progression[bar % len(progression)]) + 12
        for beat in range(4):
            harp_notes.append((root, 18, bar * 4 + beat, 0.5))
            harp_notes.append((root + 7, 15, bar * 4 + beat + 0.5, 0.5))
    mid.tracks.append(create_track("Harp", INST['harp'], 3, harp_notes))
    
    # Pista 5: Flauta (ornamentos celestiales)
    flute_notes = [
        (84, 20, 0, 2), (86, 22, 2, 2), (88, 25, 4, 4),
        (86, 22, 8, 2), (84, 20, 10, 2), (83, 18, 12, 4),
        (84, 20, 16, 2), (86, 22, 18, 2), (88, 25, 20, 4),
        (86, 22, 24, 2), (84, 20, 26, 2), (83, 18, 28, 4),
        (84, 20, 32, 2), (86, 22, 34, 2), (88, 25, 36, 4),
        (86, 22, 40, 2), (84, 20, 42, 2), (83, 18, 44, 4),
        (84, 20, 48, 2), (86, 22, 50, 2), (88, 25, 52, 4),
    ]
    mid.tracks.append(create_track("Flute", INST['flute'], 4, flute_notes))
    
    # Pista 6: Clarinete (sostenidos suaves)
    clarinet_notes = []
    for bar in range(0, total_bars, 2):
        root = note_to_midi(progression[bar % len(progression)]) - 5
        clarinet_notes.append((root, 25, bar * 4, 8))
    mid.tracks.append(create_track("Clarinet", INST['clarinet'], 5, clarinet_notes))
    
    # Pista 7: Celesta (destellos mágicos)
    celesta_notes = []
    for bar in range(2, total_bars, 4):
        celesta_notes.append((91, 12, bar * 4, 1))
        celesta_notes.append((88, 10, bar * 4 + 2, 1))
    mid.tracks.append(create_track("Celesta", INST['celesta'], 6, celesta_notes))
    
    # Tempo
    mid.tracks[0].insert(0, MetaMessage('set_tempo', tempo=mido.bpm2tempo(bpm), time=0))
    mid.tracks[0].insert(0, MetaMessage('time_signature', numerator=4, denominator=4, time=0))
    
    return mid, bpm

# ============================================================
# CANCIÓN 3: Réquiem — soldados caídos
# E menor, 60 BPM, marcha fúnebre con orquesta completa
# ============================================================

def compose_requiem():
    """Réquiem solemne con orquesta completa"""
    mid = MidiFile(ticks_per_beat=TPQ)
    bpm = 60
    total_bars = 24
    
    # Progresión: Em - C - G - D - Em - B7 - Em
    progression = ['E', 'C', 'G', 'D', 'E', 'B', 'E']
    
    # Pista 1: Cuerdas (melodía fúnebre)
    strings_notes = []
    # Intro solemne
    intro = [
        (64, 30, 0, 2), (67, 35, 2, 2), (71, 40, 4, 4),
        (70, 35, 8, 2), (67, 30, 10, 2), (64, 25, 12, 4),
    ]
    strings_notes.extend(intro)
    
    # Desarrollo fúnebre
    dev = [
        (62, 35, 16, 1), (64, 40, 17, 1), (67, 45, 18, 2),
        (69, 50, 20, 1), (71, 55, 21, 1), (74, 60, 22, 2),
        (72, 55, 24, 1), (71, 50, 25, 1), (69, 45, 26, 2),
        (67, 40, 28, 1), (64, 35, 29, 1), (62, 30, 30, 2),
        (64, 35, 32, 1), (67, 40, 33, 1), (69, 45, 34, 2),
        (71, 50, 36, 1), (72, 55, 37, 1), (74, 60, 38, 2),
    ]
    strings_notes.extend(dev)
    
    # Clímax solemne
    climax = [
        (76, 65, 40, 1), (74, 60, 41, 1), (71, 55, 42, 2),
        (72, 60, 44, 1), (74, 65, 45, 1), (76, 70, 46, 2),
        (77, 65, 48, 1), (76, 60, 49, 1), (74, 55, 50, 2),
        (72, 50, 52, 1), (71, 45, 53, 1), (69, 40, 54, 2),
    ]
    strings_notes.extend(climax)
    
    # Resolución final
    end = [
        (67, 30, 56, 2), (64, 25, 58, 2), (62, 20, 60, 4),
    ]
    strings_notes.extend(end)
    mid.tracks.append(create_track("Strings", INST['strings'], 0, strings_notes))
    
    # Pista 2: Trompa francesa (lamento)
    horn_notes = [
        (59, 30, 0, 4), (55, 25, 4, 4), (52, 30, 8, 4),
        (55, 35, 12, 4), (59, 40, 16, 4), (62, 45, 20, 4),
        (59, 40, 24, 4), (55, 35, 28, 4), (52, 30, 32, 4),
        (55, 35, 36, 4), (59, 40, 40, 4), (62, 45, 44, 4),
        (59, 40, 48, 4), (55, 35, 52, 4), (52, 30, 56, 4),
    ]
    mid.tracks.append(create_track("French Horn", INST['french_horn'], 1, horn_notes))
    
    # Pista 3: Timpani (golpes solemnes)
    timpani_notes = []
    for bar in range(0, total_bars, 2):
        timpani_notes.append((38, 50, bar * 4, 2))
        timpani_notes.append((38, 40, bar * 4 + 2, 2))
    mid.tracks.append(create_track("Timpani", INST['timpani'], 9, timpani_notes))
    
    # Pista 4: Cello (bajo profundo)
    cello_notes = []
    for bar in range(total_bars):
        root = note_to_midi(progression[bar % len(progression)]) - 12
        cello_notes.append((root, 35, bar * 4, 2))
        cello_notes.append((root + 7, 30, bar * 4 + 2, 2))
    mid.tracks.append(create_track("Cello", INST['cello'], 2, cello_notes))
    
    # Pista 5: Contrabajo (raíz de acordes)
    bass_notes = []
    for bar in range(total_bars):
        root = note_to_midi(progression[bar % len(progression)]) - 24
        bass_notes.append((root, 40, bar * 4, 4))
    mid.tracks.append(create_track("Contrabass", INST['contrabass'], 3, bass_notes))
    
    # Pista 6: Coro (sostenidos etéreos)
    choir_notes = []
    for bar in range(0, total_bars, 4):
        root = note_to_midi(progression[bar % len(progression)]) + 12
        choir_notes.append((root, 20, bar * 4, 16))
        choir_notes.append((root + 7, 18, bar * 4, 16))
    mid.tracks.append(create_track("Choir", INST['choir'], 4, choir_notes))
    
    # Pista 7: Arpa (arpegios fúnebres)
    harp_notes = []
    for bar in range(total_bars):
        root = note_to_midi(progression[bar % len(progression)]) + 12
        for beat in range(4):
            harp_notes.append((root, 15, bar * 4 + beat, 0.5))
            harp_notes.append((root + 3, 12, bar * 4 + beat + 0.5, 0.5))
    mid.tracks.append(create_track("Harp", INST['harp'], 5, harp_notes))
    
    # Pista 8: Oboe (lamento melódico)
    oboe_notes = [
        (64, 25, 0, 4), (67, 30, 4, 4), (69, 35, 8, 4),
        (67, 30, 12, 4), (64, 25, 16, 4), (62, 20, 20, 4),
        (64, 25, 24, 4), (67, 30, 28, 4), (69, 35, 32, 4),
        (67, 30, 36, 4), (64, 25, 40, 4), (62, 20, 44, 4),
        (64, 25, 48, 4), (67, 30, 52, 4), (69, 35, 56, 4),
    ]
    mid.tracks.append(create_track("Oboe", INST['oboe'], 6, oboe_notes))
    
    # Pista 9: Trombón (sostenidos graves)
    trombone_notes = []
    for bar in range(0, total_bars, 2):
        root = note_to_midi(progression[bar % len(progression)]) - 5
        trombone_notes.append((root, 25, bar * 4, 8))
    mid.tracks.append(create_track("Trombone", INST['trombone'], 7, trombone_notes))
    
    # Pista 10: Tuba (fundamento grave)
    tuba_notes = []
    for bar in range(0, total_bars, 4):
        root = note_to_midi(progression[bar % len(progression)]) - 19
        tuba_notes.append((root, 35, bar * 4, 16))
    mid.tracks.append(create_track("Tuba", INST['tuba'], 8, tuba_notes))
    
    # Tempo
    mid.tracks[0].insert(0, MetaMessage('set_tempo', tempo=mido.bpm2tempo(bpm), time=0))
    mid.tracks[0].insert(0, MetaMessage('time_signature', numerator=4, denominator=4, time=0))
    
    return mid, bpm

# ============================================================
# MAIN
# ============================================================

if __name__ == '__main__':
    print("\n" + "="*60)
    print("COMPOSITOR AVANZADO: 3 Canciones con Orquesta Completa")
    print("="*60)
    
    # Canción 1
    print("\n[1/3] Componiendo: Concierto de orquesta (triste)...")
    mid1, bpm1 = compose_sad_orchestra()
    mid1_path = os.path.join(OUTPUT_DIR, "01_sad_orchestra.mid")
    mid1.save(mid1_path)
    print(f"  MIDI: {mid1_path}")
    wav1 = render_wav(mid1_path)
    ogg1 = convert_ogg(wav1)
    print(f"  OGG: {ogg1}")
    
    # Canción 2
    print("\n[2/3] Componiendo: Romeo y Julieta (romántica)...")
    mid2, bpm2 = compose_romeo_julieta()
    mid2_path = os.path.join(OUTPUT_DIR, "02_romeo_julieta.mid")
    mid2.save(mid2_path)
    print(f"  MIDI: {mid2_path}")
    wav2 = render_wav(mid2_path)
    ogg2 = convert_ogg(wav2)
    print(f"  OGG: {ogg2}")
    
    # Canción 3
    print("\n[3/3] Componiendo: Réquiem (soldados caídos)...")
    mid3, bpm3 = compose_requiem()
    mid3_path = os.path.join(OUTPUT_DIR, "03_requiem.mid")
    mid3.save(mid3_path)
    print(f"  MIDI: {mid3_path}")
    wav3 = render_wav(mid3_path)
    ogg3 = convert_ogg(wav3)
    print(f"  OGG: {ogg3}")
    
    print("\n" + "="*60)
    print("COMPLETADO")
    print("="*60)
    print(f"\nArchivos generados en: {OUTPUT_DIR}")
    print(f"  1. {os.path.basename(ogg1)} - Concierto triste")
    print(f"  2. {os.path.basename(ogg2)} - Romeo y Julieta")
    print(f"  3. {os.path.basename(ogg3)} - Réquiem")
