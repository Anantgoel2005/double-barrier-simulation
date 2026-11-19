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
C_LINE = RGBColor(229, 231, 235)       # Divider Line

FONT_SERIF = "Times New Roman"
FONT_SANS = "Calibri"

TOTAL_SLIDES = 14

def add_header(slide, title_text, category_text="ACADEMIC PROJECT PRESENTATION", slide_num=None):
    """Draws a standardized academic header and footer on each content slide."""
    # Category / Super-title
    cat_box = slide.shapes.add_textbox(Inches(0.8), Inches(0.35), Inches(10), Inches(0.3))
    tf_c = cat_box.text_frame
    tf_c.word_wrap = True
    tf_c.margin_left = tf_c.margin_top = tf_c.margin_right = tf_c.margin_bottom = 0
    p_c = tf_c.paragraphs[0]
    p_c.text = category_text.upper()
    p_c.font.name = FONT_SANS
    p_c.font.size = Pt(11)
    p_c.font.bold = True
    p_c.font.color.rgb = C_MUTED

    # Title (Large, 26pt bold)
    title_box = slide.shapes.add_textbox(Inches(0.8), Inches(0.68), Inches(11.733), Inches(0.65))
    tf_t = title_box.text_frame
    tf_t.word_wrap = True
    tf_t.margin_left = tf_t.margin_top = tf_t.margin_right = tf_t.margin_bottom = 0
    p_t = tf_t.paragraphs[0]
    p_t.text = title_text
    p_t.font.name = FONT_SERIF
    p_t.font.size = Pt(25)
    p_t.font.bold = True
    p_t.font.color.rgb = C_TITLE

    # Header Divider Line
    line = slide.shapes.add_shape(
        MSO_SHAPE.RECTANGLE,
        Inches(0.8), Inches(1.38), Inches(11.733), Inches(0.018)
    )
    line.fill.solid()
    line.fill.fore_color.rgb = C_LINE
    line.line.color.rgb = C_LINE

    # Footer Divider Line
    f_line = slide.shapes.add_shape(
        MSO_SHAPE.RECTANGLE,
        Inches(0.8), Inches(6.85), Inches(11.733), Inches(0.015)
    )
    f_line.fill.solid()
    f_line.fill.fore_color.rgb = C_LINE
    f_line.line.color.rgb = C_LINE

    # Footer Metadata
    meta_box = slide.shapes.add_textbox(Inches(0.8), Inches(6.93), Inches(9.0), Inches(0.35))
    tf_m = meta_box.text_frame
    p_m = tf_m.paragraphs[0]
    p_m.text = "Resonant Tunnelling in Double Barrier Heterostructures | School of Engineering & Technology, BMU"
    p_m.font.name = FONT_SANS
    p_m.font.size = Pt(10)
    p_m.font.color.rgb = C_MUTED

    # Slide Number
    if slide_num:
        num_box = slide.shapes.add_textbox(Inches(10.2), Inches(6.93), Inches(2.333), Inches(0.35))
        tf_n = num_box.text_frame
        p_n = tf_n.paragraphs[0]
        p_n.text = f"Slide {slide_num} of {TOTAL_SLIDES}"
        p_n.alignment = PP_ALIGN.RIGHT
        p_n.font.name = FONT_SANS
        p_n.font.size = Pt(10)
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

add_card(s1, Inches(0.8), Inches(0.8), Inches(11.733), Inches(5.9), bg_color=RGBColor(255, 255, 255), border_color=C_TITLE)

# Super-title
tb = s1.shapes.add_textbox(Inches(1.2), Inches(1.25), Inches(11.0), Inches(0.4))
p = tb.text_frame.paragraphs[0]
p.text = "BML MUNJAL UNIVERSITY   •   SCHOOL OF ENGINEERING & TECHNOLOGY"
p.font.name = FONT_SANS
p.font.size = Pt(12)
p.font.bold = True
p.font.color.rgb = C_MUTED
p.alignment = PP_ALIGN.CENTER

# Main Title (Large, 30pt & 21pt)
tb = s1.shapes.add_textbox(Inches(1.2), Inches(1.8), Inches(11.0), Inches(1.5))
tb.text_frame.word_wrap = True
p = tb.text_frame.paragraphs[0]
p.text = "Resonant Tunnelling in a Double-Barrier Structure"
p.font.name = FONT_SERIF
p.font.size = Pt(32)
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
div = s1.shapes.add_shape(MSO_SHAPE.RECTANGLE, Inches(4.5), Inches(3.55), Inches(4.333), Inches(0.025))
div.fill.solid()
div.fill.fore_color.rgb = C_TITLE
div.line.color.rgb = C_TITLE

# Authors Block (Prominent, 17pt)
tb = s1.shapes.add_textbox(Inches(1.2), Inches(3.8), Inches(11.0), Inches(0.9))
p = tb.text_frame.paragraphs[0]
p.text = "PROJECT AUTHORS"
p.font.name = FONT_SANS
p.font.size = Pt(11)
p.font.bold = True
p.font.color.rgb = C_MUTED
p.alignment = PP_ALIGN.CENTER

p2 = tb.text_frame.add_paragraph()
p2.text = "Mohammad Azmal Shah   •   Pavan Karthik   •   Anant Goel   •   Darshan Mittal"
p2.font.name = FONT_SERIF
p2.font.size = Pt(17)
p2.font.bold = True
p2.font.color.rgb = C_TITLE
p2.alignment = PP_ALIGN.CENTER

