import sys
import os
from pptx import Presentation
from pptx.util import Inches, Pt
from pptx.dml.color import RGBColor
from pptx.enum.text import PP_ALIGN
from pptx.enum.shapes import MSO_SHAPE

# -------------------------------------------------------------
# PRESENTATION INITIALIZATION (Widescreen 16:9)
# -------------------------------------------------------------
prs = Presentation()
prs.slide_width = Inches(13.333)
prs.slide_height = Inches(7.5)
blank_layout = prs.slide_layouts[6]  # Blank slide

# -------------------------------------------------------------
# COLOR PALETTE (Clean, Academic, Minimalist, Monochrome/Charcoal)
# -------------------------------------------------------------
C_BG = RGBColor(255, 255, 255)         # Pure White
C_CARD_BG = RGBColor(248, 249, 250)    # Soft Light Gray Card
C_BORDER = RGBColor(209, 213, 219)     # Subtle Gray Border
C_TITLE = RGBColor(17, 24, 39)         # Dark Charcoal / Black
C_BODY = RGBColor(31, 41, 55)          # Dark Slate Body
C_MUTED = RGBColor(107, 114, 128)      # Medium Gray Subtitle / Meta
C_ACCENT = RGBColor(31, 41, 55)        # Solid Graphite Accent
C_LINE = RGBColor(229, 231, 235)       # Divider Line

FONT_SERIF = "Times New Roman"
FONT_SANS = "Calibri"

def add_header(slide, title_text, category_text="ACADEMIC PROJECT REPORT", slide_num=None):
    """Draws a standardized academic header and footer on each content slide."""
    # Category / Super-title
    cat_box = slide.shapes.add_textbox(Inches(0.8), Inches(0.4), Inches(10), Inches(0.35))
    tf_c = cat_box.text_frame
    tf_c.word_wrap = True
    tf_c.margin_left = tf_c.margin_top = tf_c.margin_right = tf_c.margin_bottom = 0
    p_c = tf_c.paragraphs[0]
    p_c.text = category_text.upper()
    p_c.font.name = FONT_SANS
    p_c.font.size = Pt(9.5)
    p_c.font.bold = True
    p_c.font.color.rgb = C_MUTED

    # Title
    title_box = slide.shapes.add_textbox(Inches(0.8), Inches(0.72), Inches(11.5), Inches(0.65))
    tf_t = title_box.text_frame
    tf_t.word_wrap = True
    tf_t.margin_left = tf_t.margin_top = tf_t.margin_right = tf_t.margin_bottom = 0
    p_t = tf_t.paragraphs[0]
    p_t.text = title_text
    p_t.font.name = FONT_SERIF
    p_t.font.size = Pt(22)
    p_t.font.bold = True
    p_t.font.color.rgb = C_TITLE

    # Header Divider Line
    line = slide.shapes.add_shape(
        MSO_SHAPE.RECTANGLE,
        Inches(0.8), Inches(1.42), Inches(11.733), Inches(0.015)
    )
    line.fill.solid()
    line.fill.fore_color.rgb = C_LINE
    line.line.color.rgb = C_LINE

    # Footer Divider Line
    f_line = slide.shapes.add_shape(
        MSO_SHAPE.RECTANGLE,
        Inches(0.8), Inches(6.85), Inches(11.733), Inches(0.012)
    )
    f_line.fill.solid()
    f_line.fill.fore_color.rgb = C_LINE
    f_line.line.color.rgb = C_LINE

    # Footer Metadata
    meta_box = slide.shapes.add_textbox(Inches(0.8), Inches(6.95), Inches(8), Inches(0.35))
    tf_m = meta_box.text_frame
    p_m = tf_m.paragraphs[0]
    p_m.text = "Resonant Tunnelling in Double Barrier Structures | School of Engineering & Technology, BMU"
    p_m.font.name = FONT_SANS
    p_m.font.size = Pt(9)
    p_m.font.color.rgb = C_MUTED

    # Slide Number
    if slide_num:
        num_box = slide.shapes.add_textbox(Inches(10.5), Inches(6.95), Inches(2.0), Inches(0.35))
        tf_n = num_box.text_frame
        p_n = tf_n.paragraphs[0]
        p_n.text = f"Slide {slide_num} of 15"
        p_n.alignment = PP_ALIGN.RIGHT
        p_n.font.name = FONT_SANS
        p_n.font.size = Pt(9)
        p_n.font.color.rgb = C_MUTED

def add_card(slide, left, top, width, height, bg_color=C_CARD_BG, border_color=C_BORDER):
    """Draws a subtle card container for content grouping."""
    shape = slide.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, left, top, width, height)
    shape.fill.solid()
    shape.fill.fore_color.rgb = bg_color
    shape.line.color.rgb = border_color
    shape.line.width = Pt(1.0)
    return shape

# =============================================================
# SLIDE 1: TITLE SLIDE
# =============================================================
s1 = prs.slides.add_slide(blank_layout)

# Decorative outer border card
add_card(s1, Inches(0.8), Inches(0.8), Inches(11.733), Inches(5.9), bg_color=RGBColor(255, 255, 255), border_color=C_TITLE)

# Super-title
tb = s1.shapes.add_textbox(Inches(1.2), Inches(1.3), Inches(11.0), Inches(0.4))
p = tb.text_frame.paragraphs[0]
p.text = "BML MUNJAL UNIVERSITY  •  SCHOOL OF ENGINEERING & TECHNOLOGY"
p.font.name = FONT_SANS
p.font.size = Pt(11)
p.font.bold = True
p.font.color.rgb = C_MUTED
p.alignment = PP_ALIGN.CENTER

# Main Title
tb = s1.shapes.add_textbox(Inches(1.2), Inches(1.8), Inches(11.0), Inches(1.4))
tb.text_frame.word_wrap = True
p = tb.text_frame.paragraphs[0]
p.text = "Resonant Tunnelling in a Double-Barrier Structure:"
p.font.name = FONT_SERIF
p.font.size = Pt(28)
p.font.bold = True
p.font.color.rgb = C_TITLE
p.alignment = PP_ALIGN.CENTER

p2 = tb.text_frame.add_paragraph()
p2.text = "Transfer Matrix Modeling, Negative Differential Resistance & 3D Wavepacket Simulation"
p2.font.name = FONT_SERIF
p2.font.size = Pt(20)
p2.font.color.rgb = RGBColor(55, 65, 81)
p2.alignment = PP_ALIGN.CENTER

# Divider line
div = s1.shapes.add_shape(MSO_SHAPE.RECTANGLE, Inches(4.5), Inches(3.45), Inches(4.333), Inches(0.02))
div.fill.solid()
div.fill.fore_color.rgb = C_TITLE
div.line.color.rgb = C_TITLE

# Authors Block
tb = s1.shapes.add_textbox(Inches(1.2), Inches(3.7), Inches(11.0), Inches(0.8))
p = tb.text_frame.paragraphs[0]
p.text = "PROJECT AUTHORS"
p.font.name = FONT_SANS
p.font.size = Pt(10)
p.font.bold = True
p.font.color.rgb = C_MUTED
p.alignment = PP_ALIGN.CENTER

