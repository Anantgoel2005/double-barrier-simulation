"""
RTD_GUI_PYTHON - Standalone Desktop Application for Resonant Tunnelling & RTD Diode
Runs on 100% pure standard Python (Python 3.x + Tkinter).
ZERO external packages required (no numpy, no scipy, no matplotlib needed).

Features:
  - Interactive sliders: Barrier Height (V0), Thickness (Lb), Well Width (Lw), Diode Bias (Va), Incident Energy (E)
  - Exact Transfer Matrix Method (TMM) calculation in complex arithmetic
  - Real-time plots:
      1. Conduction Band Profile V(x) & Wavefunction |psi(x)|^2
      2. Transmission Spectrum T(E) with resonance detection
      3. RTD Diode I-V Curve with Negative Differential Resistance (NDR) highlighted
      4. Interactive 3D Quantum Cavity View (drag to rotate in 3D)
  - Auto-Snap to Resonant Peak
  - Live 3D Wavepacket Oscillation Animation

Run:
  python rtd_gui_python.py
"""

import math
import cmath
import tkinter as tk
from tkinter import ttk

# Physical Constants (SI)
HBAR = 1.054571817e-34  # J*s
M0 = 9.1093837e-31       # kg
E_CH = 1.602176634e-19   # C
KB = 1.380649e-23        # J/K
TEMP = 300.0             # K
KBT = KB * TEMP
M_EFF = 0.067 * M0       # GaAs effective mass

class RTDSimulationApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Resonant Tunnelling & RTD Diode Simulator (Pure Python)")
        self.root.geometry("1300x820")
        self.root.configure(bg="#0f141c")

        # Simulation Parameters
        self.V0 = tk.DoubleVar(value=0.30)
        self.Lb = tk.DoubleVar(value=3.00)
        self.Lw = tk.DoubleVar(value=5.00)
        self.Va = tk.DoubleVar(value=0.00)
        self.E  = tk.DoubleVar(value=0.088)

        self.animating = False
        self.wave_t = 0.0
        self.view_3d = tk.BooleanVar(value=False)
        self.use_log = tk.BooleanVar(value=False)

        # 3D View rotation angles
        self.rot_x = 0.55
        self.rot_y = -0.65
        self.zoom = 1.0
        self.drag_start = None

        self.peaks = []
        self.iv_cache = None

        self.build_ui()
        self.update_simulation(recalc_iv=True)

    def build_ui(self):
        # Main layout: Left control sidebar, Right plot dashboard
        sidebar = tk.Frame(self.root, bg="#171f2c", width=340, padx=16, pady=16)
        sidebar.pack(side=tk.LEFT, fill=tk.Y)
        sidebar.pack_propagate(False)

        # Title
        tk.Label(sidebar, text="Resonant Tunnelling Lab", font=("Segoe UI", 14, "bold"),
                 fg="#38bdf8", bg="#171f2c").pack(anchor="w", pady=(0, 2))
        tk.Label(sidebar, text="Quantum Double Barrier & RTD Simulator", font=("Segoe UI", 9),
                 fg="#94a3b8", bg="#171f2c").pack(anchor="w", pady=(0, 16))

        # Sliders
        self.add_slider(sidebar, "Barrier Height (V₀) [eV]:", self.V0, 0.10, 1.20, 0.01, " eV", recalc=True)
        self.add_slider(sidebar, "Barrier Thickness (L_b) [nm]:", self.Lb, 1.0, 7.0, 0.1, " nm", recalc=True)
        self.add_slider(sidebar, "Quantum Well Width (L_w) [nm]:", self.Lw, 2.0, 12.0, 0.1, " nm", recalc=True)
        self.add_slider(sidebar, "Applied Diode Bias (V_a) [V]:", self.Va, 0.0, 0.35, 0.005, " V", recalc=False)
        self.add_slider(sidebar, "Incident Energy (E) [eV]:", self.E, 0.005, 0.60, 0.002, " eV", recalc=False)

        # Action Buttons
        btn_frame = tk.Frame(sidebar, bg="#171f2c")
        btn_frame.pack(fill=tk.X, pady=12)

        tk.Button(btn_frame, text="⚡ Auto-Snap to Resonant Peak", bg="#0284c7", fg="white",
                  font=("Segoe UI", 9, "bold"), relief="flat", cursor="hand2",
                  command=self.snap_to_resonance).pack(fill=tk.X, pady=4)

        self.btn_anim = tk.Button(btn_frame, text="▶ Animate 3D Wavepacket", bg="#1e2838", fg="#f1f5f9",
                                  font=("Segoe UI", 9, "bold"), relief="groove", cursor="hand2",
                                  command=self.toggle_animation)
        self.btn_anim.pack(fill=tk.X, pady=4)

        tk.Button(btn_frame, text="🔄 Toggle 2D / 3D Cavity View", bg="#1e2838", fg="#f1f5f9",
                  font=("Segoe UI", 9), relief="groove", cursor="hand2",
                  command=self.toggle_3d).pack(fill=tk.X, pady=4)

        # Status & Readout Card
        readout_card = tk.LabelFrame(sidebar, text="Device Metrics", font=("Segoe UI", 9, "bold"),
                                     bg="#1e2838", fg="#fbbf24", padx=10, pady=10)
        readout_card.pack(fill=tk.X, pady=8)

        self.lbl_E1 = tk.Label(readout_card, text="Resonance E₁: --", font=("Segoe UI", 8), fg="#f1f5f9", bg="#1e2838", anchor="w")
        self.lbl_E1.pack(fill=tk.X)
        self.lbl_tau = tk.Label(readout_card, text="Lifetime τ: --", font=("Segoe UI", 8), fg="#f1f5f9", bg="#1e2838", anchor="w")
        self.lbl_tau.pack(fill=tk.X)
        self.lbl_pvcr = tk.Label(readout_card, text="PVCR Ratio: --", font=("Segoe UI", 8), fg="#f1f5f9", bg="#1e2838", anchor="w")
        self.lbl_pvcr.pack(fill=tk.X)
        self.lbl_peak = tk.Label(readout_card, text="Peak Voltage: --", font=("Segoe UI", 8), fg="#f1f5f9", bg="#1e2838", anchor="w")
        self.lbl_peak.pack(fill=tk.X)

        self.lbl_status = tk.Label(readout_card, text="Thermal Equilibrium", font=("Segoe UI", 9, "bold"),
                                   fg="#38bdf8", bg="#1e2838", wraplength=280, justify="left")
        self.lbl_status.pack(fill=tk.X, pady=(8, 0))

        # Dashboard Area
        dashboard = tk.Frame(self.root, bg="#0f141c")
        dashboard.pack(side=tk.RIGHT, fill=tk.BOTH, expand=True, padx=12, pady=12)

        # 4 Quadrants: Top-Left (Band Profile), Top-Right (Transmission T(E)),
        # Bottom-Left (RTD I-V), Bottom-Right (3D Quantum Cavity)
        dashboard.rowconfigure(0, weight=1)
        dashboard.rowconfigure(1, weight=1)
        dashboard.columnconfigure(0, weight=1)
        dashboard.columnconfigure(1, weight=1)

        # Canvas 1: Band Profile
        f1 = tk.Frame(dashboard, bg="#171f2c", bd=1, relief="solid")
        f1.grid(row=0, column=0, sticky="nsew", padx=6, pady=6)
        tk.Label(f1, text="Conduction Band Profile V(x) & |ψ(x)|²", font=("Segoe UI", 9, "bold"),
                 fg="#f1f5f9", bg="#171f2c").pack(anchor="w", padx=8, pady=4)
        self.c_band = tk.Canvas(f1, bg="#0f141c", highlightthickness=0)
        self.c_band.pack(fill=tk.BOTH, expand=True, padx=8, pady=(0, 8))

        # Canvas 2: Transmission Spectrum
        f2 = tk.Frame(dashboard, bg="#171f2c", bd=1, relief="solid")
        f2.grid(row=0, column=1, sticky="nsew", padx=6, pady=6)
        tk.Label(f2, text="Transmission Spectrum T(E)", font=("Segoe UI", 9, "bold"),
                 fg="#f1f5f9", bg="#171f2c").pack(anchor="w", padx=8, pady=4)
        self.c_trans = tk.Canvas(f2, bg="#0f141c", highlightthickness=0)
        self.c_trans.pack(fill=tk.BOTH, expand=True, padx=8, pady=(0, 8))

        # Canvas 3: RTD I-V Curve
        f3 = tk.Frame(dashboard, bg="#171f2c", bd=1, relief="solid")
        f3.grid(row=1, column=0, sticky="nsew", padx=6, pady=6)
        tk.Label(f3, text="Resonant Tunnelling Diode I-V Curve (NDR)", font=("Segoe UI", 9, "bold"),
                 fg="#f1f5f9", bg="#171f2c").pack(anchor="w", padx=8, pady=4)
        self.c_iv = tk.Canvas(f3, bg="#0f141c", highlightthickness=0)
        self.c_iv.pack(fill=tk.BOTH, expand=True, padx=8, pady=(0, 8))

        # Canvas 4: 3D Quantum Cavity View
        f4 = tk.Frame(dashboard, bg="#171f2c", bd=1, relief="solid")
        f4.grid(row=1, column=1, sticky="nsew", padx=6, pady=6)
        tk.Label(f4, text="3D Quantum Cavity View (Drag to Rotate)", font=("Segoe UI", 9, "bold"),
                 fg="#f1f5f9", bg="#171f2c").pack(anchor="w", padx=8, pady=4)
        self.c_3d = tk.Canvas(f4, bg="#080c14", highlightthickness=0, cursor="fleur")
        self.c_3d.pack(fill=tk.BOTH, expand=True, padx=8, pady=(0, 8))

        # 3D Mouse Drag & Zoom Bindings
        self.c_3d.bind("<ButtonPress-1>", self.on_3d_press)
        self.c_3d.bind("<B1-Motion>", self.on_3d_drag)
        self.c_3d.bind("<MouseWheel>", self.on_3d_zoom)

    def add_slider(self, parent, label_text, var, from_, to, step, unit, recalc):
        f = tk.Frame(parent, bg="#171f2c")
        f.pack(fill=tk.X, pady=5)

        val_lbl = tk.Label(f, text=f"{var.get():.3f}{unit}", font=("Segoe UI", 8, "bold"),
                           fg="#38bdf8", bg="#171f2c")
        lbl = tk.Label(f, text=label_text, font=("Segoe UI", 8), fg="#f1f5f9", bg="#171f2c")
        lbl.pack(side=tk.LEFT)
        val_lbl.pack(side=tk.RIGHT)

        def on_change(val):
            v = float(val)
            val_lbl.config(text=f"{v:.3f}{unit}")
            self.update_simulation(recalc_iv=recalc)

        s = ttk.Scale(parent, from_=from_, to=to, variable=var, command=on_change)
        s.pack(fill=tk.X, pady=(0, 4))

    # ---------------------------------------------------------------------
    # EXACT TRANSFER MATRIX METHOD (TMM)
    # ---------------------------------------------------------------------
    def calculate_tmm(self, E_eV, Va_V, compute_psi=False):
        E_J = E_eV * E_CH
        V0_J = self.V0.get() * E_CH
        Va_J = Va_V * E_CH
        Lb_m = self.Lb.get() * 1e-9
        Lw_m = self.Lw.get() * 1e-9
        L_tot = 2 * Lb_m + Lw_m

        if E_J <= 0:
            return 0.0, None

        k_L = math.sqrt(2 * M_EFF * E_J) / HBAR
        k_R_arg = 2 * M_EFF * (E_J + Va_J)
        k_R = cmath.sqrt(k_R_arg) / HBAR

        alpha_L = 1j * k_L / M_EFF
        alpha_R = 1j * k_R / M_EFF

        n_slices = 40
        dx = L_tot / n_slices

        # Transfer matrix propagation
        M00, M01, M10, M11 = 1.0 + 0j, 0.0 + 0j, 0.0 + 0j, 1.0 + 0j
        slice_matrices = []

        for i in range(n_slices):
            x = (i + 0.5) * dx
            V_flat = V0_J if (x < Lb_m or x > Lb_m + Lw_m) else 0.0
            V_x = V_flat - Va_J * (x / L_tot)

            kj = cmath.sqrt(2 * M_EFF * (E_J - V_x)) / HBAR
            cos_kd = cmath.cos(kj * dx)
            sinc_kd = dx if abs(kj) < 1e-12 else cmath.sin(kj * dx) / kj

            A00, A01 = cos_kd, M_EFF * sinc_kd
            A10, A11 = -(kj**2 / M_EFF) * sinc_kd, cos_kd

            if compute_psi:
                slice_matrices.append((A00, A01, A10, A11, x * 1e9, V_x / E_CH))

            N00 = A00*M00 + A01*M10
            N01 = A00*M01 + A01*M11
            N10 = A10*M00 + A11*M10
            N11 = A10*M01 + A11*M11
            M00, M01, M10, M11 = N00, N01, N10, N11

        detM = M00*M11 - M01*M10
        inv00, inv01 = M11/detM, -M01/detM
        inv10, inv11 = -M10/detM, M00/detM

        u1 = inv00 + inv01 * alpha_R
        u2 = inv10 + inv11 * alpha_R

        t_coeff = (2 * alpha_L) / (alpha_L * u1 + u2)
        r_coeff = t_coeff * u1 - 1.0

        T = (k_R.real / k_L) * (abs(t_coeff)**2)
        T = max(0.0, min(1.0, float(T)))

        if not compute_psi:
            return T, None

        # Reconstruct Wavefunction across contacts and active region
        x_nm_list = []
        V_eV_list = []
        psi_sq_list = []
        Lc_nm = 5.0
        n_c = 25

        # Emitter contact
        for i in range(n_c):
            x_nm = -Lc_nm + (Lc_nm * i) / (n_c - 1)
            x_m = x_nm * 1e-9
            psi = cmath.exp(1j * k_L * x_m) + r_coeff * cmath.exp(-1j * k_L * x_m)
            x_nm_list.append(x_nm)
            V_eV_list.append(0.0)
            psi_sq_list.append(abs(psi)**2)

        # Active region slices
        st = [1.0 + r_coeff, alpha_L * (1.0 - r_coeff)]
        for A00, A01, A10, A11, x_nm, V_eV in slice_matrices:
            st0 = A00 * st[0] + A01 * st[1]
            st1 = A10 * st[0] + A11 * st[1]
            st = [st0, st1]
            x_nm_list.append(x_nm)
            V_eV_list.append(V_eV)
            psi_sq_list.append(abs(st[0])**2)

        # Collector contact
        L_tot_nm = L_tot * 1e9
        for i in range(n_c):
            x_nm = L_tot_nm + (Lc_nm * i) / (n_c - 1)
            x_m = (x_nm - L_tot_nm) * 1e-9
            psi = t_coeff * cmath.exp(1j * k_R * x_m)
            x_nm_list.append(x_nm)
            V_eV_list.append(-Va_V)
            psi_sq_list.append(abs(psi)**2)

        sim_data = {
            "x": x_nm_list,
            "V": V_eV_list,
            "psi_sq": psi_sq_list,
            "T": T
        }
        return T, sim_data

    # ---------------------------------------------------------------------
    # TSU-ESAKI DIODE I-V CURVE
    # ---------------------------------------------------------------------
    def calculate_rtd_iv(self):
        EF_J = 0.04 * E_CH
        nV = 30
        nE = 35
        V_max = 0.35
        E_max_eV = max(self.V0.get() * 1.05, 0.25)
        dE_J = (E_max_eV / nE) * E_CH

        J0 = (E_CH * M_EFF * KBT) / (2 * math.pi**2 * HBAR**3)
        V_arr = []
        J_arr = []

        for iv in range(nV):
            Va = (V_max * iv) / (nV - 1)
            V_arr.append(Va)
            if Va == 0:
                J_arr.append(0.0)
                continue

            J_sum = 0.0
            for ie in range(1, nE + 1):
                E_eV = (E_max_eV * ie) / nE
                E_J = E_eV * E_CH
                T, _ = self.calculate_tmm(E_eV, Va, False)

                arg1 = (EF_J - E_J) / KBT
                arg2 = (EF_J - E_J - E_CH * Va) / KBT
                s1 = arg1 if arg1 > 35 else math.log(1.0 + math.exp(arg1))
                s2 = arg2 if arg2 > 35 else (0.0 if arg2 < -35 else math.log(1.0 + math.exp(arg2)))
                supply = max(0.0, s1 - s2)
                J_sum += T * supply * dE_J

            J_A_cm2 = (J0 * J_sum) * 1e-4
            J_arr.append(J_A_cm2)

        # Peak and Valley
        J_peak = max(J_arr)
        idx_p = J_arr.index(J_peak)
        V_peak = V_arr[idx_p]

        J_valley = min(J_arr[idx_p:]) if idx_p < len(J_arr) else J_peak
        idx_v = J_arr.index(J_valley, idx_p) if idx_p < len(J_arr) else idx_p
        V_valley = V_arr[idx_v]
        pvcr = (J_peak / J_valley) if J_valley > 0 else 1.0

        return {
            "V": V_arr, "J": J_arr,
            "V_peak": V_peak, "J_peak": J_peak,
            "V_valley": V_valley, "J_valley": J_valley,
            "pvcr": pvcr
        }

    # ---------------------------------------------------------------------
    # UPDATE SIMULATION & DRAW ALL 4 QUADRANTS
    # ---------------------------------------------------------------------
    def update_simulation(self, recalc_iv=True):
        E_cur = self.E.get()
        Va_cur = self.Va.get()
        V0_cur = self.V0.get()

        # 1. Compute Wavefunction
        _, self.last_sim = self.calculate_tmm(E_cur, Va_cur, compute_psi=True)

        # 2. Compute Transmission Spectrum
        n_pts = 90
        E_max = V0_cur * 1.25
        self.spec_E = []
        self.spec_T = []
        self.peaks = []

        for i in range(1, n_pts + 1):
            Ei = (E_max * i) / n_pts
            Ti, _ = self.calculate_tmm(Ei, Va_cur, False)
            self.spec_E.append(Ei)
            self.spec_T.append(Ti)

            if i >= 3:
                y1, y2, y3 = self.spec_T[i-3], self.spec_T[i-2], self.spec_T[i-1]
                if y2 > y1 and y2 >= y3 and y2 > 0.05:
                    self.peaks.append((self.spec_E[i-2], y2))

        # 3. Compute I-V curve
        if recalc_iv or self.iv_cache is None:
            self.iv_cache = self.calculate_rtd_iv()
        iv = self.iv_cache

        # 4. Render All Canvases
        self.draw_band_profile()
        self.draw_transmission()
        self.draw_iv()
        self.draw_3d_cavity()

        # 5. Update Metrics Readout
        if self.peaks:
            pk1_E = self.peaks[0][0]
            self.lbl_E1.config(text=f"Resonance E₁: {pk1_E:.3f} eV")
            gamma = 0.003 * (3.0 / self.Lb.get())
            tau_fs = (HBAR / (gamma * E_CH)) * 1e15
            self.lbl_tau.config(text=f"Lifetime τ: {tau_fs:.0f} fs")
        else:
            self.lbl_E1.config(text="Resonance E₁: None")
            self.lbl_tau.config(text="Lifetime τ: N/A")

        self.lbl_pvcr.config(text=f"PVCR Ratio: {iv['pvcr']:.1f}")
        self.lbl_peak.config(text=f"Peak Voltage: {iv['V_peak']:.3f} V")

        if Va_cur < 0.01:
            self.lbl_status.config(text="Thermal Equilibrium (Zero Bias)", fg="#38bdf8")
        elif abs(Va_cur - iv['V_peak']) < 0.02:
            self.lbl_status.config(text="🔥 RESONANT PEAK: Well Level Aligns with Emitter!", fg="#4ade80")
        elif iv['V_peak'] < Va_cur < iv['V_valley']:
            self.lbl_status.config(text="⚡ NEGATIVE DIFFERENTIAL RESISTANCE (NDR Active!)", fg="#f87171")
        elif Va_cur >= iv['V_valley']:
            self.lbl_status.config(text="Valley Region: Level Dropped Below Emitter", fg="#c084fc")
        else:
            self.lbl_status.config(text="Pre-Resonant Tunneling", fg="#94a3b8")

    # ---------------------------------------------------------------------
    # 2D CANVAS DRAWING ROUTINES
    # ---------------------------------------------------------------------
    def draw_band_profile(self):
        c = self.c_band
        c.delete("all")
        w = c.winfo_width() or 400
        h = c.winfo_height() or 220
        sim = self.last_sim
        if not sim: return

        pad_l, pad_r, pad_t, pad_b = 40, 20, 20, 25
        pw = w - pad_l - pad_r
        ph = h - pad_t - pad_b

        x_min, x_max = sim['x'][0], sim['x'][-1]
        y_min, y_max = -self.Va.get() - 0.05, self.V0.get() * 1.35

        map_x = lambda x: pad_l + ((x - x_min) / (x_max - x_min)) * pw
        map_y = lambda y: pad_t + ph - ((y - y_min) / (y_max - y_min)) * ph

        # Barrier shading
        Lb = self.Lb.get()
        Lw = self.Lw.get()
        V0 = self.V0.get()
        c.create_rectangle(map_x(0), map_y(V0), map_x(Lb), map_y(0), fill="#2e1a20", outline="")
        c.create_rectangle(map_x(Lb + Lw), map_y(V0), map_x(Lb + Lw + Lb), map_y(0), fill="#2e1a20", outline="")

        # Axis line at y=0
        c.create_line(pad_l, map_y(0), pad_l + pw, map_y(0), fill="#334155")

        # Potential Profile Line
        pts_v = []
        for x, v in zip(sim['x'], sim['V']):
            pts_v.extend([map_x(x), map_y(v)])
        c.create_line(pts_v, fill="#f8fafc", width=2)

        # Incident Energy Line
        E_cur = self.E.get()
        c.create_line(pad_l, map_y(E_cur), pad_l + pw, map_y(E_cur), fill="#38bdf8", dash=(4, 4))

        # Probability Density |psi(x)|^2
        max_psi = max(sim['psi_sq']) if max(sim['psi_sq']) > 1e-4 else 1.0
        scale = 0.09 / max_psi
        pts_psi = []
        for x, p in zip(sim['x'], sim['psi_sq']):
            pts_psi.extend([map_x(x), map_y(E_cur + p * scale)])
        c.create_line(pts_psi, fill="#38bdf8", width=2)

        # Labels
        c.create_text(pad_l + 5, map_y(V0) - 8, text=f"V₀={V0:.2f}eV", fill="#94a3b8", font=("Segoe UI", 8), anchor="w")
        c.create_text(pad_l + 5, map_y(E_cur) - 8, text=f"E={E_cur:.3f}eV", fill="#38bdf8", font=("Segoe UI", 8), anchor="w")

    def draw_transmission(self):
        c = self.c_trans
        c.delete("all")
        w = c.winfo_width() or 400
        h = c.winfo_height() or 220
        if not hasattr(self, 'spec_E'): return

        pad_l, pad_r, pad_t, pad_b = 40, 20, 20, 25
        pw = w - pad_l - pad_r
        ph = h - pad_t - pad_b

        E_max = self.V0.get() * 1.25
        map_x = lambda e: pad_l + (e / E_max) * pw
        map_y = lambda t: pad_t + ph - min(1.0, t) * ph

        c.create_line(pad_l, pad_t, pad_l, pad_t + ph, fill="#334155")
        c.create_line(pad_l, pad_t + ph, pad_l + pw, pad_t + ph, fill="#334155")

        # Spectrum Curve
        pts = []
        for e, t in zip(self.spec_E, self.spec_T):
            pts.extend([map_x(e), map_y(t)])
        c.create_line(pts, fill="#4ade80", width=2)

        # Peaks
        for pk_E, pk_T in self.peaks:
            px, py = map_x(pk_E), map_y(pk_T)
            c.create_oval(px - 3, py - 3, px + 3, py + 3, fill="#fbbf24", outline="")
            c.create_text(px, py - 10, text=f"{pk_E:.3f}eV", fill="#fbbf24", font=("Segoe UI", 8))

        # Operating E
        E_cur = self.E.get()
        c.create_line(map_x(E_cur), pad_t, map_x(E_cur), pad_t + ph, fill="#38bdf8", dash=(3, 3))

    def draw_iv(self):
        c = self.c_iv
        c.delete("all")
        w = c.winfo_width() or 400
        h = c.winfo_height() or 220
        iv = self.iv_cache
        if not iv: return

        pad_l, pad_r, pad_t, pad_b = 45, 20, 20, 25
        pw = w - pad_l - pad_r
        ph = h - pad_t - pad_b

        V_max = iv['V'][-1]
        J_max = max(iv['J']) * 1.15 if max(iv['J']) > 0 else 1.0

        map_x = lambda v: pad_l + (v / V_max) * pw
        map_y = lambda j: pad_t + ph - (j / J_max) * ph

        # Highlight NDR Region
        if iv['V_valley'] > iv['V_peak']:
            x1 = map_x(iv['V_peak'])
            x2 = map_x(iv['V_valley'])
            c.create_rectangle(x1, pad_t, x2, pad_t + ph, fill="#2e1a20", outline="")
            c.create_text((x1 + x2)/2, pad_t + 12, text="NDR (dI/dV < 0)", fill="#f87171", font=("Segoe UI", 8, "bold"))

        # Axes
        c.create_line(pad_l, pad_t, pad_l, pad_t + ph, fill="#334155")
        c.create_line(pad_l, pad_t + ph, pad_l + pw, pad_t + ph, fill="#334155")

        # Curve
        pts = []
        for v, j in zip(iv['V'], iv['J']):
            pts.extend([map_x(v), map_y(j)])
        c.create_line(pts, fill="#4ade80", width=2)

        # Mark Peak & Valley
        px, py = map_x(iv['V_peak']), map_y(iv['J_peak'])
        c.create_oval(px - 4, py - 4, px + 4, py + 4, fill="#fbbf24", outline="")
        c.create_text(px, py - 10, text="Peak", fill="#fbbf24", font=("Segoe UI", 8))

        vx, vy = map_x(iv['V_valley']), map_y(iv['J_valley'])
        c.create_oval(vx - 4, vy - 4, vx + 4, vy + 4, fill="#c084fc", outline="")
        c.create_text(vx, vy + 12, text="Valley", fill="#c084fc", font=("Segoe UI", 8))

        # Current Bias Marker
        Va_cur = self.Va.get()
        # Interpolate J
        cur_J = 0
        for i in range(len(iv['V']) - 1):
            if iv['V'][i] <= Va_cur <= iv['V'][i+1]:
                frac = (Va_cur - iv['V'][i]) / (iv['V'][i+1] - iv['V'][i])
                cur_J = iv['J'][i] + frac * (iv['J'][i+1] - iv['J'][i])
                break
        c.create_oval(map_x(Va_cur) - 5, map_y(cur_J) - 5, map_x(Va_cur) + 5, map_y(cur_J) + 5, fill="#38bdf8", outline="white")

    # ---------------------------------------------------------------------
    # 3D QUANTUM CAVITY WIREFRAME / SURFACE
    # ---------------------------------------------------------------------
    def project_3d(self, x, y, z, cx, cy, scale):
        # Rotate around Y
        x1 = x * math.cos(self.rot_y) + z * math.sin(self.rot_y)
        z1 = -x * math.sin(self.rot_y) + z * math.cos(self.rot_y)
        # Rotate around X
        y2 = y * math.cos(self.rot_x) - z1 * math.sin(self.rot_x)
        z2 = y * math.sin(self.rot_x) + z1 * math.cos(self.rot_x)
        dist = 30.0
        factor = (dist / (dist + z2)) * scale * self.zoom
        return cx + x1 * factor, cy - y2 * factor

    def draw_3d_cavity(self):
        c = self.c_3d
        c.delete("all")
        w = c.winfo_width() or 400
        h = c.winfo_height() or 220
        sim = self.last_sim
        if not sim: return

        cx = w / 2
        cy = h / 2 + 25
        scale = 16

        # Draw 3D Ground Grid
        for g in range(-8, 9, 2):
            p1 = self.project_3d(g, 0, -6, cx, cy, scale)
            p2 = self.project_3d(g, 0, 6, cx, cy, scale)
            c.create_line(p1[0], p1[1], p2[0], p2[1], fill="#1e293b")

            p3 = self.project_3d(-8, 0, g, cx, cy, scale)
            p4 = self.project_3d(8, 0, g, cx, cy, scale)
            c.create_line(p3[0], p3[1], p4[0], p4[1], fill="#1e293b")

        # Draw 3D Barriers (Prisms)
        Lb = self.Lb.get()
        Lw = self.Lw.get()
        V0 = self.V0.get() * 3.5
        center_x = (2 * Lb + Lw) / 2

        self.draw_3d_box(c, (Lb/2) - center_x, V0/2, 0, Lb, V0, 5, cx, cy, scale)
        self.draw_3d_box(c, (Lb + Lw + Lb/2) - center_x, V0/2, 0, Lb, V0, 5, cx, cy, scale)

        # Draw 3D Wavefunction Surface Ribs
        nx = 35
        ny = 9
        max_p = max(sim['psi_sq']) if max(sim['psi_sq']) > 1e-4 else 1.0

        for iy in range(ny):
            y_norm = (iy / (ny - 1)) * 2 - 1
            env = math.exp(-y_norm * y_norm * 3)
            y_3d = y_norm * 2.5

            pts = []
            for ix in range(nx):
                x_norm = ix / (nx - 1)
                idx = int(x_norm * (len(sim['psi_sq']) - 1))
                x_3d = (x_norm * 16) - 8

                if self.animating:
                    phase = self.wave_t * 6
                    h_val = max(0.0, math.sin(phase) * (sim['psi_sq'][idx] / max_p)) * 3.5 * env
                else:
                    h_val = (sim['psi_sq'][idx] / max_p) * 3.0 * env

                pt = self.project_3d(x_3d, h_val, y_3d, cx, cy, scale)
                pts.extend([pt[0], pt[1]])

            col = "#38bdf8" if iy == ny//2 else "#0284c7"
            c.create_line(pts, fill=col, width=1.5 if iy == ny//2 else 1)

    def draw_3d_box(self, c, x, y, z, w, h, d, cx, cy, scale):
        hw, hh, hd = w/2, h/2, d/2
        corners = [
            self.project_3d(x - hw, y - hh, z - hd, cx, cy, scale),
            self.project_3d(x + hw, y - hh, z - hd, cx, cy, scale),
            self.project_3d(x + hw, y + hh, z - hd, cx, cy, scale),
            self.project_3d(x - hw, y + hh, z - hd, cx, cy, scale),
            self.project_3d(x - hw, y - hh, z + hd, cx, cy, scale),
            self.project_3d(x + hw, y - hh, z + hd, cx, cy, scale),
            self.project_3d(x + hw, y + hh, z + hd, cx, cy, scale),
            self.project_3d(x - hw, y + hh, z + hd, cx, cy, scale)
        ]
        # Top Face
        c.create_polygon([corners[3][0], corners[3][1], corners[2][0], corners[2][1],
                          corners[6][0], corners[6][1], corners[7][0], corners[7][1]],
                         fill="#3d1b22", outline="#ef4444")
        # Front Face
        c.create_polygon([corners[4][0], corners[4][1], corners[5][0], corners[5][1],
                          corners[6][0], corners[6][1], corners[7][0], corners[7][1]],
                         fill="#2e141a", outline="#ef4444")

    # 3D Mouse Event Handlers
    def on_3d_press(self, event):
        self.drag_start = (event.x, event.y)

    def on_3d_drag(self, event):
        if self.drag_start:
            dx = event.x - self.drag_start[0]
            dy = event.y - self.drag_start[1]
            self.rot_y += dx * 0.01
            self.rot_x = max(0.1, min(1.5, self.rot_x + dy * 0.01))
            self.drag_start = (event.x, event.y)
            self.draw_3d_cavity()

    def on_3d_zoom(self, event):
        factor = 1.1 if event.delta > 0 else 0.9
        self.zoom = max(0.5, min(2.5, self.zoom * factor))
        self.draw_3d_cavity()

    def snap_to_resonance(self):
        if self.peaks:
            self.E.set(round(self.peaks[0][0], 3))
            self.update_simulation(recalc_iv=False)

    def toggle_animation(self):
        self.animating = not self.animating
        self.btn_anim.config(text="⏸ Pause 3D Wavepacket" if self.animating else "▶ Animate 3D Wavepacket")
        if self.animating:
            self.animate_loop()

    def animate_loop(self):
        if self.animating:
            self.wave_t += 0.04
            self.draw_3d_cavity()
            self.root.after(30, self.animate_loop)

    def toggle_3d(self):
        self.view_3d.set(not self.view_3d.get())
        self.draw_3d_cavity()


if __name__ == "__main__":
    root = tk.Tk()
    app = RTDSimulationApp(root)
    root.mainloop()
