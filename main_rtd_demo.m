% =========================================================================
% MAIN_RTD_DEMO - Complete Resonant Tunnelling & Diode Simulation Suite
%
% This script runs a comprehensive simulation of quantum resonant tunnelling
% in a double-barrier heterostructure (e.g. AlGaAs/GaAs/AlGaAs):
%   1. Resonant Tunnelling & Transmission Spectrum T(E)
%   2. Wavefunction standing wave cavity amplification in the quantum well
%   3. Systematic parameter sweeps:
%      - Varying barrier height (V0)
%      - Varying barrier thickness (Lb)
%      - Varying quantum well width (Lw)
%   4. Resonant Tunnelling Diode (RTD) operation:
%      - Band diagram alignment at zero, peak, and valley bias
%      - Complete I-V curve with Negative Differential Resistance (NDR)
%   5. 3D Heterostructure & Wavefunction surface visualization
%
% To run the interactive graphical app, simply execute:
%   rtd_interactive_app
% To run the 3D time-dependent wavepacket dynamics, execute:
%   rtd_3d_wavepacket('resonant')
% =========================================================================

clear; close all; clc;

fprintf('=================================================================\n');
fprintf('   RESONANT TUNNELLING IN DOUBLE BARRIER STRUCTURE & RTD DIODE   \n');
fprintf('=================================================================\n\n');

% -------------------------------------------------------------------------
% 1. Baseline Device Parameters (AlGaAs / GaAs / AlGaAs)
% -------------------------------------------------------------------------
geom.V0         = 0.30;   % Barrier height [eV] (conduction band offset)
geom.Lb         = 3.00;   % Barrier thickness [nm]
geom.Lw         = 5.00;   % Quantum well width [nm]
geom.V_bias     = 0.00;   % Bias voltage [V]
geom.m_eff_well = 0.067;  % GaAs electron effective mass (m*/m0)
geom.m_eff_barr = 0.092;  % Al0.3Ga0.7As electron effective mass (m*/m0)
geom.n_slices   = 100;    % Discretization slices
geom.L_contact  = 6.00;   % Lead length to visualize [nm]

% Energy grid for transmission calculation
E_eV = linspace(0.001, geom.V0 * 1.25, 400);

% Compute Transmission Coefficient T(E)
fprintf('Step 1: Calculating baseline transmission spectrum T(E)...\n');
[T, R] = calculate_tmm(E_eV, geom);

% Find resonance peaks and linewidths (FWHM)
[pks, locs, w_fwhm] = find_resonance_peaks(T, E_eV);

hbar = 1.0545718e-34;
e_ch = 1.6021766e-19;

fprintf('Detected %d resonance peak(s):\n', length(pks));
for k = 1:length(pks)
    gamma_eV = w_fwhm(k);
    tau_fs = (hbar / (gamma_eV * e_ch)) * 1e15;
    fprintf('  Resonance E_%d = %.4f eV | Peak T = %.4f | FWHM Gamma = %.4f eV | Lifetime tau = %.1f fs\n', ...
            k, locs(k), pks(k), gamma_eV, tau_fs);
end
fprintf('\n');

% Calculate spatial wave function profile at the fundamental resonance
E_res = locs(1);
[~, ~, sim_res] = calculate_tmm(E_res, geom, true);

% Calculate spatial wave function profile off-resonance for comparison
E_off = E_res * 0.50;
[~, ~, sim_off] = calculate_tmm(E_off, geom, true);

% -------------------------------------------------------------------------
% FIGURE 1: Transmission Spectrum & Resonant Wavefunction Cavity
% -------------------------------------------------------------------------
fig1 = figure('Name', 'Resonant Tunnelling: Fundamentals & Wavefunction', ...
              'Color', 'w', 'Position', [100, 100, 1100, 700]);

% Subplot 1: Band profile & Wavefunction at Resonance vs Off-Resonance
subplot(2, 1, 1);
plot(sim_res.x_nm, sim_res.V_eV, 'k-', 'LineWidth', 2.5); hold on; grid on;

% Shade barriers
fill([0 geom.Lb geom.Lb 0], [0 0 geom.V0 geom.V0], ...
     [0.9 0.7 0.7], 'EdgeColor', 'none', 'FaceAlpha', 0.4);
x2_s = geom.Lb + geom.Lw; x2_e = x2_s + geom.Lb;
fill([x2_s x2_e x2_e x2_s], [0 0 geom.V0 geom.V0], ...
     [0.9 0.7 0.7], 'EdgeColor', 'none', 'FaceAlpha', 0.4);

% Probability densities
scale_fac = 0.08 / max(sim_res.prob_density);
h_res = plot(sim_res.x_nm, E_res + sim_res.prob_density * scale_fac, ...
             'b-', 'LineWidth', 2.2);