# Links Card
tb = s1.shapes.add_textbox(Inches(1.2), Inches(5.0), Inches(11.0), Inches(1.2))
tf = tb.text_frame
p = tf.paragraphs[0]
p.text = "GitHub Repository: https://github.com/Anantgoel2005/double-barrier-simulation"
p.font.name = FONT_SANS
p.font.size = Pt(11.5)
p.font.color.rgb = C_BODY
p.alignment = PP_ALIGN.CENTER

p2 = tf.add_paragraph()
p2.text = "Live Interactive 3D WebGL Simulation: https://anantgoel2005.github.io/double-barrier-simulation/"
p2.font.name = FONT_SANS
p2.font.size = Pt(11.5)
p2.font.bold = True
p2.font.color.rgb = C_TITLE
p2.alignment = PP_ALIGN.CENTER

# =============================================================
# SLIDE 2: MOTIVATION & PROBLEM STATEMENT
# =============================================================
s2 = prs.slides.add_slide(blank_layout)
add_header(s2, "Motivation: Overcoming Classical Drift Limits", "PROJECT BACKGROUND", 2)

col_w = Inches(3.64)
col_h = Inches(5.1)

# Card 1: Classical Limits
add_card(s2, Inches(0.8), Inches(1.6), col_w, col_h)
tb = s2.shapes.add_textbox(Inches(1.0), Inches(1.8), col_w - Inches(0.4), col_h - Inches(0.4))
tf = tb.text_frame
tf.word_wrap = True
p = tf.paragraphs[0]
p.text = "1. Classical Drift Limits"
p.font.name = FONT_SERIF
p.font.size = Pt(19)
p.font.bold = True
p.font.color.rgb = C_TITLE

bullets1 = [
    ("Velocity Saturation:", "Drift velocity saturates at ~10⁷ cm/s, imposing transit delays."),
    ("Frequency Ceiling:", "Conventional transistors (HEMTs, BJTs) cutoff below 500 GHz."),
    ("Leakage & Scaling:", "Direct gate tunneling and 60 mV/dec subthreshold limit CMOS.")
]
for title, desc in bullets1:
    p = tf.add_paragraph()
    p.space_before = Pt(14)
    p.text = f"• {title}\n  "
    p.font.name = FONT_SANS
    p.font.size = Pt(14)
    p.font.bold = True
    p.font.color.rgb = C_TITLE
    run = p.add_run()
    run.text = desc
    run.font.bold = False
    run.font.color.rgb = C_BODY

# Card 2: Quantum Solution
add_card(s2, Inches(4.84), Inches(1.6), col_w, col_h)
tb = s2.shapes.add_textbox(Inches(5.04), Inches(1.8), col_w - Inches(0.4), col_h - Inches(0.4))
tf = tb.text_frame
tf.word_wrap = True
p = tf.paragraphs[0]
p.text = "2. The Quantum Solution"
p.font.name = FONT_SERIF
p.font.size = Pt(19)
p.font.bold = True
p.font.color.rgb = C_TITLE

bullets2 = [
    ("Resonant Tunneling:", "Exploits wave interference rather than suppressing it."),
    ("Femtosecond Lifetime:", "Quasi-bound dwell time τ ~ 164 fs enables THz operation."),
    ("Coherent Phase Match:", "Round-trip interference yields near-unity transmission (T → 1.0).")
]
for title, desc in bullets2:
    p = tf.add_paragraph()
    p.space_before = Pt(14)
    p.text = f"• {title}\n  "
    p.font.name = FONT_SANS
    p.font.size = Pt(14)
    p.font.bold = True
    p.font.color.rgb = C_TITLE
    run = p.add_run()
    run.text = desc
    run.font.bold = False
    run.font.color.rgb = C_BODY

# Card 3: Technological Impact
add_card(s2, Inches(8.88), Inches(1.6), col_w, col_h)
tb = s2.shapes.add_textbox(Inches(9.08), Inches(1.8), col_w - Inches(0.4), col_h - Inches(0.4))
tf = tb.text_frame
tf.word_wrap = True
p = tf.paragraphs[0]
p.text = "3. Macroscopic NDR Impact"
p.font.name = FONT_SERIF
p.font.size = Pt(19)
p.font.bold = True
p.font.color.rgb = C_TITLE

bullets3 = [
    ("Negative Resistance:", "dI/dV < 0 enables direct microwave & THz amplification."),
    ("Record THz Oscillators:", "Fundamental RTD oscillators achieve > 1.98 THz at 300 K."),
    ("Multi-Valued Logic:", "Single 2-terminal device replaces multi-transistor memory cells.")
]
for title, desc in bullets3:
    p = tf.add_paragraph()
    p.space_before = Pt(14)
    p.text = f"• {title}\n  "
    p.font.name = FONT_SANS
    p.font.size = Pt(14)
    p.font.bold = True
    p.font.color.rgb = C_TITLE
    run = p.add_run()
    run.text = desc
    run.font.bold = False
    run.font.color.rgb = C_BODY

# =============================================================
# SLIDE 3: PROJECT OBJECTIVES & KEY DELIVERABLES
# =============================================================
s3 = prs.slides.add_slide(blank_layout)
add_header(s3, "Project Objectives & Key Deliverables", "GOALS & METHODOLOGY", 3)