p2 = tb.text_frame.add_paragraph()
p2.text = "Mohammad Azmal Shah   •   Pavan Karthik   •   Anant Goel   •   Darshan Mittal"
p2.font.name = FONT_SERIF
p2.font.size = Pt(15)
p2.font.bold = True
p2.font.color.rgb = C_TITLE
p2.alignment = PP_ALIGN.CENTER

# Links Card
tb = s1.shapes.add_textbox(Inches(1.2), Inches(4.8), Inches(11.0), Inches(1.2))
tf = tb.text_frame
p = tf.paragraphs[0]
p.text = "Open-Source Repository: https://github.com/Anantgoel2005/double-barrier-simulation"
p.font.name = FONT_SANS
p.font.size = Pt(10.5)
p.font.color.rgb = C_BODY
p.alignment = PP_ALIGN.CENTER

p2 = tf.add_paragraph()
p2.text = "Live Interactive 3D WebGL Simulation: https://anantgoel2005.github.io/double-barrier-simulation/"
p2.font.name = FONT_SANS
p2.font.size = Pt(10.5)
p2.font.bold = True
p2.font.color.rgb = C_TITLE
p2.alignment = PP_ALIGN.CENTER

p3 = tf.add_paragraph()
p3.text = "Final Academic Report & Presentation  •  Academic Session 2026"
p3.font.name = FONT_SANS
p3.font.size = Pt(9.5)
p3.font.color.rgb = C_MUTED
p3.alignment = PP_ALIGN.CENTER

# =============================================================
# SLIDE 2: MOTIVATION & PROBLEM STATEMENT
# =============================================================
s2 = prs.slides.add_slide(blank_layout)
add_header(s2, "Motivation & Problem Statement: The Limits of Drift Transport", "PROJECT BACKGROUND", 2)

col_w = Inches(3.64)
col_h = Inches(5.0)

# Card 1: Classical CMOS Limits
add_card(s2, Inches(0.8), Inches(1.65), col_w, col_h)
tb = s2.shapes.add_textbox(Inches(1.0), Inches(1.85), col_w - Inches(0.4), col_h - Inches(0.4))
tf = tb.text_frame
tf.word_wrap = True
p = tf.paragraphs[0]
p.text = "1. Classical Drift Limits"
p.font.name = FONT_SERIF
p.font.size = Pt(16)
p.font.bold = True
p.font.color.rgb = C_TITLE

bullets1 = [
    ("Velocity Saturation:", "Drift velocity saturates at ~10⁷ cm/s in semiconductors, imposing transit delays."),
    ("Frequency Ceiling:", "Conventional transistors (HEMTs, BJTs) face practical fundamental cutoffs below 500 GHz."),
    ("Thermal & Leakage:", "Direct gate tunneling and subthreshold swing (60 mV/dec) bottleneck scaling.")
]
for title, desc in bullets1:
    p = tf.add_paragraph()
    p.text = f"• {title} "
    p.font.name = FONT_SANS
    p.font.size = Pt(11.5)
    p.font.bold = True
    p.font.color.rgb = C_TITLE
    # append desc
    run = p.add_run()
    run.text = desc
    run.font.bold = False
    run.font.color.rgb = C_BODY

# Card 2: Quantum Transit
add_card(s2, Inches(4.84), Inches(1.65), col_w, col_h)
tb = s2.shapes.add_textbox(Inches(5.04), Inches(1.85), col_w - Inches(0.4), col_h - Inches(0.4))
tf = tb.text_frame
tf.word_wrap = True
p = tf.paragraphs[0]
p.text = "2. The Quantum Solution"
p.font.name = FONT_SERIF
p.font.size = Pt(16)
p.font.bold = True
p.font.color.rgb = C_TITLE

bullets2 = [
    ("Resonant Tunneling:", "Exploits wave mechanics rather than suppressing them via double barrier cavities."),
    ("Femtosecond Lifetime:", "Quasi-bound state dwell times τ ~ 50–200 fs enable terahertz operation."),
    ("Coherent Phase Matching:", "Constructive de Broglie interference achieves near-unity transmission (T → 1.0).")
]
for title, desc in bullets2:
    p = tf.add_paragraph()
    p.text = f"• {title} "
    p.font.name = FONT_SANS
    p.font.size = Pt(11.5)
    p.font.bold = True
    p.font.color.rgb = C_TITLE
    run = p.add_run()
    run.text = desc
    run.font.bold = False
    run.font.color.rgb = C_BODY

# Card 3: Technological Impact
add_card(s2, Inches(8.88), Inches(1.65), col_w, col_h)
tb = s2.shapes.add_textbox(Inches(9.08), Inches(1.85), col_w - Inches(0.4), col_h - Inches(0.4))
tf = tb.text_frame
tf.word_wrap = True
p = tf.paragraphs[0]
p.text = "3. Macroscopic NDR Impact"
p.font.name = FONT_SERIF
p.font.size = Pt(16)
p.font.bold = True
p.font.color.rgb = C_TITLE

bullets3 = [
    ("Negative Conductance:", "dI/dV < 0 enables power generation and high-speed multi-stable switching."),
    ("Record THz Oscillators:", "Fundamental room-temperature RTD oscillators achieve > 1.98 THz."),
    ("Circuit Simplification:", "Replaces complex transistor arrays in multi-valued logic (MVL) and sub-2 ps pulse generators.")
]
for title, desc in bullets3:
    p = tf.add_paragraph()
    p.text = f"• {title} "
    p.font.name = FONT_SANS
    p.font.size = Pt(11.5)
    p.font.bold = True
    p.font.color.rgb = C_TITLE
    run = p.add_run()
    run.text = desc
    run.font.bold = False
    run.font.color.rgb = C_BODY

# =============================================================
# SLIDE 3: PROJECT OBJECTIVES & SCOPE
# =============================================================
s3 = prs.slides.add_slide(blank_layout)
add_header(s3, "Project Objectives & Technical Scope", "GOALS & METHODOLOGY", 3)

objectives = [
    ("1. Exact Quantum Transport Modeling", 
     "Formulate and implement the Transfer Matrix Method (TMM) with BenDaniel-Duke boundary conditions to account for position-dependent effective mass m*(x) under arbitrary external bias voltage Va."),
    ("2. Parametric Sensitivity Sweeps",
     "Systematically investigate how variations in barrier height (V₀), barrier thickness (Lb), and quantum well width (Lw) modulate transmission spectra T(E), resonance eigen-energies, linewidths (Γ), and dwell lifetimes (τ)."),
    ("3. Resonant Tunnelling Diode (RTD) I-V Solver",
     "Integrate the transmission probability against the transverse electron Fermi-Dirac supply function via the Tsu-Esaki formula to quantify peak current J_peak, valley current J_valley, and the Peak-to-Valley Current Ratio (PVCR)."),
    ("4. Dynamic 3D Time-Dependent Wavepacket Simulation",
     "Develop a dynamic Split-Step Fourier Method (SSFM) solver for the Time-Dependent Schrödinger Equation (TDSE) to directly visualize cavity trapping and phase buildup on resonance versus total barrier reflection off resonance."),
    ("5. Tri-Platform Open-Source Dissemination",
     "Package the entire framework across three production tiers: a 3D WebGL web simulation on GitHub Pages, a zero-dependency Python desktop GUI, and an automated MATLAB research suite.")
]