h_off = plot(sim_off.x_nm, E_off + sim_off.prob_density * scale_fac, ...
             'r--', 'LineWidth', 1.8);

yline(E_res, 'b:', 'LineWidth', 1.2);
yline(E_off, 'r:', 'LineWidth', 1.2);

xlabel('Position x [nm]', 'FontSize', 11, 'FontWeight', 'bold');
ylabel('Energy [eV]', 'FontSize', 11, 'FontWeight', 'bold');
title(sprintf('Double Barrier Conduction Band Profile & Probability Density |\\psi(x)|^2\n(Resonant Cavity Amplification in Well vs Off-Resonance Barrier Reflection)'), ...
      'FontSize', 12, 'FontWeight', 'bold');
legend([h_res, h_off], ...
       {sprintf('On-Resonance (E = %.3f eV, T = %.3f) - Standing Wave Buildup', E_res, sim_res.T), ...
        sprintf('Off-Resonance (E = %.3f eV, T = %.4f) - Almost Total Reflection', E_off, sim_off.T)}, ...
       'Location', 'northeast', 'FontSize', 10);
ylim([-0.05, geom.V0 * 1.3]);
xlim([sim_res.x_nm(1), sim_res.x_nm(end)]);

% Subplot 2: Transmission Spectrum (Linear & Semilog)
subplot(2, 1, 2);
yyaxis left;
plot(E_eV, T, 'b-', 'LineWidth', 2.2); hold on; grid on;
ylabel('Transmission Probability T(E) [Linear]', 'FontSize', 11, 'FontWeight', 'bold');
ylim([0, 1.15]);

% Mark peaks
plot(locs, pks, 'ro', 'MarkerFaceColor', 'r', 'MarkerSize', 7);
for k = 1:length(pks)
    text(locs(k), min(1.05, pks(k) + 0.06), sprintf('E_%d = %.3f eV\n(\\tau = %.1f fs)', k, locs(k), (hbar/(w_fwhm(k)*e_ch))*1e15), ...
         'FontSize', 9, 'FontWeight', 'bold', 'HorizontalAlignment', 'center');
end

yyaxis right;
semilogy(E_eV, max(1e-6, T), 'g--', 'LineWidth', 1.5);
ylabel('log_{10} T(E) [Semilog]', 'FontSize', 11, 'FontWeight', 'bold');
ylim([1e-6, 2]);

xline(geom.V0, 'k--', sprintf('Barrier Height V_0 = %.2f eV', geom.V0), ...
      'LabelVerticalAlignment', 'bottom', 'FontSize', 10);

xlabel('Incident Electron Energy E [eV]', 'FontSize', 11, 'FontWeight', 'bold');
title('Transmission Coefficient Spectrum T(E)', 'FontSize', 12, 'FontWeight', 'bold');
xlim([0, geom.V0 * 1.25]);

% -------------------------------------------------------------------------
% FIGURE 2: Systematic Parametric Variations (V0, Lb, Lw)
% -------------------------------------------------------------------------
fprintf('Step 2: Computing parametric sweeps (Barrier Height, Thickness, Well Width)...\n');
fig2 = figure('Name', 'Resonant Tunnelling: Effect of V0, Lb, and Lw', ...
              'Color', 'w', 'Position', [120, 120, 1250, 450]);

% Subplot 1: Vary Barrier Height V0
subplot(1, 3, 1);
V0_list = [0.20, 0.30, 0.45, 0.60];
colors_V0 = lines(length(V0_list));
hold on; grid on;
for iv0 = 1:length(V0_list)
    g_temp = geom;
    g_temp.V0 = V0_list(iv0);
    T_sweep = calculate_tmm(E_eV, g_temp);
    plot(E_eV, T_sweep, 'LineWidth', 2.0, 'Color', colors_V0(iv0, :), ...
         'DisplayName', sprintf('V_0 = %.2f eV', V0_list(iv0)));
end
xlabel('Energy E [eV]', 'FontWeight', 'bold');
ylabel('Transmission T(E)', 'FontWeight', 'bold');
title('Varying Barrier Height V_0', 'FontWeight', 'bold', 'FontSize', 11);
legend('Location', 'northeast');
xlim([0, 0.40]); ylim([0, 1.1]);

% Subplot 2: Vary Barrier Thickness Lb (Linewidth & Lifetime Control)
subplot(1, 3, 2);
Lb_list = [2.0, 3.0, 4.0, 5.0];
colors_Lb = parula(length(Lb_list) + 1);
hold on; grid on;
for ilb = 1:length(Lb_list)
    g_temp = geom;
    g_temp.Lb = Lb_list(ilb);
    T_sweep = calculate_tmm(E_eV, g_temp);
    plot(E_eV, T_sweep, 'LineWidth', 2.0, 'Color', colors_Lb(ilb, :), ...
         'DisplayName', sprintf('L_b = %.1f nm', Lb_list(ilb)));
