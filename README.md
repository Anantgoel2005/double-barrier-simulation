# Resonant Tunnelling & RTD Diode Simulator

[![Live Demo](https://img.shields.io/badge/Live%20Demo-GitHub%20Pages-brightgreen.svg?style=for-the-badge&logo=github)](https://anantgoel2005.github.io/double-barrier-simulation/)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![WebGL 3D](https://img.shields.io/badge/3D%20Graphics-Three.js%20%7C%20WebGL-blue.svg)](https://threejs.org/)
[![Python](https://img.shields.io/badge/Python-3.x%20(Pure%20Stdlib)-3776AB.svg?logo=python&logoColor=white)](https://www.python.org/)
[![MATLAB](https://img.shields.io/badge/MATLAB-R2018b%2B-red.svg)](https://www.mathworks.com/products/matlab.html)

A multi-platform quantum simulation laboratory for **Resonant Tunnelling** in double-barrier semiconductor heterostructures (e.g., $\text{Al}_x\text{Ga}_{1-x}\text{As} / \text{GaAs} / \text{Al}_x\text{Ga}_{1-x}\text{As}$) and its electronic application in the **Resonant Tunnelling Diode (RTD)**.

🔗 **Try the live simulation instantly in your browser:**  
👉 **[https://anantgoel2005.github.io/double-barrier-simulation/](https://anantgoel2005.github.io/double-barrier-simulation/)**

---

## ⚡ Quick Start: 3 Ways to Run

### Option 1: Interactive 3D Web App (Zero Setup)
Open the simulation directly in any modern browser (Chrome, Edge, Firefox, Safari):

* **Live on GitHub Pages (Instant)**: Open **[https://anantgoel2005.github.io/double-barrier-simulation/](https://anantgoel2005.github.io/double-barrier-simulation/)**
* **Local Offline**: Double-click `Launch_Web_Simulation.bat` (or open `index.html` in your browser).

#### Features:
* **Sliders**: Real-time adjustment of Barrier Height ($V_0$), Barrier Thickness ($L_b$), Quantum Well Width ($L_w$), Diode Bias ($V_a$), and Incident Energy ($E$).
* **3D Quantum Cavity View**: Interactive WebGL 3D perspective of the double-barrier heterostructure. Click and drag to orbit, scroll to zoom, and toggle dynamic wavepacket animation.
* **Auto-Snap to Peak**: Instantly snaps electron energy to the nearest bound state eigen-energy.
* **4 Real-Time Dashboards**:
  1. Conduction band diagram $V(x)$ + Wavefunction probability density $|\psi(x)|^2$.
  2. Transmission spectrum $T(E)$ with resonance peaks marked.
  3. Resonant Tunnelling Diode $I-V$ curve with **Negative Differential Resistance (NDR)** shaded.
  4. Real-time metrics: fundamental resonance ($E_1$), linewidth ($\Gamma$), lifetime ($\tau$), Peak Voltage ($V_p$), Peak Current ($J_p$), and Peak-to-Valley Current Ratio (PVCR).

---

### Option 2: Python Desktop Application
Built entirely using Python's standard library (`tkinter`, `math`, `cmath`). **No external packages required** (no NumPy, SciPy, or Matplotlib needed).

```bash
# Run directly with Python:
python rtd_gui_python.py

# Or on Windows, double-click:
Launch_Python_GUI.bat
```

---

### Option 3: MATLAB Simulation Suite
If you have MATLAB installed:

```matlab
% 1. Launch the interactive GUI dashboard:
rtd_interactive_app

% 2. Run the dynamic 3D time-dependent wavepacket simulation:
rtd_3d_wavepacket('resonant')

% 3. Generate 3D energy landscapes:
rtd_3d_landscape

% 4. Run the comprehensive 4-figure demo:
main_rtd_demo
```

---

## 🔬 Physics & Theoretical Background

### 1. The Fabry-Pérot Quantum Resonator
A double-barrier structure acts as the quantum mechanical analog of an optical **Fabry-Pérot interferometer**:

```
      Emitter Lead             Barrier 1           Quantum Well           Barrier 2            Collector Lead
  --------------------|-----------------------|-------------------|-----------------------|--------------------
    V(x) = 0          |        V(x) = V₀      |     V(x) = 0      |        V(x) = V₀      |    V(x) = -q·V_a
                      |<--------- L_b ------->|<------ L_w ------>|<--------- L_b ------->|
```

* The two thin potential barriers function as semi-transparent quantum mirrors.
* The central quantum well forms a resonant optical-like cavity.
* When electron waves undergo constructive interference inside the well:
  $$2 k_w L_w + \phi_1 + \phi_2 = 2 \pi n, \quad n = 1, 2, 3, \dots$$
* At these exact resonance energies $E = E_n$, the transmission probability reaches a sharp peak ($T \to 1$), and the probability density $|\psi(x)|^2$ inside the well is amplified by orders of magnitude compared to the incident wave.

---

### 2. How Parameter Changes Affect Resonant Tunnelling

| Parameter | Physical Role | Effect on Transmission $T(E)$ |
| :--- | :--- | :--- |
| **Barrier Height ($V_0$)** | Confinement depth | Higher $V_0$ increases barrier reflection, deepens bound states, and exponentially suppresses non-resonant leakage current. |
| **Barrier Thickness ($L_b$)** | Transparency & Cavity $Q$-factor | Thicker $L_b$ dramatically narrows the transmission linewidth ($\Gamma = \text{FWHM}$) and exponentially extends state lifetime ($\tau = \hbar / \Gamma$). |
| **Quantum Well Width ($L_w$)** | Cavity length & Eigen-energies | Controls resonance positions ($E_n \approx \frac{n^2 \pi^2 \hbar^2}{2 m^* L_w^2}$). Widening $L_w$ lowers existing peaks and introduces higher-order states ($E_1, E_2, E_3$). |

---

### 3. Application in a Diode: Negative Differential Resistance (NDR)

In a **Resonant Tunnelling Diode (RTD)**, an external voltage $V_a$ is applied across the active region:

```
Energy
  ^
  |        Emitter          Well          Collector
  |       ---------
  |      | Fermi   |      --- Er
  |      | Sea (EF)|     |   |
  |  ----+---------+-----+---+--------------------- (Zero Bias: J ~ 0)
  |
  |       ---------
  |      | Fermi   |===> --- Er (Aligned!)
  |  ----+---------+-----+---+--------------------- (Resonant Bias V_p: J = J_peak)
  |
  |       ---------
  |      | Fermi   |
  |  ----+---------+-----+---
  |                      |   |--- Er (Below E_c)    (Valley Bias V_v: NDR Region, dI/dV < 0)
  +--------------------------------------------------> Position x
```

1. **Zero Bias ($V_a = 0$)**: The quasi-bound level $E_r$ sits above the emitter Fermi level $E_F$. Electrons lack sufficient energy to tunnel; current $J \approx 0$.
2. **Resonant Bias ($V_a = V_{peak} \approx 2 E_r / q$)**: Conduction band tilts, lowering $E_r$ into alignment with occupied emitter states ($0 < E_r < E_F$). Resonant tunneling causes a current surge to a peak $J_{peak}$.
3. **Negative Differential Resistance ($V_{peak} < V_a < V_{valley}$)**: Further bias pushes $E_r$ below the emitter conduction band edge ($E_c$). Electrons cannot tunnel into forbidden states while conserving transverse momentum and energy. Resonant tunneling abruptly quenches, producing:
   $$\frac{dI}{dV} < 0 \quad \text{(Negative Differential Resistance)}$$
4. **Valley & Thermionic Emission ($V_a > V_{valley}$)**: Current drops to a minimum $J_{valley}$. At higher bias, classical thermionic and Fowler-Nordheim field emission take over.

The current density $J(V_a)$ is computed using the **Tsu-Esaki formula**:
$$J(V_a) = \frac{e m^* k_B T}{2 \pi^2 \hbar^3} \int_0^\infty T(E, V_a) \ln\left( \frac{1 + \exp\left(\frac{E_F - E}{k_B T}\right)}{1 + \exp\left(\frac{E_F - E - e V_a}{k_B T}\right)} \right) dE$$

---

## 📂 Repository Structure

```
double-barrier-simulation/
├── index.html                 # Main interactive 3D Web Application (GitHub Pages entry)
├── rtd_simulation.html        # Standalone copy of Web Application
├── rtd_gui_python.py          # Native Python Desktop GUI (Zero external dependencies)
├── Launch_Web_Simulation.bat  # 1-click launcher for the Web simulation
├── Launch_Python_GUI.bat      # 1-click launcher for the Python Desktop GUI
├── calculate_tmm.m            # MATLAB: Transfer Matrix Method physics engine
├── calculate_rtd_iv.m         # MATLAB: Tsu-Esaki RTD current density solver
├── find_resonance_peaks.m     # MATLAB: Peak & FWHM detector (Toolbox-independent)
├── rtd_interactive_app.m      # MATLAB: Interactive GUI application with sliders
├── rtd_3d_wavepacket.m        # MATLAB: 3D Time-Dependent Schrödinger Equation simulation
├── rtd_3d_landscape.m         # MATLAB: 3D Transmission & Stark shift surfaces
├── main_rtd_demo.m            # MATLAB: Automated 4-figure demonstration script
├── README.md                  # Comprehensive documentation and physics guide
├── LICENSE                    # MIT License
└── .gitignore                 # Standard git ignore file
```

---

## 🌐 Repository & Live Web Demo

* **GitHub Repository:** [https://github.com/Anantgoel2005/double-barrier-simulation](https://github.com/Anantgoel2005/double-barrier-simulation)
* **Live Interactive 3D Simulation:** [https://anantgoel2005.github.io/double-barrier-simulation/](https://anantgoel2005.github.io/double-barrier-simulation/)

### Cloning & Running Locally
```bash
git clone https://github.com/Anantgoel2005/double-barrier-simulation.git
cd double-barrier-simulation

# 1. Open Interactive Web App:
# Double-click index.html or Launch_Web_Simulation.bat

# 2. Run Python Desktop App:
python rtd_gui_python.py
```

---

## 📄 License

This project is licensed under the [MIT License](LICENSE).
Feel free to use, modify, and distribute for academic, educational, or commercial purposes.
