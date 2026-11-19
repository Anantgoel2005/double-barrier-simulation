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

    line = slide.shapes.add_shape(
        MSO_SHAPE.RECTANGLE,
        Inches(0.8), Inches(1.38), Inches(11.733), Inches(0.018)
    )
    line.fill.solid()
    line.fill.fore_color.rgb = C_LINE
    line.line.color.rgb = C_LINE

    f_line = slide.shapes.add_shape(
        MSO_SHAPE.RECTANGLE,
        Inches(0.8), Inches(6.85), Inches(11.733), Inches(0.015)
    )
    f_line.fill.solid()
    f_line.fill.fore_color.rgb = C_LINE
    f_line.line.color.rgb = C_LINE

    meta_box = slide.shapes.add_textbox(Inches(0.8), Inches(6.93), Inches(9.0), Inches(0.35))
    tf_m = meta_box.text_frame
    p_m = tf_m.paragraphs[0]
    p_m.text = "Resonant Tunnelling in Double Barrier Heterostructures | School of Engineering & Technology, BMU"
    p_m.font.name = FONT_SANS
    p_m.font.size = Pt(10)
    p_m.font.color.rgb = C_MUTED

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

tb = s1.shapes.add_textbox(Inches(1.2), Inches(1.25), Inches(11.0), Inches(0.4))
p = tb.text_frame.paragraphs[0]
p.text = "BML MUNJAL UNIVERSITY   •   SCHOOL OF ENGINEERING & TECHNOLOGY"
p.font.name = FONT_SANS
p.font.size = Pt(12)
p.font.bold = True
p.font.color.rgb = C_MUTED
p.alignment = PP_ALIGN.CENTER

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

div = s1.shapes.add_shape(MSO_SHAPE.RECTANGLE, Inches(4.5), Inches(3.55), Inches(4.333), Inches(0.025))
div.fill.solid()
div.fill.fore_color.rgb = C_TITLE
div.line.color.rgb = C_TITLE

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
# SLIDE 2: MOTIVATION & PROBLEM STATEMENT (SIMPLIFIED)
# =============================================================
s2 = prs.slides.add_slide(blank_layout)
add_header(s2, "Motivation: Overcoming Classical Drift Limits", "PROJECT BACKGROUND", 2)

col_w = Inches(3.64)
col_h = Inches(3.8)

# Card 1: Classical Limits
add_card(s2, Inches(0.8), Inches(1.6), col_w, col_h)
tb = s2.shapes.add_textbox(Inches(1.0), Inches(1.8), col_w - Inches(0.4), col_h - Inches(0.4))
tf = tb.text_frame
tf.word_wrap = True
p = tf.paragraphs[0]
p.text = "1. Classical Drift Limits"
p.font.name = FONT_SERIF
p.font.size = Pt(18)
p.font.bold = True
p.font.color.rgb = C_TITLE

bullets1 = [
    ("Speed Limit:", "Electrons bump into atoms; drift velocity saturates at ~10⁷ cm/s."),
    ("Frequency Ceiling:", "Normal transistors cannot exceed 500 GHz."),
    ("Scaling Barrier:", "Gate oxide leakage and heat prevent smaller chip scaling.")
]
for title, desc in bullets1:
    p = tf.add_paragraph()
    p.space_before = Pt(10)
    p.text = f"• {title} "
    p.font.name = FONT_SANS
    p.font.size = Pt(13.5)
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
p.font.size = Pt(18)
p.font.bold = True
p.font.color.rgb = C_TITLE

bullets2 = [
    ("Wave Tunnelling:", "Electrons behave like waves and leak straight through thin walls."),
    ("Femtosecond Speed:", "Cavity transit takes only ~164 fs (quadrillionths of a second!)."),
    ("Perfect Flow (T → 1.0):", "Resonant wave alignment makes thick barriers seem invisible.")
]
for title, desc in bullets2:
    p = tf.add_paragraph()
    p.space_before = Pt(10)
    p.text = f"• {title} "
    p.font.name = FONT_SANS
    p.font.size = Pt(13.5)
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
p.font.size = Pt(18)
p.font.bold = True
p.font.color.rgb = C_TITLE