end
xlabel('Energy E [eV]', 'FontWeight', 'bold');
ylabel('Transmission T(E)', 'FontWeight', 'bold');
title('Varying Barrier Thickness L_b', 'FontWeight', 'bold', 'FontSize', 11);
legend('Location', 'northeast');
xlim([0.05, 0.15]); ylim([0, 1.1]);

% Subplot 3: Vary Quantum Well Width Lw (Bound State Energy Shift)
subplot(1, 3, 3);
Lw_list = [3.5, 5.0, 7.0, 10.0];
colors_Lw = cool(length(Lw_list));
hold on; grid on;
for ilw = 1:length(Lw_list)
    g_temp = geom;
    g_temp.Lw = Lw_list(ilw);
    T_sweep = calculate_tmm(E_eV, g_temp);
    plot(E_eV, T_sweep, 'LineWidth', 2.0, 'Color', colors_Lw(ilw, :), ...
         'DisplayName', sprintf('L_w = %.1f nm', Lw_list(ilw)));
end
xlabel('Energy E [eV]', 'FontWeight', 'bold');
ylabel('Transmission T(E)', 'FontWeight', 'bold');
title('Varying Quantum Well Width L_w', 'FontWeight', 'bold', 'FontSize', 11);
legend('Location', 'northeast');
xlim([0, 0.35]); ylim([0, 1.1]);

% -------------------------------------------------------------------------
% FIGURE 3: Resonant Tunnelling Diode (RTD) I-V & Band Alignment
% -------------------------------------------------------------------------
fprintf('Step 3: Calculating RTD Diode I-V curve via Tsu-Esaki formula...\n');
rtd_opts.V_min = 0.0;
rtd_opts.V_max = 0.35;
rtd_opts.nV    = 50;
rtd_opts.nE    = 100;
rtd_opts.Temp_K = 300;
rtd_opts.E_Fermi = 0.04; % 40 meV
iv_data = calculate_rtd_iv(geom, rtd_opts);

fprintf('RTD Diode Characteristics:\n');
fprintf('  Peak Voltage V_p:    %.3f V\n', iv_data.V_peak);
fprintf('  Peak Current J_p:    %.1f A/cm^2\n', iv_data.J_peak);
fprintf('  Valley Voltage V_v:  %.3f V\n', iv_data.V_valley);
fprintf('  Valley Current J_v:  %.1f A/cm^2\n', iv_data.J_valley);
fprintf('  PVCR (J_p / J_v):    %.2f\n\n', iv_data.PVCR);

fig3 = figure('Name', 'Resonant Tunnelling Diode (RTD): Band Alignment & I-V Curve', ...
              'Color', 'w', 'Position', [140, 140, 1200, 680]);

% Left panels: 3 operating regimes
bias_cases = [0.0, iv_data.V_peak, iv_data.V_valley];
case_names = {'(a) Zero Bias: V = 0 V (Thermal Equilibrium)', ...
              sprintf('(b) Peak Bias: V = %.2f V (Resonant Transmission)', iv_data.V_peak), ...
              sprintf('(c) Valley Bias: V = %.2f V (NDR & Quenched Tunneling)', iv_data.V_valley)};

for ic = 1:3
    subplot(3, 2, 2*ic - 1);
    g_bias = geom;
    g_bias.V_bias = bias_cases(ic);
    [~, ~, s_b] = calculate_tmm(rtd_opts.E_Fermi, g_bias, true);

    plot(s_b.x_nm, s_b.V_eV, 'k-', 'LineWidth', 2.0); hold on; grid on;
    % Fermi level line in emitter
    yline(rtd_opts.E_Fermi, 'g--', 'E_F (Emitter)', 'LineWidth', 1.5);
    % Collector Fermi level
    yline(rtd_opts.E_Fermi - bias_cases(ic), 'm--', 'E_{F,coll}', 'LineWidth', 1.2);

    % Resonant level inside well
    E_res_cur = E_res - bias_cases(ic) * 0.5;
    line([geom.Lb, geom.Lb + geom.Lw], [E_res_cur, E_res_cur], ...
         'Color', [0.8 0.2 0.2], 'LineWidth', 2.5);

    title(case_names{ic}, 'FontSize', 10, 'FontWeight', 'bold');
    ylabel('E [eV]', 'FontWeight', 'bold');
    ylim([-bias_cases(ic) - 0.08, geom.V0 * 1.2]);
    if ic == 3, xlabel('Position x [nm]', 'FontWeight', 'bold'); end
end

% Right panel: Full RTD I-V characteristic with Negative Differential Resistance
subplot(3, 2, [2, 4, 6]);
plot(iv_data.V, iv_data.J, 'Color', [0.1 0.6 0.2], 'LineWidth', 2.8); hold on; grid on;

