#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Pomodoro Timebox Avanzado 🍅
Versión con notificaciones y sonido para macOS.
"""

import time
import streamlit as st
from plyer import notification
from playsound import playsound
import threading
import os

# ----------------------------
# Configuración general
# ----------------------------
st.set_page_config(page_title="Pomodoro Timebox", page_icon="🍅", layout="centered")
st.title("🍅 Pomodoro Timebox")
st.caption("Con notificaciones y sonido al finalizar cada fase.")

# ----------------------------
# Estado inicial
# ----------------------------
if "is_running" not in st.session_state:
    st.session_state.is_running = False
if "seconds_left" not in st.session_state:
    st.session_state.seconds_left = 25 * 60
if "phase" not in st.session_state:
    st.session_state.phase = "Trabajo"

# ----------------------------
# Funciones auxiliares
# ----------------------------
def format_time(seconds):
    mins, secs = divmod(seconds, 60)
    return f"{mins:02d}:{secs:02d}"

def play_sound():
    """Reproduce un sonido corto (beep)"""
    try:
        sound_path = "/System/Library/Sounds/Glass.aiff"  # sonido nativo de macOS
        playsound(sound_path)
    except Exception:
        pass  # evitar errores si no hay sonido disponible

def notify(title, message):
    """Envía una notificación nativa de macOS"""
    notification.notify(title=title, message=message, timeout=5)

def start_timer():
    st.session_state.is_running = True

def pause_timer():
    st.session_state.is_running = False

def reset_timer():
    st.session_state.is_running = False
    st.session_state.seconds_left = 25 * 60
    st.session_state.phase = "Trabajo"

# ----------------------------
# Interfaz principal
# ----------------------------
col1, col2, col3 = st.columns(3)
with col1:
    st.button("▶️ Iniciar", on_click=start_timer)
with col2:
    st.button("⏸️ Pausar", on_click=pause_timer)
with col3:
    st.button("🔄 Reiniciar", on_click=reset_timer)

# ----------------------------
# Mostrar contador
# ----------------------------
st.markdown(f"### 🧭 Fase: **{st.session_state.phase}**")
time_display = st.empty()
time_display.markdown(f"# ⏱️ {format_time(st.session_state.seconds_left)}")

# ----------------------------
# Temporizador
# ----------------------------
if st.session_state.is_running:
    while st.session_state.seconds_left > 0 and st.session_state.is_running:
        time_display.markdown(f"# ⏱️ {format_time(st.session_state.seconds_left)}")
        time.sleep(1)
        st.session_state.seconds_left -= 1
        st.rerun()

# ----------------------------
# Cambio de fase
# ----------------------------
if st.session_state.seconds_left <= 0:
    play_sound()
    if st.session_state.phase == "Trabajo":
        st.session_state.phase = "Descanso"
        st.session_state.seconds_left = 5 * 60
        notify("🎉 ¡Pomodoro terminado!", "Toma un descanso de 5 minutos 🧘‍♂️")
        st.success("¡Buen trabajo! 🌟 Descansa un poco.")
        st.session_state.is_running = True
        threading.Thread(target=play_sound).start()
        st.rerun()
    else:
        st.session_state.phase = "Trabajo"
        st.session_state.seconds_left = 25 * 60
        st.session_state.is_running = False
        notify("🚀 Descanso terminado", "Vuelve al trabajo 🍅")
        st.info("🎯 Nuevo ciclo de trabajo listo.")
        threading.Thread(target=play_sound).start()