bullets3 = [
    ("Negative Resistance:", "Increasing voltage knocks levels out of sync, abruptly cutting current."),
    ("Record THz Oscillators:", "Generates continuous signals above 1.98 THz for next-gen 6G."),
    ("Compact Logic:", "One diode replaces multi-transistor memory and switching cells.")
]
for title, desc in bullets3:
    p = tf.add_paragraph()
    p.space_before = Pt(10)
    p.text = f"• {title} "
    p.font.name = FONT_SANS
    p.font.size = Pt(13.5)
    p.font.bold = True
    p.font.color.rgb = C_TITLE
    run = p.add_run()
    run.text = desc
    run.font.bold = False
    run.font.color.rgb = C_BODY

# Bottom Layman Callout Card
add_card(s2, Inches(0.8), Inches(5.6), Inches(11.733), Inches(1.05))
tb = s2.shapes.add_textbox(Inches(1.05), Inches(5.7), Inches(11.2), Inches(0.85))
tf = tb.text_frame
tf.word_wrap = True
p = tf.paragraphs[0]
p.text = "IN PLAIN TERMS: WHY THIS MATTERS"
p.font.name = FONT_SANS
p.font.size = Pt(11)
p.font.bold = True
p.font.color.rgb = C_MUTED

p2 = tf.add_paragraph()
p2.text = "Classical chips are bottlenecked because electrons collide with atoms as they drift. By placing two atomic walls just nanometers apart, electrons glide straight through via wave resonance in femtoseconds—making Resonant Tunnelling Diodes the fastest electronic oscillators in the world."
p2.font.name = FONT_SANS
p2.font.size = Pt(12)
p2.font.color.rgb = C_TITLE

# =============================================================
# SLIDE 3: OBJECTIVES (SIMPLIFIED)
# =============================================================
s3 = prs.slides.add_slide(blank_layout)
add_header(s3, "Project Objectives & Key Deliverables", "GOALS & METHODOLOGY", 3)