y_pos = Inches(1.65)
for title, desc in objectives:
    add_card(s3, Inches(0.8), y_pos, Inches(11.733), Inches(0.92))
    tb = s3.shapes.add_textbox(Inches(1.0), y_pos + Inches(0.06), Inches(11.333), Inches(0.8))
    tf = tb.text_frame
    tf.word_wrap = True
    p = tf.paragraphs[0]
    p.text = title
    p.font.name = FONT_SERIF
    p.font.size = Pt(14)
    p.font.bold = True
    p.font.color.rgb = C_TITLE
    
    p2 = tf.add_paragraph()
    p2.text = desc
    p2.font.name = FONT_SANS
    p2.font.size = Pt(10.5)
    p2.font.color.rgb = C_BODY
    y_pos += Inches(1.02)

# =============================================================
# SLIDE 4: LITERATURE SURVEY & MILESTONES
# =============================================================
s4 = prs.slides.add_slide(blank_layout)
add_header(s4, "Literature Survey & Milestone Historical Studies", "LITERATURE REVIEW", 4)

# Create a clean academic table
rows = [
    ["Reference", "Focus / Structure", "Methodology", "Key Finding / Contribution", "Relevance to This Project"],
    ["L. Esaki & R. Tsu (1970)", "Semiconductor superlattices", "Quantum size effects", "Predicted mini-bands and negative differential conductivity", "Theoretical foundation of engineered potential barriers"],
    ["R. Tsu & L. Esaki (1973)", "Finite superlattice tunneling", "Analytical 1D transmission", "Derived the standard Tsu-Esaki electrical tunneling current equation", "Exact formulation used in our macroscopic RTD I-V solver"],
    ["L. L. Chang et al. (1974)", "GaAs/AlGaAs double barrier", "MBE experimental growth", "First experimental demonstration of resonant tunneling and NDR", "Provides baseline material parameters for GaAs/AlGaAs heterostructure"],
    ["D. BenDaniel & C. Duke (1966)", "Heterointerface boundary", "Wavefunction matching", "Current-conserving boundary conditions for variable effective mass m*(x)", "Exact matching conditions implemented in our TMM matrix formulation"],
    ["B. Jonsson & S. Eng (1990)", "Arbitrary quantum wells", "Piecewise Transfer Matrix", "Discretized arbitrary/tilted potentials into uniform step slices", "Numerical potential discretization scheme under applied bias voltage Va"],
    ["S. Suzuki & M. Asada (2010–2022)", "InP-based RTD oscillators", "Integrated planar antennas", "Room-temperature continuous-wave fundamental oscillation up to 1.98 THz", "Validates practical ultra-high-frequency applications of RTD devices"]
]

table_shape = s4.shapes.add_table(len(rows), 5, Inches(0.8), Inches(1.65), Inches(11.733), Inches(4.9))
table = table_shape.table

# Set Column Widths
col_widths = [Inches(2.2), Inches(2.1), Inches(2.1), Inches(2.8), Inches(2.533)]
for i, w in enumerate(col_widths):
    table.columns[i].width = w

for r_idx, row in enumerate(rows):
    for c_idx, val in enumerate(row):
        cell = table.cell(r_idx, c_idx)
        cell.text = val
        p = cell.text_frame.paragraphs[0]
        if r_idx == 0:
            p.font.name = FONT_SANS
            p.font.size = Pt(11)
            p.font.bold = True
            p.font.color.rgb = RGBColor(255, 255, 255)
            cell.fill.solid()
            cell.fill.fore_color.rgb = C_TITLE
        else:
            p.font.name = FONT_SANS
            p.font.size = Pt(9.5)
            p.font.color.rgb = C_BODY
            cell.fill.solid()
            cell.fill.fore_color.rgb = RGBColor(255, 255, 255) if r_idx % 2 == 1 else RGBColor(248, 249, 250)

# =============================================================
# SLIDE 5: FABRY-PÉROT ANALOGY & WORKING PRINCIPLE
# =============================================================
s5 = prs.slides.add_slide(blank_layout)
add_header(s5, "Physical Working Principle: The Fabry-Pérot Analogy", "PHYSICAL MECHANISM", 5)

# Left Side: Explanation Card
add_card(s5, Inches(0.8), Inches(1.65), Inches(5.8), Inches(5.0))
tb = s5.shapes.add_textbox(Inches(1.0), Inches(1.85), Inches(5.4), Inches(4.6))
tf = tb.text_frame
tf.word_wrap = True

p = tf.paragraphs[0]
p.text = "de Broglie Wave Interference in a Quantum Well"
p.font.name = FONT_SERIF
p.font.size = Pt(15)
p.font.bold = True
p.font.color.rgb = C_TITLE

points = [
    ("Optics vs. Quantum Analogy:", "Resonant tunneling is isomorphic to an optical Fabry-Pérot etalon where the two potential barriers act as partially reflective mirrors."),
    ("Phase Quantization Condition:", "Constructive de Broglie interference occurs when round-trip phase accumulation satisfies: 2 k_w L_w + φ₁ + φ₂ = 2 π n (n = 1, 2, ...)"),
    ("Resonant Eigen-States:", "At the quasi-bound eigen-energy E₁, incident electron waves interfere constructively inside the well, causing the internal probability density |ψ|² to amplify by > 54×."),
    ("Near-Unity Transmission:", "Despite individual thick, opaque barriers, total transmission approaches T(E₁) → 1.00 at the resonance peak."),
    ("Off-Resonance Destructive Interference:", "Electrons with E ≠ E₁ undergo destructive interference in the well, resulting in > 99% barrier reflection.")
]

for title, desc in points:
    p = tf.add_paragraph()
    p.text = f"• {title} "
    p.font.name = FONT_SANS
    p.font.size = Pt(10.5)
    p.font.bold = True
    p.font.color.rgb = C_TITLE
    run = p.add_run()
    run.text = desc
    run.font.bold = False
    run.font.color.rgb = C_BODY

# Right Side: Figure 1
s5.shapes.add_picture('slide_figures/fig1_potential_profile.png', Inches(6.8), Inches(1.65), width=Inches(5.733))

# =============================================================
# SLIDE 6: THEORETICAL METHODOLOGY: TRANSFER MATRIX METHOD
# =============================================================
s6 = prs.slides.add_slide(blank_layout)
add_header(s6, "Theoretical Formulation: Piecewise Transfer Matrix Method (TMM)", "THEORETICAL METHODOLOGY", 6)