objectives = [
    ("1. Exact Quantum Transport Solver (TMM)", 
     "Formulate the Transfer Matrix Method with BenDaniel-Duke boundary conditions for variable effective mass m*(x) under arbitrary applied bias Va."),
    ("2. Parametric Sensitivity Sweeps",
     "Systematically quantify how barrier height (V₀), barrier thickness (Lb), and well width (Lw) govern transmission spectra T(E), resonance linewidth (Γ), and lifetime (τ)."),
    ("3. Resonant Tunnelling Diode (RTD) I-V Solver",
     "Implement the macroscopic Tsu-Esaki current density formula at 300 K, extracting peak current J_peak, valley current J_valley, and PVCR."),
    ("4. Dynamic 3D Time-Dependent Wavepacket Simulation",
     "Develop a dynamic Split-Step Fourier Method (SSFM) solver to visualize cavity standing-wave buildup on resonance vs. total reflection off resonance."),
    ("5. Tri-Platform Open-Source Release",
     "Package the code into an interactive 3D WebGL web app on GitHub Pages, a zero-dependency Python desktop GUI, and an automated MATLAB research suite.")
]

y_pos = Inches(1.58)
for title, desc in objectives:
    add_card(s3, Inches(0.8), y_pos, Inches(11.733), Inches(0.95))
    tb = s3.shapes.add_textbox(Inches(1.05), y_pos + Inches(0.08), Inches(11.2), Inches(0.8))
    tf = tb.text_frame
    tf.word_wrap = True
    p = tf.paragraphs[0]
    p.text = title
    p.font.name = FONT_SERIF
    p.font.size = Pt(16)
    p.font.bold = True
    p.font.color.rgb = C_TITLE
    
    p2 = tf.add_paragraph()
    p2.text = desc
    p2.font.name = FONT_SANS
    p2.font.size = Pt(13)
    p2.font.color.rgb = C_BODY
    y_pos += Inches(1.03)

# =============================================================
# SLIDE 4: LITERATURE SURVEY & MILESTONES
# =============================================================
s4 = prs.slides.add_slide(blank_layout)
add_header(s4, "Literature Survey & Milestone Historical Studies", "LITERATURE REVIEW", 4)

rows = [
    ["Reference", "Focus / Structure", "Key Contribution", "Relevance to Project"],
    ["L. Esaki & R. Tsu (1970)", "Semiconductor superlattices", "Predicted quantum size effects and negative differential conductivity", "Theoretical foundation of engineered potential barriers"],
    ["R. Tsu & L. Esaki (1973)", "Finite superlattice tunneling", "Derived standard electrical tunneling current integral formula", "Exact formulation implemented in our RTD I-V solver"],
    ["L. L. Chang et al. (1974)", "GaAs/AlGaAs double barrier", "First experimental measurement of resonant tunneling and NDR", "Provides baseline physical parameters for GaAs/AlGaAs"],
    ["D. BenDaniel & C. Duke (1966)", "Heterointerface boundary", "Derived current-conserving boundary conditions for variable m*(x)", "Exact matching conditions implemented in our TMM matrix"],
    ["S. Suzuki & M. Asada (2022)", "InP RTD THz oscillators", "Achieved fundamental room-temperature continuous oscillation at 1.98 THz", "Validates modern practical applications in THz sources"]
]

table_shape = s4.shapes.add_table(len(rows), 4, Inches(0.8), Inches(1.65), Inches(11.733), Inches(4.9))
table = table_shape.table

col_widths = [Inches(2.6), Inches(2.6), Inches(3.6), Inches(2.933)]
for i, w in enumerate(col_widths):
    table.columns[i].width = w

for r_idx, row in enumerate(rows):
    for c_idx, val in enumerate(row):
        cell = table.cell(r_idx, c_idx)
        cell.text = val
        p = cell.text_frame.paragraphs[0]
        if r_idx == 0:
            p.font.name = FONT_SANS
            p.font.size = Pt(13)
            p.font.bold = True
            p.font.color.rgb = RGBColor(255, 255, 255)
            cell.fill.solid()
            cell.fill.fore_color.rgb = C_TITLE
        else:
            p.font.name = FONT_SANS
            p.font.size = Pt(12)
            p.font.color.rgb = C_BODY
            cell.fill.solid()
            cell.fill.fore_color.rgb = RGBColor(255, 255, 255) if r_idx % 2 == 1 else RGBColor(248, 249, 250)

# =============================================================
# SLIDE 5: FABRY-PÉROT ANALOGY & WORKING PRINCIPLE
# =============================================================
s5 = prs.slides.add_slide(blank_layout)
add_header(s5, "Working Principle: The Fabry-Pérot Analogy", "PHYSICAL MECHANISM", 5)

# Left Side: Explanation Card
add_card(s5, Inches(0.8), Inches(1.6), Inches(5.6), Inches(5.1))
tb = s5.shapes.add_textbox(Inches(1.05), Inches(1.8), Inches(5.1), Inches(4.7))
tf = tb.text_frame
tf.word_wrap = True

p = tf.paragraphs[0]
p.text = "de Broglie Wave Interference"
p.font.name = FONT_SERIF
p.font.size = Pt(18)
p.font.bold = True
p.font.color.rgb = C_TITLE

points = [
    ("Optical Analogy:", "Double barriers act as partially reflective quantum mirrors, forming a resonant cavity."),
    ("Phase Matching:", "Constructive interference occurs when round-trip phase satisfies: 2 kw Lw + φ₁ + φ₂ = 2 π n"),
    ("Cavity Amplification:", "At resonance E₁, standing-wave probability density |ψ|² inside the well amplifies by > 54×."),
    ("Near-Unity Transmission:", "Despite thick barriers, coherent constructive interference drives transmission T → 1.00."),
    ("Off-Resonance Quenching:", "Electrons with E ≠ E₁ undergo destructive interference, causing > 99% barrier reflection.")
]

for title, desc in points:
    p = tf.add_paragraph()
    p.space_before = Pt(11)
    p.text = f"• {title} "
    p.font.name = FONT_SANS
    p.font.size = Pt(13)
    p.font.bold = True
    p.font.color.rgb = C_TITLE
    run = p.add_run()
    run.text = desc
    run.font.bold = False
    run.font.color.rgb = C_BODY

