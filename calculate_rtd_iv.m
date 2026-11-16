function [iv_data] = calculate_rtd_iv(geom, options)
% CALCULATE_RTD_IV - Computes I-V Characteristic for Resonant Tunnelling Diode (RTD)
%
% Syntax:
%   iv_data = calculate_rtd_iv(geom)
%   iv_data = calculate_rtd_iv(geom, options)
%
% Inputs:
%   geom    - Double-barrier geometry structure (V0, Lb, Lw, m_eff_well, etc.)
%   options - Optional configuration structure:
%               .V_min     - Minimum bias voltage [V] (default: 0)
%               .V_max     - Maximum bias voltage [V] (default: 0.35)
%               .nV        - Number of bias voltage sample points (default: 60)
%               .nE        - Number of energy points per bias (default: 120)
%               .Temp_K    - Temperature [K] (default: 300)
%               .E_Fermi   - Emitter Fermi level [eV] (default: 0.04)
%               .Area_um2  - Device active junction area [um^2] (default: 10)
%
% Outputs:
%   iv_data - Structure containing:
%               .V       - Voltage array [V]
%               .J       - Current density [A/cm^2]
%               .I_mA    - Total diode current [mA]
%               .V_peak  - Peak voltage [V]
%               .J_peak  - Peak current density [A/cm^2]
%               .V_valley- Valley voltage [V]
%               .J_valley- Valley current density [A/cm^2]
%               .PVCR    - Peak-to-Valley Current Ratio (J_peak / J_valley)
%               .is_ndr  - Logical vector identifying Negative Differential Resistance region
%
% Theory:
%   Uses the Tsu-Esaki formula integrating transmission T(E, V) against
%   the Fermi-Dirac supply function in longitudinal and transverse directions.

    if nargin < 2, options = struct(); end

    % Physical constants
    hbar = 1.054571817e-34;  % J*s
    m0   = 9.1093837015e-31;  % kg
    e_ch = 1.602176634e-19;  % C
    kB   = 1.380649e-23;      % J/K

    % Default options
    if ~isfield(options, 'V_min'),    options.V_min = 0.0; end
    if ~isfield(options, 'V_max'),    options.V_max = 0.35; end
    if ~isfield(options, 'nV'),       options.nV = 50; end
    if ~isfield(options, 'nE'),       options.nE = 120; end
    if ~isfield(options, 'Temp_K'),   options.Temp_K = 300.0; end
    if ~isfield(options, 'E_Fermi'),  options.E_Fermi = 0.04; end  % 40 meV
    if ~isfield(options, 'Area_um2'), options.Area_um2 = 10.0; end % 10 um^2

    T_K = options.Temp_K;
    kBT = kB * T_K;
    EF_J = options.E_Fermi * e_ch;
    m_well = (geom.m_eff_well) * m0;

    % Tsu-Esaki prefactor J0 = (e * m* * kB * T) / (2 * pi^2 * hbar^3)
    J0 = (e_ch * m_well * kBT) / (2 * pi^2 * hbar^3);

    V_vec = linspace(options.V_min, options.V_max, options.nV);
    J_vec = zeros(1, options.nV);

    % Energy integration grid
    E_max_eV = max(geom.V0 * 1.1, options.E_Fermi + 0.25);
    E_eV_grid = linspace(0.0005, E_max_eV, options.nE);
    dE_J = (E_eV_grid(2) - E_eV_grid(1)) * e_ch;
    E_J_grid = E_eV_grid * e_ch;

    for iv = 1:options.nV
        V_a = V_vec(iv);
        if V_a == 0
            J_vec(iv) = 0;
            continue;
        end

        geom_bias = geom;
        geom_bias.V_bias = V_a;

        % Compute transmission T(E) for this bias
        T_E = calculate_tmm(E_eV_grid, geom_bias);

        % Fermi-Dirac supply function S(E, V) = ln( (1 + exp((EF - E)/kBT)) / (1 + exp((EF - E - eV)/kBT)) )
        arg_emit = (EF_J - E_J_grid) / kBT;
        arg_coll = (EF_J - E_J_grid - e_ch * V_a) / kBT;

        % Numerically robust log-sum-exp evaluation
        s_emit = log1p_exp(arg_emit);
        s_coll = log1p_exp(arg_coll);
        supply = s_emit - s_coll;

        % Integrate over electron energies
        integrand = T_E .* supply;
        J_vec(iv) = J0 * trapz(E_J_grid, integrand);
    end

    % Convert J from A/m^2 to A/cm^2
    J_A_cm2 = J_vec * 1e-4;

    % Total device current in mA: I = J * Area
    Area_cm2 = options.Area_um2 * 1e-8;
    I_mA = J_A_cm2 * Area_cm2 * 1e3;

    % Analyze Peak, Valley, and Negative Differential Resistance (NDR)
    iv_data.V = V_vec;
    iv_data.J = J_A_cm2;
    iv_data.I_mA = I_mA;

    % Differential conductance dJ/dV
    dJ_dV = gradient(J_A_cm2, V_vec);
    iv_data.dJ_dV = dJ_dV;
    iv_data.is_ndr = (dJ_dV < 0);

    % Detect Peak and Valley
    [J_p, idx_p] = max(J_A_cm2);
    iv_data.V_peak = V_vec(idx_p);
    iv_data.J_peak = J_p;
    iv_data.I_peak_mA = I_mA(idx_p);

    % Look for valley after peak
    if idx_p < length(V_vec)
        [J_v, rel_idx_v] = min(J_A_cm2(idx_p:end));
        idx_v = idx_p + rel_idx_v - 1;
        iv_data.V_valley = V_vec(idx_v);
        iv_data.J_valley = J_v;
        iv_data.I_valley_mA = I_mA(idx_v);
        iv_data.PVCR = J_p / max(1e-6, J_v);
    else
        iv_data.V_valley = NaN;
        iv_data.J_valley = NaN;
        iv_data.I_valley_mA = NaN;
        iv_data.PVCR = 1.0;
    end
end

function val = log1p_exp(x)
    % Numerically stable computation of ln(1 + exp(x))
    val = zeros(size(x));
    idx_large = (x > 35);
    idx_small = (x < -35);
    idx_mid   = ~idx_large & ~idx_small;

    val(idx_large) = x(idx_large);
    val(idx_small) = exp(x(idx_small));
    val(idx_mid)   = log(1 + exp(x(idx_mid)));
end