# 3 Horizontal Cards
# Card 1: 1D BenDaniel-Duke Equation
add_card(s6, Inches(0.8), Inches(1.65), Inches(11.733), Inches(1.5))
tb = s6.shapes.add_textbox(Inches(1.0), Inches(1.75), Inches(11.333), Inches(1.3))
tf = tb.text_frame
tf.word_wrap = True
p = tf.paragraphs[0]
p.text = "1. BenDaniel-Duke Effective-Mass Schrödinger Equation"
p.font.name = FONT_SERIF
p.font.size = Pt(13.5)
p.font.bold = True
p.font.color.rgb = C_TITLE

p2 = tf.add_paragraph()
p2.text = "-(ħ² / 2) (d/dx) [ (1 / m*(x)) (dψ/dx) ] + V(x) ψ(x) = E ψ(x)"
p2.font.name = FONT_SERIF
p2.font.size = Pt(12)
p2.font.bold = True
p2.font.color.rgb = RGBColor(17, 24, 39)

p3 = tf.add_paragraph()
p3.text = "• Heterointerface boundary matching conditions: Enforces continuity of both ψ(x₀) and (1 / m*) (dψ/dx) at x₀ to preserve quantum probability flux conservation across heterojunctions with step effective-mass discontinuities."
p3.font.name = FONT_SANS
p3.font.size = Pt(10)
p3.font.color.rgb = C_BODY

# Card 2: Piecewise Discretization under Bias
add_card(s6, Inches(0.8), Inches(3.3), Inches(11.733), Inches(1.55))
tb = s6.shapes.add_textbox(Inches(1.0), Inches(3.4), Inches(11.333), Inches(1.35))
tf = tb.text_frame
tf.word_wrap = True
p = tf.paragraphs[0]
p.text = "2. Piecewise Discretization & Characteristic Layer Transfer Matrix"
p.font.name = FONT_SERIF
p.font.size = Pt(13.5)
p.font.bold = True
p.font.color.rgb = C_TITLE

p2 = tf.add_paragraph()
p2.text = "Active region subdivided into N thin slices Δx. In slice j:  M_j = [ [ cos(k_j Δx),  (m*_j / k_j) sin(k_j Δx) ],  [ -(k_j / m*_j) sin(k_j Δx),  cos(k_j Δx) ] ]"
p2.font.name = FONT_SERIF
p2.font.size = Pt(11)
p2.font.bold = True
p2.font.color.rgb = RGBColor(17, 24, 39)

p3 = tf.add_paragraph()
p3.text = "• Sinc Taylor Stabilization: When E → V_j (k_j → 0), sin(k_j Δx) / k_j is evaluated via Δx - (k_j² Δx³ / 6) to eliminate 0/0 numerical floating-point singular indeterminacies."
p3.font.name = FONT_SANS
p3.font.size = Pt(10)
p3.font.color.rgb = C_BODY

# Card 3: Global Matrix & Transmission Formula
add_card(s6, Inches(0.8), Inches(5.0), Inches(11.733), Inches(1.65))
tb = s6.shapes.add_textbox(Inches(1.0), Inches(5.1), Inches(11.333), Inches(1.45))
tf = tb.text_frame
tf.word_wrap = True
p = tf.paragraphs[0]
p.text = "3. Global Matrix Cascading & Transmission Coefficient T(E)"
p.font.name = FONT_SERIF
p.font.size = Pt(13.5)
p.font.bold = True
p.font.color.rgb = C_TITLE

p2 = tf.add_paragraph()
p2.text = "M_tot = M_N · M_(N-1) ··· M_1,    [ u_1, u_2 ]ᵀ = M_tot⁻¹ [ 1, α_R ]ᵀ,    t = 2 α_L / (α_L u_1 + u_2)"
p2.font.name = FONT_SERIF
p2.font.size = Pt(11)
p2.font.bold = True
p2.font.color.rgb = RGBColor(17, 24, 39)

p3 = tf.add_paragraph()
p3.text = "• Final Transmission & Reflection:  T(E) = [ (Re(k_R)/m*_R) / (k_L/m*_L) ] |t|²,    R(E) = |r|²,    ensuring T(E) + R(E) = 1.0000 exactly."
p3.font.name = FONT_SANS
p3.font.size = Pt(10)
p3.font.color.rgb = C_BODY

# =============================================================
# SLIDE 7: THEORETICAL METHODOLOGY: TSU-ESAKI & SSFM DYNAMICS
# =============================================================
s7 = prs.slides.add_slide(blank_layout)
add_header(s7, "Theoretical Formulation: Tsu-Esaki Transport & Dynamic SSFM", "THEORETICAL METHODOLOGY", 7)

# 2 Columns
w_col = Inches(5.7)

# Col 1: Tsu-Esaki
add_card(s7, Inches(0.8), Inches(1.65), w_col, Inches(5.0))
tb = s7.shapes.add_textbox(Inches(1.0), Inches(1.85), w_col - Inches(0.4), Inches(4.6))
tf = tb.text_frame
tf.word_wrap = True

p = tf.paragraphs[0]
p.text = "Macroscopic Tsu-Esaki Current Density"
p.font.name = FONT_SERIF
p.font.size = Pt(15)
p.font.bold = True
p.font.color.rgb = C_TITLE

p2 = tf.add_paragraph()
p2.text = "J(V_a) = [ e m* k_B T / (2 π² ħ³) ] ∫ T(E, V_a) ln[ (1 + exp((E_F - E)/k_B T)) / (1 + exp((E_F - E - e V_a)/k_B T)) ] dE"
p2.font.name = FONT_SERIF
p2.font.size = Pt(10.5)
p2.font.bold = True
p2.font.color.rgb = RGBColor(17, 24, 39)

bullets_te = [
    ("Transverse Supply Integration:", "Integrates 1D transmission T(E, Va) against 2D transverse Fermi-Dirac electron density supply functions in the leads."),
    ("Room Temperature (300 K):", "k_B T ≈ 25.85 meV introduces thermal broadening into the emitter electron distribution."),
    ("Fermi Level Alignment:", "When bias Va pulls E₁ below the emitter Fermi energy E_F, current surges to a maximum."),
    ("NDR Onset:", "When E₁ drops below the emitter conduction band edge, transverse momentum cannot be conserved, causing J to plummet abruptly.")
]
for title, desc in bullets_te:
    p = tf.add_paragraph()
    p.text = f"• {title} "
    p.font.name = FONT_SANS
    p.font.size = Pt(10)
    p.font.bold = True
    p.font.color.rgb = C_TITLE
    run = p.add_run()
    run.text = desc
    run.font.bold = False
    run.font.color.rgb = C_BODY

# Col 2: SSFM TDSE
add_card(s7, Inches(6.833), Inches(1.65), w_col, Inches(5.0))
tb = s7.shapes.add_textbox(Inches(7.033), Inches(1.85), w_col - Inches(0.4), Inches(4.6))
tf = tb.text_frame
tf.word_wrap = True

p = tf.paragraphs[0]
p.text = "Split-Step Fourier Method (SSFM) for TDSE"
p.font.name = FONT_SERIF
p.font.size = Pt(15)
p.font.bold = True
p.font.color.rgb = C_TITLE