# Right Side: Figure 1
s5.shapes.add_picture('slide_figures/fig1_potential_profile.png', Inches(6.6), Inches(1.6), width=Inches(5.933))

# =============================================================
# SLIDE 6: THEORETICAL METHODOLOGY: TMM
# =============================================================
s6 = prs.slides.add_slide(blank_layout)
add_header(s6, "Methodology: Transfer Matrix Method (TMM)", "THEORETICAL METHODOLOGY", 6)

add_card(s6, Inches(0.8), Inches(1.6), Inches(11.733), Inches(1.55))
tb = s6.shapes.add_textbox(Inches(1.05), Inches(1.75), Inches(11.2), Inches(1.3))
tf = tb.text_frame
tf.word_wrap = True
p = tf.paragraphs[0]
p.text = "1. BenDaniel-Duke 1D Effective-Mass Equation"
p.font.name = FONT_SERIF
p.font.size = Pt(16)
p.font.bold = True
p.font.color.rgb = C_TITLE

p2 = tf.add_paragraph()
p2.text = "-(ħ² / 2) (d/dx) [ (1 / m*(x)) (dψ/dx) ] + V(x) ψ(x) = E ψ(x)"
p2.font.name = FONT_SERIF
p2.font.size = Pt(14)
p2.font.bold = True
p2.font.color.rgb = RGBColor(17, 24, 39)

p3 = tf.add_paragraph()
p3.text = "• Boundary Matching: Continuity of ψ(x) and (1/m*)(dψ/dx) across heterojunctions strictly conserves quantum probability flux."
p3.font.name = FONT_SANS
p3.font.size = Pt(13)
p3.font.color.rgb = C_BODY

add_card(s6, Inches(0.8), Inches(3.35), Inches(11.733), Inches(1.6))
tb = s6.shapes.add_textbox(Inches(1.05), Inches(3.5), Inches(11.2), Inches(1.35))
tf = tb.text_frame
tf.word_wrap = True
p = tf.paragraphs[0]
p.text = "2. Piecewise Discretization & Sinc Stabilization"
p.font.name = FONT_SERIF
p.font.size = Pt(16)
p.font.bold = True
p.font.color.rgb = C_TITLE

p2 = tf.add_paragraph()
p2.text = "M_j = [ [ cos(k_j Δx),  (m*_j / k_j) sin(k_j Δx) ],  [ -(k_j / m*_j) sin(k_j Δx),  cos(k_j Δx) ] ]"
p2.font.name = FONT_SERIF
p2.font.size = Pt(13)
p2.font.bold = True
p2.font.color.rgb = RGBColor(17, 24, 39)

p3 = tf.add_paragraph()
p3.text = "• Sinc Taylor Series: Evaluates sin(kj Δx)/kj via Δx - (kj² Δx³ / 6) when E → Vj, eliminating 0/0 numerical floating-point errors."
p3.font.name = FONT_SANS
p3.font.size = Pt(13)
p3.font.color.rgb = C_BODY

add_card(s6, Inches(0.8), Inches(5.15), Inches(11.733), Inches(1.55))
tb = s6.shapes.add_textbox(Inches(1.05), Inches(5.3), Inches(11.2), Inches(1.3))
tf = tb.text_frame
tf.word_wrap = True
p = tf.paragraphs[0]
p.text = "3. Matrix Cascading & Transmission Formula"
p.font.name = FONT_SERIF
p.font.size = Pt(16)
p.font.bold = True
p.font.color.rgb = C_TITLE

p2 = tf.add_paragraph()
p2.text = "M_tot = M_N ··· M_1,     T(E) = [ (Re(k_R)/m*_R) / (k_L/m*_L) ] |t|²,     T(E) + R(E) = 1.0000"
p2.font.name = FONT_SERIF
p2.font.size = Pt(13)
p2.font.bold = True
p2.font.color.rgb = RGBColor(17, 24, 39)

p3 = tf.add_paragraph()
p3.text = "• Global Matrix: Multiplies layer matrices sequentially to solve exact transmission across arbitrary tilted band profiles."
p3.font.name = FONT_SANS
p3.font.size = Pt(13)
p3.font.color.rgb = C_BODY

# =============================================================
# SLIDE 7: THEORETICAL METHODOLOGY: TSU-ESAKI & SSFM DYNAMICS
# =============================================================
s7 = prs.slides.add_slide(blank_layout)
add_header(s7, "Methodology: Tsu-Esaki Transport & Dynamic SSFM", "THEORETICAL METHODOLOGY", 7)

w_col = Inches(5.7)

# Col 1: Tsu-Esaki
add_card(s7, Inches(0.8), Inches(1.6), w_col, Inches(5.1))
tb = s7.shapes.add_textbox(Inches(1.05), Inches(1.8), w_col - Inches(0.4), Inches(4.7))
tf = tb.text_frame
tf.word_wrap = True

p = tf.paragraphs[0]
p.text = "Tsu-Esaki Diode Current Density"
p.font.name = FONT_SERIF
p.font.size = Pt(18)
p.font.bold = True
p.font.color.rgb = C_TITLE

p2 = tf.add_paragraph()
p2.space_before = Pt(8)
p2.text = "J(Va) = [ e m* k_B T / (2 π² ħ³) ] ∫ T(E, Va) · Supply(E, Va) dE"
p2.font.name = FONT_SERIF
p2.font.size = Pt(13)
p2.font.bold = True
p2.font.color.rgb = RGBColor(17, 24, 39)

