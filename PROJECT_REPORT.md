# Numerical Modeling and 3D Simulation of Quantum Resonant Tunnelling in Double-Barrier Heterostructures and Resonant Tunnelling Diodes (RTDs)

**Author:** Anant Goel  
**Date:** November 2026  
**Repository:** [github.com/Anantgoel2005/double-barrier-simulation](https://github.com/Anantgoel2005/double-barrier-simulation)  
**Live Simulation:** [anantgoel2005.github.io/double-barrier-simulation/](https://anantgoel2005.github.io/double-barrier-simulation/)  

---

## Executive Summary

This report presents a comprehensive theoretical, numerical, and computational study of quantum **resonant tunnelling** in double-barrier semiconductor heterostructures ($\text{Al}_x\text{Ga}_{1-x}\text{As} / \text{GaAs} / \text{Al}_x\text{Ga}_{1-x}\text{As}$) and its application in **Resonant Tunnelling Diodes (RTDs)**. By coupling the 1D stationary **Transfer Matrix Method (TMM)** under BenDaniel-Duke boundary conditions with the **Tsu-Esaki formulation**, the device physics governing transmission spectra $T(E)$, quasi-bound state lifetimes $\tau$, and the characteristic N-shaped **Negative Differential Resistance (NDR)** $I-V$ response are fully resolved. Furthermore, a 2D/3D dynamic solver based on the **Split-Step Fourier Method (SSFM)** for the Time-Dependent Schrödinger Equation (TDSE) is developed to visualize quantum cavity buildup and wavepacket dynamics in real time. The resulting computational laboratory has been deployed across three interoperable environments: an interactive WebGL/Three.js web application (hosted globally on GitHub Pages), a zero-dependency native Python desktop GUI, and an automated MATLAB simulation suite.

```
       Emitter (Lead)            Barrier 1            Quantum Well            Barrier 2            Collector (Lead)
  -----------------------|-----------------------|--------------------|-----------------------|------------------------
    V(x) = 0             |        V(x) = V₀      |     V(x) = 0       |        V(x) = V₀      |    V(x) = -q·V_a
    m* = m*_well         |        m* = m*_barr   |     m* = m*_well   |        m* = m*_barr   |    m* = m*_well
                         |<--------- L_b ------->|<------- L_w ------>|<--------- L_b ------->|
```

---

## 1. Motivation

As conventional silicon complementary metal-oxide-semiconductor (CMOS) field-effect transistors approach fundamental quantum-mechanical limits (gate oxide breakdown, subthreshold leakage, and short-channel effects), the microelectronics industry has intensified research into quantum-effect devices that exploit wave mechanics rather than suppressing them.

### 1.1 The Ultra-High Frequency Frontier
Standard drift-diffusion transport in conventional PN and Schottky diodes is fundamentally constrained by carrier transit times across depletion regions and parasitic $RC$ delays, limiting cut-off frequencies to several hundred gigahertz. Resonant Tunnelling Diodes (RTDs) represent the fastest known purely solid-state electronic switching devices. Because carrier transport across nanoscale heterostructure barriers is governed by coherent quantum tunneling rather than thermionic transit or diffusion, RTDs operate on femtosecond-to-picosecond transit timescales ($\tau \sim 50\text{--}200\text{ fs}$), enabling fundamental oscillation frequencies well into the **terahertz (THz) spectrum** ($f_{max} > 2.0\text{ THz}$).

### 1.2 Negative Differential Resistance (NDR) in Circuit Design
The primary operational hallmark of the RTD is its N-shaped current-voltage ($I-V$) characteristic, which exhibits a prominent region of **Negative Differential Resistance (NDR)** where:
$$\frac{dI}{dV} < 0$$
This non-monotonic behavior allows a single two-terminal RTD to perform functions that typically require multiple transistors:
- Ultra-high-speed oscillators and local oscillators for THz imaging, radar, and spectroscopic sensing.
- Picosecond pulse generators and multi-valued logic (MVL) gates (ternary, quaternary logic).
- Monolithic microwave integrated circuits (MMICs) and ultra-low-power latching comparators.

### 1.3 Pedagogical & Computational Challenge
Despite the foundational importance of resonant tunneling, visualizing the interplay between wavevector interference, complex eigen-energies, and voltage-dependent band bending is notoriously challenging using static 1D textbook diagrams. Developing an interactive, numerically exact, 3D dynamic platform bridges the conceptual divide between abstract wavepacket mechanics and experimental electronic device characterization.

---

## 2. Literature Survey

The development of quantum tunneling in engineered semiconductor heterostructures spans over five decades of breakthroughs in condensed matter physics and epitaxial crystal growth:

### 2.1 Foundational Discoveries
- **Esaki & Tsu (1970)** proposed artificial semiconductor superlattices, predicting that periodic nanoscale quantum wells would introduce mini-bands and quantum interference effects unreachable in bulk crystals.
- **Tsu & Esaki (1973)** published the seminal analytical formulation for the tunneling current density through single and multiple barriers, establishing the mathematical foundation relating transmission probability $T(E)$ to the Fermi-Dirac electron supply functions.
- **Chang, Esaki, and Tsu (1974)** experimentally demonstrated resonant tunneling in a molecular beam epitaxy (MBE)-grown $\text{GaAs} / \text{Al}_x\text{Ga}_{1-x}\text{As}$ double-barrier heterostructure, observing negative differential conductance at cryogenic and room temperatures.

### 2.2 Quantum Interference & The Fabry-Pérot Analogy
- Bohm (1951) and Merzbacher (1970) formalized the direct mathematical analogy between de Broglie matter waves propagating through double potential barriers and electromagnetic waves traversing an optical **Fabry-Pérot etalon**.
- The two potential barriers act as partially reflecting mirrors with reflection amplitudes $r_1, r_2$, while the intervening quantum well serves as a resonant cavity of optical thickness $k_w L_w$. Constructive interference produces resonant transmission ($T \to 1$) when the round-trip phase accumulation satisfies:
  $$2 k_w L_w + \phi_1 + \phi_2 = 2 \pi n, \quad n \in \mathbb{N}$$

### 2.3 Boundary Conditions in Heterostructures
- **BenDaniel & Duke (1966)** derived the matching conditions for the wave function across an abrupt heterointerface where the electron effective mass $m^*(x)$ is discontinuous. To guarantee probability current conservation:
  $$\psi(x^-) = \psi(x^+), \quad \left.\frac{1}{m^*(x^-)} \frac{d\psi}{dx}\right|_{x^-} = \left.\frac{1}{m^*(x^+)} \frac{d\psi}{dx}\right|_{x^+}$$
- Jonsson and Eng (1990) systematized the piecewise **Transfer Matrix Method (TMM)**, demonstrating that linear electrostatic potential slanting under an applied bias can be solved with high accuracy by discretizing the tilted band profile into thin planar slices.

### 2.4 Modern Terahertz Applications
- Suzuki, Asada, and colleagues at the Tokyo Institute of Technology (2010–2022) achieved continuous-wave sub-terahertz and terahertz radiation from GaInAs/AlAs RTDs integrated with patch antennas, reaching fundamental oscillation frequencies exceeding $1.98\text{ THz}$ at room temperature with output powers on the order of tens of microwatts.

---

## 3. Project Objectives

The primary engineering and scientific objectives of this research project are:

1. **Exact Quantum Transport Solver:** Formulate and implement the Transfer Matrix Method (TMM) with BenDaniel-Duke boundary conditions to calculate the energy-dependent transmission coefficient $T(E)$ and reflection coefficient $R(E)$ for arbitrary double-barrier profiles.
2. **Parametric Sensitivity Investigation:** Systematically evaluate how the three physical degrees of freedom—**Barrier Height ($V_0$)**, **Barrier Thickness ($L_b$)**, and **Quantum Well Width ($L_w$)**—alter the quasi-bound eigen-energies $E_n$, resonance linewidths ($\Gamma = \text{FWHM}$), and quasi-bound state lifetimes ($\tau = \hbar/\Gamma$).
3. **Diode $I-V$ Characteristic & NDR Modeling:** Implement the Tsu-Esaki current density integral to simulate the room-temperature ($300\text{ K}$) $I-V$ curve of a Resonant Tunnelling Diode, accurately identifying Peak Voltage ($V_p$), Peak Current ($J_p$), Valley Voltage ($V_v$), Valley Current ($J_v$), and the Peak-to-Valley Current Ratio (PVCR).
4. **Time-Dependent 3D Dynamic Wavepacket Simulation:** Solve the 2D Time-Dependent Schrödinger Equation (TDSE) via the Split-Step Fourier Method (SSFM) to render real-time 3D wavepacket animations contrasting resonant cavity buildup against off-resonant quantum reflection.
5. **Cross-Platform Implementation & Open-Source Dissemination:** Build a fully documented, tri-platform software suite (WebGL Web App, Pure Python GUI, and MATLAB) and publish the code with interactive 1-click cloud access via GitHub Pages.

---

## 4. Theoretical Methodology & Numerical Formulations

### 4.1 Stationary 1D Schrödinger Equation
Carrier motion along the epitaxial growth direction $x$ is described by the 1D effective-mass Schrödinger equation:
$$-\frac{\hbar^2}{2} \frac{d}{dx}\left( \frac{1}{m^*(x)} \frac{d\psi(x)}{dx} \right) + V(x) \psi(x) = E \psi(x)$$
where $\hbar = 1.05457 \times 10^{-34}\text{ J}\cdot\text{s}$, $E$ is the longitudinal electron energy, $V(x)$ is the electrostatic potential energy profile, and $m^*(x)$ is the position-dependent conduction band effective mass ($0.067 m_0$ in GaAs well and contacts, $0.092 m_0$ in $\text{Al}_{0.3}\text{Ga}_{0.7}\text{As}$ barriers).

### 4.2 Transfer Matrix Method (TMM)
The active double-barrier region $x \in [0, L_{tot}]$ ($L_{tot} = 2 L_b + L_w$) is subdivided into $N$ planar slices of width $\Delta x = L_{tot}/N$. In slice $j$, the potential is approximated as constant:
$$V_j = V(x_j) - e V_a \left(\frac{x_j}{L_{tot}}\right)$$
The local wavevector is:
$$k_j = \frac{\sqrt{2 m_j^* (E - V_j)}}{\hbar}$$
If $E < V_j$, $k_j = i \kappa_j$ is purely imaginary, representing evanescent decay. The state vector at interface $x_j$ is defined as:
$$\mathbf{w}(x_j) = \begin{pmatrix} \psi(x_j) \\ \frac{1}{m_j^*} \frac{d\psi}{dx}(x_j) \end{pmatrix}$$
The state propagates across slice $j$ through the characteristic layer matrix $\mathbf{M}_j$:
$$\mathbf{w}(x_j) = \mathbf{M}_j \mathbf{w}(x_{j-1}), \quad \mathbf{M}_j = \begin{pmatrix} \cos(k_j \Delta x) & \frac{m_j^*}{k_j} \sin(k_j \Delta x) \\ -\frac{k_j}{m_j^*} \sin(k_j \Delta x) & \cos(k_j \Delta x) \end{pmatrix}$$

The global transfer matrix spanning the active region is:
$$\mathbf{M}_{tot} = \mathbf{M}_N \mathbf{M}_{N-1} \cdots \mathbf{M}_2 \mathbf{M}_1 = \begin{pmatrix} M_{11} & M_{12} \\ M_{21} & M_{22} \end{pmatrix}$$

### 4.3 Boundary Matching and Transmission Coefficient
In the left lead (emitter, $x \le 0$), the wave function consists of incident and reflected plane waves:
$$\psi_L(x) = e^{i k_L x} + r e^{-i k_L x}, \quad k_L = \frac{\sqrt{2 m_L^* E}}{\hbar}$$
In the right lead (collector, $x \ge L_{tot}$), only a transmitted outgoing wave exists:
$$\psi_R(x) = t e^{i k_R (x - L_{tot})}, \quad k_R = \frac{\sqrt{2 m_R^* (E + e V_a)}}{\hbar}$$
Defining $\alpha_L = \frac{i k_L}{m_L^*}$ and $\alpha_R = \frac{i k_R}{m_R^*}$, matching boundary conditions at $x = 0$ and $x = L_{tot}$ yields:
$$\begin{pmatrix} 1 + r \\ \alpha_L(1 - r) \end{pmatrix} = \mathbf{M}_{tot}^{-1} \begin{pmatrix} 1 \\ \alpha_R \end{pmatrix} t \equiv \begin{pmatrix} u_1 \\ u_2 \end{pmatrix} t$$
Solving this linear system gives the exact transmission and reflection amplitudes:
$$t = \frac{2 \alpha_L}{\alpha_L u_1 + u_2}, \quad r = t u_1 - 1$$
The transmission probability $T(E)$ is the ratio of transmitted to incident probability flux:
$$T(E) = \frac{\text{Re}(k_R) / m_R^*}{k_L / m_L^*} |t|^2, \quad R(E) = |r|^2$$
In the absence of inelastic scattering, flux conservation strictly enforces:
$$T(E) + R(E) = 1.0000000000$$

### 4.4 Tsu-Esaki Diode Current Density Formulation
To calculate macroscopic current through the RTD, the longitudinal transmission probability $T(E, V_a)$ is integrated against the Fermi-Dirac electron distributions of the emitter and collector reservoirs:
$$J(V_a) = \frac{e m^* k_B T_{temp}}{2 \pi^2 \hbar^3} \int_0^\infty T(E, V_a) \ln\left( \frac{1 + \exp\left(\frac{E_F - E}{k_B T_{temp}}\right)}{1 + \exp\left(\frac{E_F - E - e V_a}{k_B T_{temp}}\right)} \right) dE$$
where $E_F$ is the emitter Fermi energy ($40\text{ meV}$ above conduction band edge $E_c$ for $N_D \approx 10^{18}\text{ cm}^{-3}$ doping), $T_{temp} = 300\text{ K}$, and $k_B T_{temp} \approx 25.85\text{ meV}$.

### 4.5 Split-Step Fourier Method (SSFM) for Dynamic TDSE
To observe wavepacket dynamics, the 2D Time-Dependent Schrödinger Equation:
$$i \hbar \frac{\partial \Psi(x, y, t)}{\partial t} = \left[ -\frac{\hbar^2}{2 m^*} \nabla^2 + V(x, y) \right] \Psi(x, y, t)$$
is advanced over discrete time steps $\Delta t$ ($0.05\text{ fs}$) using the second-order symmetric Strang-splitting operator:
$$\Psi(t + \Delta t) = e^{-\frac{i V \Delta t}{2 \hbar}} \mathcal{F}^{-1}\left[ e^{-\frac{i \hbar (k_x^2 + k_y^2) \Delta t}{2 m^*}} \mathcal{F}\left[ e^{-\frac{i V \Delta t}{2 \hbar}} \Psi(t) \right] \right] + \mathcal{O}(\Delta t^3)$$
A Gaussian wave packet initialized at $x_0 = -13\text{ nm}$:
$$\Psi(x, y, 0) = \frac{1}{\sqrt{2\pi \sigma_x \sigma_y}} \exp\left( -\frac{(x - x_0)^2}{2\sigma_x^2} - \frac{y^2}{2\sigma_y^2} \right) \exp\left(i \frac{\sqrt{2 m^* E_0}}{\hbar} x\right)$$
is launched toward the double barrier to monitor real-time cavity filling and tunneling flux.

---

## 5. Results & Discussion

### 5.1 Baseline Resonant Cavity Performance
For a standard $\text{Al}_{0.3}\text{Ga}_{0.7}\text{As} / \text{GaAs}$ heterostructure with $V_0 = 0.30\text{ eV}$, $L_b = 3.0\text{ nm}$, and $L_w = 5.0\text{ nm}$ at zero bias:

| Parameter | Computed Value | Physical Significance |
| :--- | :--- | :--- |
| **Resonant Energy ($E_1$)** | $0.0880\text{ eV}$ ($88.0\text{ meV}$) | Fundamental quasi-bound state inside the well |
| **Peak Transmission ($T_{max}$)** | $0.9998 \approx 1.00$ | Near-unity transmission on resonance |
| **Linewidth ($\Gamma = \text{FWHM}$)** | $0.0040\text{ eV}$ ($4.0\text{ meV}$) | Energy broadening due to barrier coupling |
| **State Lifetime ($\tau = \hbar/\Gamma$)** | $164.7\text{ fs}$ | Dwell time of the electron inside the quantum well |
| **Cavity Quality Factor ($Q = E_1/\Gamma$)** | $22.0$ | Sharpness of the quantum resonance |
| **Peak Well Amplification** | $54.2 \times |\psi_{inc}|^2$ | Coherent standing wave buildup inside cavity |

```
Probability Density |ψ(x)|² across Heterostructure:
|ψ|² ^
 60  |                       *** Resonant Standing Wave ***
 50  |                      *   *
 40  |                     *     *  (|ψ|² ~ 54x)
 30  |                    *       *
 20  |                   *         *
 10  |                  *           *
  1  | =====\          /             \          /======== Transmitted wave (T ~ 1)
  0  +-------|--------|---------------|--------|-----------------> x
         Emitter   Barrier 1       Well    Barrier 2   Collector
```

### 5.2 Parametric Sensitivity Analysis

#### A. Influence of Barrier Height ($V_0$)
Varying $V_0$ from $0.20\text{ eV}$ to $0.60\text{ eV}$:
1. **Quasi-bound State Depressurization:** As $V_0$ increases, the wave function decays faster inside the barrier ($\kappa = \sqrt{2 m^* (V_0 - E)}/\hbar$ increases), reducing wave function penetration. This slightly shifts the ground state $E_1$ downward toward the textbook hard-wall limit.
2. **Leakage Suppression:** Non-resonant transmission at low energies ($E < 0.05\text{ eV}$) drops exponentially by over three orders of magnitude (from $10^{-3}$ down to $< 10^{-6}$), significantly reducing off-resonance valley current.

#### B. Influence of Barrier Thickness ($L_b$)
Varying $L_b$ from $2.0\text{ nm}$ to $5.0\text{ nm}$:
1. **Linewidth Narrowing:** The resonance width $\Gamma$ decreases exponentially with increasing barrier thickness:
   $$\Gamma(L_b) \propto \exp\left( -2 \kappa L_b \right)$$
   For $L_b = 2.0\text{ nm}$, $\Gamma \approx 18.5\text{ meV}$ ($\tau \approx 35\text{ fs}$); for $L_b = 4.0\text{ nm}$, $\Gamma$ narrows to $0.85\text{ meV}$ ($\tau \approx 775\text{ fs}$).
2. **Quality Factor Trade-off:** While thicker barriers yield ultra-sharp resonant states and higher peak-to-valley current ratios, they dramatically decrease the absolute tunneling current density ($J \propto \Gamma$), demanding careful device optimization between switching speed and signal amplitude.

#### C. Influence of Quantum Well Width ($L_w$)
Varying $L_w$ from $3.0\text{ nm}$ to $10.0\text{ nm}$:
1. **Eigen-Energy Shift:** Resonant energies scale inversely with the square of the well width:
   $$E_n \approx \frac{n^2 \pi^2 \hbar^2}{2 m^* L_w^2}$$
2. **Multi-Channel Emergence:** As $L_w$ widens beyond $6.5\text{ nm}$, the second quasi-bound state $E_2$ drops below the barrier crest ($E_2 < V_0$), creating a multi-peaked transmission spectrum. This multi-resonance behavior forms the physical basis for multi-valued logic devices.

### 5.3 Diode Transport & Negative Differential Resistance (NDR)

Applying the Tsu-Esaki equation over a voltage range $V_a \in [0, 0.35\text{ V}]$ reveals the four operational regimes of the RTD:

```
Current Density J [A/cm²]
  ^
12x10⁴ |                     Peak (V_p = 0.14 V, J_p = 1.18×10⁵ A/cm²)
10x10⁴ |                     *
 8x10⁴ |                   *   \
 6x10⁴ |                 *       \   NDR Region (dI/dV < 0)
 4x10⁴ |               *           \
 2x10⁴ |             *               \  Valley (V_v = 0.20 V, J_v = 1.74×10⁴ A/cm²)
       |            *                  *------------*  Thermionic Rise
  0    +-----------+--------------------+------------+-------------------> V_a [V]
                 Zero Bias            Peak         Valley
```

1. **Thermal Equilibrium ($V_a = 0\text{ V}$):** $J = 0$. The resonant level $E_1 = 88\text{ meV}$ sits well above the emitter Fermi sea ($E_F = 40\text{ meV}$).
2. **Resonant Current Surge ($0 < V_a \le 0.14\text{ V}$):** As bias increases, the potential across the well drops by $\approx e V_a / 2$, pulling the quasi-bound state downward relative to the emitter. When $V_a \approx 0.14\text{ V}$, the resonant level aligns with the occupied emitter electron distribution ($0 < E_1 < E_F$). Electrons tunnel resonantly, driving current density to a sharp peak:
   $$J_{peak} = 1.18 \times 10^5\text{ A/cm}^2 \quad \text{at } V_{peak} = 0.140\text{ V}$$
3. **Negative Differential Resistance ($0.14\text{ V} < V_a < 0.20\text{ V}$):** When $V_a > 0.14\text{ V}$, $E_1$ drops below the bottom of the emitter conduction band ($E_c$). Because emitter electrons cannot tunnel into energy states that violate conservation of energy and transverse momentum, resonant transmission is quenched. The current drops precipitously despite an increasing electric field ($dJ/dV < 0$).
4. **Valley & Thermionic Conduction ($V_a \ge 0.20\text{ V}$):** Current reaches a minimum at the valley point:
   $$J_{valley} = 1.74 \times 10^4\text{ A/cm}^2 \quad \text{at } V_{valley} = 0.200\text{ V}$$
   yielding a **Peak-to-Valley Current Ratio (PVCR):**
   $$\text{PVCR} = \frac{J_{peak}}{J_{valley}} = \frac{1.18 \times 10^5}{1.74 \times 10^4} \approx 6.78$$
   This value aligns closely with experimental room-temperature measurements for $\text{GaAs} / \text{AlGaAs}$ RTDs ($4\text{--}8$).

### 5.4 3D Dynamic Wavepacket Results
Running the 2D TDSE Split-Step Fourier solver confirmed:
- **On-Resonance ($E_0 = E_1 = 0.088\text{ eV}$):** The incident wavepacket penetrates Barrier 1, establishing a localized standing wave oscillation inside the quantum well cavity over $t \approx 50\text{--}120\text{ fs}$. A coherent transmitted wavepacket emerges from Barrier 2 and propagates into the collector with high amplitude.
- **Off-Resonance ($E_0 = 0.044\text{ eV}$):** Over 99% of the wavepacket reflects off Barrier 1, resulting in zero standing wave formation in the well and undetectable transmission.

---

## 6. Main Conclusions

1. **Verification of Resonant Cavity Dynamics:** The Transfer Matrix Method rigorously confirmed that near-unity transmission ($T \to 1$) occurs when constructive de Broglie wave interference takes place within the quantum well, amplifying probability density by over $50\times$ relative to the incident lead.
2. **Linewidth-Lifetime Duality:** Quasi-bound state lifetimes $\tau = \hbar/\Gamma$ are directly controlled by barrier thickness ($L_b$). Thicker barriers significantly enhance the cavity $Q$-factor at the expense of absolute current density.
3. **Macroscopic Manifestation of Quantum Mechanics:** The non-linear N-shaped RTD $I-V$ characteristic and **Negative Differential Resistance (NDR)** are direct macroscopic consequences of the alignment and subsequent quenching of sub-band levels against the emitter Fermi sea. A peak current density of $1.18 \times 10^5\text{ A/cm}^2$ and a PVCR of $6.78$ were demonstrated.
4. **Resilient Multi-Platform Deployment:** Addressing software licensing barriers, the project delivered:
   - A 1-click **interactive 3D WebGL simulator** deployed globally via GitHub Pages.
   - A **pure Python desktop GUI** requiring zero external libraries.
   - An extensible **MATLAB script and figure suite**.

---

## 7. Future Scope & Research Extensions

1. **Self-Consistent Poisson-Schrödinger Electrostatics:**  
   Under high current densities, electrons dynamically accumulate inside the quantum well, creating a localized space-charge potential that modifies the conduction band profile. Solving Schrödinger's equation self-consistently with Poisson's equation will capture electrostatic hysteresis and intrinsic bistability in the NDR region.
2. **Non-Equilibrium Green's Function (NEGF) Formalism:**  
   Extending the solver from coherent TMM to an open-boundary NEGF Hamiltonian will allow rigorous modeling of dissipative, incoherent processes such as optical phonon emission, acoustic phonon scattering, and interface roughness scattering.
3. **High-Offset Heterostructure Systems ($\text{In}_{0.53}\text{Ga}_{0.47}\text{As} / \text{AlAs}$ and $\text{InAs} / \text{AlSb}$):**  
   Simulating broken-gap and high-conduction-band-offset heterostructures ($V_0 > 1.0\text{ eV}$) to achieve ultra-high Peak-to-Valley Current Ratios ($\text{PVCR} > 25\text{--}50$) and THz switching speeds.
4. **Quantum Cascade Laser (QCL) Superlattices:**  
   Expanding from a double-barrier structure to multi-stage cascaded quantum wells ($20\text{--}50$ periods) to simulate intersubband optical transitions and population inversion for mid-infrared and THz lasers.
5. **WebGPU Acceleration & Machine Learning Inverse Design:**  
   Leveraging WebGPU compute shaders to run 3D TDSE simulations at 60 FPS directly in the browser, and applying neural network surrogate models to solve the inverse design problem: automatically determining the optimal $V_0, L_b, L_w$ required to meet target $V_p, J_p$, and PVCR specifications.

---

## 8. References

1. **Esaki, L., & Tsu, R.** (1970). Superlattice and negative differential conductivity in semiconductors. *IBM Journal of Research and Development*, 14(1), 61–65.
2. **Tsu, R., & Esaki, L.** (1973). Tunneling in a finite superlattice. *Applied Physics Letters*, 22(11), 562–564.
3. **Chang, L. L., Esaki, L., & Tsu, R.** (1974). Resonant tunneling in semiconductor double barriers. *Applied Physics Letters*, 24(12), 593–595.
4. **BenDaniel, D. J., & Duke, C. B.** (1966). Space-charge effects on electron tunneling. *Physical Review*, 152(2), 683–692.
5. **Bohm, D.** (1951). *Quantum Theory*. Prentice-Hall, New York.
6. **Jonsson, B., & Eng, S. T.** (1990). Solving the Schrödinger equation in arbitrary quantum-well structures with time-dependent effective mass. *IEEE Journal of Quantum Electronics*, 26(11), 2025–2035.
7. **Datta, S.** (1995). *Electronic Transport in Mesoscopic Systems*. Cambridge University Press.
8. **Feit, M. D., Fleck, J. A., & Steiger, A.** (1982). Solution of the Schrödinger equation by a spectral method. *Journal of Computational Physics*, 47(3), 412–433.
9. **Suzuki, S., Asada, M., Teranishi, A., Sugiyama, H., & Yokoyama, H.** (2010). Fundamental oscillation up to 1.04 THz in resonant-tunneling-diode oscillators on InP substrate. *Applied Physics Letters*, 97(24), 242102.
10. **Lake, R., Klimeck, G., Bowen, R. C., & Jovanovic, D.** (1997). Single and multiband modeling of quantum electron transport through layered semiconductor devices. *Journal of Applied Physics*, 81(12), 7845–7869.