objectives = [
    ("1. Exact Quantum Transport Modeling", 
     "Mathematically solve electron wave transmission through biased semiconductor barriers using the Transfer Matrix Method (TMM)."),
    ("2. Understand the Three Structural Knobs",
     "Systematically test how changing wall height (V₀), wall thickness (Lb), and room width (Lw) controls speed, leakage, and resonance."),
    ("3. Resonant Tunnelling Diode (RTD) I-V Solver",
     "Calculate actual electrical current at room temperature (300 K) to demonstrate Negative Differential Resistance (dI/dV < 0)."),
    ("4. Dynamic 3D Wavepacket Movie",
     "Simulate moving electron wave packets in real time to visualize cavity trapping on resonance vs. bouncing off when mismatched."),
    ("5. Free Open-Source Tri-Platform Tools",
     "Deliver an interactive 3D WebGL web simulation on GitHub Pages, a zero-dependency Python desktop app, and a complete MATLAB suite.")
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
# SLIDE 4: LITERATURE SURVEY & MILESTONES (SIMPLIFIED)
# =============================================================
s4 = prs.slides.add_slide(blank_layout)
add_header(s4, "Literature Survey & Milestone Studies", "LITERATURE REVIEW", 4)

rows = [
    ["Reference", "Focus / Structure", "Key Breakthrough (In Plain Terms)", "Relevance to Our Work"],
    ["L. Esaki & R. Tsu (1970)", "Semiconductor superlattices", "Predicted that periodic barriers create artificial quantum energy bands", "Foundational theory of engineered quantum barriers"],
    ["R. Tsu & L. Esaki (1973)", "Tunneling current theory", "Derived standard equation connecting quantum transmission to electrical current", "Exact equation used in our RTD current-voltage solver"],
    ["L. L. Chang et al. (1974)", "GaAs/AlGaAs double barrier", "First physical lab demonstration of resonant tunneling and negative resistance", "Provides the baseline material dimensions for our simulation"],
    ["D. BenDaniel & C. Duke (1966)", "Heterointerface boundary", "Formulated matching rules when electron mass changes across barrier boundaries", "Prevents false math artifacts across different materials in TMM"],
    ["S. Suzuki & M. Asada (2022)", "InP RTD THz oscillators", "Built room-temperature oscillators operating up to 1.98 THz using RTDs", "Proves practical industrial use for ultra-fast 6G wireless"]
]

table_shape = s4.shapes.add_table(len(rows), 4, Inches(0.8), Inches(1.65), Inches(11.733), Inches(4.9))
table = table_shape.table

col_widths = [Inches(2.5), Inches(2.4), Inches(4.1), Inches(2.733)]
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
# SLIDE 5: FABRY-PÉROT ANALOGY & WORKING PRINCIPLE (INTUITIVE)
# =============================================================
s5 = prs.slides.add_slide(blank_layout)
add_header(s5, "Working Principle: The Organ Pipe & Quantum Mirror", "PHYSICAL MECHANISM", 5)

add_card(s5, Inches(0.8), Inches(1.6), Inches(5.6), Inches(5.1))
tb = s5.shapes.add_textbox(Inches(1.05), Inches(1.8), Inches(5.1), Inches(4.7))
tf = tb.text_frame
tf.word_wrap = True

p = tf.paragraphs[0]
p.text = "How Does Resonant Tunnelling Work?"
p.font.name = FONT_SERIF
p.font.size = Pt(18)
p.font.bold = True
p.font.color.rgb = C_TITLE

points = [
    ("The Quantum Mirror:", "Two ultra-thin semiconductor walls create a microscopic 'quantum room' (well) between them."),
    ("The Organ Pipe Analogy:", "Just as an organ pipe or guitar string only rings loudly at specific musical notes, the well only accepts electron waves with a matching wavelength."),
    ("Round-Trip Resonance:", "When incoming electron wave energy matches the cavity note (E₁), waves bouncing between the walls interfere constructively: 2 kw Lw + φ₁ + φ₂ = 2 π n"),
    ("Walls Vanish (T → 100%):", "Constructive interference amplifies probability density inside by > 54×, and electrons sail straight through effortlessly!"),
    ("Wrong Note = Bounces Off:", "If the electron energy doesn't match E₁, waves cancel out and > 99% bounces straight back.")
]

for title, desc in points:
    p = tf.add_paragraph()
    p.space_before = Pt(10)
    p.text = f"• {title} "
    p.font.name = FONT_SANS
    p.font.size = Pt(12.5)
    p.font.bold = True
    p.font.color.rgb = C_TITLE
    run = p.add_run()
    run.text = desc
    run.font.bold = False
    run.font.color.rgb = C_BODY

# Right Side: Figure 1
s5.shapes.add_picture('slide_figures/fig1_potential_profile.png', Inches(6.6), Inches(1.6), width=Inches(5.933))

# =============================================================
# SLIDE 6: THEORETICAL METHODOLOGY: TMM (SIMPLIFIED)
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
p3.text = "• Layman Intuition: Describes how electron waves travel through materials where effective mass m* changes. Matching boundary conditions ensures no electrons magically disappear at interfaces."
p3.font.name = FONT_SANS
p3.font.size = Pt(13)
p3.font.color.rgb = C_BODY

add_card(s6, Inches(0.8), Inches(3.35), Inches(11.733), Inches(1.6))
tb = s6.shapes.add_textbox(Inches(1.05), Inches(3.5), Inches(11.2), Inches(1.35))
tf = tb.text_frame
tf.word_wrap = True
p = tf.paragraphs[0]
p.text = "2. Slicing the Barriers & Sinc Stabilization"
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
p3.text = "• Layman Intuition: When a voltage tilts the barriers, we chop the slanted hill into tiny flat steps. When energy exactly matches a step height (E → Vj), Taylor series sinc expansion prevents computer divide-by-zero crashes."
p3.font.name = FONT_SANS
p3.font.size = Pt(13)
p3.font.color.rgb = C_BODY

add_card(s6, Inches(0.8), Inches(5.15), Inches(11.733), Inches(1.55))
tb = s6.shapes.add_textbox(Inches(1.05), Inches(5.3), Inches(11.2), Inches(1.3))
tf = tb.text_frame
tf.word_wrap = True
p = tf.paragraphs[0]
p.text = "3. Multiplying Matrices to Get Tunneling Probability T(E)"
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
p3.text = "• Layman Intuition: Like chaining optical lenses in a camera, multiplying slice matrices directly calculates what percentage of incoming electrons successfully tunnel through to the other side."
p3.font.name = FONT_SANS
p3.font.size = Pt(13)
p3.font.color.rgb = C_BODY

# =============================================================
# SLIDE 7: THEORETICAL METHODOLOGY: TSU-ESAKI & SSFM DYNAMICS
# =============================================================
s7 = prs.slides.add_slide(blank_layout)
add_header(s7, "Methodology: Tsu-Esaki Current & Wavepacket Movie", "THEORETICAL METHODOLOGY", 7)

w_col = Inches(5.7)

# Col 1: Tsu-Esaki
add_card(s7, Inches(0.8), Inches(1.6), w_col, Inches(5.1))
tb = s7.shapes.add_textbox(Inches(1.05), Inches(1.8), w_col - Inches(0.4), Inches(4.7))
tf = tb.text_frame
tf.word_wrap = True

p = tf.paragraphs[0]
p.text = "Calculating Diode Current (Tsu-Esaki)"
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
    ("What the Formula Does:", "Counts all electrons waiting in the emitter lead and calculates total electrical current flowing through the barrier."),
    ("Room Temperature (300 K):", "Accounts for heat thermal energy (25.85 meV) kicking electrons around."),
    ("Current Peak:", "When voltage pulls the well's resonant level into line with the waiting electrons, current shoots up to a maximum."),
    ("Current Drop (NDR):", "Higher voltage knocks the level below the reservoir, shutting off the flow.")
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
p.text = "Wavepacket Movie (Split-Step Fourier)"
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
    ("What the Solver Does:", "Acts like a high-speed quantum video camera, stepping through time (femtoseconds) to track the electron pulse."),
    ("Two-Step Trick:", "Applies barrier potential push in physical space, then flips into frequency space (FFT) to handle wave dispersion."),
    ("100% Probability Conserved:", "No electron disappears into thin air; total probability remains exactly 1.0000 across all time."),
    ("Visual Proof:", "Directly reveals cavity trapping on resonance versus immediate reflection off resonance.")
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
add_header(s8, "Results: Transmission Spectrum & Resonant Peak", "SIMULATION RESULTS", 8)

# Left Side: Figure 2
s8.shapes.add_picture('slide_figures/fig2_transmission_spectrum.png', Inches(0.8), Inches(1.6), width=Inches(5.733))

# Right Side: 4 Metric Cards
right_x = Inches(6.8)
cards_data = [
    ("The Resonant Note (E₁)", "88.0 meV", "Electrons with this exact energy pass through with ~100% transmission."),
    ("Resonance Width (Γ at FWHM)", "4.0 meV", "Defines the sharpness of the energy filter; narrower = sharper filter."),
    ("Cavity Dwell Time (τ)", "164.7 fs", "How long the electron lingers in the cavity (1.65 × 10⁻¹³ s = ultrafast!)."),
    ("Standing Wave Buildup", "54.2× Amplification", "Trapped wave builds up to over 54 times the incident beam intensity (Q = 22.0).")
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
# SLIDE 9: RESULTS: PARAMETRIC SENSITIVITY SWEEPS (3 KNOBS)
# =============================================================
s9 = prs.slides.add_slide(blank_layout)
add_header(s9, "Results: The Three Structural Knobs (In Plain Terms)", "SIMULATION RESULTS", 9)

c_w = Inches(3.64)
c_h = Inches(5.1)

# 1. Barrier Height V0
add_card(s9, Inches(0.8), Inches(1.6), c_w, c_h)
tb = s9.shapes.add_textbox(Inches(1.05), Inches(1.8), c_w - Inches(0.4), c_h - Inches(0.4))
tf = tb.text_frame
tf.word_wrap = True
p = tf.paragraphs[0]
p.text = "1. Wall Height (V₀)"
p.font.name = FONT_SERIF
p.font.size = Pt(19)
p.font.bold = True
p.font.color.rgb = C_TITLE

points_v0 = [
    ("What It Means:", "How tall the energy walls are (tested 0.20 to 0.60 eV)."),
    ("Leakage Stopper:", "Taller walls exponentially block unwanted off-resonance leakage below 10⁻⁶."),
    ("Noise Filter:", "Acts like acoustic soundproofing, preventing unwanted stray electrons from leaking through.")
]
for title, desc in points_v0:
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

# 2. Barrier Thickness Lb
add_card(s9, Inches(4.84), Inches(1.6), c_w, c_h)
tb = s9.shapes.add_textbox(Inches(5.09), Inches(1.8), c_w - Inches(0.4), c_h - Inches(0.4))
tf = tb.text_frame
tf.word_wrap = True
p = tf.paragraphs[0]
p.text = "2. Wall Thickness (Lb)"
p.font.name = FONT_SERIF
p.font.size = Pt(19)
p.font.bold = True
p.font.color.rgb = C_TITLE

points_lb = [
    ("What It Means:", "How thick each barrier wall is (tested 1.5 to 4.5 nm)."),
    ("Sharpness vs. Speed:", "Thicker walls narrow the resonance peak (sharper energy filter) but trap electrons longer."),
    ("The Trade-off:", "Increasing thickness from 2 to 4 nm slows dwell time from 35 fs to 775 fs (trades current for selectivity).")
]
for title, desc in points_lb:
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

# 3. Well Width Lw
add_card(s9, Inches(8.88), Inches(1.6), c_w, c_h)
tb = s9.shapes.add_textbox(Inches(9.13), Inches(1.8), c_w - Inches(0.4), c_h - Inches(0.4))
tf = tb.text_frame
tf.word_wrap = True
p = tf.paragraphs[0]
p.text = "3. Room Width (Lw)"
p.font.name = FONT_SERIF
p.font.size = Pt(19)
p.font.bold = True
p.font.color.rgb = C_TITLE

points_lw = [
    ("What It Means:", "Width of the quantum room between walls (tested 3 to 8 nm)."),
    ("Tuning the Musical Pitch:", "Resonant energy scales as 1/Lw². A wider room lowers the resonant note (from 145 meV down to 62 meV)."),
    ("Harmonic Notes:", "Widening past 6.5 nm fits higher-order resonant states (E₂, E₃) inside the room.")
]
for title, desc in points_lw:
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
# SLIDE 10: RESULTS: RTD I-V CHARACTERISTICS & NDR (INTUITIVE)
# =============================================================
s10 = prs.slides.add_slide(blank_layout)
add_header(s10, "Results: Negative Resistance (The Sweet Spot Switch)", "ELECTRICAL TRANSPORT", 10)

# Left Side: Figure 3
s10.shapes.add_picture('slide_figures/fig3_rtd_iv_curve.png', Inches(0.8), Inches(1.6), width=Inches(5.733))

# Right Side: 4 Operating Regimes
right_x = Inches(6.8)
add_card(s10, right_x, Inches(1.6), Inches(5.733), Inches(5.1))

tb = s10.shapes.add_textbox(right_x + Inches(0.25), Inches(1.8), Inches(5.2), Inches(4.7))
tf = tb.text_frame
tf.word_wrap = True

p = tf.paragraphs[0]
p.text = "How the Negative Resistance Switch Works"
p.font.name = FONT_SERIF
p.font.size = Pt(18)
p.font.bold = True
p.font.color.rgb = C_TITLE

regimes = [
    ("1. Off (0 V):", "No current flows. The internal room energy sits too high above waiting electrons."),
    ("2. Peak Sweet Spot (0.14 V):", "Current surges to 1.18 × 10⁵ A/cm²! Voltage aligns the internal state with incoming electrons, opening the floodgates."),
    ("3. The Drop / NDR (0.14 V - 0.20 V):", "Increasing voltage pushes the state past alignment. Electrons can no longer tunnel, and current abruptly plummets! Turning voltage UP makes current go DOWN (dI/dV < 0)."),
    ("4. Valley Point & PVCR (0.20 V):", "Current drops to 1.74 × 10⁴ A/cm². The Peak-to-Valley ratio is 6.78 at room temperature.")
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
# SLIDE 11: RESULTS: DYNAMIC WAVEPACKET SIMULATION (INTUITIVE)
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
p.text = "Watching the Quantum Wave in Real Time"
p.font.name = FONT_SERIF
p.font.size = Pt(18)
p.font.bold = True
p.font.color.rgb = C_TITLE

wp_points = [
    ("The Moving Wave Packet:", "Represents a single moving electron traveling toward the double barrier structure."),
    ("On-Resonance (Matching Note E = 88 meV):", "• The wave strikes the barrier and enters the room.\n• Internal reflections amplify into a steady standing wave (t ≈ 50–120 fs).\n• A clean, coherent pulse smoothly transmits out the other side."),
    ("Off-Resonance (Mismatched Note E = 44 meV):", "• Like a water wave hitting a concrete seawall, over 99% of the wave splashes straight backwards.\n• Zero standing wave forms inside the room; nothing transmits."),
    ("3D Stark Tilt:", "Applied voltage slants the energy landscape, showing in real time how voltage turns the resonant channel ON or OFF.")
]

for title, desc in wp_points:
    p = tf.add_paragraph()
    p.space_before = Pt(11)
    p.text = f"• {title} "
    p.font.name = FONT_SANS
    p.font.size = Pt(12.5)
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
    ("Zero Setup Needed:", "Runs immediately in any modern browser on phone, tablet, or PC."),
    ("Interactive 3D Cavity:", "Rotate and zoom a 3D WebGL model of the quantum barriers and wavepacket."),
    ("Live Sliders:", "Adjust wall height, thickness, well width, and voltage to see transmission change instantly."),
    ("Try It Live:", "anantgoel2005.github.io/double-barrier-simulation/")
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
    ("No External Packages:", "Built using 100% pure Python standard library (tkinter). No pip installs required!"),
    ("4 Live Dashboards:", "Displays Potential Profile, Transmission T(E), RTD I-V curve, and 3D wireframe."),
    ("Instant Response:", "High-speed complex matrix math renders slider updates smoothly."),
    ("1-Click Launch:", "Double click Launch_Python_GUI.bat on Windows.")
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
    ("Automated Solver Scripts:", "calculate_tmm.m, calculate_rtd_iv.m, and find_resonance_peaks.m."),
    ("3D Wavepacket Movies:", "rtd_3d_wavepacket.m outputs dynamic 3D split-step Fourier simulations."),
    ("Stark Energy Maps:", "rtd_3d_landscape.m models full 3D energy surfaces as bias voltage changes."),
    ("GUI App Included:", "rtd_interactive_app.m provides full slider dashboard.")
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
# SLIDE 13: MAIN CONCLUSIONS & PHYSICAL TAKEAWAYS (SIMPLIFIED)
# =============================================================
s13 = prs.slides.add_slide(blank_layout)
add_header(s13, "Main Conclusions: What We Learned", "PROJECT CONCLUSIONS", 13)

conclusions = [
    ("1. Quantum Waves Can Make Barriers Invisible",
     "Constructive de Broglie wave interference inside a double-barrier cavity amplifies probability by > 54×, allowing electrons with matching energy (88 meV) to pass straight through with near 100% transmission."),
    ("2. Origin of Negative Resistance Discovered",
     "The diode's unique N-shaped curve happens because voltage tunes the well's energy level into alignment (peak current), then pulls it past alignment (sudden current drop), yielding a high PVCR of 6.78."),
    ("3. Speed vs. Selectivity Trade-Off Quantified",
     "Thicker barrier walls create an extremely sharp energy filter, but trap electrons longer (~775 fs). Thinner walls allow lightning-fast switching (~35 fs) with higher current flow."),
    ("4. Complex Physics Made Accessible & Open Source",
     "Bridged theoretical nanoelectronics with intuitive engineering tools: a public GitHub repository, zero-install 3D WebGL web simulation, and lightweight Python GUI.")
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
    ("1. Space Charge & Memory Hysteresis (Poisson-Schrödinger)",
     "Account for electrons piling up inside the quantum well. This trapped charge creates electrostatic memory (hysteresis), enabling ultra-dense quantum memory cells."),
    ("2. Real-World Heat & Vibration Scattering (NEGF)",
     "Incorporate electron collisions with lattice vibrations (phonons) and rough wall edges to model performance at extreme operating temperatures."),
    ("3. Super-High Barriers for 6G Wireless (InGaAs/AlAs)",
     "Explore newer semiconductor alloys with walls over 1.2 eV tall to achieve record Peak-to-Valley ratios (PVCR > 25) for ultra-low-noise terahertz communication chips."),
    ("4. Quantum Cascade Lasers (Multi-Barrier Superlattices)",
     "Stack 20 to 50 barrier cavities in series to create cascading optical transitions, emitting coherent infrared and terahertz laser beams for medical and security imaging.")
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