bullets_te = [
    ("Transverse Supply Integration:", "Integrates 1D transmission T(E, Va) against 2D Fermi electron supplies in the leads."),
    ("Room Temperature (300 K):", "k_B T ≈ 25.85 meV introduces realistic thermal carrier broadening."),
    ("Resonant Peak Surge:", "When Va pulls E₁ into the emitter Fermi sea, current density surges to maximum J_peak."),
    ("NDR Quenching:", "When E₁ drops below emitter conduction band edge, current plummets abruptly (dI/dV < 0).")
]
for title, desc in bullets_te:
    p = tf.add_paragraph()
    p.space_before = Pt(10)
    p.text = f"• {title} "
    p.font.name = FONT_SANS
    p.font.size = Pt(13)
    p.font.bold = True
    p.font.color.rgb = C_TITLE
    run = p.add_run()
    run.text = desc
    run.font.bold = False
    run.font.color.rgb = C_BODY

# Col 2: SSFM TDSE
add_card(s7, Inches(6.833), Inches(1.6), w_col, Inches(5.1))
tb = s7.shapes.add_textbox(Inches(7.083), Inches(1.8), w_col - Inches(0.4), Inches(4.7))
tf = tb.text_frame
tf.word_wrap = True

p = tf.paragraphs[0]
p.text = "Split-Step Fourier Method (TDSE)"
p.font.name = FONT_SERIF
p.font.size = Pt(18)
p.font.bold = True
p.font.color.rgb = C_TITLE

p2 = tf.add_paragraph()
p2.space_before = Pt(8)
p2.text = "Ψ(t+Δt) ≈ e^(-i V Δt / 2ħ) F⁻¹[ e^(-i ħ k² Δt / 2m*) F[ e^(-i V Δt / 2ħ) Ψ ] ]"
p2.font.name = FONT_SERIF
p2.font.size = Pt(13)
p2.font.bold = True
p2.font.color.rgb = RGBColor(17, 24, 39)

bullets_ssfm = [
    ("Symmetric Strang Splitting:", "Splits kinetic and potential operators with second-order O(Δt³) local accuracy."),
    ("Dual-Domain Execution:", "Potential rotation in real space (x, y); kinetic dispersion in wavevector space (kx, ky) via FFT."),
    ("Unconditionally Unitary:", "Preserves total wavefunction probability norm ∫|Ψ|² dx = 1.0000 exactly across all time steps."),
    ("Real-Time Wavepacket Dynamics:", "Directly animates wavepacket collision, standing-wave formation, and transmitted pulse train.")
]
for title, desc in bullets_ssfm:
    p = tf.add_paragraph()
    p.space_before = Pt(10)
    p.text = f"• {title} "
    p.font.name = FONT_SANS
    p.font.size = Pt(13)
    p.font.bold = True
    p.font.color.rgb = C_TITLE
    run = p.add_run()
    run.text = desc
    run.font.bold = False
    run.font.color.rgb = C_BODY

# =============================================================
# SLIDE 8: RESULTS: TRANSMISSION SPECTRUM & METRICS
# =============================================================
s8 = prs.slides.add_slide(blank_layout)
add_header(s8, "Results: Transmission Spectrum & Resonant States", "SIMULATION RESULTS", 8)

# Left Side: Figure 2
s8.shapes.add_picture('slide_figures/fig2_transmission_spectrum.png', Inches(0.8), Inches(1.6), width=Inches(5.733))

# Right Side: 4 Metric Cards
right_x = Inches(6.8)
cards_data = [
    ("Resonant Energy (E₁)", "88.0 meV", "Lowest quasi-bound quantum well eigenstate"),
    ("Linewidth (Γ at FWHM)", "4.0 meV", "Broadening due to finite barrier coupling"),
    ("Dwell Lifetime (τ)", "164.7 fs", "Mean particle dwell time in cavity (τ = ħ / Γ)"),
    ("Quality Factor & Buildup", "Q = 22.0  |  54.2×", "Near-unity transmission (T → 1.00) & internal buildup")
]

y_pos = Inches(1.6)
for title, val, sub in cards_data:
    add_card(s8, right_x, y_pos, Inches(5.733), Inches(1.18))
    tb = s8.shapes.add_textbox(right_x + Inches(0.25), y_pos + Inches(0.08), Inches(5.2), Inches(1.0))
    tf = tb.text_frame
    tf.word_wrap = True
    p = tf.paragraphs[0]
    p.text = title
    p.font.name = FONT_SANS
    p.font.size = Pt(12)
    p.font.bold = True
    p.font.color.rgb = C_MUTED
    
    p2 = tf.add_paragraph()
    p2.text = val
    p2.font.name = FONT_SERIF
    p2.font.size = Pt(21)
    p2.font.bold = True
    p2.font.color.rgb = C_TITLE
    
    p3 = tf.add_paragraph()
    p3.text = sub
    p3.font.name = FONT_SANS
    p3.font.size = Pt(11)
    p3.font.color.rgb = C_BODY
    y_pos += Inches(1.3)

# =============================================================
# SLIDE 9: RESULTS: PARAMETRIC SENSITIVITY SWEEPS
# =============================================================
s9 = prs.slides.add_slide(blank_layout)
add_header(s9, "Results: Parametric Sensitivity Analysis", "SIMULATION RESULTS", 9)

c_w = Inches(3.64)
c_h = Inches(5.1)

# 1. Barrier Height V0
add_card(s9, Inches(0.8), Inches(1.6), c_w, c_h)
tb = s9.shapes.add_textbox(Inches(1.05), Inches(1.8), c_w - Inches(0.4), c_h - Inches(0.4))
tf = tb.text_frame
tf.word_wrap = True
p = tf.paragraphs[0]
p.text = "1. Barrier Height (V₀)"
p.font.name = FONT_SERIF
p.font.size = Pt(19)
p.font.bold = True
p.font.color.rgb = C_TITLE