% Highlight Negative Differential Resistance (NDR) region
ndr_idx = find(iv_data.is_ndr);
if ~isempty(ndr_idx)
    plot(iv_data.V(ndr_idx), iv_data.J(ndr_idx), 'r-', 'LineWidth', 3.8);
    fill([iv_data.V_peak iv_data.V_valley iv_data.V_valley iv_data.V_peak], ...
         [0 0 max(iv_data.J)*1.1 max(iv_data.J)*1.1], [1 0.85 0.85], ...
         'EdgeColor', 'none', 'FaceAlpha', 0.4);
end

% Mark Peak and Valley Points
plot(iv_data.V_peak, iv_data.J_peak, 'ko', 'MarkerFaceColor', [1 0.5 0], 'MarkerSize', 10);
plot(iv_data.V_valley, iv_data.J_valley, 'ks', 'MarkerFaceColor', [0.7 0.2 0.9], 'MarkerSize', 10);

text(iv_data.V_peak, iv_data.J_peak * 1.05, ...
     sprintf('  Peak: (%.2f V, %.1f A/cm^2)', iv_data.V_peak, iv_data.J_peak), ...
     'FontSize', 10, 'FontWeight', 'bold');
text(iv_data.V_valley, iv_data.J_valley * 0.80, ...
     sprintf('  Valley: (%.2f V, %.1f A/cm^2)\n  PVCR = %.2f', iv_data.V_valley, iv_data.J_valley, iv_data.PVCR), ...
     'FontSize', 10, 'FontWeight', 'bold');

% Annotate NDR region
text((iv_data.V_peak + iv_data.V_valley)/2, (iv_data.J_peak + iv_data.J_valley)/2, ...
     'NDR Region\n(dI/dV < 0)', 'Color', 'r', 'FontWeight', 'bold', ...
     'HorizontalAlignment', 'center', 'FontSize', 12);

xlabel('Applied Bias Voltage V_a [V]', 'FontSize', 12, 'FontWeight', 'bold');
ylabel('Current Density J [A/cm^2]', 'FontSize', 12, 'FontWeight', 'bold');
title('Resonant Tunnelling Diode I-V Characteristic Curve', 'FontSize', 13, 'FontWeight', 'bold');
xlim([0, max(iv_data.V)]);
ylim([0, max(iv_data.J) * 1.15]);

% -------------------------------------------------------------------------
% FIGURE 4: 3D Visualization of Heterostructure & Wavefunction
% -------------------------------------------------------------------------
fprintf('Step 4: Generating 3D heterostructure potential & wavefunction surface...\n');
fig4 = figure('Name', '3D Resonant Tunnelling Simulation', ...
              'Color', 'w', 'Position', [160, 160, 1000, 650]);

ax3d = axes('Parent', fig4);
y_transverse = linspace(-6, 6, 50);
[X3D, Y3D] = meshgrid(sim_res.x_nm, y_transverse);
V_profile_3D = repmat(sim_res.V_eV, length(y_transverse), 1);
Psi_3D = repmat(sim_res.prob_density, length(y_transverse), 1) .* exp(-(Y3D / 3.0).^2);

% Double barrier potential surface
surf(ax3d, X3D, Y3D, V_profile_3D, 'FaceAlpha', 0.35, 'EdgeColor', 'none');
hold(ax3d, 'on');

% Resonant standing wave surface
surf(ax3d, X3D, Y3D, E_res + 0.08 * (Psi_3D / max(sim_res.prob_density)), ...
     'FaceAlpha', 0.88, 'EdgeColor', 'none');

colormap(ax3d, turbo(256));
shading(ax3d, 'interp');
view(ax3d, -42, 40); grid(ax3d, 'on');

xlabel(ax3d, 'Transport Coordinate x [nm]', 'FontSize', 11, 'FontWeight', 'bold');
ylabel(ax3d, 'Transverse Coordinate y [nm]', 'FontSize', 11, 'FontWeight', 'bold');
zlabel(ax3d, 'Energy [eV]', 'FontSize', 11, 'FontWeight', 'bold');
title(ax3d, sprintf('3D Heterostructure Simulation: Double Barrier Potential & Resonant Wavefunction\n(Resonant Cavity Energy E_1 = %.3f eV)', E_res), ...
      'FontSize', 12, 'FontWeight', 'bold');
zlim(ax3d, [-0.05, geom.V0 * 1.3]);
cbar = colorbar(ax3d);
ylabel(cbar, 'Energy / Probability Density');

fprintf('\nAll calculations and figures completed successfully!\n');
fprintf('To launch the Interactive GUI, type:  rtd_interactive_app\n');
fprintf('To launch the 3D TDSE Wavepacket, type:  rtd_3d_wavepacket\n');
fprintf('To view the 3D Landscape Surfaces, type: rtd_3d_landscape\n');
