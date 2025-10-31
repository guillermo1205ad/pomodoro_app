#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Pomodoro Timebox 🍅 (versión para Streamlit Cloud)
Sin dependencias externas (notificaciones ni sonidos locales)
"""

import time
import streamlit as st

# ----------------------------
# Configuración general
# ----------------------------
st.set_page_config(page_title="Pomodoro Timebox", page_icon="🍅", layout="centered")
st.title("🍅 Pomodoro Timebox")
st.caption("Versión para la nube (sin sonidos ni notificaciones).")

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
    if st.session_state.phase == "Trabajo":
        st.session_state.phase = "Descanso"
        st.session_state.seconds_left = 5 * 60
        st.success("🎉 ¡Pomodoro terminado! Toma un descanso de 5 minutos.")
        st.session_state.is_running = True
        st.rerun()
    else:
        st.session_state.phase = "Trabajo"
        st.session_state.seconds_left = 25 * 60
        st.session_state.is_running = False
        st.balloons()
        st.info("🚀 ¡Descanso terminado! Volvamos al trabajo 🍅")