points_v0 = [
    ("Sweep Range:", "0.20 eV to 0.60 eV (Al fraction x = 0.2 to 0.6)."),
    ("Attenuation Parameter:", "κ = [2 mb*(V₀ - E)]¹/² / ħ increases monotonically."),
    ("Leakage Suppression:", "Exponential suppression of sub-barrier leakage below 10⁻⁶."),
    ("State Confinement:", "Higher barriers elevate E₁ due to reduced evanescent penetration.")
]
for title, desc in points_v0:
    p = tf.add_paragraph()
    p.space_before = Pt(12)
    p.text = f"• {title}\n  "
    p.font.name = FONT_SANS
    p.font.size = Pt(13)
    p.font.bold = True
    p.font.color.rgb = C_TITLE
    run = p.add_run()
    run.text = desc
    run.font.bold = False
    run.font.color.rgb = C_BODY

# 2. Barrier Thickness Lb
add_card(s9, Inches(4.84), Inches(1.6), c_w, c_h)
tb = s9.shapes.add_textbox(Inches(5.09), Inches(1.8), c_w - Inches(0.4), c_h - Inches(0.4))
tf = tb.text_frame
tf.word_wrap = True
p = tf.paragraphs[0]
p.text = "2. Barrier Thickness (Lb)"
p.font.name = FONT_SERIF
p.font.size = Pt(19)
p.font.bold = True
p.font.color.rgb = C_TITLE

points_lb = [
    ("Sweep Range:", "1.5 nm to 4.5 nm."),
    ("Exponential Linewidth:", "Linewidth scales as Γ ∝ exp(-2 κ Lb)."),
    ("Drastic Narrowing:", "Increasing Lb from 2 to 4 nm narrows Γ from 18.5 meV to 0.85 meV."),
    ("Lifetime Trade-off:", "Dwell time τ expands from 35.6 fs to 774.5 fs (speed vs. current trade-off).")
]
for title, desc in points_lb:
    p = tf.add_paragraph()
    p.space_before = Pt(12)
    p.text = f"• {title}\n  "
    p.font.name = FONT_SANS
    p.font.size = Pt(13)
    p.font.bold = True
    p.font.color.rgb = C_TITLE
    run = p.add_run()
    run.text = desc
    run.font.bold = False
    run.font.color.rgb = C_BODY

# 3. Well Width Lw
add_card(s9, Inches(8.88), Inches(1.6), c_w, c_h)
tb = s9.shapes.add_textbox(Inches(9.13), Inches(1.8), c_w - Inches(0.4), c_h - Inches(0.4))
tf = tb.text_frame
tf.word_wrap = True
p = tf.paragraphs[0]
p.text = "3. Well Width (Lw)"
p.font.name = FONT_SERIF
p.font.size = Pt(19)
p.font.bold = True
p.font.color.rgb = C_TITLE

points_lw = [
    ("Sweep Range:", "3.0 nm to 8.0 nm."),
    ("Quantum Well Scaling:", "Eigen-energies scale as En ∝ 1 / Lw²."),
    ("Red Shift:", "Expanding Lw from 3 to 6 nm lowers E₁ from 145 meV to 62 meV."),
    ("Higher Harmonic States:", "For Lw > 6.5 nm, higher-order states (E₂, E₃) enter the well.")
]
for title, desc in points_lw:
    p = tf.add_paragraph()
    p.space_before = Pt(12)
    p.text = f"• {title}\n  "
    p.font.name = FONT_SANS
    p.font.size = Pt(13)
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
add_header(s10, "Results: RTD Electrical Transport & NDR Regimes", "ELECTRICAL TRANSPORT", 10)

# Left Side: Figure 3
s10.shapes.add_picture('slide_figures/fig3_rtd_iv_curve.png', Inches(0.8), Inches(1.6), width=Inches(5.733))

# Right Side: 4 Operating Regimes
right_x = Inches(6.8)
add_card(s10, right_x, Inches(1.6), Inches(5.733), Inches(5.1))

tb = s10.shapes.add_textbox(right_x + Inches(0.25), Inches(1.8), Inches(5.2), Inches(4.7))
tf = tb.text_frame
tf.word_wrap = True

p = tf.paragraphs[0]
p.text = "Four Operational Transport Regimes"
p.font.name = FONT_SERIF
p.font.size = Pt(18)
p.font.bold = True
p.font.color.rgb = C_TITLE

regimes = [
    ("1. Equilibrium (Va = 0 V):", "J = 0. Well bound state E₁ = 88 meV sits above the emitter Fermi sea (E_F = 40 meV)."),
    ("2. Resonant Current Surge:", "Peak: J_peak = 1.18 × 10⁵ A/cm² at V_peak = 0.140 V. Bias aligns E₁ with occupied emitter states."),
    ("3. NDR Region (0.14 V < Va < 0.20 V):", "Negative Differential Resistance (dI/dV < 0). E₁ drops below conduction band edge, abruptly quenching tunneling."),
    ("4. Valley Point & PVCR:", "J_valley = 1.74 × 10⁴ A/cm² at Va = 0.20 V, achieving PVCR = 6.78 at room temperature (300 K).")
]

for title, desc in regimes:
    p = tf.add_paragraph()
    p.space_before = Pt(12)
    p.text = f"• {title} "
    p.font.name = FONT_SANS
    p.font.size = Pt(13)
    p.font.bold = True
    p.font.color.rgb = C_TITLE
    run = p.add_run()
    run.text = desc
    run.font.bold = False
    run.font.color.rgb = C_BODY

