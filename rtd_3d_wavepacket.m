function rtd_3d_wavepacket(mode_choice, user_geom)
% RTD_3D_WAVEPACKET - 3D Time-Dependent Quantum Wavepacket Simulation
%
% Visualizes quantum resonant tunnelling in real-time 3D.
% Solves the 2D Time-Dependent Schrödinger Equation (TDSE):
%   i*hbar * dPsi/dt = [-(hbar^2 / 2m*) * (d^2/dx^2 + d^2/dy^2) + V(x,y)] * Psi
% using the Split-Step Fourier Method (SSFM) and renders a dynamic 3D surface.
%
% Syntax:
%   rtd_3d_wavepacket()                     % Runs resonant mode by default
%   rtd_3d_wavepacket('resonant')           % Incident energy matches resonant level
%   rtd_3d_wavepacket('off_resonant')       % Incident energy misses resonant level
%   rtd_3d_wavepacket('compare')            % Side-by-side comparison of both
%   rtd_3d_wavepacket(mode, user_geom)      % Custom double-barrier parameters
%
% Inputs:
%   mode_choice - 'resonant' | 'off_resonant' | 'compare' (default: 'resonant')
%   user_geom   - Struct with fields .V0 (eV), .Lb (nm), .Lw (nm)

    if nargin < 1 || isempty(mode_choice)
        mode_choice = 'resonant';
    end

    % Physical constants
    hbar = 1.054571817e-34;  % J*s
    m0   = 9.1093837015e-31;  % kg
    e_ch = 1.602176634e-19;  % C
    m_eff = 0.067 * m0;       % GaAs effective mass

    % Default Geometry (AlGaAs / GaAs / AlGaAs)
    geom.V0 = 0.30;   % Barrier height [eV]
    geom.Lb = 2.50;   % Barrier thickness [nm]
    geom.Lw = 5.00;   % Quantum well width [nm]
    if nargin >= 2 && isstruct(user_geom)
        if isfield(user_geom, 'V0'), geom.V0 = user_geom.V0; end
        if isfield(user_geom, 'Lb'), geom.Lb = user_geom.Lb; end
        if isfield(user_geom, 'Lw'), geom.Lw = user_geom.Lw; end
    end

    % Find the ground state resonance energy Er using TMM first
    E_test = linspace(0.01, geom.V0 * 0.98, 200);
    T_test = calculate_tmm(E_test, geom);
    [pks, locs] = find_resonance_peaks(T_test, E_test);
    if ~isempty(pks)
        [~, max_pk_idx] = max(pks);
        E_res_eV = locs(max_pk_idx);
    else
        E_res_eV = 0.09; % fallback
    end
    E_off_eV = E_res_eV * 0.50; % Off-resonance energy

    fprintf('======================================================\n');
    fprintf('  3D QUANTUM WAVEPACKET SIMULATION: DOUBLE BARRIER     \n');
    fprintf('======================================================\n');
    fprintf('Barrier Height:      %.2f eV\n', geom.V0);
    fprintf('Barrier Thickness:   %.2f nm\n', geom.Lb);
    fprintf('Well Width:          %.2f nm\n', geom.Lw);
    fprintf('Resonant Energy Er:  %.4f eV\n', E_res_eV);
    fprintf('Off-Resonance Energy:%.4f eV\n', E_off_eV);
    fprintf('Mode Selected:       %s\n', mode_choice);
    fprintf('======================================================\n\n');

    switch lower(mode_choice)
        case 'compare'
            run_comparison_simulation(geom, E_res_eV, E_off_eV, hbar, m_eff, e_ch);
        case 'off_resonant'
            run_single_simulation(geom, E_off_eV, 'OFF-RESONANCE (Reflection)', hbar, m_eff, e_ch);
        otherwise
            run_single_simulation(geom, E_res_eV, 'ON-RESONANCE (Tunneling & Cavity Buildup)', hbar, m_eff, e_ch);
    end
end