p2 = tf.add_paragraph()
p2.text = "Ψ(t+Δt) ≈ exp(-i V Δt / 2ħ) F⁻¹[ exp(-i ħ k² Δt / 2m*) F[ exp(-i V Δt / 2ħ) Ψ(t) ] ]"
p2.font.name = FONT_SERIF
p2.font.size = Pt(10.5)
p2.font.bold = True
p2.font.color.rgb = RGBColor(17, 24, 39)

bullets_ssfm = [
    ("Symmetric Strang Splitting:", "Separates non-commuting kinetic (T) and potential (V) energy operators with O(Δt³) second-order local error."),
    ("Dual-Domain Propagation:", "Potential phase rotation applied in real space (x, y); kinetic dispersion applied in spectral wavevector space (kx, ky) via FFT."),
    ("Unconditionally Unitary:", "Preserves total wavefunction probability norm ∫|Ψ|² dx = 1.0000 across thousands of time steps without numerical dissipation."),
    ("Real-Time Wavepacket Dynamics:", "Directly simulates incident Gaussian pulse collision, partial tunneling, cavity trapping, and transmitted packet pulse train.")
]
for title, desc in bullets_ssfm:
    p = tf.add_paragraph()
    p.text = f"• {title} "
    p.font.name = FONT_SANS
    p.font.size = Pt(10)
    p.font.bold = True
    p.font.color.rgb = C_TITLE
    run = p.add_run()
    run.text = desc
    run.font.bold = False
    run.font.color.rgb = C_BODY

# =============================================================
# SLIDE 8: RESULTS: TRANSMISSION SPECTRUM & CAVITY METRICS
# =============================================================
s8 = prs.slides.add_slide(blank_layout)
add_header(s8, "Results (1): Transmission Spectrum & Quasi-Bound Cavity Metrics", "SIMULATION RESULTS", 8)

# Left Side: Figure 2
s8.shapes.add_picture('slide_figures/fig2_transmission_spectrum.png', Inches(0.8), Inches(1.65), width=Inches(5.733))

# Right Side: Computed Metrics Cards
right_x = Inches(6.8)
add_card(s8, right_x, Inches(1.65), Inches(5.733), Inches(5.0))

tb = s8.shapes.add_textbox(right_x + Inches(0.2), Inches(1.85), Inches(5.333), Inches(4.6))
tf = tb.text_frame
tf.word_wrap = True

p = tf.paragraphs[0]
p.text = "Baseline Structure Computed Parameters"
p.font.name = FONT_SERIF
p.font.size = Pt(15)
p.font.bold = True
p.font.color.rgb = C_TITLE

p2 = tf.add_paragraph()
p2.text = "Al₀.₃Ga₀.₇As/GaAs Heterostructure: V₀ = 0.30 eV, L_b = 3.0 nm, L_w = 5.0 nm"
p2.font.name = FONT_SANS
p2.font.size = Pt(10)
p2.font.color.rgb = C_MUTED

metrics = [
    ("Resonance Eigen-Energy (E₁):", "88.0 meV (0.0880 eV)", "Lowest quasi-bound quantum well eigenstate"),
    ("Linewidth (Γ at FWHM):", "4.0 meV (0.0040 eV)", "Energy broadening due to finite barrier transmission coupling"),
    ("Quasi-Bound State Lifetime (τ):", "164.7 fs (1.65 × 10⁻¹³ s)", "Mean dwell time of trapped wavepacket (τ = ħ / Γ)"),
    ("Peak Transmission (T_max):", "0.9998 ≈ 1.00", "Near-perfect constructive de Broglie wave interference"),
    ("Cavity Quality Factor (Q):", "22.0", "Cavity sharpness index (Q = E₁ / Γ)"),
    ("Internal Buildup Factor:", "54.2× |ψ_inc|²", "Peak standing-wave probability density amplification in well")
]

for title, val, meaning in metrics:
    p = tf.add_paragraph()
    p.text = f"• {title} "
    p.font.name = FONT_SANS
    p.font.size = Pt(10)
    p.font.bold = True
    p.font.color.rgb = C_TITLE
    
    r_val = p.add_run()
    r_val.text = f"{val}  "
    r_val.font.bold = True
    r_val.font.color.rgb = RGBColor(17, 24, 39)
    
    r_m = p.add_run()
    r_m.text = f"({meaning})"
    r_m.font.italic = True
    r_m.font.color.rgb = C_MUTED

# =============================================================
# SLIDE 9: RESULTS: PARAMETRIC SENSITIVITY SWEEPS
# =============================================================
s9 = prs.slides.add_slide(blank_layout)
add_header(s9, "Results (2): Parametric Sensitivity Sweeps (V₀, L_b, L_w)", "SIMULATION RESULTS", 9)

# 3 Full Height Cards
c_w = Inches(3.64)
c_h = Inches(5.0)

# 1. Barrier Height V0
add_card(s9, Inches(0.8), Inches(1.65), c_w, c_h)
tb = s9.shapes.add_textbox(Inches(1.0), Inches(1.85), c_w - Inches(0.4), c_h - Inches(0.4))
tf = tb.text_frame
tf.word_wrap = True
p = tf.paragraphs[0]
p.text = "1. Barrier Height (V₀)"
p.font.name = FONT_SERIF
p.font.size = Pt(16)
p.font.bold = True
p.font.color.rgb = C_TITLE

points_v0 = [
    ("Sweep Range:", "0.20 eV to 0.60 eV (Al mole fraction x = 0.2 to 0.6)."),
    ("Decay Parameter κ:", "κ = [2 m*_b (V₀ - E)]¹/² / ħ increases with barrier height."),
    ("Sub-Barrier Suppression:", "Exponential reduction of non-resonant leakage transmission below 10⁻⁶."),
    ("Confinement Shift:", "Deeper quantum well slightly elevates E₁ due to reduced wave penetration into the barriers.")
]
for title, desc in points_v0:
    p = tf.add_paragraph()
    p.text = f"• {title} "
    p.font.name = FONT_SANS
    p.font.size = Pt(10.5)
    p.font.bold = True
    p.font.color.rgb = C_TITLE
    run = p.add_run()
    run.text = desc
    run.font.bold = False
    run.font.color.rgb = C_BODY

# 2. Barrier Thickness Lb
add_card(s9, Inches(4.84), Inches(1.65), c_w, c_h)
tb = s9.shapes.add_textbox(Inches(5.04), Inches(1.85), c_w - Inches(0.4), c_h - Inches(0.4))
tf = tb.text_frame
tf.word_wrap = True
p = tf.paragraphs[0]
p.text = "2. Barrier Thickness (L_b)"
p.font.name = FONT_SERIF
p.font.size = Pt(16)
p.font.bold = True
p.font.color.rgb = C_TITLE

