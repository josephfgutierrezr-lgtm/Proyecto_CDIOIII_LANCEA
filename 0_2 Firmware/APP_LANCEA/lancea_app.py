import customtkinter as ctk
import serial
import serial.tools.list_ports
import threading
import pandas as pd
import numpy as np
import os
import json
from datetime import datetime
from tkinter import filedialog, messagebox
from matplotlib.figure import Figure
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import matplotlib.pyplot as plt
import time
import math

ctk.set_appearance_mode("Dark")
ctk.set_default_color_theme("blue")

# ── PALETA DE COLORES ──────────────────────────────────────────────────────────
BG_DEEP   = "#03060A"
BG_BASE   = "#070D14"
BG_PANEL  = "#0B1520"
BG_CARD   = "#0F1C2E"
BG_HOVER  = "#132540"
ACCENT1   = "#00C8FF"   # cian eléctrico
ACCENT2   = "#F0A500"   # ámbar dorado
ACCENT3   = "#00FF88"   # verde neón
RED_ALERT = "#FF3B5C"
TEXT_PRI  = "#E8F4FD"
TEXT_SEC  = "#6B8BA4"
TEXT_DIM  = "#334B62"
BORDER    = "#1A3050"

# ── DIRECTORIO RAÍZ ───────────────────────────────────────────────────────────
ROOT_DIR    = "LANCEA_DATA"
ATHLETES    = os.path.join(ROOT_DIR, "atletas")
SD_IMPORTS  = os.path.join(ROOT_DIR, "sd_imports")   # volcados desde tarjeta SD
CONFIG_FILE = os.path.join(ROOT_DIR, "config.json")


def ensure_dirs():
    """Crea la estructura de carpetas si no existe."""
    os.makedirs(ROOT_DIR,   exist_ok=True)
    os.makedirs(ATHLETES,   exist_ok=True)
    os.makedirs(SD_IMPORTS, exist_ok=True)


def athlete_dir(name: str) -> str:
    safe = "".join(c for c in name if c.isalnum() or c in " _-").strip()
    path = os.path.join(ATHLETES, safe)
    os.makedirs(path, exist_ok=True)
    return path


def load_config() -> dict:
    ensure_dirs()
    if os.path.exists(CONFIG_FILE):
        try:
            with open(CONFIG_FILE, "r", encoding="utf-8") as f:
                return json.load(f)
        except Exception:
            pass
    return {"athletes": ["Invitado"], "last_athlete": "Invitado"}


def save_config(cfg: dict):
    ensure_dirs()
    with open(CONFIG_FILE, "w", encoding="utf-8") as f:
        json.dump(cfg, f, indent=2, ensure_ascii=False)


# ── IP del XIAO cuando el PC se conecta al hotspot LANCEA_AP ──────────────
LANCEA_WIFI_IP = "192.168.4.1"


def get_session_dirs(athlete_name: str) -> dict:
    """Crea y devuelve la jerarquia de carpetas para la sesion del dia actual.

    LANCEA_DATA/atletas/<nombre>/<YYYY-MM-DD>/
        1_datos_crudos/
        2_graficas/
        3_analisis/
    """
    safe = "".join(c for c in athlete_name if c.isalnum() or c in " _-").strip()
    date_str = datetime.now().strftime("%Y-%m-%d")
    base = os.path.join(ROOT_DIR, "atletas", safe, date_str)
    dirs = {
        "raw":     os.path.join(base, "1_datos_crudos"),
        "plots":   os.path.join(base, "2_graficas"),
        "reports": os.path.join(base, "3_analisis"),
    }
    for p in dirs.values():
        os.makedirs(p, exist_ok=True)
    return dirs