% -------------------------------------------------------------------------
% Run single 3D dynamic wavepacket simulation
% -------------------------------------------------------------------------
function run_single_simulation(geom, E_incident_eV, title_str, hbar, m_eff, e_ch)
    % Computational Grid (in SI units)
    Lx = 40e-9;   % Domain [-20 nm, +20 nm]
    Ly = 18e-9;   % Domain [-9 nm, +9 nm]
    Nx = 160;
    Ny = 70;

    x = linspace(-Lx/2, Lx/2, Nx);
    y = linspace(-Ly/2, Ly/2, Ny);
    dx = x(2) - x(1);
    dy = y(2) - y(1);
    [X, Y] = meshgrid(x, y);

    % Barriers centered around x = 0
    % Quantum well spans from -Lw/2 to +Lw/2
    % Barrier 1: [-Lw/2 - Lb, -Lw/2]
    % Barrier 2: [ Lw/2,  Lw/2 + Lb]
    Lb_m = geom.Lb * 1e-9;
    Lw_m = geom.Lw * 1e-9;
    x_b1_start = -Lw_m/2 - Lb_m;
    x_b1_end   = -Lw_m/2;
    x_b2_start =  Lw_m/2;
    x_b2_end   =  Lw_m/2 + Lb_m;

    V0_J = geom.V0 * e_ch;
    V = zeros(Ny, Nx);
    is_barrier = (X >= x_b1_start & X <= x_b1_end) | (X >= x_b2_start & X <= x_b2_end);
    V(is_barrier) = V0_J;

    % Initial Wavepacket
    E_J = E_incident_eV * e_ch;
    k0 = sqrt(2 * m_eff * E_J) / hbar;
    x0 = -13e-9;  % Launch position in nm
    y0 = 0;
    sigma_x = 2.0e-9;
    sigma_y = 2.8e-9;

    Psi = exp(- (X - x0).^2 / (2 * sigma_x^2) - (Y - y0).^2 / (2 * sigma_y^2)) .* exp(1i * k0 * X);
    % Normalize
    norm_factor = sqrt(sum(sum(abs(Psi).^2)) * dx * dy);
    Psi = Psi / norm_factor;

    % Momentum grid for Split-Step Fourier Method
    kx = (2*pi/Lx) * [0:(Nx/2-1), -Nx/2:-1];
    ky = (2*pi/Ly) * [0:(Ny/2-1), -Ny/2:-1];
    [KX, KY] = meshgrid(kx, ky);
    K_sq = KX.^2 + KY.^2;

    % Time stepping parameters
    dt = 0.5e-16;  % 0.05 fs
    N_steps = 180;
    plot_interval = 2;

    % Kinetic and Potential evolution phase operators
    U_V_half = exp(-1i * (V * dt) / (2 * hbar));
    U_K      = exp(-1i * (hbar * K_sq / (2 * m_eff)) * dt);

    % Setup 3D Figure
    fig = figure('Name', ['3D RTD Wavepacket Simulation: ', title_str], ...
                 'Color', [0.10, 0.12, 0.16], 'Position', [100, 100, 1000, 650]);

    ax = axes('Parent', fig, 'Color', [0.12, 0.14, 0.18]);
    grid(ax, 'on');
    set(ax, 'XColor', [0.8 0.8 0.8], 'YColor', [0.8 0.8 0.8], 'ZColor', [0.8 0.8 0.8]);
    view(ax, -38, 48);

    X_nm = X * 1e9;
    Y_nm = Y * 1e9;
    prob_dens = abs(Psi).^2 * 1e-18; % Scaled for display

    h_surf = surf(ax, X_nm, Y_nm, prob_dens, 'EdgeColor', 'none');
    colormap(ax, turbo(256));
    caxis(ax, [0, 0.05]);
    cbar = colorbar(ax);
    set(cbar, 'Color', [0.9 0.9 0.9]);
    ylabel(cbar, '|\Psi(x, y)|^2 [arb. units]', 'FontSize', 11, 'Color', 'w');

    xlabel(ax, 'Transport Axis x [nm]', 'FontSize', 12, 'FontWeight', 'bold', 'Color', 'w');
    ylabel(ax, 'Transverse Axis y [nm]', 'FontSize', 12, 'FontWeight', 'bold', 'Color', 'w');
    zlabel(ax, 'Probability Density |\Psi|^2', 'FontSize', 12, 'FontWeight', 'bold', 'Color', 'w');
    zlim(ax, [0, 0.06]);
    xlim(ax, [-18, 18]);
    ylim(ax, [-8, 8]);

    % Draw 3D semi-transparent potential barrier planes
    hold(ax, 'on');
    draw_barrier_slabs(ax, x_b1_start*1e9, x_b1_end*1e9, x_b2_start*1e9, x_b2_end*1e9, 0.05, 8);

    title_handle = title(ax, sprintf('%s | E = %.3f eV | t = 0.0 fs', title_str, E_incident_eV), ...
                         'FontSize', 14, 'FontWeight', 'bold', 'Color', [1 0.85 0.3]);

    shading(ax, 'interp');
    camlight(ax, 'right');
    lighting(ax, 'gouraud');

    % Text banner showing transmission vs reflection status
    status_text = text(ax, -16, -6, 0.055, 'Incident wavepacket approaching barriers...', ...
                       'Color', [0.4 1 0.5], 'FontSize', 11, 'FontWeight', 'bold');

    % SSFM Time Evolution Loop
    for step = 1:N_steps
        % Half step in potential
        Psi = U_V_half .* Psi;
        % Full step in kinetic momentum space
        Psi_k = fft2(Psi);
        Psi_k = U_K .* Psi_k;
        Psi = ifft2(Psi_k);
        % Half step in potential
        Psi = U_V_half .* Psi;

        % Absorbing boundary condition at grid edges to prevent wrap-around
        Psi(:, 1:8) = Psi(:, 1:8) .* repmat(linspace(0, 1, 8), Ny, 1);
        Psi(:, end-7:end) = Psi(:, end-7:end) .* repmat(linspace(1, 0, 8), Ny, 1);

        if mod(step, plot_interval) == 0 && isvalid(fig)
            t_fs = step * dt * 1e15;
            prob_dens = abs(Psi).^2 * 1e-18;
            set(h_surf, 'ZData', prob_dens, 'CData', prob_dens);

            % Update status message
            well_prob = sum(sum(prob_dens(:, X_nm >= x_b1_end*1e9 & X_nm <= x_b2_start*1e9)));
            trans_prob = sum(sum(prob_dens(:, X_nm > x_b2_end*1e9)));

            if step < 40
                msg = 'Incident packet propagating toward Barrier 1...';
                col = [0.4 1 0.5];
            elseif step < 90
                if well_prob > 0.05
                    msg = sprintf('RESONANT BUILDUP! Standing wave forming in well (Density: %.2f)', well_prob);
                    col = [1.0 0.8 0.2];
                else
                    msg = 'Striking barrier: strong quantum reflection...';
                    col = [1.0 0.4 0.4];
                end
            else
                if trans_prob > 0.08
                    msg = sprintf('RESONANT TRANSMISSION! Packet emerging on collector side (T ~ %.2f)', trans_prob);
                    col = [0.2 0.9 1.0];
                else
                    msg = 'OFF-RESONANCE: Packet reflected back; virtually zero transmission.';
                    col = [1.0 0.3 0.3];
                end
            end

            set(status_text, 'String', msg, 'Color', col);
            set(title_handle, 'String', sprintf('%s | E = %.3f eV | t = %.1f fs', title_str, E_incident_eV, t_fs));
            drawnow limitrate;
        end
    end