# =============================================================
# SLIDE 11: RESULTS: DYNAMIC WAVEPACKET SIMULATION
# =============================================================
s11 = prs.slides.add_slide(blank_layout)
add_header(s11, "Results: Dynamic 3D Wavepacket Simulation", "DYNAMIC SIMULATION", 11)

# Left Side: Figure 4
s11.shapes.add_picture('slide_figures/fig4_wavepacket_comparison.png', Inches(0.8), Inches(1.6), width=Inches(5.733))

# Right Side: Physics Description
right_x = Inches(6.8)
add_card(s11, right_x, Inches(1.6), Inches(5.733), Inches(5.1))

tb = s11.shapes.add_textbox(right_x + Inches(0.25), Inches(1.8), Inches(5.2), Inches(4.7))
tf = tb.text_frame
tf.word_wrap = True

p = tf.paragraphs[0]
p.text = "Wavepacket Collision & Trapping Dynamics"
p.font.name = FONT_SERIF
p.font.size = Pt(18)
p.font.bold = True
p.font.color.rgb = C_TITLE

wp_points = [
    ("Incident Gaussian Pulse:", "Initialized in emitter lead with central energy E₀: Ψ(x, 0) = (2πσ²)⁻¹/⁴ exp[-(x - x₀)² / 4σ²] exp(i k₀ x)."),
    ("On-Resonance Dynamics (E₀ = 88 meV):", "Wavepacket splits at first barrier; multiple internal reflections establish a standing wave over t ≈ 50–120 fs, and coherent pulses transmit into collector."),
    ("Off-Resonance Dynamics (E₀ = 44 meV):", "Over 99% of probability density reflects off the first barrier; cavity penetration is negligible (|ψ|² < 10⁻⁴)."),
    ("3D Potential Landscape:", "Simulates real-time Stark band slanting, dynamically tuning resonance into and out of alignment.")
]

for title, desc in wp_points:
    p = tf.add_paragraph()
    p.space_before = Pt(12)
    p.text = f"• {title} "
    p.font.name = FONT_SANS
    p.font.size = Pt(13)
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
add_header(s12, "Multi-Platform Software Implementation", "SYSTEM ARCHITECTURE", 12)

c_w = Inches(3.64)
c_h = Inches(5.1)

# Tier 1: WebGL
add_card(s12, Inches(0.8), Inches(1.6), c_w, c_h)
tb = s12.shapes.add_textbox(Inches(1.05), Inches(1.8), c_w - Inches(0.4), c_h - Inches(0.4))
tf = tb.text_frame
tf.word_wrap = True
p = tf.paragraphs[0]
p.text = "1. Interactive 3D Web App"
p.font.name = FONT_SERIF
p.font.size = Pt(18)
p.font.bold = True
p.font.color.rgb = C_TITLE

points_web = [
    ("Platform:", "Modern web browsers (Desktop & Mobile) hosted on GitHub Pages."),
    ("Rendering Engine:", "WebGL / Three.js 3D quantum cavity with Canvas 3D fallback."),
    ("Real-Time Controls:", "Interactive sliders for V₀, Lb, Lw, Va, and electron energy E."),
    ("Live Deployment:", "anantgoel2005.github.io/double-barrier-simulation/")
]
for title, desc in points_web:
    p = tf.add_paragraph()
    p.space_before = Pt(14)
    p.text = f"• {title}\n  "
    p.font.name = FONT_SANS
    p.font.size = Pt(13.5)
    p.font.bold = True
    p.font.color.rgb = C_TITLE
    run = p.add_run()
    run.text = desc
    run.font.bold = False
    run.font.color.rgb = C_BODY

# Tier 2: Python GUI
add_card(s12, Inches(4.84), Inches(1.6), c_w, c_h)
tb = s12.shapes.add_textbox(Inches(5.09), Inches(1.8), c_w - Inches(0.4), c_h - Inches(0.4))
tf = tb.text_frame
tf.word_wrap = True
p = tf.paragraphs[0]
p.text = "2. Desktop Python GUI"
p.font.name = FONT_SERIF
p.font.size = Pt(18)
p.font.bold = True
p.font.color.rgb = C_TITLE

points_py = [
    ("Zero Dependencies:", "Pure Python standard library (tkinter, math, cmath). Zero pip packages needed."),
    ("4-Quadrant Dashboard:", "Potential Profile, Transmission T(E), RTD I-V, and 3D Wireframe Cavity."),
    ("High Performance:", "Optimized pure-Python complex matrix multiplication & 3D projection."),
    ("1-Click Launch:", "Run via python rtd_gui_python.py or batch file.")
]
for title, desc in points_py:
    p = tf.add_paragraph()
    p.space_before = Pt(14)
    p.text = f"• {title}\n  "
    p.font.name = FONT_SANS
    p.font.size = Pt(13.5)
    p.font.bold = True
    p.font.color.rgb = C_TITLE
    run = p.add_run()
    run.text = desc
    run.font.bold = False
    run.font.color.rgb = C_BODY

# Tier 3: MATLAB Suite
add_card(s12, Inches(8.88), Inches(1.6), c_w, c_h)
tb = s12.shapes.add_textbox(Inches(9.13), Inches(1.8), c_w - Inches(0.4), c_h - Inches(0.4))
tf = tb.text_frame
tf.word_wrap = True
p = tf.paragraphs[0]
p.text = "3. MATLAB Research Suite"
p.font.name = FONT_SERIF
p.font.size = Pt(18)
p.font.bold = True
p.font.color.rgb = C_TITLE