def generar_reporte_automatico(csv_path: str, athlete_name: str) -> str:
    """Lee el CSV de sesion, genera estadisticas y exporta graficas PNG."""
    try:
        df = pd.read_csv(csv_path)
        if df.empty or len(df) < 1:
            return ""
        dirs = get_session_dirs(athlete_name)
        session_id = datetime.now().strftime("%H%M%S")

        # Estadisticas
        resumen = df.describe().round(3)
        resumen.to_csv(os.path.join(dirs["reports"], "estadisticas_" + session_id + ".csv"))

        # Graficas
        plt.style.use("dark_background")
        n = len(df)
        cols_num = [c for c in ["Velocidad","Angulo","Distancia","maxAccel","Energia","Potencia"]
                    if c in df.columns]
        if not cols_num:
            return ""
        n_plots = len(cols_num) + (1 if "Angulo" in df.columns and "Distancia" in df.columns else 0)
        rows_fig = max(1, (n_plots + 1) // 2)
        fig, axes = plt.subplots(rows_fig, 2, figsize=(12, 4 * rows_fig))
        axes_flat = axes.flatten() if hasattr(axes, "flatten") else [axes]
        fig.suptitle("Analisis de Sesion  -  " + athlete_name,
                     fontsize=14, color="#00C8FF", fontweight="bold")
        color_map = {"Velocidad":"#00C8FF","Angulo":"#F0A500","Distancia":"#00FF88",
                     "maxAccel":"#FF6B35","Energia":"#A855F7","Potencia":"#EC4899"}
        units = {"Velocidad":"m/s","Angulo":"deg","Distancia":"m",
                 "maxAccel":"m/s2","Energia":"J","Potencia":"W"}
        idx = 0
        for col in cols_num:
            if idx >= len(axes_flat): break
            ax = axes_flat[idx]; idx += 1
            color = color_map.get(col, "#FFFFFF")
            ax.plot(range(1, n+1), df[col], marker="o", color=color,
                    linewidth=2, markersize=6, alpha=0.9)
            ax.fill_between(range(1, n+1), df[col], alpha=0.15, color=color)
            if col == "Angulo":
                ax.axhspan(32, 39, alpha=0.12, color="#00FF88", label="zona optima")
                ax.legend(fontsize=8, labelcolor="#00FF88")
            ax.set_title(col + " por lanzamiento", color="#E8F4FD", fontsize=10)
            ax.set_xlabel("Lanzamiento", color="#6B8BA4", fontsize=8)
            ax.set_ylabel(units.get(col, ""), color="#6B8BA4", fontsize=8)
            ax.tick_params(colors="#6B8BA4", labelsize=8)
            ax.grid(True, alpha=0.2, color="#1A3050")
            for sp in ax.spines.values(): sp.set_edgecolor("#1A3050")
        if "Angulo" in df.columns and "Distancia" in df.columns and idx < len(axes_flat):
            ax = axes_flat[idx]; idx += 1
            sc = ax.scatter(df["Angulo"], df["Distancia"],
                            c=range(n), cmap="plasma", s=100, alpha=0.9)
            ax.axvspan(32, 39, alpha=0.1, color="#00FF88", label="angulo optimo")
            for i, (ang, dist) in enumerate(zip(df["Angulo"], df["Distancia"])):
                ax.annotate("#" + str(i+1), (ang, dist),
                            textcoords="offset points", xytext=(5,4),
                            fontsize=7, color="#6B8BA4")
            ax.set_title("Angulo vs Distancia", color="#E8F4FD", fontsize=10)
            ax.set_xlabel("Angulo (deg)", color="#6B8BA4", fontsize=8)
            ax.set_ylabel("Distancia (m)", color="#6B8BA4", fontsize=8)
            ax.tick_params(colors="#6B8BA4", labelsize=8)
            ax.grid(True, alpha=0.2, color="#1A3050")
            ax.legend(fontsize=8, labelcolor="#00FF88")
            for sp in ax.spines.values(): sp.set_edgecolor("#1A3050")
            plt.colorbar(sc, ax=ax, label="Orden")
        for j in range(idx, len(axes_flat)):
            axes_flat[j].set_visible(False)
        plt.tight_layout()
        plot_path = os.path.join(dirs["plots"], "grafica_" + session_id + ".png")
        plt.savefig(plot_path, dpi=150, bbox_inches="tight", facecolor="#070D14")
        plt.close()
        return plot_path
    except Exception as e:
        print("[ERROR reporte] " + str(e))
        return ""


# ── COMPONENTES VISUALES REUTILIZABLES ────────────────────────────────────────

class GlowLabel(ctk.CTkLabel):
    """Label con pseudo-brillo usando borde de color."""
    pass


class SectionTitle(ctk.CTkLabel):
    def __init__(self, parent, text, **kw):
        super().__init__(
            parent, text=text.upper(),
            font=ctk.CTkFont(family="Consolas", size=11, weight="bold"),
            text_color=TEXT_SEC, **kw
        )


class KPICard(ctk.CTkFrame):
    def __init__(self, parent, label, unit, accent, **kw):
        super().__init__(parent,
            fg_color=BG_CARD, border_width=1, border_color=BORDER,
            corner_radius=8, **kw)
        self.accent = accent

        SectionTitle(self, label).pack(pady=(14, 4), padx=16, anchor="w")

        self.val_lbl = ctk.CTkLabel(
            self, text="–",
            font=ctk.CTkFont(family="Consolas", size=52, weight="bold"),
            text_color=accent)
        self.val_lbl.pack(padx=16, anchor="w")

        self.unit_lbl = ctk.CTkLabel(
            self, text=unit,
            font=ctk.CTkFont(family="Consolas", size=13),
            text_color=TEXT_DIM)
        self.unit_lbl.pack(padx=16, pady=(0, 14), anchor="w")

    def set(self, value: str):
        self.val_lbl.configure(text=value)


class NavButton(ctk.CTkButton):
    def __init__(self, parent, text, icon, cmd, **kw):
        super().__init__(parent,
            text=f"  {icon}  {text}",
            command=cmd, height=44, anchor="w",
            font=ctk.CTkFont(family="Consolas", size=13),
            fg_color="transparent",
            hover_color=BG_HOVER,
            text_color=TEXT_SEC,
            corner_radius=6, **kw)

    def activate(self):
        self.configure(fg_color=BG_HOVER, text_color=ACCENT1)

    def deactivate(self):
        self.configure(fg_color="transparent", text_color=TEXT_SEC)


class StatusBadge(ctk.CTkFrame):
    def __init__(self, parent, **kw):
        super().__init__(parent, fg_color="transparent", **kw)
        self.dot = ctk.CTkLabel(self, text="●",
            font=ctk.CTkFont(size=12), text_color=RED_ALERT)
        self.dot.pack(side="left", padx=(0, 6))
        self.lbl = ctk.CTkLabel(self, text="DESCONECTADO",
            font=ctk.CTkFont(family="Consolas", size=11, weight="bold"),
            text_color=RED_ALERT)
        self.lbl.pack(side="left")

    def online(self, port=""):
        self.dot.configure(text_color=ACCENT3)
        self.lbl.configure(text=f"ENLACE  {port}", text_color=ACCENT3)

    def offline(self):
        self.dot.configure(text_color=RED_ALERT)
        self.lbl.configure(text="DESCONECTADO", text_color=RED_ALERT)


# ── APLICACIÓN PRINCIPAL ───────────────────────────────────────────────────────

class LanceaApp(ctk.CTk):
    def __init__(self):
        super().__init__()
        ensure_dirs()

        self.title("LANCEA  ·  Intelligent Javelin Telemetry  ·  v3.0")
        self.geometry("1440x900")
        self.minsize(1100, 720)
        self.configure(fg_color=BG_DEEP)

        self.cfg = load_config()
        self.current_athlete: str = self.cfg.get("last_athlete", "Invitado")
        self.serial_port = None
        self.is_reading  = False
        self.log_file    = None
        self.last_v = 0.0
        self.last_a = 0.0
        self._nav_btns: list[NavButton] = []

        # ── Rutas de sesion activa ──────────────────────────────────────────
        self._session_csv_path = None
        self._session_ts = ""

        # ── Estado de transferencia SD ──────────────────────────────────────
        self._sd_transfer_active = False
        self._sd_buffer: list[str] = []
        self._sd_file_path: str | None = None

        # ── Sesión en vivo ───────────────────────────────────────────────────
        self._session_throws: list[dict] = []   # lanzamientos de la sesión actual
        self._live_buf: dict = {}               # bloque THROW acumulando
        self._in_throw_block = False            # dentro de THROW_START…THROW_END
        self._dump_active = False               # dentro de DUMP_START…DUMP_END
        self._dump_rows: list[str] = []         # filas CSV del volcado

        self._build_layout()
        self._show_live()

    # ── LAYOUT ─────────────────────────────────────────────────────────────────

    def _build_layout(self):
        self.grid_columnconfigure(1, weight=1)
        self.grid_rowconfigure(0, weight=1)

        # SIDEBAR
        self.sidebar = ctk.CTkFrame(self, width=260, fg_color=BG_BASE,
            corner_radius=0, border_width=0)
        self.sidebar.grid(row=0, column=0, sticky="nsew")
        self.sidebar.grid_propagate(False)
        self._build_sidebar()

        # ÁREA CENTRAL
        self.main_area = ctk.CTkFrame(self, fg_color=BG_BASE,
            corner_radius=0, border_width=0)
        self.main_area.grid(row=0, column=1, sticky="nsew")
        self.main_area.grid_columnconfigure(0, weight=1)
        self.main_area.grid_rowconfigure(0, weight=1)

        self._build_live_frame()
        self._build_history_frame()
        self._build_wifi_frame()
        self._build_sd_frame()
        self._build_config_frame()

    def _build_sidebar(self):
        sb = self.sidebar

        # Logo area
        logo_frame = ctk.CTkFrame(sb, fg_color="transparent")
        logo_frame.pack(fill="x", padx=20, pady=(32, 8))

        ctk.CTkLabel(logo_frame, text="⟁ LANCEA",
            font=ctk.CTkFont(family="Consolas", size=26, weight="bold"),
            text_color=ACCENT1).pack(anchor="w")
        ctk.CTkLabel(logo_frame, text="JAVELIN TELEMETRY SYSTEM",
            font=ctk.CTkFont(family="Consolas", size=9),
            text_color=TEXT_DIM).pack(anchor="w")

        # Divider
        ctk.CTkFrame(sb, height=1, fg_color=BORDER).pack(fill="x", padx=20, pady=16)

        # Atleta seleccionado
        ctk.CTkLabel(sb, text="ATLETA ACTIVO",
            font=ctk.CTkFont(family="Consolas", size=10, weight="bold"),
            text_color=TEXT_DIM).pack(padx=20, anchor="w")

        self.athlete_menu = ctk.CTkOptionMenu(
            sb, values=self.cfg["athletes"],
            command=self._set_athlete,
            font=ctk.CTkFont(family="Consolas", size=13),
            fg_color=BG_CARD, button_color=BG_HOVER,
            button_hover_color=ACCENT1,
            dropdown_fg_color=BG_PANEL,
            text_color=TEXT_PRI, height=38, corner_radius=6)
        self.athlete_menu.set(self.current_athlete)
        self.athlete_menu.pack(fill="x", padx=20, pady=(6, 20))

        # Divider
        ctk.CTkFrame(sb, height=1, fg_color=BORDER).pack(fill="x", padx=20, pady=4)

        # Navegación
        ctk.CTkLabel(sb, text="MÓDULOS",
            font=ctk.CTkFont(family="Consolas", size=10, weight="bold"),
            text_color=TEXT_DIM).pack(padx=20, pady=(16, 6), anchor="w")

        nav_items = [
            ("TELEMETRIA EN VIVO",     "◈", self._show_live),
            ("ANALIZADOR DE LOGS",     "◧", self._show_history),
            ("WiFi · PANEL & ATLETAS", "⊕", self._show_wifi),
            ("SD · VOLCADO & ANALISIS","▣", self._show_sd),
            ("GESTION DE ATLETAS",     "◉", self._show_config),
        ]
        for label, icon, cmd in nav_items:
            btn = NavButton(sb, label, icon, cmd)
            btn.pack(fill="x", padx=12, pady=2)
            self._nav_btns.append(btn)

        # Footer status
        ctk.CTkFrame(sb, height=1, fg_color=BORDER).pack(fill="x", padx=20, side="bottom", pady=16)
        self.status_badge = StatusBadge(sb)
        self.status_badge.pack(side="bottom", padx=20, pady=(0, 8), anchor="w")

        version_lbl = ctk.CTkLabel(sb, text="LANCEA  ©  2025  /  v2.0",
            font=ctk.CTkFont(family="Consolas", size=9),
            text_color=TEXT_DIM)
        version_lbl.pack(side="bottom", padx=20, pady=(0, 4), anchor="w")

    # ── FRAME TELEMETRÍA VIVO ──────────────────────────────────────────────────

    def _build_live_frame(self):
        # grid de 4 filas — barra conexion SIEMPRE visible en row=0
        # row=0  barra conexion (fija)
        # row=1  KPIs        (fija)
        # row=2  coach+console (expande)
        # row=3  historial   (fija)
        self.live_frame = ctk.CTkFrame(self.main_area, fg_color="transparent")
        self.live_frame.grid_columnconfigure(0, weight=1)
        self.live_frame.grid_rowconfigure(2, weight=1)

        # ── ROW 0  BARRA DE CONEXION ──────────────────────────────────────────
        ctrl = ctk.CTkFrame(self.live_frame, fg_color=BG_PANEL,
            border_width=1, border_color=ACCENT1, corner_radius=8)
        ctrl.grid(row=0, column=0, padx=20, pady=(14,6), sticky="ew")

        ctk.CTkLabel(ctrl, text="PUERTO:",
            font=ctk.CTkFont(family="Consolas", size=11, weight="bold"),
            text_color=TEXT_SEC).pack(side="left", padx=(14,4), pady=10)

        self.port_menu = ctk.CTkComboBox(ctrl,
            values=self._get_ports(),
            font=ctk.CTkFont(family="Consolas", size=12),
            fg_color=BG_CARD, border_color=BORDER,
            button_color=BG_HOVER, dropdown_fg_color=BG_PANEL,
            width=160, height=34)
        self.port_menu.pack(side="left", padx=4, pady=10)

        ctk.CTkButton(ctrl, text="R",
            command=self._refresh_ports,
            width=34, height=34, fg_color=BG_CARD,
            hover_color=BG_HOVER, font=ctk.CTkFont(size=13),
            corner_radius=6, border_width=1,
            border_color=BORDER).pack(side="left", padx=(2,8))

        self.ts_label = ctk.CTkLabel(ctrl, text="",
            font=ctk.CTkFont(family="Consolas", size=10),
            text_color=TEXT_DIM)
        self.ts_label.pack(side="left", padx=4)
        self._update_clock()

        # Botones derecha
        self.btn_serial = ctk.CTkButton(ctrl,
            text="CONECTAR ESP32",
            command=self._toggle_serial,
            font=ctk.CTkFont(family="Consolas", size=12, weight="bold"),
            fg_color=ACCENT3, hover_color="#00CC6E", text_color="#000000",
            height=34, corner_radius=6, width=180)
        self.btn_serial.pack(side="right", padx=(4,14), pady=10)

        ctk.CTkButton(ctrl, text="DUMP",
            command=self._request_dump,
            font=ctk.CTkFont(family="Consolas", size=11, weight="bold"),
            fg_color="#A855F7", hover_color="#9333EA", text_color="#FFFFFF",
            height=34, corner_radius=6, width=72).pack(side="right", padx=4)

        ctk.CTkButton(ctrl, text="RESET",
            command=self._request_reset,
            font=ctk.CTkFont(family="Consolas", size=11),
            fg_color=BG_CARD, hover_color=BG_HOVER,
            border_width=1, border_color=BORDER,
            height=34, corner_radius=6, width=68).pack(side="right", padx=4)

        # ── ROW 1  KPIs ───────────────────────────────────────────────────────
        kpi_outer = ctk.CTkFrame(self.live_frame, fg_color="transparent")
        kpi_outer.grid(row=1, column=0, padx=20, pady=(0,6), sticky="ew")
        for c in range(7):
            kpi_outer.columnconfigure(c, weight=1)

        self.kpi_vel  = KPICard(kpi_outer, "VELOCIDAD",  "m/s",  ACCENT1)
        self.kpi_ang  = KPICard(kpi_outer, "ANGULO",     "deg",  ACCENT2)
        self.kpi_dist = KPICard(kpi_outer, "DISTANCIA",  "m",    ACCENT3)
        self.kpi_acel = KPICard(kpi_outer, "ACEL MAX",   "m/s2", "#FF6B35")
        self.kpi_ener = KPICard(kpi_outer, "ENERGIA",    "J",    "#A855F7")
        self.kpi_pow  = KPICard(kpi_outer, "POTENCIA",   "W",    "#EC4899")
        self.kpi_raw  = KPICard(kpi_outer, "SESION",     "#",    TEXT_SEC)

        self.kpi_vel.grid( row=0, column=0, padx=(0,3), sticky="nsew")
        self.kpi_ang.grid( row=0, column=1, padx=3,     sticky="nsew")
        self.kpi_dist.grid(row=0, column=2, padx=3,     sticky="nsew")
        self.kpi_acel.grid(row=0, column=3, padx=3,     sticky="nsew")
        self.kpi_ener.grid(row=0, column=4, padx=3,     sticky="nsew")
        self.kpi_pow.grid( row=0, column=5, padx=3,     sticky="nsew")
        self.kpi_raw.grid( row=0, column=6, padx=(3,0), sticky="nsew")

        # ── ROW 2  COACH + CONSOLA (expande) ──────────────────────────────────
        mid = ctk.CTkFrame(self.live_frame, fg_color="transparent")
        mid.grid(row=2, column=0, padx=20, pady=(0,6), sticky="nsew")
        mid.columnconfigure(0, weight=1)
        mid.columnconfigure(1, weight=2)
        mid.rowconfigure(0, weight=1)

        coach = ctk.CTkFrame(mid, fg_color=BG_CARD,
            border_width=1, border_color=BORDER, corner_radius=8)
        coach.grid(row=0, column=0, padx=(0,8), sticky="nsew")

        SectionTitle(coach, "COACH VIRTUAL LANCEA").pack(
            padx=16, pady=(12,6), anchor="w")
        ctk.CTkFrame(coach, height=1, fg_color=BORDER).pack(fill="x", padx=16)

        self.feedback_text = ctk.CTkLabel(coach,
            text="Esperando lanzamiento",
            font=ctk.CTkFont(family="Consolas", size=18, weight="bold"),
            text_color=TEXT_SEC, justify="center", wraplength=240)
        self.feedback_text.pack(expand=True)

        self.coach_sub = ctk.CTkLabel(coach, text="",
            font=ctk.CTkFont(family="Consolas", size=11),
            text_color=TEXT_DIM, wraplength=240, justify="center")
        self.coach_sub.pack(pady=(0,12))

        console_frame = ctk.CTkFrame(mid, fg_color=BG_CARD,
            border_width=1, border_color=BORDER, corner_radius=8)
        console_frame.grid(row=0, column=1, sticky="nsew")
        console_frame.grid_rowconfigure(1, weight=1)
        console_frame.grid_columnconfigure(0, weight=1)

        SectionTitle(console_frame, "CONSOLA SERIAL").grid(
            row=0, column=0, padx=16, pady=(12,6), sticky="w")
        self.live_console = ctk.CTkTextbox(console_frame,
            font=ctk.CTkFont(family="Consolas", size=12),
            fg_color=BG_BASE, text_color=ACCENT3,
            scrollbar_button_color=BG_HOVER, border_width=0)
        self.live_console.grid(
            row=1, column=0, padx=10, pady=(0,10), sticky="nsew")

        # ── ROW 3  HISTORIAL DE SESION (fija abajo) ───────────────────────────
        hist_outer = ctk.CTkFrame(self.live_frame, fg_color=BG_CARD,
            border_width=1, border_color=BORDER, corner_radius=8)
        hist_outer.grid(row=3, column=0, padx=20, pady=(0,14), sticky="ew")

        hist_hdr = ctk.CTkFrame(hist_outer, fg_color="transparent")
        hist_hdr.pack(fill="x", padx=14, pady=(8,4))
        SectionTitle(hist_hdr, "HISTORIAL DE SESION").pack(side="left")
        ctk.CTkButton(hist_hdr, text="Ver analisis",
            command=self._go_to_session_analysis,
            width=100, height=22,
            font=ctk.CTkFont(family="Consolas", size=10),
            fg_color=ACCENT1, hover_color="#00A8D4", text_color="#000000",
            corner_radius=4).pack(side="right")

        self.session_scroll = ctk.CTkScrollableFrame(hist_outer,
            fg_color=BG_BASE, scrollbar_button_color=BG_HOVER,
            corner_radius=6, height=72)
        self.session_scroll.pack(fill="x", padx=10, pady=(0,8))
        self.session_scroll.columnconfigure((0,1,2,3,4,5,6,7), weight=1)

        for ci, (lbl, color) in enumerate([
            ("#", TEXT_DIM), ("V m/s", ACCENT1), ("Ang", ACCENT2),
            ("Dist m", ACCENT3), ("Acel", "#FF6B35"),
            ("t s", TEXT_SEC), ("E J", "#A855F7"), ("P W", "#EC4899")
        ]):
            ctk.CTkLabel(self.session_scroll, text=lbl,
                font=ctk.CTkFont(family="Consolas", size=10, weight="bold"),
                text_color=color).grid(
                row=0, column=ci, padx=4, pady=2, sticky="ew")
        self._session_row_count = 0
    # ── FRAME ANALIZADOR ───────────────────────────────────────────────────────

    def _build_history_frame(self):
        self.history_frame = ctk.CTkFrame(self.main_area, fg_color="transparent")

        # Header
        header = ctk.CTkFrame(self.history_frame, fg_color="transparent")
        header.pack(fill="x", padx=24, pady=(24, 16))
        ctk.CTkLabel(header, text="ANALIZADOR DE LANZAMIENTOS",
            font=ctk.CTkFont(family="Consolas", size=20, weight="bold"),
            text_color=TEXT_PRI).pack(side="left")

        # Toolbar
        toolbar = ctk.CTkFrame(self.history_frame, fg_color=BG_PANEL,
            border_width=1, border_color=BORDER, corner_radius=8)
        toolbar.pack(fill="x", padx=24, pady=(0, 16))

        ctk.CTkButton(toolbar, text="📂  ABRIR ARCHIVO",
            command=self._analyze_file,
            font=ctk.CTkFont(family="Consolas", size=12),
            fg_color=ACCENT1, hover_color="#00A8D4", text_color="#000000",
            height=36, corner_radius=6).pack(side="left", padx=12, pady=10)

        ctk.CTkButton(toolbar, text="📁  EXPLORAR ATLETA",
            command=self._browse_athlete_folder,
            font=ctk.CTkFont(family="Consolas", size=12),
            fg_color=BG_CARD, hover_color=BG_HOVER, text_color=TEXT_PRI,
            height=36, corner_radius=6, border_width=1, border_color=BORDER
            ).pack(side="left", padx=4, pady=10)

        ctk.CTkButton(toolbar, text="WiFi LANCEA",
            command=self._import_from_wifi,
            font=ctk.CTkFont(family="Consolas", size=12, weight="bold"),
            fg_color=BG_CARD, hover_color=BG_HOVER, text_color=ACCENT1,
            height=36, corner_radius=6, border_width=1, border_color=ACCENT1
            ).pack(side="left", padx=4, pady=10)

        self.wifi_ip_entry = ctk.CTkEntry(toolbar,
            placeholder_text="192.168.4.1",
            font=ctk.CTkFont(family="Consolas", size=11),
            fg_color=BG_CARD, border_color=BORDER,
            text_color=TEXT_SEC, width=115, height=36)
        self.wifi_ip_entry.insert(0, LANCEA_WIFI_IP)
        self.wifi_ip_entry.pack(side="left", padx=(0,4), pady=10)

        self.wifi_status_lbl = ctk.CTkLabel(toolbar, text="",
            font=ctk.CTkFont(family="Consolas", size=10),
            text_color=TEXT_DIM)
        self.wifi_status_lbl.pack(side="left", padx=4)

        self.file_label = ctk.CTkLabel(toolbar, text="  Sin archivo cargado",
            font=ctk.CTkFont(family="Consolas", size=11, slant="italic"),
            text_color=TEXT_DIM)
        self.file_label.pack(side="left", padx=12)

        # Content
        self.history_content = ctk.CTkFrame(self.history_frame,
            fg_color=BG_CARD, border_width=1, border_color=BORDER,
            corner_radius=8)
        self.history_content.pack(fill="both", expand=True, padx=24, pady=(0, 20))
        self.history_content.grid_columnconfigure(0, weight=1)
        self.history_content.grid_rowconfigure(0, weight=1)

        # Placeholder
        placeholder = ctk.CTkFrame(self.history_content, fg_color="transparent")
        placeholder.pack(expand=True)
        ctk.CTkLabel(placeholder, text="◧",
            font=ctk.CTkFont(size=64), text_color=TEXT_DIM).pack()
        ctk.CTkLabel(placeholder, text="Abre un archivo CSV o LOG para analizarlo",
            font=ctk.CTkFont(family="Consolas", size=14),
            text_color=TEXT_DIM).pack(pady=8)

    # ── FRAME GESTIÓN ATLETAS ──────────────────────────────────────────────────

    def _build_config_frame(self):
        self.config_frame = ctk.CTkFrame(self.main_area, fg_color="transparent")

        header = ctk.CTkFrame(self.config_frame, fg_color="transparent")
        header.pack(fill="x", padx=24, pady=(24, 16))
        ctk.CTkLabel(header, text="GESTIÓN DE ATLETAS",
            font=ctk.CTkFont(family="Consolas", size=20, weight="bold"),
            text_color=TEXT_PRI).pack(side="left")

        # Formulario nuevo atleta
        form = ctk.CTkFrame(self.config_frame, fg_color=BG_CARD,
            border_width=1, border_color=BORDER, corner_radius=8)
        form.pack(fill="x", padx=24, pady=(0, 16))

        SectionTitle(form, "◉  REGISTRAR NUEVO ATLETA").pack(
            padx=20, pady=(18, 10), anchor="w")

        row = ctk.CTkFrame(form, fg_color="transparent")
        row.pack(fill="x", padx=20, pady=(0, 18))

        self.new_athlete_entry = ctk.CTkEntry(row,
            placeholder_text="Nombre completo del atleta",
            font=ctk.CTkFont(family="Consolas", size=13),
            fg_color=BG_BASE, border_color=BORDER,
            text_color=TEXT_PRI, height=40, width=340)
        self.new_athlete_entry.pack(side="left", padx=(0, 12))

        ctk.CTkButton(row, text="+ REGISTRAR",
            command=self._add_athlete,
            font=ctk.CTkFont(family="Consolas", size=12, weight="bold"),
            fg_color=ACCENT1, hover_color="#00A8D4", text_color="#000000",
            height=40, corner_radius=6, width=140).pack(side="left")

        # Lista de atletas
        list_frame = ctk.CTkFrame(self.config_frame, fg_color=BG_CARD,
            border_width=1, border_color=BORDER, corner_radius=8)
        list_frame.pack(fill="both", expand=True, padx=24, pady=(0, 24))

        SectionTitle(list_frame, "◈  ATLETAS REGISTRADOS").pack(
            padx=20, pady=(18, 10), anchor="w")

        self.athlete_scroll = ctk.CTkScrollableFrame(list_frame,
            fg_color=BG_BASE, scrollbar_button_color=BG_HOVER, corner_radius=6)
        self.athlete_scroll.pack(fill="both", expand=True, padx=16, pady=(0, 16))

        self._refresh_athlete_list()

    # ── LÓGICA SERIAL ──────────────────────────────────────────────────────────

    def _get_ports(self):
        ports = [p.device for p in serial.tools.list_ports.comports()]
        return ports if ports else ["Sin puertos"]

    def _refresh_ports(self):
        ports = self._get_ports()
        self.port_menu.configure(values=ports)
        if ports: self.port_menu.set(ports[0])

    def _toggle_serial(self):
        if not self.is_reading:
            try:
                port = self.port_menu.get()
                self.serial_port = serial.Serial(port, 115200, timeout=1)
                self.is_reading = True
                self.btn_serial.configure(
                    text="■  DESCONECTAR",
                    fg_color=RED_ALERT, hover_color="#CC2F4A", text_color="#FFFFFF")
                self.status_badge.online(port)
                threading.Thread(target=self._listen_serial, daemon=True).start()
                self._log_console(f"[{datetime.now().strftime('%H:%M:%S')}] ENLACE ESTABLECIDO · {port} · 115200 baud\n")
            except Exception as e:
                messagebox.showerror("Error de conexión", str(e))
        else:
            self.is_reading = False
            if self.serial_port:
                try: self.serial_port.close()
                except: pass
            if self.log_file:
                try: self.log_file.close()
                except: pass
                self.log_file = None
            self.btn_serial.configure(
                text="▶  INICIAR ENLACE",
                fg_color=ACCENT3, hover_color="#00CC6E", text_color="#000000")
            self.status_badge.offline()
            self._log_console(f"[{datetime.now().strftime('%H:%M:%S')}] ENLACE TERMINADO\n")

    def _listen_serial(self):
        while self.is_reading:
            try:
                if self.serial_port.in_waiting:
                    raw = self.serial_port.readline().decode("utf-8", errors="ignore").strip()
                    if raw:
                        self.after(0, lambda l=raw: self._process_line(l))
                else:
                    time.sleep(0.005)
            except Exception:
                break

    def _process_line(self, line: str):
        s = line.strip()

        # ── Protocolo SD (compatibilidad hacia atrás) ─────────────────────────
        if s == "SD_START":
            self._sd_transfer_active = True; self._sd_buffer = []
            ts = datetime.now().strftime("%Y%m%d_%H%M%S")
            self._sd_file_path = os.path.join(SD_IMPORTS, f"sd_{self.current_athlete}_{ts}.csv")
            self._sd_set_status("RECIBIENDO DATOS SD…", ACCENT2)
            self.sd_progress.set(0); self.sd_progress_lbl.configure(text="0 líneas recibidas")
            self._log_console(line + "\n"); return
        if s == "SD_END":
            self._sd_transfer_active = False; self._sd_flush_to_file()
            self._sd_set_status("TRANSFERENCIA COMPLETA ✓", ACCENT3)
            self._refresh_sd_file_list()
            if self._sd_file_path: self._sd_load_and_analyze(self._sd_file_path)
            self._log_console(line + "\n"); return
        if self._sd_transfer_active:
            self._sd_buffer.append(line)
            n = len(self._sd_buffer)
            self.sd_progress.set(0.1 + 0.8 * ((n % 500) / 500))
            self.sd_progress_lbl.configure(text=f"{n} líneas recibidas")
            self._log_console(line + "\n"); return

        # ── Protocolo DUMP (historial RAM del ESP) ────────────────────────────
        if s == "DUMP_START":
            self._dump_active = True; self._dump_rows = []
            self._log_console(line + "\n"); return
        if s == "DUMP_END":
            self._dump_active = False
            self._process_dump()
            self._log_console(line + "\n"); return
        if self._dump_active:
            self._dump_rows.append(s)
            self._log_console(line + "\n"); return

        # ── Bloque de lanzamiento THROW_START … THROW_END ─────────────────────
        if s == "THROW_START":
            self._in_throw_block = True; self._live_buf = {}
            self._log_console("\n" + "─"*48 + "\n"); return
        if s == "THROW_END":
            self._in_throw_block = False
            self._finalize_throw(self._live_buf)
            self._log_console("─"*48 + "\n"); return

        # ── Línea LIVE: telemetría continua (no se loguea línea a línea) ──────
        if s.startswith("LIVE:"):
            # no imprimir en consola — demasiado volumen
            return

        # ── Línea informativa normal ───────────────────────────────────────────
        self._log_console(line + "\n")

        # Escribir al log de sesión
        if self.log_file is None: self._start_log_file()
        if self.log_file:
            self.log_file.write(f"{line}\n"); self.log_file.flush()

        # Acumular en bloque throw si estamos dentro
        if self._in_throw_block:
            self._parse_throw_field(line, self._live_buf)

        # Actualizar KPIs en tiempo real
        try:
            lo = line.lower()
            if "velocidad" in lo and ":" in line:
                v = line.split(":")[1].split()[0]
                self.kpi_vel.set(v); self.last_v = float(v)
            if ("angulo" in lo or "ángulo" in lo) and ":" in line:
                a = line.split(":")[1].split()[0]
                self.kpi_ang.set(a); self.last_a = float(a)
            if "distancia" in lo and ":" in line:
                d = line.split(":")[1].split()[0]
                self.kpi_dist.set(d)
                self._give_feedback(self.last_v, self.last_a)
            if "aceleracion maxima" in lo and ":" in line:
                self.kpi_acel.set(line.split(":")[1].split()[0])
            if "energia cinetica" in lo and ":" in line:
                self.kpi_ener.set(line.split(":")[1].split()[0])
            if "potencia" in lo and ":" in line:
                self.kpi_pow.set(line.split(":")[1].split()[0])
        except Exception:
            pass

    def _parse_throw_field(self, line: str, buf: dict):
        """Extrae clave:valor de una línea y la guarda en buf."""
        try:
            if ":" in line:
                k, v = line.split(":", 1)
                buf[k.strip().lower()] = v.strip().split()[0]
        except Exception:
            pass

    def _finalize_throw(self, buf: dict):
        """Llamado al recibir THROW_END. Guarda en sesión y actualiza tabla."""
        if not buf: return
        try:
            rec = {
                "num":         int(buf.get("lanzamiento #", len(self._session_throws)+1).split("#")[-1].strip() if "#" in buf.get("lanzamiento #","") else buf.get("lanzamiento #", len(self._session_throws)+1)),
                "velocidad":   float(buf.get("velocidad",   0)),
                "angulo":      float(buf.get("angulo",      0)),
                "distancia":   float(buf.get("distancia",   0)),
                "aceleracion maxima": float(buf.get("aceleracion maxima", 0)),
                "tiempo de impulso":  float(buf.get("tiempo de impulso",  0)),
                "energia cinetica":   float(buf.get("energia cinetica",   0)),
                "potencia":    float(buf.get("potencia",    0)),
            }
        except Exception:
            return
        self._session_throws.append(rec)
        self._add_session_row(rec)
        self.kpi_raw.set(str(len(self._session_throws)))
        self._save_throw_to_log(rec)
        self._generar_reporte_sesion()

    def _add_session_row(self, rec: dict):
        """Añade una fila a la tabla de historial de sesión en la UI."""
        r = self._session_row_count + 1   # fila 0 es cabecera
        self._session_row_count += 1
        vals = [
            (str(rec["num"]),                         TEXT_DIM),
            (f"{rec['velocidad']:.2f}",              ACCENT1),
            (f"{rec['angulo']:.1f}",                 ACCENT2),
            (f"{rec['distancia']:.2f}",              ACCENT3),
            (f"{rec['aceleracion maxima']:.2f}",     "#FF6B35"),
            (f"{rec['tiempo de impulso']:.3f}",      TEXT_SEC),
            (f"{rec['energia cinetica']:.2f}",       "#A855F7"),
            (f"{rec['potencia']:.2f}",               "#EC4899"),
        ]
        for ci, (txt, color) in enumerate(vals):
            ctk.CTkLabel(self.session_scroll, text=txt,
                font=ctk.CTkFont(family="Consolas", size=11),
                text_color=color).grid(row=r, column=ci, padx=4, pady=1, sticky="ew")

    def _save_throw_to_log(self, rec: dict):
        """Guarda el lanzamiento en .log y acumula fila en CSV de sesion."""
        if self.log_file is None: self._start_log_file()
        if self.log_file:
            parts = [
                "# LANZAMIENTO #", str(rec["num"]),
                " | V=",    "{:.2f}".format(rec["velocidad"]),    " m/s",
                " | A=",    "{:.1f}".format(rec["angulo"]),        " deg",
                " | D=",    "{:.2f}".format(rec["distancia"]),     " m",
                " | Acel=", "{:.2f}".format(rec["aceleracion maxima"]),
                " | E=",    "{:.2f}".format(rec["energia cinetica"]), " J",
                " | P=",    "{:.2f}".format(rec["potencia"]),      " W",
            ]
            self.log_file.write("".join(parts) + chr(10))
            self.log_file.flush()

        csv_path = getattr(self, "_session_csv_path", None)
        if csv_path:
            file_exists = os.path.exists(csv_path)
            try:
                import csv as _csv
                with open(csv_path, "a", encoding="utf-8", newline="") as cf:
                    writer = _csv.DictWriter(cf, fieldnames=[
                        "num","Velocidad","Angulo","Distancia",
                        "maxAccel","impulseTime","Energia","Potencia"])
                    if not file_exists:
                        writer.writeheader()
                    writer.writerow({
                        "num":         rec["num"],
                        "Velocidad":   round(rec["velocidad"], 2),
                        "Angulo":      round(rec["angulo"], 1),
                        "Distancia":   round(rec["distancia"], 2),
                        "maxAccel":    round(rec["aceleracion maxima"], 2),
                        "impulseTime": round(rec["tiempo de impulso"], 3),
                        "Energia":     round(rec["energia cinetica"], 2),
                        "Potencia":    round(rec["potencia"], 2),
                    })
            except Exception as e:
                print("[CSV] Error: " + str(e))

    def _generar_reporte_sesion(self):
        """Lanza generar_reporte_automatico en hilo para no bloquear la UI."""
        csv_path = getattr(self, "_session_csv_path", None)
        if not csv_path or not os.path.exists(csv_path):
            return
        def _run():
            plot_path = generar_reporte_automatico(csv_path, self.current_athlete)
            if plot_path:
                base  = os.path.basename(plot_path)
                dname = os.path.dirname(plot_path)
                msg   = "[ANALISIS] Reporte: " + base + chr(10) + "[ANALISIS] Carpeta: " + dname + chr(10)
                self.after(0, lambda m=msg: self._log_console(m))
        threading.Thread(target=_run, daemon=True).start()

    def _request_dump(self):
        """Envía el comando DUMP al ESP32."""
        if not self.is_reading or self.serial_port is None:
            messagebox.showwarning("Sin enlace", "Conecta el ESP32 primero.")
            return
        try:
            self.serial_port.write(b"DUMP\n")
            self._log_console(f"[{datetime.now().strftime('%H:%M:%S')}] → CMD: DUMP enviado\n")
        except Exception as e:
            messagebox.showerror("Error", str(e))

    def _request_reset(self):
        """Envía RESET al ESP32 y limpia la tabla de sesión local."""
        if not self.is_reading or self.serial_port is None:
            messagebox.showwarning("Sin enlace", "Conecta el ESP32 primero.")
            return
        if not messagebox.askyesno("Confirmar RESET",
            "¿Borrar historial del ESP32 y reiniciar contador?\n"
            "(Los logs guardados en disco no se eliminan)"):
            return
        try:
            self.serial_port.write(b"RESET\n")
            self._session_throws.clear()
            self._session_row_count = 0
            for w in self.session_scroll.winfo_children():
                w.destroy()
            self._log_console(f"[{datetime.now().strftime('%H:%M:%S')}] → CMD: RESET enviado\n")
        except Exception as e:
            messagebox.showerror("Error", str(e))

    def _go_to_session_analysis(self):
        """Lleva al analizador con los datos de la sesión actual."""
        if not self._session_throws:
            messagebox.showinfo("Sin datos", "No hay lanzamientos en la sesión actual.")
            return
        import pandas as pd
        df = pd.DataFrame(self._session_throws)
        self._show_history()
        self._render_session_df(df)

    def _process_dump(self):
        """Procesa las filas CSV recibidas del DUMP."""
        import pandas as pd, io
        rows = [r for r in self._dump_rows if r.startswith("CSV_ROW:")]
        hdr  = next((r for r in self._dump_rows if r.startswith("CSV_HEADER:")), None)
        if not rows or not hdr: return
        cols = hdr.replace("CSV_HEADER:", "").split(",")
        data = [r.replace("CSV_ROW:", "").split(",") for r in rows]
        try:
            df = pd.DataFrame(data, columns=cols).apply(pd.to_numeric, errors="coerce")
            # Fusionar con sesión local si hay datos nuevos
            for _, row in df.iterrows():
                rec = {c: row[c] for c in df.columns}
                rec["num"] = int(rec.get("num", 0))
                if not any(t["num"] == rec["num"] for t in self._session_throws):
                    self._session_throws.append(rec)
                    self._add_session_row(rec)
            self._log_console(f"[DUMP] {len(rows)} lanzamientos recibidos.\n")
            # Mostrar análisis automáticamente
            self._show_history()
            self._render_session_df(df)
        except Exception as e:
            self._log_console(f"[DUMP][ERROR] {e}\n")

    def _log_console(self, text: str):
        self.live_console.insert("end", text)
        self.live_console.see("end")

    def _sd_flush_to_file(self):
        """Guarda el buffer SD acumulado a disco."""
        if not self._sd_file_path or not self._sd_buffer:
            return
        try:
            with open(self._sd_file_path, "w", encoding="utf-8") as f:
                f.write(
                    f"# ══════════════════════════════════════\n"
                    f"# LANCEA · VOLCADO SD\n"
                    f"# ATLETA : {self.current_athlete}\n"
                    f"# FECHA  : {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n"
                    f"# LÍNEAS : {len(self._sd_buffer)}\n"
                    f"# ══════════════════════════════════════\n"
                )
                f.writelines(l + "\n" for l in self._sd_buffer)
            self.sd_progress.set(1.0)
            self.sd_progress_lbl.configure(
                text=f"{len(self._sd_buffer)} líneas · guardado en {os.path.basename(self._sd_file_path)}")
        except Exception as e:
            messagebox.showerror("Error al guardar SD", str(e))

    def _start_log_file(self):
        ts = datetime.now().strftime("%Y%m%d_%H%M%S")
        self._session_ts = ts
        dirs = get_session_dirs(self.current_athlete)
        path = os.path.join(dirs["raw"], "sesion_" + ts + ".log")
        self._session_csv_path = os.path.join(dirs["raw"], "sesion_" + ts + ".csv")
        try:
            self.log_file = open(path, "a", encoding="utf-8")
            nl = chr(10)
            header = (
                "# ══════════════════════════════════════" + nl +
                "# LANCEA - REGISTRO DE SESION" + nl +
                "# ATLETA : " + self.current_athlete + nl +
                "# FECHA  : " + datetime.now().strftime("%Y-%m-%d %H:%M:%S") + nl +
                "# ARCHIVO: " + path + nl +
                "# ══════════════════════════════════════" + nl
            )
            self.log_file.write(header)
            self.log_file.flush()
        except Exception as e:
            self.log_file = None
            self._session_csv_path = None

    def _give_feedback(self, v: float, a: float):
        angle_ok = 32 <= a <= 39
        if angle_ok and v >= 25:
            msg = "✅  LANZAMIENTO ÉLITE"
            sub = f"Ángulo óptimo {a:.1f}°  ·  {v:.1f} m/s"
            color = ACCENT3
        elif angle_ok:
            msg = "⚡  ÁNGULO CORRECTO"
            sub = f"Aumenta la velocidad de salida  ({v:.1f} m/s)"
            color = ACCENT2
        elif v >= 25:
            msg = "⚠  AJUSTAR ÁNGULO"
            sub = f"Objetivo 32°–39°  (actual {a:.1f}°)"
            color = ACCENT2
        else:
            msg = "↩  REVISAR TÉCNICA"
            sub = f"Ángulo {a:.1f}°  ·  velocidad {v:.1f} m/s"
            color = RED_ALERT

        self.feedback_text.configure(text=msg, text_color=color)
        self.coach_sub.configure(text=sub)

    # ── IMPORTAR DESDE LANCEA WiFi ────────────────────────────────────────────

    def _import_from_wifi(self):
        """PC conectado a LANCEA_AP -> descarga CSV -> analiza directo."""
        import urllib.request, urllib.error, io
        ip = self.wifi_ip_entry.get().strip() or LANCEA_WIFI_IP
        self.wifi_status_lbl.configure(text="Conectando...", text_color=ACCENT2)
        self.update_idletasks()

        def _run():
            try:
                # Estado del dispositivo
                try:
                    with urllib.request.urlopen("http://" + ip + "/status", timeout=3) as r:
                        import json as _j
                        info = _j.loads(r.read().decode())
                        n_throws = info.get("throws", "?")
                except Exception:
                    n_throws = "?"

                # Descargar CSV
                with urllib.request.urlopen("http://" + ip + "/csv", timeout=5) as r:
                    raw = r.read().decode("utf-8")

                df = pd.read_csv(io.StringIO(raw), comment="#", on_bad_lines="skip")
                if df.empty:
                    self.after(0, lambda: self._wifi_done(False,
                        "El dispositivo no tiene lanzamientos todavia."))
                    return

                # Guardar CSV
                dirs = get_session_dirs(self.current_athlete)
                ts = datetime.now().strftime("%Y%m%d_%H%M%S")
                save_path = os.path.join(dirs["raw"], "wifi_import_" + ts + ".csv")
                df.to_csv(save_path, index=False)

                # Reporte en hilo (no bloquea)
                generar_reporte_automatico(save_path, self.current_athlete)

                n_str = str(n_throws)
                self.after(0, lambda d=df, p=save_path, n=n_str:
                    self._wifi_done(True, n + " lanzamientos importados", d, p))

            except urllib.error.URLError:
                err = "No se pudo conectar a " + ip + chr(10) + "Verifica que el PC este conectado a LANCEA_AP"
                self.after(0, lambda m=err: self._wifi_done(False, m))
            except Exception as e:
                err = str(e)
                self.after(0, lambda m=err: self._wifi_done(False, "Error: " + m))

        threading.Thread(target=_run, daemon=True).start()

    def _wifi_done(self, ok: bool, msg: str, df=None, path: str = ""):
        """Callback en hilo principal tras importacion WiFi."""
        try:
            self.wifi_ip_entry.configure(state="normal")
        except Exception:
            pass
        if ok:
            self.wifi_status_lbl.configure(text="OK " + msg, text_color=ACCENT3)
            self._show_history()
            self.after(150, lambda d=df, p=path: self._wifi_render(d, p))
        else:
            self.wifi_status_lbl.configure(text="Error", text_color=RED_ALERT)
            messagebox.showerror("LANCEA WiFi", msg)

    def _wifi_render(self, df, path: str = ""):
        """Renderiza datos WiFi una vez el frame del analizador esta visible."""
        if df is None or df.empty:
            return
        # Normalizar nombres de columnas (el CSV puede tener minusculas)
        col_map = {
            "velocidad":"Velocidad","angulo":"Angulo","distancia":"Distancia",
            "maxaccel":"maxAccel","impulsetime":"impulseTime",
            "energia":"Energia","potencia":"Potencia",
        }
        df = df.rename(columns={c: col_map.get(c.lower(), c) for c in df.columns})
        df = df.apply(pd.to_numeric, errors="coerce")
        fname = os.path.basename(path) if path else "WiFi import"
        self.file_label.configure(text="  WiFi  " + fname)
        for w in self.history_content.winfo_children():
            w.destroy()
        self._render_session_df(df)

    # ── ANALIZADOR DE ARCHIVOS ─────────────────────────────────────────────────

    def _analyze_file(self):
        path = filedialog.askopenfilename(
            filetypes=[("Archivos LANCEA", "*.csv *.txt *.log"),
                       ("Todos los archivos", "*.*")])
        if not path: return
        self._load_file(path)

    def _browse_athlete_folder(self):
        folder = athlete_dir(self.current_athlete)
        path = filedialog.askopenfilename(
            initialdir=folder,
            filetypes=[("Archivos LANCEA", "*.csv *.txt *.log"),
                       ("Todos los archivos", "*.*")])
        if not path: return
        self._load_file(path)

    def _load_file(self, path: str):
        self.file_label.configure(text=f"  ◫  {os.path.basename(path)}")
        for w in self.history_content.winfo_children():
            w.destroy()

        try:
            df = pd.read_csv(path, sep=None, engine="python",
                             comment="#", on_bad_lines="skip")
            if "Ax" in df.columns or "ax" in df.columns:
                self._render_sensor_plot(df, path)
            else:
                self._render_text_log(path)
        except Exception:
            self._render_text_log(path)

    def _render_session_df(self, df):
        """Muestra análisis de la sesión actual (DataFrame de lanzamientos)."""
        for w in self.history_content.winfo_children():
            w.destroy()

        container = ctk.CTkFrame(self.history_content, fg_color="transparent")
        container.pack(fill="both", expand=True, padx=14, pady=14)
        container.columnconfigure((0,1,2,3), weight=1)
        container.rowconfigure(1, weight=1)

        # KPIs de sesión
        krow = ctk.CTkFrame(container, fg_color="transparent")
        krow.grid(row=0, column=0, columnspan=4, sticky="ew", pady=(0,10))
        krow.columnconfigure((0,1,2,3,4,6), weight=1)

        def sk(parent, title, val, unit, color, col):
            c = ctk.CTkFrame(parent, fg_color=BG_BASE, border_width=1,
                border_color=BORDER, corner_radius=6)
            c.grid(row=0, column=col, padx=4, sticky="ew")
            SectionTitle(c, title).pack(padx=10, pady=(8,2), anchor="w")
            ctk.CTkLabel(c, text=val,
                font=ctk.CTkFont(family="Consolas", size=28, weight="bold"),
                text_color=color).pack(padx=10, anchor="w")
            ctk.CTkLabel(c, text=unit,
                font=ctk.CTkFont(family="Consolas", size=10),
                text_color=TEXT_DIM).pack(padx=10, pady=(0,8), anchor="w")

        def safe(col, fn):
            try: return f"{fn(df[col].dropna()):.2f}" if col in df.columns else "–"
            except: return "–"

        sk(krow, "LANZAMIENTOS",   str(len(df)),                         "#",    TEXT_SEC, 0)
        sk(krow, "VEL. MÁX",       safe("Velocidad", max),               "m/s",  ACCENT1,  1)
        sk(krow, "VEL. PROM",      safe("Velocidad", lambda s: s.mean()),"m/s",  ACCENT1,  2)
        sk(krow, "ÁNGULO PROM",    safe("Angulo",    lambda s: s.mean()),"°",    ACCENT2,  3)
        sk(krow, "DIST. MÁX",      safe("Distancia", max),               "m",    ACCENT3,  4)
        sk(krow, "ENERGÍA MÁX",    safe("Energia",   max),               "J",    "#A855F7",5)
        sk(krow, "POTENCIA MÁX",   safe("Potencia",  max),               "W",    "#EC4899",6)

        # Gráficas
        import matplotlib
        fig = Figure(figsize=(12, 5), facecolor=BG_BASE, tight_layout=True)
        axes = [fig.add_subplot(2, 3, i+1) for i in range(6)]
        plots = [
            ("Velocidad",   ACCENT1,  "Velocidad (m/s)"),
            ("Angulo",      ACCENT2,  "Ángulo (°)"),
            ("Distancia",   ACCENT3,  "Distancia (m)"),
            ("maxAccel",    "#FF6B35","Acel. Máx (m/s²)"),
            ("Energia",     "#A855F7","Energía (J)"),
            ("Potencia",    "#EC4899","Potencia (W)"),
        ]
        for i, (col, color, label) in enumerate(plots):
            ax = axes[i]
            ax.set_facecolor(BG_PANEL)
            colname = col
            # buscar variante case-insensitive
            for c in df.columns:
                if c.lower() == col.lower():
                    colname = c; break
            if colname in df.columns:
                nums = list(range(1, len(df)+1))
                ax.bar(nums, df[colname], color=color, alpha=0.8, width=0.6)
                ax.plot(nums, df[colname], color="white", linewidth=1, alpha=0.5, marker="o", markersize=3)
                if col == "Angulo":
                    ax.axhspan(32, 39, alpha=0.12, color=ACCENT3, label="zona óptima")
            ax.set_title(label, color=TEXT_PRI, fontfamily="monospace", fontsize=9)
            ax.tick_params(colors=TEXT_SEC, labelsize=7)
            for sp in ax.spines.values(): sp.set_edgecolor(BORDER)
            ax.grid(color=BORDER, linestyle="--", alpha=0.3, axis="y")

        canvas = FigureCanvasTkAgg(fig, container)
        canvas.draw()
        canvas.get_tk_widget().grid(row=1, column=0, columnspan=4, sticky="nsew")

        self.file_label.configure(text=f"  ◈  Sesión activa · {len(df)} lanzamientos")

    def _render_text_log(self, path: str):
        """Renderiza un LOG de texto con resumen de KPIs extraídos."""
        with open(path, "r", encoding="utf-8", errors="ignore") as f:
            lines = f.readlines()

        # Extraer métricas
        velocidades, angulos, distancias = [], [], []
        for line in lines:
            lo = line.lower()
            try:
                if "velocidad" in lo:
                    velocidades.append(float(line.split(":")[1].split()[0]))
                if "angulo" in lo or "ángulo" in lo:
                    angulos.append(float(line.split(":")[1].split()[0]))
                if "distancia" in lo:
                    distancias.append(float(line.split(":")[1].split()[0]))
            except Exception:
                pass

        container = ctk.CTkFrame(self.history_content, fg_color="transparent")
        container.pack(fill="both", expand=True, padx=16, pady=16)
        container.columnconfigure((0, 1), weight=1)
        container.rowconfigure(1, weight=1)

        # KPI cards de resumen
        summary = ctk.CTkFrame(container, fg_color="transparent")
        summary.grid(row=0, column=0, columnspan=2, sticky="ew", pady=(0, 12))
        summary.columnconfigure((0, 1, 2), weight=1)

        def mini_kpi(parent, title, val, unit, accent, col):
            card = ctk.CTkFrame(parent, fg_color=BG_BASE, border_width=1,
                border_color=BORDER, corner_radius=6)
            card.grid(row=0, column=col, padx=6, sticky="ew")
            SectionTitle(card, title).pack(padx=12, pady=(10, 2), anchor="w")
            ctk.CTkLabel(card, text=val,
                font=ctk.CTkFont(family="Consolas", size=32, weight="bold"),
                text_color=accent).pack(padx=12, anchor="w")
            ctk.CTkLabel(card, text=unit,
                font=ctk.CTkFont(family="Consolas", size=11),
                text_color=TEXT_DIM).pack(padx=12, pady=(0, 10), anchor="w")

        v_max = f"{max(velocidades):.2f}" if velocidades else "–"
        a_avg = f"{sum(angulos)/len(angulos):.1f}" if angulos else "–"
        d_max = f"{max(distancias):.2f}" if distancias else "–"

        mini_kpi(summary, "VEL. MÁX REGISTRADA", v_max, "m/s", ACCENT1, 0)
        mini_kpi(summary, "ÁNGULO PROMEDIO",      a_avg, "°",   ACCENT2, 1)
        mini_kpi(summary, "DISTANCIA MÁX",        d_max, "m",   ACCENT3, 2)

        # Textbox con el log
        txt = ctk.CTkTextbox(container,
            font=ctk.CTkFont(family="Consolas", size=12),
            fg_color=BG_BASE, text_color=ACCENT3,
            border_width=1, border_color=BORDER, corner_radius=6,
            scrollbar_button_color=BG_HOVER)
        txt.grid(row=1, column=0, columnspan=2, sticky="nsew")
        txt.insert("1.0", "".join(lines))
        txt.configure(state="disabled")

    def _render_sensor_plot(self, df: pd.DataFrame, path: str):
        """Gráfica de datos de sensor con fondo oscuro y estilo LANCEA."""
        fig = Figure(figsize=(10, 5), facecolor=BG_BASE, tight_layout=True)
        ax = fig.add_subplot(111)
        ax.set_facecolor(BG_PANEL)

        # Determinar columnas
        ax_col = "Ax" if "Ax" in df.columns else "ax"
        ay_col = "Ay" if "Ay" in df.columns else "ay"
        az_col = "Az" if "Az" in df.columns else "az"

        if ax_col in df.columns:
            ax.plot(df[ax_col], color="#3A86FF", linewidth=1.2, label="Ax", alpha=0.9)
        if ay_col in df.columns:
            ax.plot(df[ay_col], color=ACCENT2,   linewidth=1.2, label="Ay", alpha=0.9)
        if az_col in df.columns:
            ax.plot(df[az_col], color=ACCENT3,   linewidth=1.2, label="Az", alpha=0.9)

        try:
            mag = np.sqrt(df.get(ax_col, 0)**2 + df.get(ay_col, 0)**2 + df.get(az_col, 0)**2)
            ax.plot(mag, color=ACCENT1, linewidth=2, label="|a|", linestyle="--")
        except Exception:
            pass

        ax.set_title(f"ANÁLISIS DINÁMICO · {os.path.basename(path)}",
            color=TEXT_PRI, fontfamily="monospace", fontsize=12, pad=12)
        ax.set_xlabel("muestra", color=TEXT_SEC, fontfamily="monospace")
        ax.set_ylabel("aceleración (g)", color=TEXT_SEC, fontfamily="monospace")
        ax.tick_params(colors=TEXT_SEC)
        for spine in ax.spines.values():
            spine.set_edgecolor(BORDER)
        ax.grid(color=BORDER, linestyle="--", alpha=0.5)
        legend = ax.legend(facecolor=BG_CARD, edgecolor=BORDER, labelcolor=TEXT_PRI,
            fontsize=10, framealpha=0.9)

        canvas = FigureCanvasTkAgg(fig, self.history_content)
        canvas.draw()
        canvas.get_tk_widget().pack(fill="both", expand=True, padx=8, pady=8)

    # ── FRAME WiFi · PANEL & ATLETAS ──────────────────────────────────────────

    def _build_wifi_frame(self):
        """Panel WiFi con 3 filas fijas:
        row=0  barra IP + botones (fija)
        row=1  panel izquierdo: atletas | panel derecho: tabla lanzamientos (expande)
        row=2  barra de estado (fija)
        """
        self.wifi_frame = ctk.CTkFrame(self.main_area, fg_color="transparent")
        self.wifi_frame.grid_columnconfigure(0, weight=1)
        self.wifi_frame.grid_rowconfigure(1, weight=1)

        # ── ROW 0  BARRA DE CONEXION WiFi ─────────────────────────────────
        top = ctk.CTkFrame(self.wifi_frame, fg_color=BG_PANEL,
            border_width=1, border_color=ACCENT1, corner_radius=8)
        top.grid(row=0, column=0, padx=20, pady=(14,6), sticky="ew")

        ctk.CTkLabel(top, text="LANCEA WiFi",
            font=ctk.CTkFont(family="Consolas", size=13, weight="bold"),
            text_color=ACCENT1).pack(side="left", padx=(14,8), pady=10)

        ctk.CTkFrame(top, width=1, fg_color=BORDER).pack(
            side="left", fill="y", pady=8)

        ctk.CTkLabel(top, text="IP:",
            font=ctk.CTkFont(family="Consolas", size=11),
            text_color=TEXT_SEC).pack(side="left", padx=(10,4))

        self.wifi_panel_ip = ctk.CTkEntry(top,
            font=ctk.CTkFont(family="Consolas", size=12),
            fg_color=BG_CARD, border_color=BORDER, text_color=TEXT_PRI,
            width=130, height=32)
        self.wifi_panel_ip.insert(0, LANCEA_WIFI_IP)
        self.wifi_panel_ip.pack(side="left", padx=4, pady=10)

        ctk.CTkButton(top, text="Conectar",
            command=self._wifi_panel_refresh,
            font=ctk.CTkFont(family="Consolas", size=11, weight="bold"),
            fg_color=ACCENT3, hover_color="#00CC6E", text_color="#000000",
            height=32, corner_radius=6, width=90).pack(side="left", padx=6)

        ctk.CTkButton(top, text="Importar CSV",
            command=self._import_from_wifi,
            font=ctk.CTkFont(family="Consolas", size=11),
            fg_color=ACCENT1, hover_color="#00A8D4", text_color="#000000",
            height=32, corner_radius=6, width=110).pack(side="left", padx=4)

        ctk.CTkButton(top, text="Reset atleta",
            command=self._wifi_reset_atleta,
            font=ctk.CTkFont(family="Consolas", size=11),
            fg_color=BG_CARD, hover_color=BG_HOVER, text_color=RED_ALERT,
            border_width=1, border_color=RED_ALERT,
            height=32, corner_radius=6, width=100).pack(side="right", padx=(4,14))

        self.wifi_panel_status = ctk.CTkLabel(top, text="Sin conexion",
            font=ctk.CTkFont(family="Consolas", size=10),
            text_color=TEXT_DIM)
        self.wifi_panel_status.pack(side="right", padx=8)

        # ── ROW 1  CONTENIDO: atletas + lanzamientos ──────────────────────
        body = ctk.CTkFrame(self.wifi_frame, fg_color="transparent")
        body.grid(row=1, column=0, padx=20, pady=(0,6), sticky="nsew")
        body.grid_columnconfigure(0, weight=1)
        body.grid_columnconfigure(1, weight=2)
        body.grid_rowconfigure(0, weight=1)

        # ── Panel ATLETAS (izquierda) ──────────────────────────────────────
        left = ctk.CTkFrame(body, fg_color=BG_CARD,
            border_width=1, border_color=BORDER, corner_radius=8)
        left.grid(row=0, column=0, padx=(0,8), sticky="nsew")
        left.grid_rowconfigure(2, weight=1)
        left.grid_columnconfigure(0, weight=1)

        SectionTitle(left, "ATLETAS EN DISPOSITIVO").grid(
            row=0, column=0, padx=14, pady=(12,6), sticky="w")

        # Formulario nuevo atleta
        add_row = ctk.CTkFrame(left, fg_color="transparent")
        add_row.grid(row=1, column=0, padx=12, pady=(0,8), sticky="ew")
        add_row.columnconfigure(0, weight=1)

        self.wifi_new_athlete = ctk.CTkEntry(add_row,
            placeholder_text="Nombre del atleta",
            font=ctk.CTkFont(family="Consolas", size=11),
            fg_color=BG_BASE, border_color=BORDER,
            text_color=TEXT_PRI, height=32)
        self.wifi_new_athlete.grid(row=0, column=0, padx=(0,4), sticky="ew")

        ctk.CTkButton(add_row, text="+",
            command=self._wifi_add_athlete,
            font=ctk.CTkFont(family="Consolas", size=13, weight="bold"),
            fg_color=ACCENT3, hover_color="#00CC6E", text_color="#000000",
            height=32, corner_radius=6, width=36).grid(row=0, column=1)

        # Lista de atletas
        self.wifi_athlete_list = ctk.CTkScrollableFrame(left,
            fg_color=BG_BASE, scrollbar_button_color=BG_HOVER,
            corner_radius=6)
        self.wifi_athlete_list.grid(
            row=2, column=0, padx=10, pady=(0,10), sticky="nsew")

        # ── Panel LANZAMIENTOS (derecha) ───────────────────────────────────
        right = ctk.CTkFrame(body, fg_color=BG_CARD,
            border_width=1, border_color=BORDER, corner_radius=8)
        right.grid(row=0, column=1, sticky="nsew")
        right.grid_rowconfigure(1, weight=1)
        right.grid_columnconfigure(0, weight=1)

        # Header derecha con badges
        right_top = ctk.CTkFrame(right, fg_color="transparent")
        right_top.grid(row=0, column=0, padx=14, pady=(12,4), sticky="ew")
        self.wifi_throws_title = SectionTitle(right_top, "LANZAMIENTOS")
        self.wifi_throws_title.pack(side="left")

        # Badges KPI
        self.wifi_badge_v   = ctk.CTkLabel(right_top, text="",
            font=ctk.CTkFont(family="Consolas", size=11, weight="bold"),
            text_color=ACCENT1)
        self.wifi_badge_v.pack(side="right", padx=6)
        self.wifi_badge_d   = ctk.CTkLabel(right_top, text="",
            font=ctk.CTkFont(family="Consolas", size=11, weight="bold"),
            text_color=ACCENT3)
        self.wifi_badge_d.pack(side="right", padx=6)
        self.wifi_badge_a   = ctk.CTkLabel(right_top, text="",
            font=ctk.CTkFont(family="Consolas", size=11, weight="bold"),
            text_color=ACCENT2)
        self.wifi_badge_a.pack(side="right", padx=6)

        # Tabla lanzamientos
        self.wifi_throws_scroll = ctk.CTkScrollableFrame(right,
            fg_color=BG_BASE, scrollbar_button_color=BG_HOVER, corner_radius=6)
        self.wifi_throws_scroll.grid(
            row=1, column=0, padx=10, pady=(0,10), sticky="nsew")
        self.wifi_throws_scroll.columnconfigure((0,1,2,3,4,5,6,7), weight=1)

        for ci, (lbl, color) in enumerate([
            ("#", TEXT_DIM), ("V m/s", ACCENT1), ("Ang", ACCENT2),
            ("Dist m", ACCENT3), ("Acel", "#FF6B35"),
            ("t s", TEXT_SEC), ("E J", "#A855F7"), ("Ang?", TEXT_SEC)
        ]):
            ctk.CTkLabel(self.wifi_throws_scroll, text=lbl,
                font=ctk.CTkFont(family="Consolas", size=10, weight="bold"),
                text_color=color).grid(
                row=0, column=ci, padx=4, pady=2, sticky="ew")

        # ── ROW 2  BARRA DE ESTADO ─────────────────────────────────────────
        bot = ctk.CTkFrame(self.wifi_frame, fg_color=BG_PANEL,
            border_width=1, border_color=BORDER, corner_radius=6)
        bot.grid(row=2, column=0, padx=20, pady=(0,14), sticky="ew")

        self.wifi_estado_lbl = ctk.CTkLabel(bot, text="Estado: ---",
            font=ctk.CTkFont(family="Consolas", size=10),
            text_color=TEXT_DIM)
        self.wifi_estado_lbl.pack(side="left", padx=14, pady=6)

        self.wifi_atleta_activo_lbl = ctk.CTkLabel(bot, text="",
            font=ctk.CTkFont(family="Consolas", size=10, weight="bold"),
            text_color=ACCENT2)
        self.wifi_atleta_activo_lbl.pack(side="right", padx=14, pady=6)

        # Estado interno
        self._wifi_panel_athletes = []    # lista de nombres recibida del ESP
        self._wifi_panel_active   = -1    # indice activo
        self._wifi_panel_throws   = []    # lanzamientos recibidos

    # ── METODOS WiFi PANEL ─────────────────────────────────────────────────────

    def _wifi_get_ip(self) -> str:
        return self.wifi_panel_ip.get().strip() or LANCEA_WIFI_IP

    def _wifi_panel_refresh(self):
        """Consulta /status y /csv al ESP para actualizar el panel."""
        import urllib.request, urllib.error
        ip = self._wifi_get_ip()
        self.wifi_panel_status.configure(text="Conectando...", text_color=ACCENT2)
        self.update_idletasks()

        def _run():
            try:
                import json as _j, io
                # Estado
                with urllib.request.urlopen(
                        "http://" + ip + "/status", timeout=3) as r:
                    info = _j.loads(r.read().decode())

                # CSV de todos los atletas
                with urllib.request.urlopen(
                        "http://" + ip + "/csv?a=Todos", timeout=5) as r:
                    raw_csv = r.read().decode("utf-8")

                self.after(0, lambda i=info, c=raw_csv:
                    self._wifi_panel_update(i, c))

            except urllib.error.URLError:
                self.after(0, lambda: self.wifi_panel_status.configure(
                    text="Sin conexion — verifica LANCEA_AP",
                    text_color=RED_ALERT))
            except Exception as e:
                self.after(0, lambda m=str(e): self.wifi_panel_status.configure(
                    text="Error: " + m, text_color=RED_ALERT))

        threading.Thread(target=_run, daemon=True).start()

    def _wifi_panel_update(self, info: dict, raw_csv: str):
        """Actualiza la UI con los datos recibidos del ESP."""
        import io
        # Status bar
        estado  = info.get("estado", "?")
        atleta  = info.get("atleta_activo", "?")
        n       = info.get("throws", 0)
        self.wifi_panel_status.configure(
            text="Conectado | " + str(n) + " lanzamientos | " + estado,
            text_color=ACCENT3)
        self.wifi_atleta_activo_lbl.configure(
            text="Activo: " + atleta)
        self.wifi_estado_lbl.configure(
            text="Estado ESP: " + estado + " | uptime: " +
                 str(info.get("uptime_s","?")) + " s",
            text_color=TEXT_DIM if estado=="IDLE" else ACCENT2)

        # Parsear CSV
        try:
            df = pd.read_csv(io.StringIO(raw_csv), comment="#", on_bad_lines="skip")
        except Exception:
            df = pd.DataFrame()

        self._wifi_panel_throws = df

        # Extraer lista de atletas del CSV
        if not df.empty and "Atleta" in df.columns:
            athletes = list(df["Atleta"].dropna().unique())
        else:
            athletes = [atleta] if atleta != "?" else ["Invitado"]

        # Guardar activo para resaltarlo
        self._wifi_panel_active_name = atleta
        self._wifi_refresh_athlete_list(athletes, atleta)

        # Mostrar throws del atleta activo
        self._wifi_refresh_throws(df, atleta)

    def _wifi_refresh_athlete_list(self, athletes: list, active_name: str):
        """Redibuja la lista de atletas en el panel izquierdo."""
        for w in self.wifi_athlete_list.winfo_children():
            w.destroy()

        for name in athletes:
            is_active = (name == active_name)
            row = ctk.CTkFrame(self.wifi_athlete_list,
                fg_color=BG_HOVER if is_active else BG_PANEL,
                border_width=1,
                border_color=ACCENT2 if is_active else BORDER,
                corner_radius=6)
            row.pack(fill="x", pady=3, padx=2)

            ctk.CTkLabel(row,
                text=("► " if is_active else "  ") + name,
                font=ctk.CTkFont(family="Consolas", size=12,
                                 weight="bold" if is_active else "normal"),
                text_color=ACCENT2 if is_active else TEXT_PRI
            ).pack(side="left", padx=10, pady=8)

            if not is_active:
                ctk.CTkButton(row, text="Activar",
                    command=lambda n=name: self._wifi_select_athlete(n),
                    font=ctk.CTkFont(family="Consolas", size=10),
                    fg_color=ACCENT3, hover_color="#00CC6E", text_color="#000000",
                    height=26, corner_radius=4, width=70
                ).pack(side="right", padx=8, pady=6)

    def _wifi_refresh_throws(self, df, athlete_name: str):
        """Redibuja la tabla de lanzamientos del atleta activo."""
        # Limpiar filas anteriores (mantener cabecera fila 0)
        for w in self.wifi_throws_scroll.winfo_children():
            if hasattr(w, '_wifi_row'):
                w.destroy()

        # Limpiar todo y redibujar cabecera + datos
        for w in self.wifi_throws_scroll.winfo_children():
            w.destroy()

        for ci, (lbl, color) in enumerate([
            ("#", TEXT_DIM), ("V m/s", ACCENT1), ("Ang", ACCENT2),
            ("Dist m", ACCENT3), ("Acel", "#FF6B35"),
            ("t s", TEXT_SEC), ("E J", "#A855F7"), ("Ang?", TEXT_SEC)
        ]):
            ctk.CTkLabel(self.wifi_throws_scroll, text=lbl,
                font=ctk.CTkFont(family="Consolas", size=10, weight="bold"),
                text_color=color).grid(
                row=0, column=ci, padx=4, pady=2, sticky="ew")

        if df is None or df.empty:
            ctk.CTkLabel(self.wifi_throws_scroll,
                text="Sin lanzamientos",
                font=ctk.CTkFont(family="Consolas", size=11),
                text_color=TEXT_DIM).grid(
                row=1, column=0, columnspan=8, pady=16)
            self.wifi_throws_title.configure(
                text=("LANZAMIENTOS — " + athlete_name).upper())
            self.wifi_badge_v.configure(text="")
            self.wifi_badge_a.configure(text="")
            self.wifi_badge_d.configure(text="")
            return

        # Filtrar por atleta
        if "Atleta" in df.columns:
            df_f = df[df["Atleta"] == athlete_name]
        else:
            df_f = df

        col_map = {"velocidad":"Velocidad","angulo":"Angulo","distancia":"Distancia",
                   "maxaccel":"maxAccel","energia":"Energia","potencia":"Potencia"}
        df_f = df_f.rename(columns={c: col_map.get(c.lower(),c) for c in df_f.columns})
        df_f = df_f.apply(pd.to_numeric, errors="coerce")

        # Actualizar titulo y badges
        n = len(df_f)
        self.wifi_throws_title.configure(
            text=("LANZAMIENTOS — " + athlete_name + " (" + str(n) + ")").upper())

        if n > 0:
            def safe_max(col):
                return "{:.2f}".format(df_f[col].max()) if col in df_f.columns else "-"
            def safe_mean(col):
                return "{:.1f}".format(df_f[col].mean()) if col in df_f.columns else "-"
            self.wifi_badge_v.configure(text="V:" + safe_max("Velocidad") + " m/s")
            self.wifi_badge_a.configure(text="A:" + safe_mean("Angulo") + "deg")
            self.wifi_badge_d.configure(text="D:" + safe_max("Distancia") + " m")
        else:
            self.wifi_badge_v.configure(text="")
            self.wifi_badge_a.configure(text="")
            self.wifi_badge_d.configure(text="")

        # Filas
        for ri, (_, row) in enumerate(df_f.iterrows()):
            r = ri + 1
            ang = row.get("Angulo", 0)
            ang_color = ACCENT3 if 32<=ang<=39 else (ACCENT2 if 28<=ang<=44 else RED_ALERT)
            ang_label = "Optimo" if 32<=ang<=39 else ("Bajo" if ang<32 else "Alto")

            vals = [
                (str(int(row.get("num", ri+1))),      TEXT_DIM),
                ("{:.2f}".format(row.get("Velocidad",0)), ACCENT1),
                ("{:.1f}".format(row.get("Angulo",0)),    ACCENT2),
                ("{:.2f}".format(row.get("Distancia",0)), ACCENT3),
                ("{:.2f}".format(row.get("maxAccel",0)),  "#FF6B35"),
                ("{:.3f}".format(row.get("impulseTime",0)),TEXT_SEC),
                ("{:.2f}".format(row.get("Energia",0)),   "#A855F7"),
                (ang_label,                                ang_color),
            ]
            for ci, (txt, color) in enumerate(vals):
                ctk.CTkLabel(self.wifi_throws_scroll, text=txt,
                    font=ctk.CTkFont(family="Consolas", size=11),
                    text_color=color).grid(
                    row=r, column=ci, padx=4, pady=1, sticky="ew")

    def _wifi_select_athlete(self, name: str):
        """Envía POST /add_atleta (ya existe) + GET /set_atleta al ESP."""
        import urllib.request, urllib.error, urllib.parse
        ip = self._wifi_get_ip()

        def _run():
            try:
                # Buscar el indice del atleta en la lista actual
                # Usamos status para obtener la lista actualizada
                import json as _j
                with urllib.request.urlopen(
                        "http://" + ip + "/status", timeout=3) as r:
                    info = _j.loads(r.read().decode())

                # El ESP no expone indice directamente, usamos la pagina /atletas
                # que acepta /set_atleta?i=N — necesitamos el indice
                # Como workaround: hacemos POST /add_atleta con el nombre
                # (si ya existe devuelve su indice y lo activa)
                data = urllib.parse.urlencode({"nombre": name}).encode()
                req  = urllib.request.Request(
                    "http://" + ip + "/add_atleta",
                    data=data, method="POST")
                urllib.request.urlopen(req, timeout=3)

                # Refrescar panel
                self.after(500, self._wifi_panel_refresh)
            except Exception as e:
                self.after(0, lambda m=str(e): self.wifi_panel_status.configure(
                    text="Error: " + m, text_color=RED_ALERT))

        threading.Thread(target=_run, daemon=True).start()

    def _wifi_add_athlete(self):
        """Registra un nuevo atleta en el ESP via POST /add_atleta."""
        import urllib.request, urllib.error, urllib.parse
        name = self.wifi_new_athlete.get().strip()
        if not name:
            return
        ip = self._wifi_get_ip()

        def _run():
            try:
                data = urllib.parse.urlencode({"nombre": name}).encode()
                req  = urllib.request.Request(
                    "http://" + ip + "/add_atleta",
                    data=data, method="POST")
                urllib.request.urlopen(req, timeout=3)
                self.after(0, lambda: self.wifi_new_athlete.delete(0, "end"))
                self.after(500, self._wifi_panel_refresh)
            except Exception as e:
                self.after(0, lambda m=str(e): self.wifi_panel_status.configure(
                    text="Error al agregar: " + m, text_color=RED_ALERT))

        threading.Thread(target=_run, daemon=True).start()

    def _wifi_reset_atleta(self):
        """Borra los lanzamientos del atleta activo en el ESP via /reset."""
        import urllib.request
        if not messagebox.askyesno("Confirmar",
            "Borrar lanzamientos del atleta activo en el dispositivo?"):
            return
        ip = self._wifi_get_ip()

        def _run():
            try:
                urllib.request.urlopen("http://" + ip + "/reset", timeout=3)
                self.after(500, self._wifi_panel_refresh)
            except Exception as e:
                self.after(0, lambda m=str(e): self.wifi_panel_status.configure(
                    text="Error: " + m, text_color=RED_ALERT))

        threading.Thread(target=_run, daemon=True).start()

        # ── FRAME SD · VOLCADO & ANÁLISIS ─────────────────────────────────────────

    def _build_sd_frame(self):
        self.sd_frame = ctk.CTkFrame(self.main_area, fg_color="transparent")

        # Header
        header = ctk.CTkFrame(self.sd_frame, fg_color="transparent")
        header.pack(fill="x", padx=24, pady=(24, 16))
        ctk.CTkLabel(header, text="SD · VOLCADO & ANÁLISIS",
            font=ctk.CTkFont(family="Consolas", size=20, weight="bold"),
            text_color=TEXT_PRI).pack(side="left")

        # ── Zona superior: dos columnas ───────────────────────────────────────
        top = ctk.CTkFrame(self.sd_frame, fg_color="transparent")
        top.pack(fill="x", padx=24, pady=(0, 14))
        top.columnconfigure((0, 1), weight=1)

        # — Panel izquierdo: conexión y control —
        ctrl_panel = ctk.CTkFrame(top, fg_color=BG_CARD,
            border_width=1, border_color=BORDER, corner_radius=8)
        ctrl_panel.grid(row=0, column=0, padx=(0, 8), sticky="nsew")

        SectionTitle(ctrl_panel, "▣  CONTROL DE TRANSFERENCIA SD").pack(
            padx=16, pady=(16, 10), anchor="w")
        ctk.CTkFrame(ctrl_panel, height=1, fg_color=BORDER).pack(fill="x", padx=16)

        # Estado de transferencia
        state_row = ctk.CTkFrame(ctrl_panel, fg_color="transparent")
        state_row.pack(fill="x", padx=16, pady=12)

        self.sd_dot = ctk.CTkLabel(state_row, text="●",
            font=ctk.CTkFont(size=14), text_color=TEXT_DIM)
        self.sd_dot.pack(side="left", padx=(0, 8))
        self.sd_status_lbl = ctk.CTkLabel(state_row, text="EN ESPERA",
            font=ctk.CTkFont(family="Consolas", size=12, weight="bold"),
            text_color=TEXT_DIM)
        self.sd_status_lbl.pack(side="left")

        # Barra de progreso
        self.sd_progress = ctk.CTkProgressBar(ctrl_panel,
            fg_color=BG_BASE, progress_color=ACCENT1, height=6, corner_radius=3)
        self.sd_progress.set(0)
        self.sd_progress.pack(fill="x", padx=16, pady=(0, 4))

        self.sd_progress_lbl = ctk.CTkLabel(ctrl_panel, text="0 líneas recibidas",
            font=ctk.CTkFont(family="Consolas", size=10), text_color=TEXT_DIM)
        self.sd_progress_lbl.pack(padx=16, pady=(0, 10), anchor="w")

        # Botón solicitar volcado
        btn_row = ctk.CTkFrame(ctrl_panel, fg_color="transparent")
        btn_row.pack(fill="x", padx=16, pady=(4, 16))

        self.btn_sd_dump = ctk.CTkButton(btn_row,
            text="▶  SOLICITAR VOLCADO SD",
            command=self._request_sd_dump,
            font=ctk.CTkFont(family="Consolas", size=12, weight="bold"),
            fg_color=ACCENT1, hover_color="#00A8D4", text_color="#000000",
            height=38, corner_radius=6)
        self.btn_sd_dump.pack(side="left", padx=(0, 8))

        ctk.CTkButton(btn_row, text="📂  ABRIR CSV / LOG",
            command=self._sd_open_local,
            font=ctk.CTkFont(family="Consolas", size=12),
            fg_color=BG_BASE, hover_color=BG_HOVER,
            border_width=1, border_color=BORDER,
            height=38, corner_radius=6).pack(side="left")

        # — Panel derecho: archivos importados —
        files_panel = ctk.CTkFrame(top, fg_color=BG_CARD,
            border_width=1, border_color=BORDER, corner_radius=8)
        files_panel.grid(row=0, column=1, padx=(8, 0), sticky="nsew")
        files_panel.grid_rowconfigure(1, weight=1)
        files_panel.grid_columnconfigure(0, weight=1)

        hdr2 = ctk.CTkFrame(files_panel, fg_color="transparent")
        hdr2.grid(row=0, column=0, sticky="ew", padx=16, pady=(16, 0))
        SectionTitle(files_panel, "◫  ARCHIVOS IMPORTADOS DESDE SD").grid(
            row=0, column=0, padx=16, pady=(16, 6), sticky="w")

        self.sd_file_list = ctk.CTkScrollableFrame(files_panel,
            fg_color=BG_BASE, scrollbar_button_color=BG_HOVER,
            corner_radius=6, height=140)
        self.sd_file_list.grid(row=1, column=0, padx=12, pady=(0, 12), sticky="nsew")
        self._refresh_sd_file_list()

        # ── Zona inferior: análisis ───────────────────────────────────────────
        analysis_outer = ctk.CTkFrame(self.sd_frame, fg_color=BG_CARD,
            border_width=1, border_color=BORDER, corner_radius=8)
        analysis_outer.pack(fill="both", expand=True, padx=24, pady=(0, 20))

        # Sub-toolbar de análisis
        atb = ctk.CTkFrame(analysis_outer, fg_color="transparent")
        atb.pack(fill="x", padx=16, pady=(14, 8))

        SectionTitle(atb, "◧  ANÁLISIS DE DATOS SD").pack(side="left")

        self.sd_chart_mode = ctk.CTkSegmentedButton(atb,
            values=["Aceleración", "Velocidad", "Ángulo", "Distancia", "Todo"],
            command=self._sd_replot,
            font=ctk.CTkFont(family="Consolas", size=11),
            fg_color=BG_BASE, selected_color=ACCENT1,
            selected_hover_color="#00A8D4",
            unselected_color=BG_BASE, unselected_hover_color=BG_HOVER,
            text_color=TEXT_PRI)
        self.sd_chart_mode.set("Todo")
        self.sd_chart_mode.pack(side="right")

        ctk.CTkFrame(analysis_outer, height=1, fg_color=BORDER).pack(fill="x", padx=16)

        # KPIs de análisis SD
        self.sd_kpi_row = ctk.CTkFrame(analysis_outer, fg_color="transparent")
        self.sd_kpi_row.pack(fill="x", padx=16, pady=10)
        self.sd_kpi_row.columnconfigure((0, 1, 2, 3, 4), weight=1)
        self._sd_kpi_labels: dict[str, ctk.CTkLabel] = {}
        sd_kpis = [
            ("V_MAX", "VEL. PICO",   "m/s", ACCENT1, 0),
            ("A_OPT", "% ÁNG. ÓPTIMO","%" , ACCENT2, 1),
            ("D_MAX", "DIST. MÁX",   "m",   ACCENT3, 2),
            ("LANZ",  "LANZAMIENTOS","#",   TEXT_SEC, 3),
            ("DUR",   "DURACIÓN",    "s",   TEXT_DIM, 4),
        ]
        for key, lbl, unit, color, col in sd_kpis:
            card = ctk.CTkFrame(self.sd_kpi_row, fg_color=BG_BASE,
                border_width=1, border_color=BORDER, corner_radius=6)
            card.grid(row=0, column=col, padx=4, sticky="ew")
            SectionTitle(card, lbl).pack(padx=10, pady=(8, 2), anchor="w")
            vl = ctk.CTkLabel(card, text="–",
                font=ctk.CTkFont(family="Consolas", size=22, weight="bold"),
                text_color=color)
            vl.pack(padx=10, anchor="w")
            ctk.CTkLabel(card, text=unit,
                font=ctk.CTkFont(family="Consolas", size=10),
                text_color=TEXT_DIM).pack(padx=10, pady=(0, 8), anchor="w")
            self._sd_kpi_labels[key] = vl

        # Área de gráfica / log
        self.sd_plot_area = ctk.CTkFrame(analysis_outer,
            fg_color=BG_BASE, corner_radius=6)
        self.sd_plot_area.pack(fill="both", expand=True, padx=16, pady=(0, 14))

        # Placeholder
        self._sd_placeholder()

        # Datos cargados en memoria para re-plot
        self._sd_df: pd.DataFrame | None = None
        self._sd_text_lines: list[str] = []

    def _sd_placeholder(self):
        for w in self.sd_plot_area.winfo_children():
            w.destroy()
        ph = ctk.CTkFrame(self.sd_plot_area, fg_color="transparent")
        ph.pack(expand=True)
        ctk.CTkLabel(ph, text="▣",
            font=ctk.CTkFont(size=48), text_color=TEXT_DIM).pack()
        ctk.CTkLabel(ph,
            text="Solicita un volcado desde el ESP32 o abre un archivo exportado de la SD",
            font=ctk.CTkFont(family="Consolas", size=12), text_color=TEXT_DIM,
            wraplength=480, justify="center").pack(pady=8)

    # ── LÓGICA SD ──────────────────────────────────────────────────────────────

    def _request_sd_dump(self):
        """Envía el comando SD_DUMP al ESP32 por el puerto serial activo."""
        if not self.is_reading or self.serial_port is None:
            messagebox.showwarning("Sin enlace",
                "Debes iniciar el enlace serial antes de solicitar el volcado.")
            return
        try:
            self.serial_port.write(b"SD_DUMP\n")
            self._sd_transfer_active = True
            self._sd_buffer = []
            self._sd_set_status("RECIBIENDO DATOS SD…", ACCENT2)
            self.sd_progress.set(0)
            self.sd_progress_lbl.configure(text="0 líneas recibidas")
            self._log_console(f"[{datetime.now().strftime('%H:%M:%S')}] → CMD: SD_DUMP enviado\n")
        except Exception as e:
            messagebox.showerror("Error", str(e))

    def _sd_set_status(self, text: str, color: str):
        self.sd_dot.configure(text_color=color)
        self.sd_status_lbl.configure(text=text, text_color=color)

    def _sd_open_local(self):
        """Abre un CSV/LOG ya exportado de la SD sin usar el puerto serial."""
        path = filedialog.askopenfilename(
            initialdir=SD_IMPORTS,
            filetypes=[("Datos SD", "*.csv *.txt *.log"),
                       ("Todos los archivos", "*.*")])
        if path:
            self._sd_load_and_analyze(path)

    def _refresh_sd_file_list(self):
        for w in self.sd_file_list.winfo_children():
            w.destroy()
        files = sorted(
            [f for f in os.listdir(SD_IMPORTS)
             if f.endswith((".csv", ".log", ".txt"))],
            reverse=True)
        if not files:
            ctk.CTkLabel(self.sd_file_list, text="Sin archivos importados",
                font=ctk.CTkFont(family="Consolas", size=11),
                text_color=TEXT_DIM).pack(pady=12)
            return
        for fname in files:
            fpath = os.path.join(SD_IMPORTS, fname)
            size  = os.path.getsize(fpath)
            size_str = f"{size/1024:.1f} KB" if size >= 1024 else f"{size} B"

            row = ctk.CTkFrame(self.sd_file_list, fg_color=BG_PANEL,
                border_width=1, border_color=BORDER, corner_radius=5)
            row.pack(fill="x", pady=3, padx=2)

            ctk.CTkLabel(row, text="▣",
                font=ctk.CTkFont(size=13), text_color=ACCENT1).pack(
                side="left", padx=10, pady=8)
            ctk.CTkLabel(row, text=fname,
                font=ctk.CTkFont(family="Consolas", size=11),
                text_color=TEXT_PRI).pack(side="left", pady=8)
            ctk.CTkLabel(row, text=size_str,
                font=ctk.CTkFont(family="Consolas", size=10),
                text_color=TEXT_DIM).pack(side="right", padx=10)

            # Click para analizar
            for child in row.winfo_children():
                child.bind("<Button-1>",
                    lambda e, p=fpath: self._sd_load_and_analyze(p))
            row.bind("<Button-1>",
                lambda e, p=fpath: self._sd_load_and_analyze(p))

    def _sd_load_and_analyze(self, path: str):
        """Detecta el tipo de archivo SD y lanza el análisis adecuado."""
        self._sd_set_status(f"CARGADO: {os.path.basename(path)}", ACCENT3)
        try:
            df = pd.read_csv(path, sep=None, engine="python",
                             comment="#", on_bad_lines="skip")
            self._sd_df = df
            self._sd_text_lines = []
            self._sd_update_kpis(df)
            self._sd_replot(self.sd_chart_mode.get())
        except Exception:
            with open(path, "r", encoding="utf-8", errors="ignore") as f:
                self._sd_text_lines = f.readlines()
            self._sd_df = None
            self._sd_update_kpis_from_text(self._sd_text_lines)
            self._sd_render_text()

    def _sd_update_kpis(self, df: pd.DataFrame):
        """Calcula y muestra KPIs desde un DataFrame numérico."""
        def col(names):
            for n in names:
                if n in df.columns: return n
            return None

        v_col  = col(["Velocidad", "velocidad", "V", "v"])
        a_col  = col(["Angulo", "angulo", "Ángulo", "A_deg"])
        d_col  = col(["Distancia", "distancia", "D"])
        ax_col = col(["Ax", "ax"])
        ay_col = col(["Ay", "ay"])
        az_col = col(["Az", "az"])

        v_max = f"{df[v_col].max():.2f}" if v_col else "–"
        d_max = f"{df[d_col].max():.2f}" if d_col else "–"
        lanz  = str(len(df)) if ax_col else "–"

        if a_col:
            pct = (((df[a_col] >= 32) & (df[a_col] <= 39)).sum() / len(df) * 100)
            a_opt = f"{pct:.0f}"
        else:
            a_opt = "–"

        dur = f"{len(df) * 0.01:.1f}" if ax_col else "–"  # asume 100 Hz

        self._sd_kpi_labels["V_MAX"].configure(text=v_max)
        self._sd_kpi_labels["A_OPT"].configure(text=a_opt)
        self._sd_kpi_labels["D_MAX"].configure(text=d_max)
        self._sd_kpi_labels["LANZ"].configure(text=lanz)
        self._sd_kpi_labels["DUR"].configure(text=dur)

    def _sd_update_kpis_from_text(self, lines: list[str]):
        """Extrae KPIs desde un archivo de texto/log."""
        vs, angs, dists = [], [], []
        for line in lines:
            lo = line.lower()
            try:
                if "velocidad" in lo: vs.append(float(line.split(":")[1].split()[0]))
                if "angulo" in lo or "ángulo" in lo:
                    angs.append(float(line.split(":")[1].split()[0]))
                if "distancia" in lo: dists.append(float(line.split(":")[1].split()[0]))
            except Exception:
                pass
        self._sd_kpi_labels["V_MAX"].configure(text=f"{max(vs):.2f}" if vs else "–")
        self._sd_kpi_labels["A_OPT"].configure(
            text=f"{sum(1 for a in angs if 32<=a<=39)/len(angs)*100:.0f}" if angs else "–")
        self._sd_kpi_labels["D_MAX"].configure(text=f"{max(dists):.2f}" if dists else "–")
        self._sd_kpi_labels["LANZ"].configure(text=str(len(vs)))
        self._sd_kpi_labels["DUR"].configure(text="–")

    def _sd_replot(self, mode: str):
        """Re-dibuja la gráfica según el modo seleccionado."""
        if self._sd_df is None:
            if self._sd_text_lines:
                self._sd_render_text()
            return
        self._sd_render_plot(self._sd_df, mode)

    def _sd_render_plot(self, df: pd.DataFrame, mode: str):
        for w in self.sd_plot_area.winfo_children():
            w.destroy()

        def col(names):
            for n in names:
                if n in df.columns: return n
            return None

        ax_col = col(["Ax","ax"]); ay_col = col(["Ay","ay"]); az_col = col(["Az","az"])
        v_col  = col(["Velocidad","velocidad","V"])
        a_col  = col(["Angulo","angulo","Ángulo"])
        d_col  = col(["Distancia","distancia","D"])

        series_map = {
            "Aceleración": [
                (ax_col, "#3A86FF", "Ax"), (ay_col, ACCENT2, "Ay"),
                (az_col, ACCENT3, "Az")],
            "Velocidad":   [(v_col, ACCENT1, "Velocidad (m/s)")],
            "Ángulo":      [(a_col, ACCENT2, "Ángulo (°)")],
            "Distancia":   [(d_col, ACCENT3, "Distancia (m)")],
        }

        if mode == "Todo":
            plots = []
            for key, series in series_map.items():
                plots.extend([(c, col_c, lbl) for c, col_c, lbl in series if c])
        else:
            plots = [(c, col_c, lbl) for c, col_c, lbl in series_map.get(mode, []) if c]

        if not plots:
            self._sd_placeholder()
            return

        n_subplots = 1 if mode != "Todo" else min(len(plots), 4)
        use_subplots = mode == "Todo" and n_subplots > 1

        if use_subplots:
            fig = Figure(figsize=(10, 5), facecolor=BG_BASE, tight_layout=True)
            axes = [fig.add_subplot(2, 2, i+1) for i in range(n_subplots)]
            for i, (c, color, label) in enumerate(plots[:n_subplots]):
                ax = axes[i]
                ax.set_facecolor(BG_PANEL)
                ax.plot(df[c], color=color, linewidth=1.2, alpha=0.9)
                if mode == "Todo" and c == a_col:
                    ax.axhspan(32, 39, alpha=0.08, color=ACCENT3, label="zona óptima")
                ax.set_title(label, color=TEXT_PRI, fontfamily="monospace", fontsize=10)
                ax.tick_params(colors=TEXT_SEC, labelsize=8)
                for sp in ax.spines.values(): sp.set_edgecolor(BORDER)
                ax.grid(color=BORDER, linestyle="--", alpha=0.4)
        else:
            fig = Figure(figsize=(10, 4), facecolor=BG_BASE, tight_layout=True)
            ax = fig.add_subplot(111)
            ax.set_facecolor(BG_PANEL)
            for c, color, label in plots:
                ax.plot(df[c], color=color, linewidth=1.4, label=label, alpha=0.92)
            if mode == "Ángulo" and a_col:
                ax.axhspan(32, 39, alpha=0.10, color=ACCENT3, label="zona óptima 32–39°")
            ax.set_title(f"SD · {mode}", color=TEXT_PRI, fontfamily="monospace", fontsize=12)
            ax.tick_params(colors=TEXT_SEC)
            for sp in ax.spines.values(): sp.set_edgecolor(BORDER)
            ax.grid(color=BORDER, linestyle="--", alpha=0.4)
            ax.legend(facecolor=BG_CARD, edgecolor=BORDER,
                labelcolor=TEXT_PRI, fontsize=10)

        canvas = FigureCanvasTkAgg(fig, self.sd_plot_area)
        canvas.draw()
        canvas.get_tk_widget().pack(fill="both", expand=True)

    def _sd_render_text(self):
        for w in self.sd_plot_area.winfo_children():
            w.destroy()
        txt = ctk.CTkTextbox(self.sd_plot_area,
            font=ctk.CTkFont(family="Consolas", size=12),
            fg_color=BG_BASE, text_color=ACCENT3,
            border_width=0, scrollbar_button_color=BG_HOVER)
        txt.pack(fill="both", expand=True, padx=4, pady=4)
        txt.insert("1.0", "".join(self._sd_text_lines))
        txt.configure(state="disabled")

    # ── INTERCEPCIÓN SERIAL PARA PROTOCOLO SD ──────────────────────────────────
    # El ESP32 debe enviar:
    #   SD_START            ← inicio del volcado
    #   <líneas de datos>
    #   SD_END              ← fin del volcado
    #
    # Esto se gestiona en _process_line sin romper la telemetría normal.

    

    def _refresh_athlete_list(self):
        for w in self.athlete_scroll.winfo_children():
            w.destroy()

        for name in self.cfg["athletes"]:
            folder = os.path.join(ATHLETES, name)
            count = 0
            if os.path.exists(folder):
                count = len([f for f in os.listdir(folder)
                             if f.endswith((".log", ".csv", ".txt"))])

            row = ctk.CTkFrame(self.athlete_scroll, fg_color=BG_PANEL,
                border_width=1, border_color=BORDER, corner_radius=6)
            row.pack(fill="x", pady=4, padx=4)

            ctk.CTkLabel(row, text="◈",
                font=ctk.CTkFont(size=18), text_color=ACCENT1).pack(
                side="left", padx=14, pady=12)
            ctk.CTkLabel(row, text=name,
                font=ctk.CTkFont(family="Consolas", size=14, weight="bold"),
                text_color=TEXT_PRI).pack(side="left", pady=12)
            ctk.CTkLabel(row, text=f"{count} registro(s)",
                font=ctk.CTkFont(family="Consolas", size=11),
                text_color=TEXT_DIM).pack(side="left", padx=12, pady=12)

            if name != "Invitado":
                ctk.CTkButton(row, text="✕",
                    command=lambda n=name: self._delete_athlete(n),
                    width=32, height=28, fg_color=BG_CARD,
                    hover_color=RED_ALERT, text_color=TEXT_SEC,
                    corner_radius=4, font=ctk.CTkFont(size=12)
                ).pack(side="right", padx=12, pady=8)

    def _add_athlete(self):
        name = self.new_athlete_entry.get().strip()
        if not name:
            return
        if name in self.cfg["athletes"]:
            messagebox.showwarning("Duplicado", f"El atleta '{name}' ya existe.")
            return
        self.cfg["athletes"].append(name)
        save_config(self.cfg)
        athlete_dir(name)
        self.new_athlete_entry.delete(0, "end")
        self.athlete_menu.configure(values=self.cfg["athletes"])
        self._refresh_athlete_list()

    def _delete_athlete(self, name: str):
        if not messagebox.askyesno("Confirmar",
            f"¿Eliminar atleta '{name}'?\n(Los archivos de log se conservan en disco)"):
            return
        self.cfg["athletes"].remove(name)
        save_config(self.cfg)
        self.athlete_menu.configure(values=self.cfg["athletes"])
        if self.current_athlete == name:
            self.current_athlete = "Invitado"
            self.athlete_menu.set("Invitado")
        self._refresh_athlete_list()

    def _set_athlete(self, name: str):
        self.current_athlete = name
        self.cfg["last_athlete"] = name
        save_config(self.cfg)
        if self.log_file:
            self.log_file.close()
            self.log_file = None

    # ── NAVEGACIÓN ─────────────────────────────────────────────────────────────

    def _hide_all(self):
        for f in [self.live_frame, self.history_frame,
                  self.wifi_frame, self.sd_frame, self.config_frame]:
            f.pack_forget()
        for btn in self._nav_btns:
            btn.deactivate()

    def _show_live(self):
        self._hide_all()
        self.live_frame.pack(fill="both", expand=True)
        self._nav_btns[0].activate()

    def _show_history(self):
        self._hide_all()
        self.history_frame.pack(fill="both", expand=True)
        self._nav_btns[1].activate()

    def _show_wifi(self):
        self._hide_all()
        self.wifi_frame.pack(fill="both", expand=True)
        self._nav_btns[2].activate()
        self._wifi_panel_refresh()

    def _show_sd(self):
        self._hide_all()
        self.sd_frame.pack(fill="both", expand=True)
        self._refresh_sd_file_list()
        self._nav_btns[3].activate()

    def _show_config(self):
        self._hide_all()
        self.config_frame.pack(fill="both", expand=True)
        self._refresh_athlete_list()
        self._nav_btns[4].activate()

    # ── RELOJ ──────────────────────────────────────────────────────────────────

    def _update_clock(self):
        now = datetime.now().strftime("%Y-%m-%d   %H:%M:%S")
        self.ts_label.configure(text=now)
        self.after(1000, self._update_clock)


# ── ENTRY POINT ───────────────────────────────────────────────────────────────

if __name__ == "__main__":
    ensure_dirs()
    app = LanceaApp()
    app.mainloop()