end

% -------------------------------------------------------------------------
% Run side-by-side comparison of Resonant vs Off-Resonant wavepacket in 3D
% -------------------------------------------------------------------------
function run_comparison_simulation(geom, E_res_eV, E_off_eV, hbar, m_eff, e_ch)
    Lx = 36e-9;
    Ly = 14e-9;
    Nx = 128;
    Ny = 50;

    x = linspace(-Lx/2, Lx/2, Nx);
    y = linspace(-Ly/2, Ly/2, Ny);
    dx = x(2) - x(1); dy = y(2) - y(1);
    [X, Y] = meshgrid(x, y);

    Lb_m = geom.Lb * 1e-9;
    Lw_m = geom.Lw * 1e-9;
    x_b1_start = -Lw_m/2 - Lb_m; x_b1_end = -Lw_m/2;
    x_b2_start =  Lw_m/2;        x_b2_end =  Lw_m/2 + Lb_m;

    V0_J = geom.V0 * e_ch;
    V = zeros(Ny, Nx);
    is_barrier = (X >= x_b1_start & X <= x_b1_end) | (X >= x_b2_start & X <= x_b2_end);
    V(is_barrier) = V0_J;

    % Resonant Wavepacket
    k0_res = sqrt(2 * m_eff * E_res_eV * e_ch) / hbar;
    x0 = -11e-9;
    sigma_x = 2.0e-9; sigma_y = 2.4e-9;
    Psi_res = exp(-(X - x0).^2 / (2*sigma_x^2) - Y.^2 / (2*sigma_y^2)) .* exp(1i * k0_res * X);
    Psi_res = Psi_res / sqrt(sum(sum(abs(Psi_res).^2)) * dx * dy);

    % Off-resonant Wavepacket
    k0_off = sqrt(2 * m_eff * E_off_eV * e_ch) / hbar;
    Psi_off = exp(-(X - x0).^2 / (2*sigma_x^2) - Y.^2 / (2*sigma_y^2)) .* exp(1i * k0_off * X);
    Psi_off = Psi_off / sqrt(sum(sum(abs(Psi_off).^2)) * dx * dy);

    kx = (2*pi/Lx) * [0:(Nx/2-1), -Nx/2:-1];
    ky = (2*pi/Ly) * [0:(Ny/2-1), -Ny/2:-1];
    [KX, KY] = meshgrid(kx, ky);
    K_sq = KX.^2 + KY.^2;

    dt = 0.5e-16;
    N_steps = 160;
    U_V_half = exp(-1i * (V * dt) / (2 * hbar));
    U_K      = exp(-1i * (hbar * K_sq / (2 * m_eff)) * dt);

    fig = figure('Name', '3D RTD Comparison: Resonant vs Off-Resonant Tunneling', ...
                 'Color', [0.10, 0.12, 0.16], 'Position', [60, 80, 1200, 600]);

    % Subplot 1: Resonant
    ax1 = subplot(1, 2, 1, 'Parent', fig);
    set(ax1, 'Color', [0.12 0.14 0.18], 'XColor', 'w', 'YColor', 'w', 'ZColor', 'w');
    view(ax1, -38, 45); grid(ax1, 'on'); hold(ax1, 'on');
    h1 = surf(ax1, X*1e9, Y*1e9, abs(Psi_res).^2 * 1e-18, 'EdgeColor', 'none');
    draw_barrier_slabs(ax1, x_b1_start*1e9, x_b1_end*1e9, x_b2_start*1e9, x_b2_end*1e9, 0.05, 7);
    zlim(ax1, [0, 0.055]); xlim(ax1, [-16, 16]); ylim(ax1, [-7, 7]);
    title(ax1, sprintf('RESONANT CASE (E = %.3f eV)\nHigh Tunneling & Well Cavity Resonator', E_res_eV), ...
          'Color', [0.3 1.0 0.5], 'FontSize', 12, 'FontWeight', 'bold');
    xlabel(ax1, 'x [nm]', 'Color', 'w'); ylabel(ax1, 'y [nm]', 'Color', 'w'); zlabel(ax1, '|\Psi|^2', 'Color', 'w');
    colormap(ax1, turbo(256));

    % Subplot 2: Off-resonant
    ax2 = subplot(1, 2, 2, 'Parent', fig);
    set(ax2, 'Color', [0.12 0.14 0.18], 'XColor', 'w', 'YColor', 'w', 'ZColor', 'w');
    view(ax2, -38, 45); grid(ax2, 'on'); hold(ax2, 'on');
    h2 = surf(ax2, X*1e9, Y*1e9, abs(Psi_off).^2 * 1e-18, 'EdgeColor', 'none');
    draw_barrier_slabs(ax2, x_b1_start*1e9, x_b1_end*1e9, x_b2_start*1e9, x_b2_end*1e9, 0.05, 7);
    zlim(ax2, [0, 0.055]); xlim(ax2, [-16, 16]); ylim(ax2, [-7, 7]);
    title(ax2, sprintf('OFF-RESONANT CASE (E = %.3f eV)\nTotal Quantum Reflection at Barrier 1', E_off_eV), ...
          'Color', [1.0 0.4 0.4], 'FontSize', 12, 'FontWeight', 'bold');
    xlabel(ax2, 'x [nm]', 'Color', 'w'); ylabel(ax2, 'y [nm]', 'Color', 'w'); zlabel(ax2, '|\Psi|^2', 'Color', 'w');
    colormap(ax2, turbo(256));

    for step = 1:N_steps
        % Step Resonant
        Psi_res = U_V_half .* Psi_res;
        P_k = U_K .* fft2(Psi_res);
        Psi_res = U_V_half .* ifft2(P_k);

        % Step Off-Resonant
        Psi_off = U_V_half .* Psi_off;
        P_k2 = U_K .* fft2(Psi_off);
        Psi_off = U_V_half .* ifft2(P_k2);

        if mod(step, 2) == 0 && isvalid(fig)
            dens_res = abs(Psi_res).^2 * 1e-18;
            dens_off = abs(Psi_off).^2 * 1e-18;
            set(h1, 'ZData', dens_res, 'CData', dens_res);
            set(h2, 'ZData', dens_off, 'CData', dens_off);
            drawnow limitrate;
        end
    end