points_lb = [
    ("Sweep Range:", "1.5 nm to 4.5 nm."),
    ("Exponential Linewidth:", "Linewidth scales exponentially: Γ(L_b) ∝ exp(-2 κ L_b)."),
    ("Sharpness vs. Current:", "Increasing L_b from 2.0 to 4.0 nm narrows Γ from 18.5 meV to 0.85 meV."),
    ("Lifetime Trade-off:", "Dwell lifetime τ increases from 35.6 fs to 774.5 fs, trading current amplitude for cavity Q-factor.")
]
for title, desc in points_lb:
    p = tf.add_paragraph()
    p.text = f"• {title} "
    p.font.name = FONT_SANS
    p.font.size = Pt(10.5)
    p.font.bold = True
    p.font.color.rgb = C_TITLE
    run = p.add_run()
    run.text = desc
    run.font.bold = False
    run.font.color.rgb = C_BODY

# 3. Well Width Lw
add_card(s9, Inches(8.88), Inches(1.65), c_w, c_h)
tb = s9.shapes.add_textbox(Inches(9.08), Inches(1.85), c_w - Inches(0.4), c_h - Inches(0.4))
tf = tb.text_frame
tf.word_wrap = True
p = tf.paragraphs[0]
p.text = "3. Well Width (L_w)"
p.font.name = FONT_SERIF
p.font.size = Pt(16)
p.font.bold = True
p.font.color.rgb = C_TITLE

points_lw = [
    ("Sweep Range:", "3.0 nm to 8.0 nm."),
    ("Eigen-Energy Scaling:", "Quasi-bound states scale inversely as E_n ∝ 1 / L_w²."),
    ("Red Shift:", "Expanding L_w from 3 nm to 6 nm lowers E₁ from 145 meV down to 62 meV."),
    ("Higher Harmonic States:", "For L_w > 6.5 nm, higher-order resonant states (E₂, E₃) enter below the barrier crest V₀ = 0.30 eV.")
]
for title, desc in points_lw:
    p = tf.add_paragraph()
    p.text = f"• {title} "
    p.font.name = FONT_SANS
    p.font.size = Pt(10.5)
    p.font.bold = True
    p.font.color.rgb = C_TITLE
    run = p.add_run()
    run.text = desc
    run.font.bold = False
    run.font.color.rgb = C_BODY

# =============================================================
# SLIDE 10: RESULTS: RTD I-V CHARACTERISTICS & NDR
# =============================================================
s10 = prs.slides.add_slide(blank_layout)
add_header(s10, "Results (3): Resonant Tunnelling Diode I-V & NDR Regimes", "ELECTRICAL TRANSPORT", 10)

# Left Side: Figure 3
s10.shapes.add_picture('slide_figures/fig3_rtd_iv_curve.png', Inches(0.8), Inches(1.65), width=Inches(5.733))

# Right Side: 4 Operating Regimes
right_x = Inches(6.8)
add_card(s10, right_x, Inches(1.65), Inches(5.733), Inches(5.0))

tb = s10.shapes.add_textbox(right_x + Inches(0.2), Inches(1.85), Inches(5.333), Inches(4.6))
tf = tb.text_frame
tf.word_wrap = True

p = tf.paragraphs[0]
p.text = "Four Distinct RTD Operational Regimes"
p.font.name = FONT_SERIF
p.font.size = Pt(15)
p.font.bold = True
p.font.color.rgb = C_TITLE

regimes = [
    ("1. Equilibrium (Va = 0 V):", "J = 0. Well eigenstate E₁ = 88 meV sits above the emitter Fermi sea (E_F = 40 meV). No net tunneling occurs."),
    ("2. Resonant Current Surge (0 < Va ≤ 0.14 V):", "Potential drop across the cavity lowers E₁ into alignment with occupied emitter states. Current surges to J_peak = 1.18 × 10⁵ A/cm² at V_peak = 0.140 V."),
    ("3. NDR Region (0.14 V < Va < 0.20 V):", "Negative Differential Resistance (dI/dV < 0). E₁ drops below the emitter conduction band edge; electrons cannot conserve transverse momentum, causing current to plummet abruptly."),
    ("4. Valley Point & PVCR (Va = 0.20 V):", "Current drops to J_valley = 1.74 × 10⁴ A/cm², achieving a Peak-to-Valley Current Ratio (PVCR) = 6.78 at 300 K."),
    ("5. Thermal Over-Barrier Leakage (Va > 0.25 V):", "Thermionic emission and classical triangular tunneling take over as bias exceeds the barrier crest.")
]

for title, desc in regimes:
    p = tf.add_paragraph()
    p.text = f"• {title} "
    p.font.name = FONT_SANS
    p.font.size = Pt(9.5)
    p.font.bold = True
    p.font.color.rgb = C_TITLE
    run = p.add_run()
    run.text = desc
    run.font.bold = False
    run.font.color.rgb = C_BODY

# =============================================================
# SLIDE 11: RESULTS: 3D TIMEDEP SCHRÖDINGER WAVEPACKET
# =============================================================
s11 = prs.slides.add_slide(blank_layout)
add_header(s11, "Results (4): Dynamic Split-Step Fourier Wavepacket Propagation", "DYNAMIC SIMULATION", 11)

# Left Side: Figure 4
s11.shapes.add_picture('slide_figures/fig4_wavepacket_comparison.png', Inches(0.8), Inches(1.65), width=Inches(5.733))

# Right Side: Physics Description
right_x = Inches(6.8)
add_card(s11, right_x, Inches(1.65), Inches(5.733), Inches(5.0))

tb = s11.shapes.add_textbox(right_x + Inches(0.2), Inches(1.85), Inches(5.333), Inches(4.6))
tf = tb.text_frame
tf.word_wrap = True

p = tf.paragraphs[0]
p.text = "Wavepacket Collision & Trapping Dynamics"
p.font.name = FONT_SERIF
p.font.size = Pt(15)
p.font.bold = True
p.font.color.rgb = C_TITLE

wp_points = [
    ("Incident Gaussian Wavepacket:", "Initialized in the emitter lead: Ψ(x, 0) = (2πσ²)⁻¹/⁴ exp[-(x - x₀)² / 4σ²] exp(i k₀ x) with longitudinal kinetic energy E₀ = ħ²k₀² / 2m*."),
    ("On-Resonance Dynamics (E₀ = E₁ = 88 meV):", "• The wavepacket strikes the first barrier and splits.\n• Inside the quantum well, multiple internal reflections undergo constructive interference.\n• A standing wave cavity buildup forms over t ≈ 50–120 fs.\n• Coherent transmitted wavepacket emits smoothly into the collector lead."),
    ("Off-Resonance Dynamics (E₀ = 44 meV):", "• Over 99% of probability density reflects off the first barrier.\n• Wavefunction inside the well is virtually zero (|ψ|² < 10⁻⁴).\n• Transmitted pulse amplitude in collector is negligible."),
    ("3D Stark Shift Visualization:", "External bias slants the 3D potential surface, dynamically tuning resonance into and out of alignment in real-time.")
]

