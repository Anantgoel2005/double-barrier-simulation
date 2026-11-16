function rtd_3d_landscape(geom)
% RTD_3D_LANDSCAPE - 3D Energy Landscapes and Transmission Surfaces
%
% Generates publication-ready 3D surface plots for Resonant Tunnelling:
%   1. 3D Transmission Surface T(E, Lw) showing how quantum well width controls
%      the bound state energy levels and creates multiple resonant channels.
%   2. 3D Transmission Surface T(E, V_bias) showing resonance Stark shifts
%      under applied electric fields.
%   3. 3D Heterostructure & Resonant Wavefunction profile |psi(x, y)|^2.
%
% Syntax:
%   rtd_3d_landscape()
%   rtd_3d_landscape(geom)

    if nargin < 1 || isempty(geom)
        geom.V0 = 0.30;       % eV
        geom.Lb = 3.0;        % nm
        geom.Lw = 5.0;        % nm
        geom.V_bias = 0.0;    % V
        geom.m_eff_well = 0.067;
        geom.m_eff_barr = 0.092;
    end

    fig = figure('Name', '3D Resonant Tunnelling Landscapes', ...
                 'Color', 'w', 'Position', [80, 80, 1300, 750]);

    % ---------------------------------------------------------------------
    % Plot 1: 3D Surface of T(E, Lw) - Effect of Quantum Well Width
    % ---------------------------------------------------------------------
    ax1 = subplot(2, 2, 1, 'Parent', fig);
    fprintf('Computing 3D Landscape: T(E, Lw)...\n');
    nE = 120;
    nLw = 40;
    E_vec = linspace(0.005, geom.V0 * 1.05, nE);
    Lw_vec = linspace(2.0, 12.0, nLw); % Well width from 2 nm to 12 nm

    T_grid_Lw = zeros(nLw, nE);
    geom_temp = geom;
    for iL = 1:nLw
        geom_temp.Lw = Lw_vec(iL);
        T_grid_Lw(iL, :) = calculate_tmm(E_vec, geom_temp);
    end

    [EE1, LLw] = meshgrid(E_vec, Lw_vec);
    surf(ax1, EE1, LLw, T_grid_Lw, 'EdgeColor', 'none');
    shading(ax1, 'interp');
    colormap(ax1, turbo(256));
    view(ax1, -35, 52);
    grid(ax1, 'on');
    xlabel(ax1, 'Energy E [eV]', 'FontSize', 11, 'FontWeight', 'bold');
    ylabel(ax1, 'Well Width L_w [nm]', 'FontSize', 11, 'FontWeight', 'bold');
    zlabel(ax1, 'Transmission T(E)', 'FontSize', 11, 'FontWeight', 'bold');
    title(ax1, '3D Transmission Landscape: T(E, L_w)', 'FontSize', 13, 'FontWeight', 'bold');
    cbar1 = colorbar(ax1);
    ylabel(cbar1, 'T(E)');

    % ---------------------------------------------------------------------
    % Plot 2: 3D Surface of T(E, V_bias) - Effect of Applied Diode Bias
    % ---------------------------------------------------------------------
    ax2 = subplot(2, 2, 2, 'Parent', fig);
    fprintf('Computing 3D Landscape: T(E, V_bias)...\n');
    nV = 40;
    V_vec = linspace(0.0, 0.35, nV); % Bias from 0 to 0.35 V
    T_grid_V = zeros(nV, nE);

    geom_bias = geom;
    for iv = 1:nV
        geom_bias.V_bias = V_vec(iv);
        T_grid_V(iv, :) = calculate_tmm(E_vec, geom_bias);
    end

    [EE2, VV] = meshgrid(E_vec, V_vec);
    surf(ax2, EE2, VV, T_grid_V, 'EdgeColor', 'none');
    shading(ax2, 'interp');
    view(ax2, -35, 52);
    grid(ax2, 'on');
    xlabel(ax2, 'Energy E [eV]', 'FontSize', 11, 'FontWeight', 'bold');
    ylabel(ax2, 'Bias Voltage V_{bias} [V]', 'FontSize', 11, 'FontWeight', 'bold');
    zlabel(ax2, 'Transmission T(E)', 'FontSize', 11, 'FontWeight', 'bold');
    title(ax2, '3D Stark Shift: T(E, V_{bias})', 'FontSize', 13, 'FontWeight', 'bold');
    cbar2 = colorbar(ax2);
    ylabel(cbar2, 'T(E)');

    % ---------------------------------------------------------------------
    % Plot 3: 3D Heterostructure Potential & Resonant Wavefunction Density
    % ---------------------------------------------------------------------
    ax3 = subplot(2, 2, [3, 4], 'Parent', fig);
    fprintf('Computing 3D Wavefunction Profile at Resonance...\n');

    % Find the fundamental resonance
    T_zero = calculate_tmm(E_vec, geom);
    [pks, locs] = find_resonance_peaks(T_zero, E_vec);
    if ~isempty(pks)
        [~, mp_idx] = max(pks);
        E_res = locs(mp_idx);
    else
        E_res = 0.088;
    end

    [~, ~, sim_res] = calculate_tmm(E_res, geom, true);
    x_nm = sim_res.x_nm;
    V_profile = sim_res.V_eV;
    prob_dens = sim_res.prob_density;

    % Extrude along transverse y direction for 3D visualization
    y_nm = linspace(-6, 6, 40);
    [X_3D, Y_3D] = meshgrid(x_nm, y_nm);
    V_3D = repmat(V_profile, length(y_nm), 1);
    Psi_3D = repmat(prob_dens, length(y_nm), 1) .* exp(- (Y_3D / 3.0).^2);

    % Render Potential Barrier Walls as 3D surface
    surf(ax3, X_3D, Y_3D, V_3D, 'FaceAlpha', 0.35, 'EdgeColor', 'none');
    hold(ax3, 'on');

    % Render Wavefunction Standing Wave Probability Density as elevated 3D surface
    % Offset by energy level E_res
    surf_psi = surf(ax3, X_3D, Y_3D, E_res + 0.08 * (Psi_3D / max(prob_dens)), ...
                    'FaceAlpha', 0.85, 'EdgeColor', 'none');
    shading(ax3, 'interp');

    % Add line indicating resonance energy
    plot3(ax3, x_nm, zeros(size(x_nm)), E_res * ones(size(x_nm)), ...
          'r--', 'LineWidth', 2.0);

    view(ax3, -42, 38);
    grid(ax3, 'on');
    xlabel(ax3, 'Transport Coordinate x [nm]', 'FontSize', 11, 'FontWeight', 'bold');
    ylabel(ax3, 'Transverse Coordinate y [nm]', 'FontSize', 11, 'FontWeight', 'bold');
    zlabel(ax3, 'Energy [eV]', 'FontSize', 11, 'FontWeight', 'bold');
    title(ax3, sprintf('3D Heterostructure: Double Barrier Potential & Resonant Wavefunction Cavity (E_r = %.3f eV)', E_res), ...
          'FontSize', 13, 'FontWeight', 'bold');
    zlim(ax3, [-0.05, geom.V0 * 1.3]);

    % Add legend annotations
    text(ax3, x_nm(1), 0, E_res + 0.03, sprintf('E_{res} = %.3f eV', E_res), ...
         'Color', 'r', 'FontWeight', 'bold', 'FontSize', 11);

    fprintf('3D Landscapes successfully generated.\n');
end