end

% -------------------------------------------------------------------------
% Helper: Draw semi-transparent 3D slabs representing double barrier walls
% -------------------------------------------------------------------------
function draw_barrier_slabs(ax, b1_x1, b1_x2, b2_x1, b2_x2, z_height, y_span)
    % Barrier 1 Slab
    patch(ax, [b1_x1 b1_x2 b1_x2 b1_x1], [-y_span -y_span y_span y_span], ...
          [0 0 0 0], [0.8 0.2 0.2], 'FaceAlpha', 0.25, 'EdgeColor', [1 0.3 0.3], 'LineWidth', 1.2);
    patch(ax, [b1_x1 b1_x2 b1_x2 b1_x1], [-y_span -y_span y_span y_span], ...
          [z_height z_height z_height z_height], [0.8 0.2 0.2], 'FaceAlpha', 0.25, 'EdgeColor', [1 0.3 0.3], 'LineWidth', 1.2);
    patch(ax, [b1_x1 b1_x1 b1_x2 b1_x2], [-y_span -y_span -y_span -y_span], ...
          [0 z_height z_height 0], [0.8 0.2 0.2], 'FaceAlpha', 0.20, 'EdgeColor', [1 0.3 0.3]);

    % Barrier 2 Slab
    patch(ax, [b2_x1 b2_x2 b2_x2 b2_x1], [-y_span -y_span y_span y_span], ...
          [0 0 0 0], [0.8 0.2 0.2], 'FaceAlpha', 0.25, 'EdgeColor', [1 0.3 0.3], 'LineWidth', 1.2);
    patch(ax, [b2_x1 b2_x2 b2_x2 b2_x1], [-y_span -y_span y_span y_span], ...
          [z_height z_height z_height z_height], [0.8 0.2 0.2], 'FaceAlpha', 0.25, 'EdgeColor', [1 0.3 0.3], 'LineWidth', 1.2);
    patch(ax, [b2_x1 b2_x1 b2_x2 b2_x2], [-y_span -y_span -y_span -y_span], ...
          [0 z_height z_height 0], [0.8 0.2 0.2], 'FaceAlpha', 0.20, 'EdgeColor', [1 0.3 0.3]);
end