for title, desc in wp_points:
    p = tf.add_paragraph()
    p.text = f"• {title} "
    p.font.name = FONT_SANS
    p.font.size = Pt(9.5)
    p.font.bold = True
    p.font.color.rgb = C_TITLE
    run = p.add_run()
    run.text = desc
    run.font.bold = False
    run.font.color.rgb = C_BODY

# =============================================================
# SLIDE 12: MULTI-PLATFORM SOFTWARE ARCHITECTURE
# =============================================================
s12 = prs.slides.add_slide(blank_layout)
add_header(s12, "Multi-Platform Software Implementation & Dissemination", "SYSTEM ARCHITECTURE", 12)

# 3 Column Cards
c_w = Inches(3.64)
c_h = Inches(5.0)

# Tier 1: WebGL
add_card(s12, Inches(0.8), Inches(1.65), c_w, c_h)
tb = s12.shapes.add_textbox(Inches(1.0), Inches(1.85), c_w - Inches(0.4), c_h - Inches(0.4))
tf = tb.text_frame
tf.word_wrap = True
p = tf.paragraphs[0]
p.text = "1. Interactive 3D Web App"
p.font.name = FONT_SERIF
p.font.size = Pt(15)
p.font.bold = True
p.font.color.rgb = C_TITLE

points_web = [
    ("Target Platform:", "Modern web browsers (Desktop & Mobile) via GitHub Pages."),
    ("Technology:", "WebGL / Three.js 3D rendering with native HTML5 Canvas 3D fallback."),
    ("Interactive Controls:", "Live sliders for V₀, L_b, L_w, Applied Bias Va, and Electron Energy E."),
    ("Visualizations:", "Real-time 3D quantum cavity, dynamic wavepacket animation, live TMM spectrum & Tsu-Esaki curve."),
    ("Live Deployment:", "anantgoel2005.github.io/double-barrier-simulation/")
]
for title, desc in points_web:
    p = tf.add_paragraph()
    p.text = f"• {title} "
    p.font.name = FONT_SANS
    p.font.size = Pt(9.5)
    p.font.bold = True
    p.font.color.rgb = C_TITLE
    run = p.add_run()
    run.text = desc
    run.font.bold = False
    run.font.color.rgb = C_BODY

# Tier 2: Python GUI
add_card(s12, Inches(4.84), Inches(1.65), c_w, c_h)
tb = s12.shapes.add_textbox(Inches(5.04), Inches(1.85), c_w - Inches(0.4), c_h - Inches(0.4))
tf = tb.text_frame
tf.word_wrap = True
p = tf.paragraphs[0]
p.text = "2. Desktop Python GUI"
p.font.name = FONT_SERIF
p.font.size = Pt(15)
p.font.bold = True
p.font.color.rgb = C_TITLE

points_py = [
    ("Target Platform:", "Cross-platform desktop (Windows, macOS, Linux)."),
    ("Zero Dependencies:", "Pure Python standard library (tkinter, math, cmath). Zero pip packages needed."),
    ("4-Quadrant Dashboard:", "Potential Profile, Transmission Spectrum T(E), Tsu-Esaki I-V, and 3D Wireframe Cavity."),
    ("High Performance:", "Optimized pure-Python complex matrix multiplication & 3D vector rotation matrix."),
    ("Execution:", "python rtd_gui_python.py or 1-click batch launcher.")
]
for title, desc in points_py:
    p = tf.add_paragraph()
    p.text = f"• {title} "
    p.font.name = FONT_SANS
    p.font.size = Pt(9.5)
    p.font.bold = True
    p.font.color.rgb = C_TITLE
    run = p.add_run()
    run.text = desc
    run.font.bold = False
    run.font.color.rgb = C_BODY

# Tier 3: MATLAB Suite
add_card(s12, Inches(8.88), Inches(1.65), c_w, c_h)
tb = s12.shapes.add_textbox(Inches(9.08), Inches(1.85), c_w - Inches(0.4), c_h - Inches(0.4))
tf = tb.text_frame
tf.word_wrap = True
p = tf.paragraphs[0]
p.text = "3. MATLAB Research Suite"
p.font.name = FONT_SERIF
p.font.size = Pt(15)
p.font.bold = True
p.font.color.rgb = C_TITLE

points_mat = [
    ("Target Platform:", "MATLAB R2018b and later."),
    ("Automated Scripts:", "• calculate_tmm.m: Piecewise TMM solver\n• calculate_rtd_iv.m: Tsu-Esaki solver\n• find_resonance_peaks.m: Peak detection"),
    ("3D TDSE SSFM Solver:", "rtd_3d_wavepacket.m provides dynamic 3D split-step Fourier simulation."),
    ("3D Energy Landscapes:", "rtd_3d_landscape.m models 2D/3D Stark surfaces under applied bias."),
    ("Interactive App:", "rtd_interactive_app.m provides graphical slider controls.")
]
for title, desc in points_mat:
    p = tf.add_paragraph()
    p.text = f"• {title} "
    p.font.name = FONT_SANS
    p.font.size = Pt(9.5)
    p.font.bold = True
    p.font.color.rgb = C_TITLE
    run = p.add_run()
    run.text = desc
    run.font.bold = False
    run.font.color.rgb = C_BODY

# =============================================================
# SLIDE 13: MAIN CONCLUSIONS & KEY FINDINGS
# =============================================================
s13 = prs.slides.add_slide(blank_layout)
add_header(s13, "Main Conclusions & Physical Takeaways", "PROJECT CONCLUSIONS", 13)

conclusions = [
    ("1. Verification of Coherent Resonant Tunnelling",
     "The Transfer Matrix Method rigorously verified that destructive interference suppresses off-resonance transmission below 10⁻⁶, while constructive phase matching amplifies internal standing-wave probability density by > 54×, yielding near-unity transmission (T → 1.00) at E₁ = 88.0 meV."),
    ("2. Microscopic Mapping of Macroscopic NDR",
     "The characteristic N-shaped RTD current-voltage curve was quantitatively mapped to sub-band alignment with the emitter Fermi sea, demonstrating a peak current density J_peak = 1.18 × 10⁵ A/cm² at 0.14 V and PVCR = 6.78 at room temperature (300 K)."),
    ("3. Fundamental Lifetime-Linewidth Trade-Off",
     "Dwell lifetimes follow τ = ħ / Γ, scaling exponentially with barrier thickness (L_b). Increasing L_b from 2 to 4 nm narrows linewidth from 18.5 meV (τ ≈ 35 fs) to 0.85 meV (τ ≈ 775 fs), proving the foundational trade-off between switching speed and current drive."),
    ("4. Robust Tri-Platform Open-Source Ecosystem",
     "The project successfully bridged rigorous condensed matter physics and intuitive visual engineering, delivering an open-source tri-platform suite featuring a live 3D WebGL web simulation, zero-dependency Python GUI, and comprehensive MATLAB suite.")
]

