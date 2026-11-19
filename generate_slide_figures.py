import numpy as np
import matplotlib.pyplot as plt
import os

# Set global matplotlib styling for clean academic look
plt.rcParams['font.family'] = 'serif'
plt.rcParams['font.serif'] = ['Times New Roman', 'DejaVu Serif']
plt.rcParams['font.size'] = 11
plt.rcParams['axes.linewidth'] = 1.0
plt.rcParams['axes.edgecolor'] = '#111827'
plt.rcParams['xtick.color'] = '#111827'
plt.rcParams['ytick.color'] = '#111827'

os.makedirs('slide_figures', exist_ok=True)

# -------------------------------------------------------------
# FIGURE 1: Conduction Band Potential & Bound State Wavefunction
# -------------------------------------------------------------
fig, ax = plt.subplots(figsize=(6.5, 4.2), dpi=300)

x = np.linspace(0, 15, 600)  # nm
# Barriers at 3-6 nm and 9-12 nm
V = np.zeros_like(x)
V[(x >= 3.5) & (x <= 6.5)] = 0.30  # Lb = 3 nm
V[(x >= 9.5) & (x <= 12.5)] = 0.30 # Lb = 3 nm; Lw = 3 nm (between 6.5 and 9.5)

ax.plot(x, V, color='#111827', linewidth=2.2, label='Conduction Band V(x)')
ax.fill_between(x, 0, V, color='#F3F4F6')

# Resonant bound state level E1 = 0.088 eV
ax.axhline(0.088, xmin=6.5/15, xmax=9.5/15, color='#374151', linestyle='--', linewidth=1.8, label=r'Eigenstate $E_1 = 88\text{ meV}$')

# Schematic wavefunction |psi(x)|^2
psi_x = np.linspace(0, 15, 600)
psi = np.zeros_like(psi_x)
# Left incident + reflected
psi[psi_x < 3.5] = 0.04 * np.cos(3 * (psi_x[psi_x < 3.5] - 1.5))**2 + 0.088
# Well resonant standing wave (amplified)
in_well = (psi_x >= 6.5) & (psi_x <= 9.5)
psi[in_well] = 0.12 * np.sin(np.pi * (psi_x[in_well] - 6.5) / 3.0)**2 + 0.088
# Decaying in barriers
psi[(psi_x >= 3.5) & (psi_x < 6.5)] = 0.088 + 0.04 * np.exp(-1.5 * (psi_x[(psi_x >= 3.5) & (psi_x < 6.5)] - 3.5))
psi[(psi_x > 9.5) & (psi_x <= 12.5)] = 0.088 + 0.04 * np.exp(-1.5 * (12.5 - psi_x[(psi_x > 9.5) & (psi_x <= 12.5)]))
# Transmitted wave
psi[psi_x > 12.5] = 0.04 * np.cos(3 * (psi_x[psi_x > 12.5] - 12.5))**2 + 0.088

ax.plot(psi_x, psi, color='#111827', linewidth=1.8, linestyle='-', label=r'Probability Density $|\psi(x)|^2$')

ax.set_xlim(0, 15)
ax.set_ylim(-0.02, 0.36)
ax.set_xlabel('Position x [nm]', fontweight='bold')
ax.set_ylabel('Energy [eV]', fontweight='bold')
ax.set_title('Conduction Band Profile & Quasi-Bound Cavity State', fontweight='bold', pad=10)

ax.text(2.0, 0.20, 'Emitter\nLead', ha='center', va='center', fontsize=9.5, fontweight='bold', bbox=dict(boxstyle='square,pad=0.3', fc='white', ec='#D1D5DB'))
ax.text(5.0, 0.32, r'Barrier $V_0$', ha='center', va='center', fontsize=9.5, fontweight='bold')
ax.text(8.0, 0.26, r'Well ($L_w$)', ha='center', va='center', fontsize=9.5, fontweight='bold')
ax.text(11.0, 0.32, r'Barrier $V_0$', ha='center', va='center', fontsize=9.5, fontweight='bold')
ax.text(13.8, 0.20, 'Collector\nLead', ha='center', va='center', fontsize=9.5, fontweight='bold', bbox=dict(boxstyle='square,pad=0.3', fc='white', ec='#D1D5DB'))

ax.grid(True, linestyle=':', alpha=0.5, color='#9CA3AF')
ax.legend(loc='lower center', frameon=True, edgecolor='#D1D5DB', fontsize=9)
plt.tight_layout()
plt.savefig('slide_figures/fig1_potential_profile.png', dpi=300)
plt.close()

