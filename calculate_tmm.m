function [T, R, sim_data] = calculate_tmm(E_eV, geom, calc_psi)
% CALCULATE_TMM - Transfer Matrix Method for Resonant Tunnelling in Double Barriers
%
% Syntax:
%   [T, R] = calculate_tmm(E_eV, geom)
%   [T, R, sim_data] = calculate_tmm(E_eV, geom, calc_psi)
%
% Inputs:
%   E_eV      - Vector or scalar of incident electron energies [eV]
%   geom      - Structure defining the double-barrier geometry:
%                 .V0         - Barrier height [eV]
%                 .Lb         - Barrier thickness [nm]
%                 .Lw         - Quantum well width [nm]
%                 .V_bias     - Applied bias voltage [V] (default: 0)
%                 .m_eff_well - Effective mass in well & leads (default: 0.067)
%                 .m_eff_barr - Effective mass in barrier (default: 0.092)
%                 .n_slices   - Number of spatial slices (default: 100)
%                 .L_contact  - Lead length to visualize [nm] (default: 5)
%   calc_psi  - Boolean flag (true/false) to compute wave function profile
%
% Outputs:
%   T         - Transmission probability vector
%   R         - Reflection probability vector (R = 1 - T)
%   sim_data  - Struct with spatial grids:
%                 .x            - Spatial grid [nm]
%                 .V_x          - Potential energy profile [eV]
%                 .psi          - Spatially resolved wave function (complex)
%                 .prob_density - Probability density |psi(x)|^2
%
% Physics:
%   Solves the 1D stationary Schrödinger equation with position-dependent
%   effective mass using the BenDaniel-Duke boundary conditions:
%   psi(x) and (1/m*(x)) * dpsi/dx are continuous across all interfaces.

    if nargin < 3
        calc_psi = false;
    end

    % Physical constants
    hbar = 1.054571817e-34;  % J*s
    m0   = 9.1093837015e-31;  % kg (electron bare mass)
    e_ch = 1.602176634e-19;  % C (elementary charge)

    % Default parameters if not specified
    if ~isfield(geom, 'V_bias'),     geom.V_bias = 0; end
    if ~isfield(geom, 'm_eff_well'), geom.m_eff_well = 0.067; end
    if ~isfield(geom, 'm_eff_barr'), geom.m_eff_barr = 0.092; end
    if ~isfield(geom, 'n_slices'),   geom.n_slices = 100; end
    if ~isfield(geom, 'L_contact'),  geom.L_contact = 5.0; end

    V0_J     = geom.V0 * e_ch;
    V_bias_J = geom.V_bias * e_ch;
    Lb_m     = geom.Lb * 1e-9;
    Lw_m     = geom.Lw * 1e-9;
    Lc_m     = geom.L_contact * 1e-9;
    L_active = 2 * Lb_m + Lw_m;

    m_well = geom.m_eff_well * m0;
    m_barr = geom.m_eff_barr * m0;

    % Discretize the active double-barrier region (from x = 0 to x = L_active)
    N_slices = max(60, geom.n_slices);
    dx = L_active / N_slices;
    x_slices = ((1:N_slices) - 0.5) * dx;

    % Determine potential V(x) and effective mass m*(x) in each slice
    V_slice = zeros(1, N_slices);
    m_slice = zeros(1, N_slices);

    for j = 1:N_slices
        xj = x_slices(j);
        if xj < Lb_m
            % First barrier
            V_flat = V0_J;
            m_slice(j) = m_barr;
        elseif xj < (Lb_m + Lw_m)
            % Quantum well
            V_flat = 0.0;
            m_slice(j) = m_well;
        else
            % Second barrier
            V_flat = V0_J;
            m_slice(j) = m_barr;
        end
        % Linear voltage drop across the active region
        V_slice(j) = V_flat - V_bias_J * (xj / L_active);
    end

    % Left lead (Emitter, x <= 0) and Right lead (Collector, x >= L_active)
    V_L = 0.0;
    m_L = m_well;
    V_R = -V_bias_J;
    m_R = m_well;

    nE = length(E_eV);
    T = zeros(1, nE);
    R = zeros(1, nE);

    % Main Transfer Matrix loop over energies
    for i = 1:nE
        E_J = E_eV(i) * e_ch;
        if E_J <= 0
            T(i) = 0;
            R(i) = 1;
            continue;
        end

        % Asymptotic wave vectors in the leads
        k_L = sqrt(2 * m_L * (E_J - V_L)) / hbar;
        k_R = sqrt(complex(2 * m_R * (E_J - V_R))) / hbar;

        alpha_L = 1i * k_L / m_L;
        alpha_R = 1i * k_R / m_R;

        % Total characteristic transfer matrix M = M_N * ... * M_1
        M = eye(2);
        for j = 1:N_slices
            kj = sqrt(complex(2 * m_slice(j) * (E_J - V_slice(j)))) / hbar;
            cos_kd = cos(kj * dx);
            if abs(kj) < 1e-12
                sinc_kd = dx;
            else
                sinc_kd = sin(kj * dx) / kj;
            end

            Mj = [cos_kd,                 m_slice(j) * sinc_kd; ...
                  -(kj^2 / m_slice(j)) * sinc_kd, cos_kd];

            M = Mj * M;
        end

        % Invert M total
        detM = M(1,1)*M(2,2) - M(1,2)*M(2,1);
        invM = [M(2,2), -M(1,2); -M(2,1), M(1,1)] / detM;

        u1 = invM(1,1) + invM(1,2) * alpha_R;
        u2 = invM(2,1) + invM(2,2) * alpha_R;

        t_coeff = (2 * alpha_L) / (alpha_L * u1 + u2);
        r_coeff = t_coeff * u1 - 1;

        % Transmission is ratio of transmitted probability current to incident
        if real(k_L) > 0
            T(i) = real( (real(k_R) / m_R) / (k_L / m_L) ) * abs(t_coeff)^2;
            R(i) = abs(r_coeff)^2;
        else
            T(i) = 0;
            R(i) = 1;
        end
        % Numerical clamp for stability
        T(i) = max(0, min(1, T(i)));
        R(i) = max(0, min(1, R(i)));
    end

    % If wave function calculation is requested (at the first or scalar energy)
    if calc_psi || nargout >= 3
        E_single_J = E_eV(1) * e_ch;
        k_L = sqrt(2 * m_L * (E_single_J - V_L)) / hbar;
        k_R = sqrt(complex(2 * m_R * (E_single_J - V_R))) / hbar;
        alpha_L = 1i * k_L / m_L;
        alpha_R = 1i * k_R / m_R;

        % Recompute M and slice matrices
        M_store = zeros(2, 2, N_slices);
        M = eye(2);
        for j = 1:N_slices
            kj = sqrt(complex(2 * m_slice(j) * (E_single_J - V_slice(j)))) / hbar;
            cos_kd = cos(kj * dx);
            if abs(kj) < 1e-12
                sinc_kd = dx;
            else
                sinc_kd = sin(kj * dx) / kj;
            end
            Mj = [cos_kd,                 m_slice(j) * sinc_kd; ...
                  -(kj^2 / m_slice(j)) * sinc_kd, cos_kd];
            M_store(:,:,j) = Mj;
            M = Mj * M;
        end

        detM = M(1,1)*M(2,2) - M(1,2)*M(2,1);
        invM = [M(2,2), -M(1,2); -M(2,1), M(1,1)] / detM;
        u1 = invM(1,1) + invM(1,2) * alpha_R;
        u2 = invM(2,1) + invM(2,2) * alpha_R;
        t_coeff = (2 * alpha_L) / (alpha_L * u1 + u2);
        r_coeff = t_coeff * u1 - 1;

        % Construct complete spatial coordinate grid (Left lead + Active + Right lead)
        Nx_contact = 50;
        x_left = linspace(-Lc_m, 0, Nx_contact);
        x_right = linspace(L_active, L_active + Lc_m, Nx_contact);

        % Wave function in left lead: psi_L(x) = exp(i*k_L*x) + r*exp(-i*k_L*x)
        psi_left = exp(1i * k_L * x_left) + r_coeff * exp(-1i * k_L * x_left);
        V_left = zeros(size(x_left));

        % Wave function in right lead: psi_R(x) = t * exp(i*k_R*(x - L_active))
        psi_right = t_coeff * exp(1i * k_R * (x_right - L_active));
        V_right = -geom.V_bias * ones(size(x_right));

        % State vector at x = 0: [psi(0); (1/m)*dpsi(0)/dx]
        state = [1 + r_coeff; alpha_L * (1 - r_coeff)];
        psi_active = zeros(1, N_slices);
        for j = 1:N_slices
            state = M_store(:,:,j) * state;
            psi_active(j) = state(1);
        end

        % Concatenate total profile
        sim_data.x_nm = [x_left, x_slices, x_right] * 1e9;
        sim_data.V_eV = [V_left, V_slice / e_ch, V_right];
        sim_data.psi  = [psi_left, psi_active, psi_right];
        sim_data.prob_density = abs(sim_data.psi).^2;
        sim_data.E_eV = E_eV(1);
        sim_data.T    = T(1);
        sim_data.R    = R(1);
        sim_data.r_coeff = r_coeff;
        sim_data.t_coeff = t_coeff;
    end
end
