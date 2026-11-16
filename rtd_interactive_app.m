function rtd_interactive_app()
% RTD_INTERACTIVE_APP - Interactive GUI for Resonant Tunnelling & RTD Diode
%
% Complete interactive laboratory for double barrier resonant tunnelling:
%   - Sliders to adjust Barrier Height (V0), Barrier Thickness (Lb),
%     and Quantum Well Width (Lw).
%   - Applied Bias slider to demonstrate band tilting and diode operation.
%   - Transmission spectrum T(E) with resonance detection.
%   - Resonant Tunneling Diode I-V curve with Negative Differential Resistance (NDR).
%   - Real-time 2D and 3D visualization of the quantum wavefunction.
%   - Buttons to launch full 3D time-dependent wavepacket dynamic simulations.
%
% Syntax:
%   rtd_interactive_app

    % Setup main figure
    fig = figure('Name', 'Resonant Tunnelling in Double Barrier & Diode Simulation', ...
                 'NumberTitle', 'off', ...
                 'Color', [0.95 0.96 0.98], ...
                 'Position', [50, 50, 1350, 800], ...
                 'MenuBar', 'figure', ...
                 'ToolBar', 'figure');

    % Default physics state
    state.V0 = 0.30;       % eV
    state.Lb = 3.0;        % nm
    state.Lw = 5.0;        % nm
    state.V_bias = 0.0;    % V
    state.E_inc = 0.088;   % eV (default incident energy)
    state.m_eff_well = 0.067;
    state.m_eff_barr = 0.092;
    state.view_mode_3d = false;
    state.iv_cache = [];
    state.need_iv_recalc = true;

    % Create UI Panels
    panel_ctrl = uipanel('Parent', fig, 'Title', 'Control Parameters', ...
                         'FontSize', 11, 'FontWeight', 'bold', ...
                         'BackgroundColor', [0.92 0.94 0.96], ...
                         'Position', [0.015, 0.02, 0.28, 0.95]);

    panel_disp = uipanel('Parent', fig, 'Title', 'Quantum Transport & RTD Dashboard', ...
                         'FontSize', 11, 'FontWeight', 'bold', ...
                         'BackgroundColor', 'w', ...
                         'Position', [0.305, 0.02, 0.68, 0.95]);

    % Create Axes inside Display Panel
    ax_pot = axes('Parent', panel_disp, 'Position', [0.08, 0.55, 0.40, 0.38]);
    ax_trans = axes('Parent', panel_disp, 'Position', [0.56, 0.55, 0.40, 0.38]);
    ax_iv = axes('Parent', panel_disp, 'Position', [0.08, 0.08, 0.40, 0.38]);
    ax_info = axes('Parent', panel_disp, 'Position', [0.56, 0.08, 0.40, 0.38]);
    axis(ax_info, 'off');

    % ---------------------------------------------------------------------
    % Add Slider & Label Controls to Panel
    % ---------------------------------------------------------------------
    y_pos = 0.90;
    dy = 0.12;

    % 1. Barrier Height V0
    uicontrol('Parent', panel_ctrl, 'Style', 'text', 'String', 'Barrier Height V0 [eV]:', ...
              'Units', 'normalized', 'Position', [0.05, y_pos, 0.60, 0.04], ...
              'BackgroundColor', [0.92 0.94 0.96], 'HorizontalAlignment', 'left', 'FontWeight', 'bold');
    txt_V0 = uicontrol('Parent', panel_ctrl, 'Style', 'text', 'String', sprintf('%.2f eV', state.V0), ...
                       'Units', 'normalized', 'Position', [0.68, y_pos, 0.28, 0.04], ...
                       'BackgroundColor', 'w', 'FontWeight', 'bold');
    sld_V0 = uicontrol('Parent', panel_ctrl, 'Style', 'slider', ...
                       'Min', 0.10, 'Max', 1.20, 'Value', state.V0, ...
                       'Units', 'normalized', 'Position', [0.05, y_pos - 0.04, 0.90, 0.035]);

    % 2. Barrier Thickness Lb
    y_pos = y_pos - dy;
    uicontrol('Parent', panel_ctrl, 'Style', 'text', 'String', 'Barrier Thickness Lb [nm]:', ...
              'Units', 'normalized', 'Position', [0.05, y_pos, 0.60, 0.04], ...
              'BackgroundColor', [0.92 0.94 0.96], 'HorizontalAlignment', 'left', 'FontWeight', 'bold');
    txt_Lb = uicontrol('Parent', panel_ctrl, 'Style', 'text', 'String', sprintf('%.2f nm', state.Lb), ...
                       'Units', 'normalized', 'Position', [0.68, y_pos, 0.28, 0.04], ...
                       'BackgroundColor', 'w', 'FontWeight', 'bold');
    sld_Lb = uicontrol('Parent', panel_ctrl, 'Style', 'slider', ...
                       'Min', 1.0, 'Max', 8.0, 'Value', state.Lb, ...
                       'Units', 'normalized', 'Position', [0.05, y_pos - 0.04, 0.90, 0.035]);

    % 3. Well Width Lw
    y_pos = y_pos - dy;
    uicontrol('Parent', panel_ctrl, 'Style', 'text', 'String', 'Quantum Well Width Lw [nm]:', ...
              'Units', 'normalized', 'Position', [0.05, y_pos, 0.60, 0.04], ...
              'BackgroundColor', [0.92 0.94 0.96], 'HorizontalAlignment', 'left', 'FontWeight', 'bold');
    txt_Lw = uicontrol('Parent', panel_ctrl, 'Style', 'text', 'String', sprintf('%.2f nm', state.Lw), ...
                       'Units', 'normalized', 'Position', [0.68, y_pos, 0.28, 0.04], ...
                       'BackgroundColor', 'w', 'FontWeight', 'bold');
    sld_Lw = uicontrol('Parent', panel_ctrl, 'Style', 'slider', ...
                       'Min', 2.0, 'Max', 12.0, 'Value', state.Lw, ...
                       'Units', 'normalized', 'Position', [0.05, y_pos - 0.04, 0.90, 0.035]);

    % 4. Applied Diode Bias V_bias
    y_pos = y_pos - dy;
    uicontrol('Parent', panel_ctrl, 'Style', 'text', 'String', 'Applied Diode Bias Va [V]:', ...
              'Units', 'normalized', 'Position', [0.05, y_pos, 0.60, 0.04], ...
              'BackgroundColor', [0.92 0.94 0.96], 'HorizontalAlignment', 'left', 'FontWeight', 'bold');
    txt_Va = uicontrol('Parent', panel_ctrl, 'Style', 'text', 'String', sprintf('%.3f V', state.V_bias), ...
                       'Units', 'normalized', 'Position', [0.68, y_pos, 0.28, 0.04], ...
                       'BackgroundColor', 'w', 'FontWeight', 'bold');
    sld_Va = uicontrol('Parent', panel_ctrl, 'Style', 'slider', ...
                       'Min', 0.0, 'Max', 0.35, 'Value', state.V_bias, ...
                       'Units', 'normalized', 'Position', [0.05, y_pos - 0.04, 0.90, 0.035]);

    % 5. Incident Electron Energy E
    y_pos = y_pos - dy;
    uicontrol('Parent', panel_ctrl, 'Style', 'text', 'String', 'Incident Energy E [eV]:', ...
              'Units', 'normalized', 'Position', [0.05, y_pos, 0.60, 0.04], ...
              'BackgroundColor', [0.92 0.94 0.96], 'HorizontalAlignment', 'left', 'FontWeight', 'bold');
    txt_E = uicontrol('Parent', panel_ctrl, 'Style', 'text', 'String', sprintf('%.3f eV', state.E_inc), ...
                      'Units', 'normalized', 'Position', [0.68, y_pos, 0.28, 0.04], ...
                      'BackgroundColor', 'w', 'FontWeight', 'bold');
    sld_E = uicontrol('Parent', panel_ctrl, 'Style', 'slider', ...
                      'Min', 0.005, 'Max', 0.60, 'Value', state.E_inc, ...
                      'Units', 'normalized', 'Position', [0.05, y_pos - 0.04, 0.90, 0.035]);

    % Action Buttons
    y_pos = y_pos - 0.07;
    btn_snap = uicontrol('Parent', panel_ctrl, 'Style', 'pushbutton', ...
                         'String', 'Auto-Snap to Resonant Peak', ...
                         'Units', 'normalized', 'Position', [0.05, y_pos, 0.90, 0.045], ...
                         'BackgroundColor', [0.3 0.7 0.9], 'ForegroundColor', 'w', ...
                         'FontWeight', 'bold', 'FontSize', 10);

    y_pos = y_pos - 0.06;
    btn_toggle3d = uicontrol('Parent', panel_ctrl, 'Style', 'togglebutton', ...
                             'String', 'Toggle 3D Wavefunction View', ...
                             'Units', 'normalized', 'Position', [0.05, y_pos, 0.90, 0.045], ...
                             'BackgroundColor', [0.8 0.85 0.9], 'FontWeight', 'bold');

    y_pos = y_pos - 0.06;
    btn_3d_wp = uicontrol('Parent', panel_ctrl, 'Style', 'pushbutton', ...
                          'String', 'Launch 3D Wavepacket TDSE', ...
                          'Units', 'normalized', 'Position', [0.05, y_pos, 0.90, 0.045], ...
                          'BackgroundColor', [0.2 0.75 0.4], 'ForegroundColor', 'w', ...
                          'FontWeight', 'bold', 'FontSize', 10);

    y_pos = y_pos - 0.06;
    btn_3d_land = uicontrol('Parent', panel_ctrl, 'Style', 'pushbutton', ...
                            'String', 'Launch 3D Energy Landscapes', ...
                            'Units', 'normalized', 'Position', [0.05, y_pos, 0.90, 0.045], ...
                            'BackgroundColor', [0.85 0.5 0.2], 'ForegroundColor', 'w', ...
                            'FontWeight', 'bold', 'FontSize', 10);

    % Connect Callbacks
    set(sld_V0, 'Callback', @cb_V0);
    set(sld_Lb, 'Callback', @cb_Lb);
    set(sld_Lw, 'Callback', @cb_Lw);
    set(sld_Va, 'Callback', @cb_Va);
    set(sld_E,  'Callback', @cb_E);
    set(btn_snap, 'Callback', @cb_snap);
    set(btn_toggle3d, 'Callback', @cb_toggle3d);
    set(btn_3d_wp, 'Callback', @cb_3d_wp);
    set(btn_3d_land, 'Callback', @cb_3d_land);

    % Initial update
    update_all();

    % =====================================================================
    % Callback Implementations
    % =====================================================================
    function cb_V0(src, ~)
        state.V0 = get(src, 'Value');
        set(txt_V0, 'String', sprintf('%.2f eV', state.V0));
        set(sld_E, 'Max', state.V0 * 1.5);
        state.need_iv_recalc = true;
        update_all();
    end

    function cb_Lb(src, ~)
        state.Lb = get(src, 'Value');
        set(txt_Lb, 'String', sprintf('%.2f nm', state.Lb));
        state.need_iv_recalc = true;
        update_all();
    end

    function cb_Lw(src, ~)
        state.Lw = get(src, 'Value');
        set(txt_Lw, 'String', sprintf('%.2f nm', state.Lw));
        state.need_iv_recalc = true;
        update_all();
    end

    function cb_Va(src, ~)
        state.V_bias = get(src, 'Value');
        set(txt_Va, 'String', sprintf('%.3f V', state.V_bias));
        update_all();
    end

    function cb_E(src, ~)
        state.E_inc = get(src, 'Value');
        set(txt_E, 'String', sprintf('%.3f eV', state.E_inc));
        update_wavefunction_and_spectrum_marker();
    end

    function cb_snap(~, ~)
        % Compute fine T(E) to find nearest peak
        E_fine = linspace(0.005, state.V0 * 1.05, 300);
        geom_cur = get_current_geom();
        T_fine = calculate_tmm(E_fine, geom_cur);
        [pks, locs] = find_resonance_peaks(T_fine, E_fine);
        if ~isempty(pks)
            % Find peak closest to current E_inc or dominant
            [~, closest_idx] = min(abs(locs - state.E_inc));
            state.E_inc = locs(closest_idx);
            set(sld_E, 'Value', state.E_inc);
            set(txt_E, 'String', sprintf('%.3f eV', state.E_inc));
            update_all();
        end
    end

    function cb_toggle3d(src, ~)
        state.view_mode_3d = get(src, 'Value');
        update_all();
    end

    function cb_3d_wp(~, ~)
        geom_cur = get_current_geom();
        rtd_3d_wavepacket('resonant', geom_cur);
    end

    function cb_3d_land(~, ~)
        geom_cur = get_current_geom();
        rtd_3d_landscape(geom_cur);
    end

    function geom = get_current_geom()
        geom.V0 = state.V0;
        geom.Lb = state.Lb;
        geom.Lw = state.Lw;
        geom.V_bias = state.V_bias;
        geom.m_eff_well = state.m_eff_well;
        geom.m_eff_barr = state.m_eff_barr;
    end

    % =====================================================================
    % Main Dashboard Render Function
    % =====================================================================
    function update_all()
        geom = get_current_geom();

        % 1. Compute Spectrum T(E)
        E_grid = linspace(0.002, state.V0 * 1.15, 250);
        T_grid = calculate_tmm(E_grid, geom);
        [pks, locs, w_fwhm] = find_resonance_peaks(T_grid, E_grid);

        % 2. Compute Wavefunction at state.E_inc
        [~, ~, sim_data] = calculate_tmm(state.E_inc, geom, true);

        % 3. Compute or reuse I-V curve
        if state.need_iv_recalc || isempty(state.iv_cache)
            opts.nV = 40;
            opts.nE = 90;
            opts.V_max = 0.35;
            state.iv_cache = calculate_rtd_iv(geom, opts);
            state.need_iv_recalc = false;
        end
        iv = state.iv_cache;

        % -----------------------------------------------------------------
        % Render Panel 1: Potential Profile & Wavefunction (2D or 3D)
        % -----------------------------------------------------------------
        cla(ax_pot);
        reset(ax_pot);
        if ~state.view_mode_3d
            % 2D Profile
            plot(ax_pot, sim_data.x_nm, sim_data.V_eV, 'k-', 'LineWidth', 2.5);
            hold(ax_pot, 'on'); grid(ax_pot, 'on');

            % Shade barriers
            fill(ax_pot, [0 state.Lb state.Lb 0], [0 0 state.V0 state.V0], ...
                 [0.9 0.7 0.7], 'EdgeColor', 'none', 'FaceAlpha', 0.4);
            x2_start = state.Lb + state.Lw;
            x2_end = x2_start + state.Lb;
            fill(ax_pot, [x2_start x2_end x2_end x2_start], [0 0 state.V0 state.V0], ...
                 [0.9 0.7 0.7], 'EdgeColor', 'none', 'FaceAlpha', 0.4);

            % Plot incident energy level
            yline(ax_pot, state.E_inc, 'r--', 'LineWidth', 1.5);

            % Plot quasi-bound states inside well
            for k = 1:length(locs)
                if locs(k) < state.V0
                    line(ax_pot, [state.Lb, state.Lb + state.Lw], [locs(k), locs(k)], ...
                         'Color', [0.2 0.6 0.2], 'LineWidth', 2.0, 'LineStyle', '-');
                end
            end

            % Plot probability density |psi(x)|^2 scaled
            scale_fac = 0.08 / max(1e-3, max(sim_data.prob_density));
            plot(ax_pot, sim_data.x_nm, state.E_inc + sim_data.prob_density * scale_fac, ...
                 'b-', 'LineWidth', 2.2);

            xlabel(ax_pot, 'Position x [nm]', 'FontWeight', 'bold');
            ylabel(ax_pot, 'Energy [eV]', 'FontWeight', 'bold');
            title(ax_pot, sprintf('Band Profile & |\\psi(x)|^2 (T = %.4f)', sim_data.T), ...
                  'FontSize', 11, 'FontWeight', 'bold');
            ylim(ax_pot, [-state.V_bias - 0.05, state.V0 * 1.25]);
            xlim(ax_pot, [sim_data.x_nm(1), sim_data.x_nm(end)]);
        else
            % 3D Extruded Heterostructure View
            y_nm = linspace(-5, 5, 30);
            [X3, Y3] = meshgrid(sim_data.x_nm, y_nm);
            V3 = repmat(sim_data.V_eV, length(y_nm), 1);
            scale_fac = 0.08 / max(1e-3, max(sim_data.prob_density));
            P3 = repmat(state.E_inc + sim_data.prob_density * scale_fac, length(y_nm), 1) .* exp(-(Y3/3).^2);

            surf(ax_pot, X3, Y3, V3, 'FaceAlpha', 0.35, 'EdgeColor', 'none');
            hold(ax_pot, 'on');
            surf(ax_pot, X3, Y3, P3, 'FaceAlpha', 0.85, 'EdgeColor', 'none');
            colormap(ax_pot, turbo(256));
            shading(ax_pot, 'interp');
            view(ax_pot, -38, 42); grid(ax_pot, 'on');
            xlabel(ax_pot, 'x [nm]'); ylabel(ax_pot, 'y [nm]'); zlabel(ax_pot, 'E [eV]');
            title(ax_pot, '3D Heterostructure & Wavefunction', 'FontSize', 11, 'FontWeight', 'bold');
        end

        % -----------------------------------------------------------------
        % Render Panel 2: Transmission Spectrum T(E)
        % -----------------------------------------------------------------
        cla(ax_trans);
        reset(ax_trans);
        plot(ax_trans, E_grid, T_grid, 'Color', [0.1 0.45 0.85], 'LineWidth', 2.2);
        hold(ax_trans, 'on'); grid(ax_trans, 'on');

        % Mark Resonance Peaks
        if ~isempty(pks)
            plot(ax_trans, locs, pks, 'ro', 'MarkerFaceColor', 'r', 'MarkerSize', 6);
            for ip = 1:length(pks)
                text(ax_trans, locs(ip), min(1.05, pks(ip) + 0.06), ...
                     sprintf('E_{%d}=%.3feV', ip, locs(ip)), ...
                     'FontSize', 9, 'FontWeight', 'bold', 'HorizontalAlignment', 'center');
            end
        end

        % Current energy operating line
        xline(ax_trans, state.E_inc, 'r--', 'LineWidth', 1.8);
        scatter(ax_trans, state.E_inc, sim_data.T, 60, 'r', 'filled');

        xlabel(ax_trans, 'Electron Energy E [eV]', 'FontWeight', 'bold');
        ylabel(ax_trans, 'Transmission T(E)', 'FontWeight', 'bold');
        title(ax_trans, 'Transmission Coefficient T(E)', 'FontSize', 11, 'FontWeight', 'bold');
        ylim(ax_trans, [0, 1.15]);
        xlim(ax_trans, [0, state.V0 * 1.15]);

        % -----------------------------------------------------------------
        % Render Panel 3: RTD I-V Characteristic Curve
        % -----------------------------------------------------------------
        cla(ax_iv);
        reset(ax_iv);
        plot(ax_iv, iv.V, iv.J, 'Color', [0.15 0.65 0.25], 'LineWidth', 2.4);
        hold(ax_iv, 'on'); grid(ax_iv, 'on');

        % Highlight NDR Region
        ndr_indices = find(iv.is_ndr);
        if ~isempty(ndr_indices)
            plot(ax_iv, iv.V(ndr_indices), iv.J(ndr_indices), 'r-', 'LineWidth', 3.2);
            fill(ax_iv, [iv.V_peak iv.V_valley iv.V_valley iv.V_peak], ...
                 [0 0 max(iv.J)*1.1 max(iv.J)*1.1], [1 0.85 0.85], ...
                 'EdgeColor', 'none', 'FaceAlpha', 0.35);
        end

        % Mark Peak and Valley
        if ~isnan(iv.V_peak)
            plot(ax_iv, iv.V_peak, iv.J_peak, 'ks', 'MarkerFaceColor', [1 0.5 0], 'MarkerSize', 8);
            text(ax_iv, iv.V_peak, iv.J_peak * 1.08, 'Peak (V_p, J_p)', ...
                 'FontSize', 9, 'FontWeight', 'bold');
        end
        if ~isnan(iv.V_valley)
            plot(ax_iv, iv.V_valley, iv.J_valley, 'kd', 'MarkerFaceColor', [0.7 0.2 0.9], 'MarkerSize', 8);
            text(ax_iv, iv.V_valley, iv.J_valley * 0.80, 'Valley (V_v, J_v)', ...
                 'FontSize', 9, 'FontWeight', 'bold');
        end

        % Current bias operating marker
        cur_J = interp1(iv.V, iv.J, state.V_bias, 'linear', 'extrap');
        plot(ax_iv, state.V_bias, cur_J, 'ro', 'MarkerFaceColor', 'r', 'MarkerSize', 8);
        xline(ax_iv, state.V_bias, 'k:', 'LineWidth', 1.5);

        xlabel(ax_iv, 'Applied Bias V_a [V]', 'FontWeight', 'bold');
        ylabel(ax_iv, 'Current Density J [A/cm^2]', 'FontWeight', 'bold');
        title(ax_iv, 'RTD Diode I-V Curve (NDR Region in Red)', 'FontSize', 11, 'FontWeight', 'bold');
        xlim(ax_iv, [0, max(iv.V)]);

        % -----------------------------------------------------------------
        % Render Panel 4: Physical Analysis & Readout
        % -----------------------------------------------------------------
        cla(ax_info);
        reset(ax_info);
        axis(ax_info, 'off');

        % Lifetime tau = hbar / Gamma
        if ~isempty(w_fwhm)
            gamma_eV = w_fwhm(1);
            tau_fs = (1.05457e-34 / (gamma_eV * 1.60218e-19)) * 1e15;
            tau_str = sprintf('%.1f fs', tau_fs);
            gamma_str = sprintf('%.4f eV', gamma_eV);
        else
            tau_str = 'N/A';
            gamma_str = 'N/A';
        end

        % Operating state string
        if state.V_bias < 0.01
            op_mode = 'Zero Bias (Thermal Equilibrium)';
            op_col = [0.2 0.2 0.7];
        elseif ~isnan(iv.V_peak) && abs(state.V_bias - iv.V_peak) < 0.02
            op_mode = 'RESONANT PEAK: Well level aligns with emitter Fermi sea!';
            op_col = [0.1 0.6 0.2];
        elseif ~isnan(iv.V_peak) && ~isnan(iv.V_valley) && state.V_bias > iv.V_peak && state.V_bias < iv.V_valley
            op_mode = 'NEGATIVE DIFFERENTIAL RESISTANCE (NDR Active!)';
            op_col = [0.8 0.1 0.1];
        elseif ~isnan(iv.V_valley) && state.V_bias >= iv.V_valley
            op_mode = 'VALLEY REGION: Level dropped below emitter conduction band';
            op_col = [0.5 0.1 0.6];
        else
            op_mode = 'Pre-Resonant Tunneling';
            op_col = [0.3 0.3 0.3];
        end

        str_lines = {
            '\bfPHYSICAL DEVICE METRICS & ANALYSIS:'
            '-------------------------------------------------------'
            sprintf('\\bullet \\bfBarrier Height (V_0):\\rm %.2f eV  |  \\bfThickness (L_b):\\rm %.2f nm', state.V0, state.Lb)
            sprintf('\\bullet \\bfQuantum Well Width (L_w):\\rm %.2f nm', state.Lw)
            sprintf('\\bullet \\bfFundamental Resonance (E_1):\\rm %s', ...
                    ternary(~isempty(locs), sprintf('%.4f eV', locs(1)), 'None'))
            sprintf('\\bullet \\bfResonance Width (\\Gamma / FWHM):\\rm %s', gamma_str)
            sprintf('\\bullet \\bfQuasi-Bound State Lifetime (\\tau):\\rm %s', tau_str)
            ' '
            '\bfRESONANT TUNNELLING DIODE (RTD) METRICS:'
            '-------------------------------------------------------'
            sprintf('\\bullet \\bfPeak Voltage (V_p):\\rm %.3f V', iv.V_peak)
            sprintf('\\bullet \\bfPeak Current Density (J_p):\\rm %.1f A/cm^2', iv.J_peak)
            sprintf('\\bullet \\bfValley Voltage (V_v):\\rm %.3f V', iv.V_valley)
            sprintf('\\bullet \\bfValley Current Density (J_v):\\rm %.1f A/cm^2', iv.J_valley)
            sprintf('\\bullet \\bfPeak-to-Valley Current Ratio (PVCR):\\rm %.2f', iv.PVCR)
            ' '
            sprintf('\\bfCURRENT STATUS:\\rm %s', op_mode)
        };

        text(ax_info, 0.02, 0.95, str_lines, 'FontSize', 10, 'VerticalAlignment', 'top');
    end

    function update_wavefunction_and_spectrum_marker()
        geom = get_current_geom();
        [~, ~, sim_data] = calculate_tmm(state.E_inc, geom, true);

        % Update 2D / 3D band plot
        if ~state.view_mode_3d
            cla(ax_pot);
            plot(ax_pot, sim_data.x_nm, sim_data.V_eV, 'k-', 'LineWidth', 2.5);
            hold(ax_pot, 'on'); grid(ax_pot, 'on');
            fill(ax_pot, [0 state.Lb state.Lb 0], [0 0 state.V0 state.V0], ...
                 [0.9 0.7 0.7], 'EdgeColor', 'none', 'FaceAlpha', 0.4);
            x2_start = state.Lb + state.Lw;
            x2_end = x2_start + state.Lb;
            fill(ax_pot, [x2_start x2_end x2_end x2_start], [0 0 state.V0 state.V0], ...
                 [0.9 0.7 0.7], 'EdgeColor', 'none', 'FaceAlpha', 0.4);

            yline(ax_pot, state.E_inc, 'r--', 'LineWidth', 1.5);
            scale_fac = 0.08 / max(1e-3, max(sim_data.prob_density));
            plot(ax_pot, sim_data.x_nm, state.E_inc + sim_data.prob_density * scale_fac, ...
                 'b-', 'LineWidth', 2.2);

            xlabel(ax_pot, 'Position x [nm]', 'FontWeight', 'bold');
            ylabel(ax_pot, 'Energy [eV]', 'FontWeight', 'bold');
            title(ax_pot, sprintf('Band Profile & |\\psi(x)|^2 (T = %.4f)', sim_data.T), ...
                  'FontSize', 11, 'FontWeight', 'bold');
            ylim(ax_pot, [-state.V_bias - 0.05, state.V0 * 1.25]);
            xlim(ax_pot, [sim_data.x_nm(1), sim_data.x_nm(end)]);
        end
    end

    function res = ternary(cond, a, b)
        if cond, res = a; else, res = b; end
    end
end