points_mat = [
    ("Core Scripts:", "calculate_tmm.m, calculate_rtd_iv.m, and find_resonance_peaks.m."),
    ("3D Dynamic Solver:", "rtd_3d_wavepacket.m implements Split-Step Fourier TDSE animation."),
    ("3D Energy Landscapes:", "rtd_3d_landscape.m models 2D/3D Stark surfaces under bias."),
    ("Interactive GUI:", "rtd_interactive_app.m provides full slider dashboard.")
]
for title, desc in points_mat:
    p = tf.add_paragraph()
    p.space_before = Pt(14)
    p.text = f"• {title}\n  "
    p.font.name = FONT_SANS
    p.font.size = Pt(13.5)
    p.font.bold = True
    p.font.color.rgb = C_TITLE
    run = p.add_run()
    run.text = desc
    run.font.bold = False
    run.font.color.rgb = C_BODY

# =============================================================
# SLIDE 13: MAIN CONCLUSIONS & PHYSICAL TAKEAWAYS
# =============================================================
s13 = prs.slides.add_slide(blank_layout)
add_header(s13, "Main Conclusions & Physical Insights", "PROJECT CONCLUSIONS", 13)

conclusions = [
    ("1. Verification of Coherent Resonant Tunnelling",
     "The Transfer Matrix Method rigorously proved that constructive phase matching amplifies internal standing-wave probability density by > 54×, yielding near-unity transmission (T → 1.00) at E₁ = 88.0 meV."),
    ("2. Microscopic Origin of Macroscopic NDR",
     "The N-shaped RTD current-voltage curve was quantitatively mapped to sub-band alignment with the emitter Fermi sea, demonstrating J_peak = 1.18 × 10⁵ A/cm² at 0.14 V and PVCR = 6.78 at 300 K."),
    ("3. Fundamental Speed-Current Trade-Off",
     "Quasi-bound dwell lifetime τ = ħ / Γ scales exponentially with barrier thickness Lb. Increasing Lb from 2 to 4 nm narrows Γ from 18.5 to 0.85 meV (expanding τ from 35.6 to 774.5 fs)."),
    ("4. Open-Source Multi-Platform Deployment",
     "Bridged theoretical condensed matter physics with interactive visualization by publishing a tri-platform suite: 3D WebGL web app on GitHub Pages, zero-dependency Python desktop GUI, and MATLAB suite.")
]

y_pos = Inches(1.58)
for title, desc in conclusions:
    add_card(s13, Inches(0.8), y_pos, Inches(11.733), Inches(1.18))
    tb = s13.shapes.add_textbox(Inches(1.05), y_pos + Inches(0.08), Inches(11.2), Inches(1.0))
    tf = tb.text_frame
    tf.word_wrap = True
    p = tf.paragraphs[0]
    p.text = title
    p.font.name = FONT_SERIF
    p.font.size = Pt(16)
    p.font.bold = True
    p.font.color.rgb = C_TITLE
    
    p2 = tf.add_paragraph()
    p2.text = desc
    p2.font.name = FONT_SANS
    p2.font.size = Pt(13)
    p2.font.color.rgb = C_BODY
    y_pos += Inches(1.28)

# =============================================================
# SLIDE 14: FUTURE RESEARCH DIRECTIONS (FINAL SLIDE)
# =============================================================
s14 = prs.slides.add_slide(blank_layout)
add_header(s14, "Future Research Scope & Next Extensions", "FUTURE WORK", 14)

future_work = [
    ("1. Self-Consistent Poisson-Schrödinger Solver",
     "Incorporate dynamic space-charge accumulation inside the quantum well cavity to model intrinsic electrostatic bistability, hysteresis loops, and plateau features in the RTD I-V curve."),
    ("2. Non-Equilibrium Green's Function (NEGF) Formalism",
     "Account for dissipative, phase-breaking scattering mechanisms, including longitudinal optical (LO) phonon emission, acoustic phonons, and interface roughness at elevated temperatures."),
    ("3. High-Bandgap-Offset Heterostructure Systems",
     "Investigate InGaAs/AlAs and InAs/AlSb heterostructures with conduction band discontinuities V₀ > 1.2 eV to achieve room-temperature Peak-to-Valley Current Ratios (PVCR > 25) for ultra-fast logic."),
    ("4. Multi-Stage Quantum Cascade Lasers (QCLs)",
     "Extend the single-cavity TMM framework to periodic superlattices (20–50 stages) to model intersubband optical transitions and population inversion for mid-infrared and THz optical sources.")
]

y_pos = Inches(1.58)
for title, desc in future_work:
    add_card(s14, Inches(0.8), y_pos, Inches(11.733), Inches(1.18))
    tb = s14.shapes.add_textbox(Inches(1.05), y_pos + Inches(0.08), Inches(11.2), Inches(1.0))
    tf = tb.text_frame
    tf.word_wrap = True
    p = tf.paragraphs[0]
    p.text = title
    p.font.name = FONT_SERIF
    p.font.size = Pt(16)
    p.font.bold = True
    p.font.color.rgb = C_TITLE
    
    p2 = tf.add_paragraph()
    p2.text = desc
    p2.font.name = FONT_SANS
    p2.font.size = Pt(13)
    p2.font.color.rgb = C_BODY
    y_pos += Inches(1.28)

# -------------------------------------------------------------
# SAVE PRESENTATION
# -------------------------------------------------------------
output_path = "Resonant_Tunnelling_Presentation.pptx"
prs.save(output_path)
print(f"Presentation successfully updated and saved to {output_path} ({len(prs.slides)} slides)")