# -------------------------------------------------------------
# FIGURE 2: Transmission Spectrum T(E)
# -------------------------------------------------------------
fig, ax = plt.subplots(figsize=(6.5, 4.2), dpi=300)

E = np.linspace(0, 0.40, 800)  # eV
# Lorentzian resonant peaks
E1, gamma1 = 0.088, 0.0040
E2, gamma2 = 0.312, 0.022
T = (gamma1/2)**2 / ((E - E1)**2 + (gamma1/2)**2) + 0.65 * (gamma2/2)**2 / ((E - E2)**2 + (gamma2/2)**2)
T = np.clip(T, 1e-6, 1.0)

ax.plot(E * 1000, T, color='#111827', linewidth=2.2)
ax.fill_between(E * 1000, 0, T, color='#F3F4F6', alpha=0.8)

# Highlight E1
ax.scatter([E1 * 1000], [1.0], color='#111827', s=50, zorder=5)
ax.annotate(r'$E_1 = 88.0\text{ meV}$' + '\n' + r'$\Gamma = 4.0\text{ meV}$' + '\n' + r'$\tau = 164.7\text{ fs}$',
            xy=(E1 * 1000, 1.0), xytext=(E1 * 1000 + 35, 0.78),
            arrowprops=dict(facecolor='#111827', shrink=0.08, width=1.0, headwidth=5),
            fontsize=9.5, bbox=dict(boxstyle='square,pad=0.4', fc='white', ec='#9CA3AF'))

# Highlight E2
ax.scatter([E2 * 1000], [0.65], color='#111827', s=50, zorder=5)
ax.annotate(r'$E_2 = 312\text{ meV}$' + '\n' + r'$\Gamma = 22.0\text{ meV}$',
            xy=(E2 * 1000, 0.65), xytext=(E2 * 1000 - 90, 0.50),
            arrowprops=dict(facecolor='#111827', shrink=0.08, width=1.0, headwidth=5),
            fontsize=9.5, bbox=dict(boxstyle='square,pad=0.4', fc='white', ec='#9CA3AF'))

ax.set_xlim(0, 400)
ax.set_ylim(-0.02, 1.08)
ax.set_xlabel('Incident Electron Energy E [meV]', fontweight='bold')
ax.set_ylabel('Transmission Probability T(E)', fontweight='bold')
ax.set_title('Resonant Transmission Spectrum T(E)', fontweight='bold', pad=10)
ax.grid(True, linestyle=':', alpha=0.5, color='#9CA3AF')

plt.tight_layout()
plt.savefig('slide_figures/fig2_transmission_spectrum.png', dpi=300)
plt.close()

# -------------------------------------------------------------
# FIGURE 3: RTD Current Density J vs Bias Voltage Va
# -------------------------------------------------------------
fig, ax = plt.subplots(figsize=(6.5, 4.2), dpi=300)

V_a = np.linspace(0, 0.35, 600)
# Model N-shaped RTD curve
J_peak = 1.18e5
V_peak = 0.14
J_valley = 1.74e4
V_valley = 0.20

# Resonant current + thermal leakage
J_res = J_peak * np.exp(-((V_a - V_peak)/0.045)**2) * (V_a <= V_peak) + \
        (J_valley + (J_peak - J_valley) * np.exp(-((V_a - V_peak)/0.025)**2)) * ((V_a > V_peak) & (V_a <= V_valley)) + \
        (J_valley + 1.2e5 * (V_a - V_valley)**2) * (V_a > V_valley)

# NDR Shading
ax.axvspan(V_peak, V_valley, color='#E5E7EB', alpha=0.6, label='NDR Region (dI/dV < 0)')

ax.plot(V_a, J_res / 1e4, color='#111827', linewidth=2.2)

# Peak marker
ax.scatter([V_peak], [J_peak / 1e4], color='#111827', s=60, zorder=5)
ax.annotate(f'Peak: (0.14 V, 11.8×10⁴ A/cm²)', xy=(V_peak, J_peak / 1e4), xytext=(V_peak - 0.09, 10.5),
            arrowprops=dict(facecolor='#111827', shrink=0.08, width=1.0, headwidth=5),
            fontsize=9.0, bbox=dict(boxstyle='square,pad=0.3', fc='white', ec='#9CA3AF'))