y_pos = Inches(1.65)
for title, desc in conclusions:
    add_card(s13, Inches(0.8), y_pos, Inches(11.733), Inches(1.15))
    tb = s13.shapes.add_textbox(Inches(1.0), y_pos + Inches(0.08), Inches(11.333), Inches(1.0))
    tf = tb.text_frame
    tf.word_wrap = True
    p = tf.paragraphs[0]
    p.text = title
    p.font.name = FONT_SERIF
    p.font.size = Pt(14)
    p.font.bold = True
    p.font.color.rgb = C_TITLE
    
    p2 = tf.add_paragraph()
    p2.text = desc
    p2.font.name = FONT_SANS
    p2.font.size = Pt(11)
    p2.font.color.rgb = C_BODY
    y_pos += Inches(1.25)

# =============================================================
# SLIDE 14: FUTURE RESEARCH DIRECTIONS
# =============================================================
s14 = prs.slides.add_slide(blank_layout)
add_header(s14, "Future Research Scope & Extensions", "FUTURE WORK", 14)

future_work = [
    ("1. Self-Consistent Poisson-Schrödinger Solver",
     "Incorporate dynamic space-charge accumulation inside the quantum well cavity. Dynamic electron buildup alters local electrostatics, leading to intrinsic bistability, hysteresis loops in the I-V curve, and plateau current features."),
    ("2. Non-Equilibrium Green's Function (NEGF) Formalism",
     "Account for dissipative, phase-breaking scattering mechanisms, including longitudinal optical (LO) phonon emission, acoustic phonon scattering, and heterointerface roughness, refining predictions at elevated operating temperatures."),
    ("3. High-Bandgap-Offset Heterostructure Systems",
     "Investigate InGaAs/AlAs and InAs/AlSb material systems with conduction band discontinuities V₀ > 1.2 eV to achieve room-temperature Peak-to-Valley Current Ratios (PVCR > 25), critical for ultra-low-noise THz logic."),
    ("4. Quantum Cascade Lasers & Superlattice Cascades",
     "Extend the single-cavity TMM framework to multi-stage periodic superlattices (20–50 stages) to model intersubband optical transitions and population inversion for mid-infrared and THz Quantum Cascade Lasers (QCLs).")
]

y_pos = Inches(1.65)
for title, desc in future_work:
    add_card(s14, Inches(0.8), y_pos, Inches(11.733), Inches(1.15))
    tb = s14.shapes.add_textbox(Inches(1.0), y_pos + Inches(0.08), Inches(11.333), Inches(1.0))
    tf = tb.text_frame
    tf.word_wrap = True
    p = tf.paragraphs[0]
    p.text = title
    p.font.name = FONT_SERIF
    p.font.size = Pt(14)
    p.font.bold = True
    p.font.color.rgb = C_TITLE
    
    p2 = tf.add_paragraph()
    p2.text = desc
    p2.font.name = FONT_SANS
    p2.font.size = Pt(11)
    p2.font.color.rgb = C_BODY
    y_pos += Inches(1.25)

# =============================================================
# SLIDE 15: SUMMARY & QUESTIONS (Q&A)
# =============================================================
s15 = prs.slides.add_slide(blank_layout)

add_card(s15, Inches(0.8), Inches(0.8), Inches(11.733), Inches(5.9), bg_color=RGBColor(255, 255, 255), border_color=C_TITLE)

tb = s15.shapes.add_textbox(Inches(1.2), Inches(1.4), Inches(11.0), Inches(0.4))
p = tb.text_frame.paragraphs[0]
p.text = "THANK YOU  •  QUESTIONS & DISCUSSION"
p.font.name = FONT_SANS
p.font.size = Pt(12)
p.font.bold = True
p.font.color.rgb = C_MUTED
p.alignment = PP_ALIGN.CENTER

tb = s15.shapes.add_textbox(Inches(1.2), Inches(2.0), Inches(11.0), Inches(1.0))
p = tb.text_frame.paragraphs[0]
p.text = "Resonant Tunnelling in a Double-Barrier Structure"
p.font.name = FONT_SERIF
p.font.size = Pt(28)
p.font.bold = True
p.font.color.rgb = C_TITLE
p.alignment = PP_ALIGN.CENTER

p2 = tb.text_frame.add_paragraph()
p2.text = "Transfer Matrix Modeling, Negative Differential Resistance & 3D Wavepacket Simulation"
p2.font.name = FONT_SERIF
p2.font.size = Pt(18)
p2.font.color.rgb = RGBColor(55, 65, 81)
p2.alignment = PP_ALIGN.CENTER

# Divider
div = s15.shapes.add_shape(MSO_SHAPE.RECTANGLE, Inches(4.5), Inches(3.3), Inches(4.333), Inches(0.02))
div.fill.solid()
div.fill.fore_color.rgb = C_TITLE
div.line.color.rgb = C_TITLE

# Authors
tb = s15.shapes.add_textbox(Inches(1.2), Inches(3.6), Inches(11.0), Inches(0.8))
p = tb.text_frame.paragraphs[0]
p.text = "PRESENTED BY"
p.font.name = FONT_SANS
p.font.size = Pt(10)
p.font.bold = True
p.font.color.rgb = C_MUTED
p.alignment = PP_ALIGN.CENTER

p2 = tb.text_frame.add_paragraph()
p2.text = "Mohammad Azmal Shah   •   Pavan Karthik   •   Anant Goel   •   Darshan Mittal"
p2.font.name = FONT_SERIF
p2.font.size = Pt(15)
p2.font.bold = True
p2.font.color.rgb = C_TITLE
p2.alignment = PP_ALIGN.CENTER

p3 = tb.text_frame.add_paragraph()
p3.text = "School of Engineering & Technology, BML Munjal University"
p3.font.name = FONT_SANS
p3.font.size = Pt(11)
p3.font.color.rgb = C_BODY
p3.alignment = PP_ALIGN.CENTER

# Project Resources Card
tb = s15.shapes.add_textbox(Inches(1.2), Inches(4.8), Inches(11.0), Inches(1.2))
tf = tb.text_frame
p = tf.paragraphs[0]
p.text = "Project Resources & Interactive Demonstrations:"
p.font.name = FONT_SANS
p.font.size = Pt(11)
p.font.bold = True
p.font.color.rgb = C_TITLE
p.alignment = PP_ALIGN.CENTER

p2 = tf.add_paragraph()
p2.text = "• Public GitHub Code Repository: https://github.com/Anantgoel2005/double-barrier-simulation"
p2.font.name = FONT_SANS
p2.font.size = Pt(10)
p2.font.color.rgb = C_BODY
p2.alignment = PP_ALIGN.CENTER

p3 = tf.add_paragraph()
p3.text = "• Live Interactive 3D WebGL Simulation: https://anantgoel2005.github.io/double-barrier-simulation/"
p3.font.name = FONT_SANS
p3.font.size = Pt(10)
p3.font.bold = True
p3.font.color.rgb = C_TITLE
p3.alignment = PP_ALIGN.CENTER

# -------------------------------------------------------------
# SAVE PRESENTATION
# -------------------------------------------------------------
output_path = "Resonant_Tunnelling_Presentation.pptx"
prs.save(output_path)
print(f"Presentation successfully saved to {output_path} ({len(prs.slides)} slides)")