# Valley marker
ax.scatter([V_valley], [J_valley / 1e4], color='#111827', s=60, zorder=5)
ax.annotate(f'Valley: (0.20 V, 1.74×10⁴ A/cm²)\nPVCR = 6.78', xy=(V_valley, J_valley / 1e4), xytext=(V_valley + 0.02, 3.2),
            arrowprops=dict(facecolor='#111827', shrink=0.08, width=1.0, headwidth=5),
            fontsize=9.0, bbox=dict(boxstyle='square,pad=0.3', fc='white', ec='#9CA3AF'))

ax.set_xlim(0, 0.35)
ax.set_ylim(0, 13.5)
ax.set_xlabel('Applied Bias Voltage $V_a$ [V]', fontweight='bold')
ax.set_ylabel(r'Current Density $J$ [$10^4\text{ A/cm}^2$]', fontweight='bold')
ax.set_title(r'Room-Temperature (300 K) RTD $I$-$V$ Characteristic', fontweight='bold', pad=10)
ax.grid(True, linestyle=':', alpha=0.5, color='#9CA3AF')
ax.legend(loc='upper left', frameon=True, edgecolor='#D1D5DB', fontsize=9.5)

plt.tight_layout()
plt.savefig('slide_figures/fig3_rtd_iv_curve.png', dpi=300)
plt.close()

# -------------------------------------------------------------
# FIGURE 4: Wavepacket Propagation (On-Resonance vs Off-Resonance)
# -------------------------------------------------------------
fig, (ax1, ax2) = plt.subplots(2, 1, figsize=(6.5, 4.4), dpi=300, sharex=True)

x_wp = np.linspace(0, 16, 500)
barriers = np.zeros_like(x_wp)
barriers[(x_wp >= 4) & (x_wp <= 7)] = 1.0
barriers[(x_wp >= 10) & (x_wp <= 13)] = 1.0

# On-resonance
ax1.fill_between(x_wp, 0, barriers * 0.9, color='#E5E7EB', alpha=0.7)
# Cavity standing wave + transmitted packet
psi_on = 0.15 * np.exp(-((x_wp - 2.5)/1.2)**2) + \
         0.85 * np.sin(np.pi * (x_wp - 7)/3.0)**2 * ((x_wp >= 7) & (x_wp <= 10)) + \
         0.45 * np.exp(-((x_wp - 14.5)/1.2)**2)
ax1.plot(x_wp, psi_on, color='#111827', linewidth=2.0)
ax1.set_ylim(0, 1.05)
ax1.set_ylabel(r'$|\Psi(x, t)|^2$', fontweight='bold')
ax1.set_title('On-Resonance ($E = E_1 = 88\\text{ meV}$): Cavity Trapping & Transmission', fontweight='bold', fontsize=10)
ax1.text(8.5, 0.9, 'Resonant Cavity Buildup', ha='center', fontsize=8.5, fontweight='bold', bbox=dict(boxstyle='square,pad=0.2', fc='white', ec='#D1D5DB'))
ax1.text(14.5, 0.55, 'Transmitted Pulse', ha='center', fontsize=8.5, fontweight='bold')
ax1.grid(True, linestyle=':', alpha=0.5)

# Off-resonance
ax2.fill_between(x_wp, 0, barriers * 0.9, color='#E5E7EB', alpha=0.7)
# High reflection back to left, almost 0 in well and right
psi_off = 0.92 * np.exp(-((x_wp - 2.2)/1.4)**2) + 0.02 * ((x_wp > 7) & (x_wp < 10))
ax2.plot(x_wp, psi_off, color='#111827', linewidth=2.0)
ax2.set_ylim(0, 1.05)
ax2.set_xlabel('Position x [nm]', fontweight='bold')
ax2.set_ylabel(r'$|\Psi(x, t)|^2$', fontweight='bold')
ax2.set_title('Off-Resonance ($E = 44\\text{ meV}$): >99% Wavepacket Reflection', fontweight='bold', fontsize=10)
ax2.text(2.2, 0.75, 'Reflected Wavepacket (>99%)', ha='center', fontsize=8.5, fontweight='bold', bbox=dict(boxstyle='square,pad=0.2', fc='white', ec='#D1D5DB'))
ax2.text(11.5, 0.4, 'Zero Cavity Penetration', ha='center', fontsize=8.5, color='#4B5563', fontstyle='italic')
ax2.grid(True, linestyle=':', alpha=0.5)

plt.tight_layout()
plt.savefig('slide_figures/fig4_wavepacket_comparison.png', dpi=300)
plt.close()

print('All 4 slide figures successfully generated in slide_figures/')
