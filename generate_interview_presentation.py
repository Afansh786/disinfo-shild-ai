"""
Generator script to build a high-impact, professional 16:9 PowerPoint presentation
for Disinfo Shield AI 2026 Interview Briefing & Technical Defense.
"""
import os
import sys
from pptx import Presentation
from pptx.util import Inches, Pt
from pptx.dml.color import RGBColor
from pptx.enum.text import PP_ALIGN, MSO_ANCHOR
from pptx.enum.shapes import MSO_SHAPE

# ── Color Palette (Cyber / Intelligence Dark Theme) ──────────────────────────
BG_DARK = RGBColor(7, 13, 30)         # #070D1E
CARD_BG = RGBColor(16, 28, 56)        # #101C38
CARD_BG_LIGHT = RGBColor(22, 38, 74)  # #16264A
CARD_BORDER = RGBColor(37, 99, 235)   # #2563EB
TEXT_WHITE = RGBColor(255, 255, 255)  # #FFFFFF
TEXT_LIGHT = RGBColor(241, 245, 249)  # #F1F5F9
TEXT_MUTED = RGBColor(148, 163, 184)  # #94A3B8
TEXT_DIM = RGBColor(100, 116, 139)    # #64748B

ACCENT_BLUE = RGBColor(59, 130, 246)  # #3B82F6
ACCENT_CYAN = RGBColor(6, 182, 212)   # #06B6D4
ACCENT_GREEN = RGBColor(16, 185, 129) # #10B981
ACCENT_AMBER = RGBColor(245, 158, 11) # #F59E0B
ACCENT_RED = RGBColor(239, 68, 68)    # #EF4444
ACCENT_PURPLE = RGBColor(139, 92, 246)# #8B5CF6

FONT_HEADING = "Segoe UI"
FONT_BODY = "Segoe UI"
FONT_MONO = "Consolas"

def create_presentation():
    prs = Presentation()
    prs.slide_width = Inches(13.333)
    prs.slide_height = Inches(7.5)
    blank_layout = prs.slide_layouts[6]  # Blank slide

    def set_slide_background(slide, color=BG_DARK):
        background = slide.background
        fill = background.fill
        fill.solid()
        fill.fore_color.rgb = color

    def add_header(slide, title, category="DISINFO SHIELD AI 2026 // TECHNICAL INTERVIEW BRIEFING", icon_text="🛡️"):
        # Header category tag
        tag_box = slide.shapes.add_textbox(Inches(0.8), Inches(0.4), Inches(11.733), Inches(0.3))
        tf = tag_box.text_frame
        tf.word_wrap = True
        tf.margin_left = tf.margin_top = tf.margin_right = tf.margin_bottom = 0
        p = tf.paragraphs[0]
        p.text = f"{icon_text}  {category}".upper()
        p.font.name = FONT_HEADING
        p.font.size = Pt(11)
        p.font.bold = True
        p.font.color.rgb = ACCENT_CYAN

        # Main slide title
        title_box = slide.shapes.add_textbox(Inches(0.8), Inches(0.72), Inches(11.733), Inches(0.6))
        tf2 = title_box.text_frame
        tf2.word_wrap = True
        tf2.margin_left = tf2.margin_top = tf2.margin_right = tf2.margin_bottom = 0
        p2 = tf2.paragraphs[0]
        p2.text = title
        p2.font.name = FONT_HEADING
        p2.font.size = Pt(22)
        p2.font.bold = True
        p2.font.color.rgb = TEXT_WHITE

        # Horizontal separator line
        line = slide.shapes.add_shape(
            MSO_SHAPE.RECTANGLE,
            Inches(0.8), Inches(1.35), Inches(11.733), Inches(0.02)
        )
        line.fill.solid()
        line.fill.fore_color.rgb = RGBColor(30, 58, 138)
        line.line.color.rgb = RGBColor(30, 58, 138)

    def add_card(slide, left, top, width, height, bg_color=CARD_BG, border_color=CARD_BORDER, border_width=1):
        shape = slide.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, left, top, width, height)
        shape.fill.solid()
        shape.fill.fore_color.rgb = bg_color
        if border_color:
            shape.line.color.rgb = border_color
            shape.line.width = Pt(border_width)
        else:
            shape.line.fill.background()
        return shape

    def add_notes(slide, notes_text):
        notes_slide = slide.notes_slide
        text_frame = notes_slide.notes_text_frame
        text_frame.text = notes_text

    # =========================================================================
    # SLIDE 1: Title & Executive Hook
    # =========================================================================
    slide1 = prs.slides.add_slide(blank_layout)
    set_slide_background(slide1)

    # Hero card container
    add_card(slide1, Inches(0.8), Inches(0.8), Inches(11.733), Inches(5.9), bg_color=CARD_BG, border_color=ACCENT_BLUE, border_width=1.5)

    # Top Pill Badge
    badge = slide1.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, Inches(1.3), Inches(1.2), Inches(4.2), Inches(0.4))
    badge.fill.solid()
    badge.fill.fore_color.rgb = RGBColor(12, 30, 68)
    badge.line.color.rgb = ACCENT_CYAN
    badge.line.width = Pt(1)
    tf = badge.text_frame
    tf.margin_top = tf.margin_bottom = tf.margin_left = tf.margin_right = 0
    p = tf.paragraphs[0]
    p.text = "⚡ OSINT & CIB FORENSICS ARCHITECTURE"
    p.alignment = PP_ALIGN.CENTER
    p.font.name = FONT_HEADING
    p.font.size = Pt(11)
    p.font.bold = True
    p.font.color.rgb = ACCENT_CYAN

    # Main Project Title
    title_box = slide1.shapes.add_textbox(Inches(1.3), Inches(1.8), Inches(10.7), Inches(1.3))
    tf = title_box.text_frame
    tf.word_wrap = True
    p = tf.paragraphs[0]
    p.text = "Disinfo Shield AI 2026"
    p.font.name = FONT_HEADING
    p.font.size = Pt(38)
    p.font.bold = True
    p.font.color.rgb = TEXT_WHITE

    sub = tf.add_paragraph()
    sub.text = "Multi-Platform Disinformation Forensics, Campaign Clustering & Fact-Checking Intelligence"
    sub.font.name = FONT_HEADING
    sub.font.size = Pt(17)
    sub.font.bold = False
    sub.font.color.rgb = ACCENT_CYAN
    sub.space_before = Pt(8)

    # 3 Summary Highlight Cards inside Title Slide
    cards_data = [
        ("🌐 8-Platform Ingestion", "Tracks WhatsApp, Telegram, X, Instagram, TikTok, Reddit, FB & YouTube.", ACCENT_BLUE),
        ("🧠 Forensic NLP Engine", "5-Dimensional heuristic matrix & drop-in Hugging Face model API.", ACCENT_PURPLE),
        ("🇮🇳 Official Fact-Checks", "Direct provenance integration with PIB Fact Check & Ministry of Defence.", ACCENT_GREEN)
    ]
    card_w = Inches(3.35)
    for i, (head, desc, color) in enumerate(cards_data):
        c_left = Inches(1.3) + i * Inches(3.65)
        add_card(slide1, c_left, Inches(3.5), card_w, Inches(1.7), bg_color=CARD_BG_LIGHT, border_color=color, border_width=1.2)
        
        tb = slide1.shapes.add_textbox(c_left + Inches(0.2), Inches(3.65), card_w - Inches(0.4), Inches(1.4))
        tf = tb.text_frame
        tf.word_wrap = True
        tf.margin_top = tf.margin_left = tf.margin_right = tf.margin_bottom = 0
        p = tf.paragraphs[0]
        p.text = head
        p.font.name = FONT_HEADING
        p.font.size = Pt(14)
        p.font.bold = True
        p.font.color.rgb = TEXT_WHITE
        
        p2 = tf.add_paragraph()
        p2.text = desc
        p2.font.name = FONT_BODY
        p2.font.size = Pt(11)
        p2.font.color.rgb = TEXT_MUTED
        p2.space_before = Pt(6)

    # Footer presenter details
    foot_box = slide1.shapes.add_textbox(Inches(1.3), Inches(5.8), Inches(10.7), Inches(0.5))
    tf = foot_box.text_frame
    p = tf.paragraphs[0]
    p.text = "🎯 Candidate Presentation & Technical Architecture Walkthrough  |  Built with FastAPI, Three.js & Forensic NLP"
    p.font.name = FONT_BODY
    p.font.size = Pt(11)
    p.font.color.rgb = TEXT_DIM

    # Try embedding app_icon if present
    if os.path.exists("app_icon.png"):
        slide1.shapes.add_picture("app_icon.png", Inches(10.8), Inches(1.2), Inches(1.2), Inches(1.2))

    add_notes(slide1, 
        "PRESENTER SCRIPT (WHAT TO SAY):\n\n"
        "\"Good morning/afternoon. Today I am presenting Disinfo Shield AI 2026.\n"
        "In modern information warfare, fake news does not stay confined to a single platform—it mutates rapidly from dark social channels like WhatsApp and Telegram to viral short video feeds and coordinated bot swarms on X.\n\n"
        "Disinfo Shield AI is an end-to-end OSINT intelligence suite that detects disinformation signals using forensic NLP, maps coordinated campaigns across 8 digital platforms, and links directly to official fact-checking authorities (such as PIB Fact Check and the Ministry of Defence) to verify national and civic security narratives.\""
    )

    # =========================================================================
    # SLIDE 2: The Problem Space: Cross-Platform Disinformation Velocity
    # =========================================================================
    slide2 = prs.slides.add_slide(blank_layout)
    set_slide_background(slide2)
    add_header(slide2, "The Problem: Cross-Platform Disinformation Velocity", "PROBLEM DEFINITION & THREAT LANDSCAPE", "⚠️")

    # 4 Key Problem Pillar Cards
    pillars = [
        ("⚡ 6x Propagation Velocity", "MIT benchmark confirms false narratives diffuse 6 times faster than accredited truth due to engineered emotional outrage and panic triggers.", ACCENT_RED),
        ("🔄 Multi-Vector Mutation", "A single text tweet on X transforms within minutes into an encrypted WhatsApp voice note, an AI-dubbed TikTok reel, and a Reddit conspiracy thread.", ACCENT_AMBER),
        ("🔒 Dark Social Blindspot", "Over 60% of panic-inducing rumors (e.g. bank runs, utility shutdowns, military skirmishes) incubate in encrypted chats before hitting open media.", ACCENT_PURPLE),
        ("⏱️ The Fact-Checking Lag", "Traditional fact-checking articles take 24–48 hours to publish. By that time, the civic panic or market disruption has already caused irreversible damage.", ACCENT_CYAN),
    ]

    p_w = Inches(5.65)
    p_h = Inches(2.55)
    coords = [
        (Inches(0.8), Inches(1.6)),
        (Inches(6.85), Inches(1.6)),
        (Inches(0.8), Inches(4.4)),
        (Inches(6.85), Inches(4.4))
    ]

    for i, (head, desc, color) in enumerate(pillars):
        x, y = coords[i]
        add_card(slide2, x, y, p_w, p_h, bg_color=CARD_BG, border_color=color, border_width=1.2)
        
        tb = slide2.shapes.add_textbox(x + Inches(0.3), y + Inches(0.25), p_w - Inches(0.6), p_h - Inches(0.5))
        tf = tb.text_frame
        tf.word_wrap = True
        tf.margin_top = tf.margin_left = tf.margin_right = tf.margin_bottom = 0
        
        p = tf.paragraphs[0]
        p.text = head
        p.font.name = FONT_HEADING
        p.font.size = Pt(15)
        p.font.bold = True
        p.font.color.rgb = color
        
        p2 = tf.add_paragraph()
        p2.text = desc
        p2.font.name = FONT_BODY
        p2.font.size = Pt(12)
        p2.font.color.rgb = TEXT_LIGHT
        p2.space_before = Pt(8)

    add_notes(slide2,
        "PRESENTER SCRIPT:\n\n"
        "\"The core problem we are solving is not just simple 'fake news'—it is Coordinated Inauthentic Behavior (CIB).\n\n"
        "Adversaries exploit platform seams: they seed a doctored claim on an anonymous forum, broadcast it via Telegram, diffuse it through encrypted WhatsApp family groups, and use bot swarms on X to force algorithmic trending.\n\n"
        "By the time a traditional fact-checker writes an article 24 hours later, the market panic or civic disturbance has already occurred. Analysts lack a unified system that connects the dots across these disparate channels in real time.\""
    )

    # =========================================================================
    # SLIDE 3: System Architecture: The Decoupled 3-Stage Pipeline
    # =========================================================================
    slide3 = prs.slides.add_slide(blank_layout)
    set_slide_background(slide3)
    add_header(slide3, "System Architecture: Decoupled 3-Stage Pipeline", "END-TO-END ARCHITECTURE", "🏗️")

    arch_steps = [
        ("STAGE 1: INGESTION", "Multi-Platform Connectors", [
            "Normalized schema across 8 platforms",
            "Live XML/RSS news syndication (Google News, BBC, PIB)",
            "Tipline & dark social export parsers",
            "Rate-limited async HTTPX client"
        ], ACCENT_BLUE),
        ("STAGE 2: ANALYSIS", "Forensic NLP & Scoring", [
            "5-dimensional heuristic extraction matrix",
            "Panic syntax & forward acceleration detection",
            "Attribution deficit & authority validation",
            "Drop-in Hugging Face transformer API interface"
        ], ACCENT_PURPLE),
        ("STAGE 3: INTELLIGENCE", "Clustering & Response", [
            "Coordinated Inauthentic Behavior (CIB) scoring",
            "Three.js 3D WebGL Threat Mesh & Globe",
            "vis.js Force-Directed Campaign Network Graph",
            "Official PIB/MoD Fact-Check Verification Suite"
        ], ACCENT_GREEN)
    ]

    col_w = Inches(3.65)
    col_h = Inches(5.3)
    for i, (badge_text, title_text, bullets, color) in enumerate(arch_steps):
        col_x = Inches(0.8) + i * Inches(4.0)
        add_card(slide3, col_x, Inches(1.6), col_w, col_h, bg_color=CARD_BG, border_color=color, border_width=1.5)
        
        # Step Badge
        sb = slide3.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, col_x + Inches(0.2), Inches(1.85), col_w - Inches(0.4), Inches(0.35))
        sb.fill.solid()
        sb.fill.fore_color.rgb = RGBColor(15, 25, 50)
        sb.line.color.rgb = color
        sb.line.width = Pt(1)
        tf_s = sb.text_frame
        p_s = tf_s.paragraphs[0]
        p_s.text = badge_text
        p_s.alignment = PP_ALIGN.CENTER
        p_s.font.name = FONT_HEADING
        p_s.font.size = Pt(10)
        p_s.font.bold = True
        p_s.font.color.rgb = color

        # Content Box
        tb = slide3.shapes.add_textbox(col_x + Inches(0.25), Inches(2.35), col_w - Inches(0.5), col_h - Inches(0.9))
        tf = tb.text_frame
        tf.word_wrap = True
        tf.margin_left = tf.margin_right = tf.margin_top = tf.margin_bottom = 0
        
        p = tf.paragraphs[0]
        p.text = title_text
        p.font.name = FONT_HEADING
        p.font.size = Pt(14)
        p.font.bold = True
        p.font.color.rgb = TEXT_WHITE
        
        for bullet in bullets:
            pb = tf.add_paragraph()
            pb.text = f"•  {bullet}"
            pb.font.name = FONT_BODY
            pb.font.size = Pt(11)
            pb.font.color.rgb = TEXT_LIGHT
            pb.space_before = Pt(10)

    add_notes(slide3,
        "PRESENTER SCRIPT:\n\n"
        "\"Our system architecture follows a clean, decoupled 3-stage pipeline: Ingestion, Forensic Analysis, and Response.\n\n"
        "1. Ingestion: We normalize heterogeneous feeds from WhatsApp, Telegram, X, and live RSS into a unified post schema with zero data loss.\n"
        "2. Forensic NLP Layer: Posts are evaluated across our 5-axis forensic engine in under 5 milliseconds.\n"
        "3. Response Layer: Synchronized posts are clustered into campaigns, rendered on our Three.js 3D Threat Mesh, and cross-referenced with official PIB and Defence fact-checking records.\""
    )

    # =========================================================================
    # SLIDE 4: Data Trustworthiness & The Fact-Checking Pipeline
    # =========================================================================
    slide4 = prs.slides.add_slide(blank_layout)
    set_slide_background(slide4)
    add_header(slide4, "Data Trustworthiness & Official Fact-Checking Pipeline", "CREDIBILITY & PROVENANCE DEFENSE", "🏛️")

    # 3 Column Provenance Architecture
    trust_pillars = [
        ("Layer 1: Live Syndication", "100% Real-Time RSS", [
            "Live XML feeds from Google News, BBC World, PIB, and Reuters.",
            "Live risk scoring computed on incoming breaking headlines.",
            "Continuous auto-refresh cycle without UI blocking."
        ], ACCENT_BLUE),
        ("Layer 2: Official Fact-Checks", "Government & Defence Desks", [
            "Direct integration with PIB Fact Check (factcheck.pib.gov.in).",
            "Indian Army (ADG PI) & Ministry of Defence official archives.",
            "Clickable outbound links for direct analyst audit."
        ], ACCENT_GREEN),
        ("Layer 3: Forensic Templates", "SIO & Meta CIB Benchmarks", [
            "Modeled on Stanford Internet Observatory & Meta takedowns.",
            "Replicates exact syntactical panic & botnet forwarding patterns.",
            "Zero PII violation; zero illicit material stored."
        ], ACCENT_PURPLE)
    ]

    for i, (title_text, sub_text, bullets, color) in enumerate(trust_pillars):
        col_x = Inches(0.8) + i * Inches(4.0)
        add_card(slide4, col_x, Inches(1.6), col_w, Inches(4.3), bg_color=CARD_BG, border_color=color, border_width=1.3)
        
        tb = slide4.shapes.add_textbox(col_x + Inches(0.25), Inches(1.85), col_w - Inches(0.5), Inches(3.8))
        tf = tb.text_frame
        tf.word_wrap = True
        tf.margin_left = tf.margin_right = tf.margin_top = tf.margin_bottom = 0
        
        p = tf.paragraphs[0]
        p.text = title_text
        p.font.name = FONT_HEADING
        p.font.size = Pt(14)
        p.font.bold = True
        p.font.color.rgb = color
        
        p_sub = tf.add_paragraph()
        p_sub.text = sub_text
        p_sub.font.name = FONT_HEADING
        p_sub.font.size = Pt(11)
        p_sub.font.bold = True
        p_sub.font.color.rgb = TEXT_WHITE
        p_sub.space_before = Pt(3)

        for bullet in bullets:
            pb = tf.add_paragraph()
            pb.text = f"•  {bullet}"
            pb.font.name = FONT_BODY
            pb.font.size = Pt(11)
            pb.font.color.rgb = TEXT_LIGHT
            pb.space_before = Pt(10)

    # Bottom summary callout card
    add_card(slide4, Inches(0.8), Inches(6.1), Inches(11.733), Inches(0.9), bg_color=CARD_BG_LIGHT, border_color=ACCENT_CYAN, border_width=1)
    callout_tb = slide4.shapes.add_textbox(Inches(1.0), Inches(6.15), Inches(11.333), Inches(0.8))
    tf_c = callout_tb.text_frame
    tf_c.word_wrap = True
    p_c = tf_c.paragraphs[0]
    p_c.text = "🛡️ KEY DEFENSE TAKEAWAY FOR INTERVIEWERS: We avoid black-box LLM hallucinations by using explainable, deterministic forensic indicators backed by verified government fact-checking registries and active outbound verification links."
    p_c.font.name = FONT_HEADING
    p_c.font.size = Pt(11)
    p_c.font.bold = True
    p_c.font.color.rgb = ACCENT_CYAN

    add_notes(slide4,
        "PRESENTER SCRIPT (KEY INTERVIEW DEFENSE):\n\n"
        "\"When presenting intelligence tools, interviewers frequently ask: 'Where is this data coming from? Can we trust it?'\n\n"
        "We answer this through our Tri-Layer Data Architecture:\n"
        "1. Real-time Live News parsed directly from accredited RSS endpoints (BBC, Google News, PIB).\n"
        "2. Authentic Fact-Check Integrations: Every flagged defence narrative maps to an official debunk record from PIB Fact Check or the Ministry of Defence, complete with a direct verification URL.\n"
        "3. Deterministic Forensic Indicators: Rather than relying on an LLM that might hallucinate a justification, our system generates transparent, auditable indicators (e.g. [PANIC_SYNTAX], [ATTRIBUTION_DEFICIT]).\""
    )

    # =========================================================================
    # SLIDE 5: AI NLP Forensic Classifier (The Engine)
    # =========================================================================
    slide5 = prs.slides.add_slide(blank_layout)
    set_slide_background(slide5)
    add_header(slide5, "AI NLP Forensic Classifier: 5-Axis Detection Matrix", "CORE NLP INNOVATION", "🧠")

    # Left Column: The 5-Axis Matrix (Width 6.2 inches)
    add_card(slide5, Inches(0.8), Inches(1.6), Inches(6.2), Inches(5.4), bg_color=CARD_BG, border_color=ACCENT_BLUE, border_width=1.3)
    tb_left = slide5.shapes.add_textbox(Inches(1.05), Inches(1.85), Inches(5.7), Inches(5.0))
    tf_l = tb_left.text_frame
    tf_l.word_wrap = True
    tf_l.margin_left = tf_l.margin_right = tf_l.margin_top = tf_l.margin_bottom = 0
    
    p = tf_l.paragraphs[0]
    p.text = "5-Dimensional Forensic Matrix"
    p.font.name = FONT_HEADING
    p.font.size = Pt(15)
    p.font.bold = True
    p.font.color.rgb = ACCENT_CYAN

    matrix_items = [
        ("🚨 Panic & Urgency Triggers", "'Midnight deadline', 'Immediate freeze', ALL-CAPS alerts."),
        ("🎭 Emotional Manipulation", "Bio-threat hysteria, manufactured outrage, scapegoating."),
        ("❓ Attribution Deficit", "'Unnamed top officials', 'Secret insider' with no press link."),
        ("📢 Astroturfing Signatures", "'Forward to 10 groups', 'Share before media deletes'."),
        ("📱 Dark Social Formatting", "Forwarded audio transcripts, synthetic SMS bait templates.")
    ]
    for m_title, m_desc in matrix_items:
        pm = tf_l.add_paragraph()
        pm.text = f"{m_title}: "
        pm.font.name = FONT_HEADING
        pm.font.size = Pt(11.5)
        pm.font.bold = True
        pm.font.color.rgb = TEXT_WHITE
        pm.space_before = Pt(8)
        
        # Add description
        pm2 = tf_l.add_paragraph()
        pm2.text = f"   └─ {m_desc}"
        pm2.font.name = FONT_BODY
        pm2.font.size = Pt(10.5)
        pm2.font.color.rgb = TEXT_MUTED

    # Right Column: Contrast Case Study (Width 5.1 inches)
    add_card(slide5, Inches(7.35), Inches(1.6), Inches(5.18), Inches(2.55), bg_color=CARD_BG_LIGHT, border_color=ACCENT_RED, border_width=1.3)
    tb_fake = slide5.shapes.add_textbox(Inches(7.55), Inches(1.8), Inches(4.78), Inches(2.2))
    tf_fake = tb_fake.text_frame
    tf_fake.word_wrap = True
    tf_fake.margin_left = tf_fake.margin_right = tf_fake.margin_top = tf_fake.margin_bottom = 0
    
    p_f = tf_fake.paragraphs[0]
    p_f.text = "🔴 Test Case: Banking Phishing SMS"
    p_f.font.name = FONT_HEADING
    p_f.font.size = Pt(13)
    p_f.font.bold = True
    p_f.font.color.rgb = ACCENT_RED
    
    p_f_score = tf_fake.add_paragraph()
    p_f_score.text = "Score: 98.4% Disinformation Risk (CRITICAL)"
    p_f_score.font.name = FONT_HEADING
    p_f_score.font.size = Pt(11)
    p_f_score.font.bold = True
    p_f_score.font.color.rgb = TEXT_WHITE
    p_f_score.space_before = Pt(4)

    p_f_desc = tf_fake.add_paragraph()
    p_f_desc.text = "Flags: [ATTRIBUTION_DEFICIT], [PANIC_SYNTAX], [PHISHING_HOOK], [FORWARD_ACCELERATION]."
    p_f_desc.font.name = FONT_MONO
    p_f_desc.font.size = Pt(9.5)
    p_f_desc.font.color.rgb = ACCENT_AMBER
    p_f_desc.space_before = Pt(6)

    # Legitimate Case Study
    add_card(slide5, Inches(7.35), Inches(4.45), Inches(5.18), Inches(2.55), bg_color=CARD_BG_LIGHT, border_color=ACCENT_GREEN, border_width=1.3)
    tb_real = slide5.shapes.add_textbox(Inches(7.55), Inches(4.65), Inches(4.78), Inches(2.2))
    tf_real = tb_real.text_frame
    tf_real.word_wrap = True
    tf_real.margin_left = tf_real.margin_right = tf_real.margin_top = tf_real.margin_bottom = 0
    
    p_r = tf_real.paragraphs[0]
    p_r.text = "🟢 Test Case: Accredited Press Dispatch"
    p_r.font.name = FONT_HEADING
    p_r.font.size = Pt(13)
    p_r.font.bold = True
    p_r.font.color.rgb = ACCENT_GREEN
    
    p_r_score = tf_real.add_paragraph()
    p_r_score.text = "Score: 10.0% Risk (VERIFIED LEGITIMATE)"
    p_r_score.font.name = FONT_HEADING
    p_r_score.font.size = Pt(11)
    p_r_score.font.bold = True
    p_r_score.font.color.rgb = TEXT_WHITE
    p_r_score.space_before = Pt(4)

    p_r_desc = tf_real.add_paragraph()
    p_r_desc.text = "Flags: Neutral journalistic cadence, direct accredited source attribution, zero urgency bait."
    p_r_desc.font.name = FONT_BODY
    p_r_desc.font.size = Pt(10.5)
    p_r_desc.font.color.rgb = TEXT_LIGHT
    p_r_desc.space_before = Pt(6)

    add_notes(slide5,
        "PRESENTER SCRIPT:\n\n"
        "\"Our NLP classifier inspects incoming content across 5 forensic dimensions. Unlike black-box models, it evaluates exact indicators: urgency triggers, attribution deficit, emotional manipulation, astroturfing markers, and dark social structures.\n\n"
        "Notice the live contrast in our demo: when fed a fraudulent 'SBI account freeze' alert, the engine triggers all 4 diagnostic red flags and scores 98.4% risk. When fed an accredited news dispatch, it validates the journalistic cadence and drops risk to 10%.\n\n"
        "Crucially, our classifier API signature matches Hugging Face transformers, allowing a fine-tuned RoBERTa model to drop in seamlessly with just 2 lines of code.\""
    )

    # =========================================================================
    # SLIDE 6: Coordinated Campaign Clustering & Graph Intelligence
    # =========================================================================
    slide6 = prs.slides.add_slide(blank_layout)
    set_slide_background(slide6)
    add_header(slide6, "Coordinated Campaign Clustering & Graph Forensics", "NETWORK INTELLIGENCE & CIB", "🕸️")

    graph_cards = [
        ("1. Narrative Clustering", "Synthesizing Isolated Posts", [
            "Groups disparate messages into unified campaigns (e.g. 'Banking Liquidity FUD', 'Border Skirmish Deepfake').",
            "Extracts common n-gram signatures and entity tokens.",
            "Computes campaign-level virality index and reach."
        ], ACCENT_BLUE),
        ("2. CIB Velocity Scoring", "Temporal Synchronization", [
            "Detects bot swarms executing coordinated posts within a tight co-action window (<45 seconds).",
            "Identifies forward multipliers across cross-platform relay nodes.",
            "Flags synchronized astroturfing campaigns."
        ], ACCENT_PURPLE),
        ("3. Force-Directed Graph", "Interactive Network Forensics", [
            "Visualizes Seed Nodes (adversary origin), Amplifiers (bot accounts), and Transmission Channels.",
            "Platform color-coded nodes (WhatsApp, X, Telegram, Reddit, TikTok).",
            "Interactive physics simulation powered by vis.js."
        ], ACCENT_CYAN)
    ]

    for i, (title_text, sub_text, bullets, color) in enumerate(graph_cards):
        col_x = Inches(0.8) + i * Inches(4.0)
        add_card(slide6, col_x, Inches(1.6), col_w, Inches(5.3), bg_color=CARD_BG, border_color=color, border_width=1.3)
        
        tb = slide6.shapes.add_textbox(col_x + Inches(0.25), Inches(1.85), col_w - Inches(0.5), Inches(4.8))
        tf = tb.text_frame
        tf.word_wrap = True
        tf.margin_left = tf.margin_right = tf.margin_top = tf.margin_bottom = 0
        
        p = tf.paragraphs[0]
        p.text = title_text
        p.font.name = FONT_HEADING
        p.font.size = Pt(14)
        p.font.bold = True
        p.font.color.rgb = color
        
        p_sub = tf.add_paragraph()
        p_sub.text = sub_text
        p_sub.font.name = FONT_HEADING
        p_sub.font.size = Pt(11)
        p_sub.font.bold = True
        p_sub.font.color.rgb = TEXT_WHITE
        p_sub.space_before = Pt(3)

        for bullet in bullets:
            pb = tf.add_paragraph()
            pb.text = f"•  {bullet}"
            pb.font.name = FONT_BODY
            pb.font.size = Pt(11)
            pb.font.color.rgb = TEXT_LIGHT
            pb.space_before = Pt(10)

    add_notes(slide6,
        "PRESENTER SCRIPT:\n\n"
        "\"A single fake post is noise; 500 accounts posting the exact same narrative within a 45-second window is a coordinated operation.\n\n"
        "Our campaign clustering module groups isolated posts across platforms into unified threat operations using semantic entity markers and temporal synchronization.\n\n"
        "On our vis.js interactive network graph, analysts can visually isolate the entire chain of transmission: tracing from the adversary seed node, through botnet amplifiers, directly to the high-exposure broadcast channels.\""
    )

    # =========================================================================
    # SLIDE 7: 3D Geospatial Threat Mesh & Strategic Sector Monitoring
    # =========================================================================
    slide7 = prs.slides.add_slide(blank_layout)
    set_slide_background(slide7)
    add_header(slide7, "3D Geospatial Threat Mesh & Strategic Sector Monitoring", "3D SITUATIONAL AWARENESS", "🌐")

    # Left: 3D Globe Features (Width 5.8 inches)
    add_card(slide7, Inches(0.8), Inches(1.6), Inches(5.8), Inches(5.3), bg_color=CARD_BG, border_color=ACCENT_CYAN, border_width=1.3)
    tb_globe = slide7.shapes.add_textbox(Inches(1.05), Inches(1.85), Inches(5.3), Inches(4.8))
    tf_g = tb_globe.text_frame
    tf_g.word_wrap = True
    tf_g.margin_left = tf_g.margin_right = tf_g.margin_top = tf_g.margin_bottom = 0
    
    p = tf_g.paragraphs[0]
    p.text = "Three.js WebGL 3D Threat Mesh"
    p.font.name = FONT_HEADING
    p.font.size = Pt(15)
    p.font.bold = True
    p.font.color.rgb = ACCENT_CYAN

    globe_bullets = [
        "Real-time 3D Earth projection with atmospheric glow & particle stars.",
        "Dynamic Bezier cyber arcs visualizing cross-border payload transfer.",
        "Smooth spherical camera interpolation (Slerp) on sector focus.",
        "Global Threat Hubs: New Delhi, Mumbai, London, Singapore, Washington DC & DarkNet Origin Farm."
    ]
    for b in globe_bullets:
        pb = tf_g.add_paragraph()
        pb.text = f"•  {b}"
        pb.font.name = FONT_BODY
        pb.font.size = Pt(11)
        pb.font.color.rgb = TEXT_LIGHT
        pb.space_before = Pt(10)

    # Right: India Strategic Sectors (Width 5.6 inches)
    add_card(slide7, Inches(6.9), Inches(1.6), Inches(5.633), Inches(5.3), bg_color=CARD_BG, border_color=ACCENT_GREEN, border_width=1.3)
    tb_india = slide7.shapes.add_textbox(Inches(7.15), Inches(1.85), Inches(5.133), Inches(4.8))
    tf_i = tb_india.text_frame
    tf_i.word_wrap = True
    tf_i.margin_left = tf_i.margin_right = tf_i.margin_top = tf_i.margin_bottom = 0
    
    p = tf_i.paragraphs[0]
    p.text = "12 Dedicated India Threat Sectors"
    p.font.name = FONT_HEADING
    p.font.size = Pt(15)
    p.font.bold = True
    p.font.color.rgb = ACCENT_GREEN

    sectors = [
        "🪖 Northern LAC Sector (Army border communication integrity)",
        "🚢 Western Naval Command (Mumbai HQ & offshore assets)",
        "⚓ Kochi Naval Base (INS Venduruthy / Southern Command)",
        "🚀 ISRO Space Centre (Bengaluru satellite telecommand)",
        "🛡️ Eastern Fleet (Vizag naval air arm & surveillance)",
        "🌉 Siliguri Corridor & BRO Arunachal Infrastructure"
    ]
    for s in sectors:
        ps = tf_i.add_paragraph()
        ps.text = f"•  {s}"
        ps.font.name = FONT_BODY
        ps.font.size = Pt(10.5)
        ps.font.color.rgb = TEXT_LIGHT
        ps.space_before = Pt(8)

    add_notes(slide7,
        "PRESENTER SCRIPT:\n\n"
        "\"To give intelligence analysts true spatial awareness, we engineered a high-performance 3D WebGL Threat Mesh using Three.js.\n\n"
        "The globe maps international influence routing arcs and features 12 dedicated Indian Strategic Defence Sectors—including Northern LAC, Western and Eastern Naval Commands, and ISRO.\n\n"
        "When an analyst selects a sector, the camera smoothly interpolates to the target coordinates, activates a radar sweep, and opens a detailed Node Forensic Dossier showing the targeted asset, botnet origin, and PIB fact-check link.\""
    )

    # =========================================================================
    # SLIDE 8: 6-Stage Temporal Cascade Simulator
    # =========================================================================
    slide8 = prs.slides.add_slide(blank_layout)
    set_slide_background(slide8)
    add_header(slide8, "6-Stage Temporal Cascade & Vector Simulator", "PROPAGATION DYNAMICS", "⏳")

    # 6 Step Cards arranged in a 2x3 grid
    stages = [
        ("STAGE 1: INCEPTION", "Dark Web / Anonymous Forum", "Adversary seeds synthetic claim, doctored image, or forged document.", ACCENT_RED),
        ("STAGE 2: BROADCAST", "Telegram Channels", "Unmoderated mega-channels broadcast narrative to initial 50k subscribers.", ACCENT_PURPLE),
        ("STAGE 3: DARK SOCIAL", "WhatsApp Forward Loops", "Encrypted peer-to-peer forwarding with 'Forwarded many times' velocity.", ACCENT_GREEN),
        ("STAGE 4: VIRALITY", "Instagram Reels & TikTok", "Algorithmic amplification using AI dubbing and sensational short video.", ACCENT_AMBER),
        ("STAGE 5: ASTROTURF", "X / Twitter Bot Swarms", "Coordinated hashtag hijacking forcing topic into national trending charts.", ACCENT_BLUE),
        ("STAGE 6: DEBUNK", "Reddit & Mainstream Press", "Public discourse peak followed by official PIB/defence fact-check rebuttal.", ACCENT_CYAN)
    ]

    s_w = Inches(3.65)
    s_h = Inches(2.5)
    s_coords = [
        (Inches(0.8), Inches(1.6)),
        (Inches(4.8), Inches(1.6)),
        (Inches(8.8), Inches(1.6)),
        (Inches(0.8), Inches(4.4)),
        (Inches(4.8), Inches(4.4)),
        (Inches(8.8), Inches(4.4))
    ]

    for i, (stg_num, stg_name, stg_desc, color) in enumerate(stages):
        sx, sy = s_coords[i]
        add_card(slide8, sx, sy, s_w, s_h, bg_color=CARD_BG, border_color=color, border_width=1.2)
        
        tb = slide8.shapes.add_textbox(sx + Inches(0.2), sy + Inches(0.2), s_w - Inches(0.4), s_h - Inches(0.4))
        tf = tb.text_frame
        tf.word_wrap = True
        tf.margin_left = tf.margin_right = tf.margin_top = tf.margin_bottom = 0
        
        p = tf.paragraphs[0]
        p.text = stg_num
        p.font.name = FONT_HEADING
        p.font.size = Pt(11)
        p.font.bold = True
        p.font.color.rgb = color
        
        p2 = tf.add_paragraph()
        p2.text = stg_name
        p2.font.name = FONT_HEADING
        p2.font.size = Pt(13)
        p2.font.bold = True
        p2.font.color.rgb = TEXT_WHITE
        p2.space_before = Pt(3)

        p3 = tf.add_paragraph()
        p3.text = stg_desc
        p3.font.name = FONT_BODY
        p3.font.size = Pt(10.5)
        p3.font.color.rgb = TEXT_LIGHT
        p3.space_before = Pt(6)

    add_notes(slide8,
        "PRESENTER SCRIPT:\n\n"
        "\"How does a malicious rumor travel from a dark web imageboard to your family's WhatsApp group? We modeled this exact lifecycle in our 3D Volumetric Cascade Simulator.\n\n"
        "The model tracks the narrative across 6 distinct stages: Inception, Broadcast, Dark Social, Visual Virality, Astroturfing, and Discourse/Debunk.\n\n"
        "Our telemetry HUD calculates real-time metrics: Mean Hop Latency (14.2 seconds), Amplification Factor (97.8%), and the Co-Action Window, enabling analysts to pinpoint the exact stage where intervention is most effective.\""
    )

    # =========================================================================
    # SLIDE 9: Indian Defence & Maritime Intelligence Connector
    # =========================================================================
    slide9 = prs.slides.add_slide(blank_layout)
    set_slide_background(slide9)
    add_header(slide9, "Indian Defence & Maritime Intelligence Connector", "NATIONAL SECURITY OSINT", "⚓")

    # Left: Strategic Scope (Width 5.8 inches)
    add_card(slide9, Inches(0.8), Inches(1.6), Inches(5.8), Inches(5.3), bg_color=CARD_BG, border_color=ACCENT_BLUE, border_width=1.3)
    tb_scope = slide9.shapes.add_textbox(Inches(1.05), Inches(1.85), Inches(5.3), Inches(4.8))
    tf_s = tb_scope.text_frame
    tf_s.word_wrap = True
    tf_s.margin_left = tf_s.margin_right = tf_s.margin_top = tf_s.margin_bottom = 0
    
    p = tf_s.paragraphs[0]
    p.text = "Strategic Monitoring Scope"
    p.font.name = FONT_HEADING
    p.font.size = Pt(15)
    p.font.bold = True
    p.font.color.rgb = ACCENT_BLUE

    scope_points = [
        "Aggregates intelligence across 8 official defence sources.",
        "Monitors major joint exercises: Milan, Malabar, Varuna, and coastal drills.",
        "Tracks carrier battle group deployments (INS Vikrant & INS Vikramaditya).",
        "Automated alerts for synthetic naval casualty and submarine deepfakes.",
        "Cross-verification with official naval press communiques."
    ]
    for sp in scope_points:
        pb = tf_s.add_paragraph()
        pb.text = f"•  {sp}"
        pb.font.name = FONT_BODY
        pb.font.size = Pt(11)
        pb.font.color.rgb = TEXT_LIGHT
        pb.space_before = Pt(10)

    # Right: Official Source Hierarchy (Width 5.6 inches)
    add_card(slide9, Inches(6.9), Inches(1.6), Inches(5.633), Inches(5.3), bg_color=CARD_BG, border_color=ACCENT_GREEN, border_width=1.3)
    tb_src = slide9.shapes.add_textbox(Inches(7.15), Inches(1.85), Inches(5.133), Inches(4.8))
    tf_src = tb_src.text_frame
    tf_src.word_wrap = True
    tf_src.margin_left = tf_src.margin_right = tf_src.margin_top = tf_src.margin_bottom = 0
    
    p = tf_src.paragraphs[0]
    p.text = "Integrated Official Registries"
    p.font.name = FONT_HEADING
    p.font.size = Pt(15)
    p.font.bold = True
    p.font.color.rgb = ACCENT_GREEN

    registries = [
        ("🏛️ Press Information Bureau (PIB)", "Official Government of India media & defence press releases."),
        ("⚓ Indian Navy Official Portal", "Direct sync with indiannavy.nic.in operational notices."),
        ("🪖 ADG PI - Indian Army", "Official public information wing countering border rumors."),
        ("🛡️ Ministry of Defence (MoD)", "Policy communiques, bilateral drills, and procurement notices.")
    ]
    for r_title, r_desc in registries:
        pr = tf_src.add_paragraph()
        pr.text = f"{r_title}"
        pr.font.name = FONT_HEADING
        pr.font.size = Pt(12)
        pr.font.bold = True
        pr.font.color.rgb = TEXT_WHITE
        pr.space_before = Pt(8)
        
        pr2 = tf_src.add_paragraph()
        pr2.text = f"   └─ {r_desc}"
        pr2.font.name = FONT_BODY
        pr2.font.size = Pt(10.5)
        pr2.font.color.rgb = TEXT_MUTED

    add_notes(slide9,
        "PRESENTER SCRIPT:\n\n"
        "\"National security requires specialized domain awareness. Disinformation targeting armed forces or naval maneuvers can cause strategic destabilization.\n\n"
        "Our Defence Intel connector continuously monitors communications across official channels like the Indian Navy portal, ADG PI, and PIB Defence.\n\n"
        "If a manipulated video claims a naval skirmish in the Arabian Sea or Indian Ocean, the connector pairs the claim immediately with official statements and verified debunk records, shutting down panic before it spreads.\""
    )

    # =========================================================================
    # SLIDE 10: Production Scalability & Tech Stack
    # =========================================================================
    slide10 = prs.slides.add_slide(blank_layout)
    set_slide_background(slide10)
    add_header(slide10, "Technology Stack & Production Engineering", "SYSTEM IMPLEMENTATION & SPECS", "⚙️")

    # 4 Stack Architecture Blocks
    stack_blocks = [
        ("BACKEND ENGINE", "FastAPI & Python 3.11", [
            "Asynchronous ASGI request processing with Uvicorn",
            "Pydantic v2 strict schema validation",
            "Zero-latency background task dispatch",
            "RESTful endpoints with complete OpenAPI docs"
        ], ACCENT_BLUE),
        ("PERSISTENCE LAYER", "SQLite with WAL Mode", [
            "Write-Ahead Logging (WAL) for high concurrency",
            "Microsecond query speeds with zero maintenance",
            "Self-contained zero-dependency deployment",
            "Clean upgrade path to PostgreSQL / TimescaleDB"
        ], ACCENT_AMBER),
        ("ANALYST CONSOLE", "Modern Vanilla ES6+ & WebGL", [
            "Three.js 3D WebGL hardware-accelerated globe",
            "vis.js dynamic force-directed network physics",
            "Chart.js interactive threat telemetry graphs",
            "Zero-bundle-bloat Vanilla CSS Glassmorphism"
        ], ACCENT_PURPLE),
        ("ENTERPRISE ROADMAP", "Production Scaling Plan", [
            "Redis / Celery task queues for 50k+ posts/sec",
            "SBERT embeddings clustered via GPU DBSCAN",
            "Triton Inference Server for fine-tuned RoBERTa",
            "Docker & Kubernetes multi-region orchestration"
        ], ACCENT_GREEN)
    ]

    coords_stack = [
        (Inches(0.8), Inches(1.6)),
        (Inches(6.85), Inches(1.6)),
        (Inches(0.8), Inches(4.4)),
        (Inches(6.85), Inches(4.4))
    ]

    for i, (b_title, b_sub, b_bullets, color) in enumerate(stack_blocks):
        bx, by = coords_stack[i]
        add_card(slide10, bx, by, p_w, p_h, bg_color=CARD_BG, border_color=color, border_width=1.2)
        
        tb = slide10.shapes.add_textbox(bx + Inches(0.25), by + Inches(0.2), p_w - Inches(0.5), p_h - Inches(0.4))
        tf = tb.text_frame
        tf.word_wrap = True
        tf.margin_left = tf.margin_right = tf.margin_top = tf.margin_bottom = 0
        
        p = tf.paragraphs[0]
        p.text = b_title
        p.font.name = FONT_HEADING
        p.font.size = Pt(11)
        p.font.bold = True
        p.font.color.rgb = color
        
        p2 = tf.add_paragraph()
        p2.text = b_sub
        p2.font.name = FONT_HEADING
        p2.font.size = Pt(13)
        p2.font.bold = True
        p2.font.color.rgb = TEXT_WHITE
        p2.space_before = Pt(2)

        for bullet in b_bullets:
            pb = tf.add_paragraph()
            pb.text = f"•  {bullet}"
            pb.font.name = FONT_BODY
            pb.font.size = Pt(10.5)
            pb.font.color.rgb = TEXT_LIGHT
            pb.space_before = Pt(4)

    add_notes(slide10,
        "PRESENTER SCRIPT:\n\n"
        "\"From an engineering perspective, we prioritized speed, modularity, and zero-friction deployment.\n\n"
        "We chose FastAPI for its asynchronous performance and type-safe Pydantic contracts. SQLite in WAL mode delivers microsecond query response on local analyst workstations with zero server administration overhead.\n\n"
        "On the frontend, we opted for vanilla ES6+ with Three.js and vis.js to achieve 60 FPS hardware acceleration without the overhead of heavy framework bundles.\n\n"
        "For enterprise production, the architecture seamlessly transitions to PostgreSQL, Redis/Celery queues, and Triton Inference Server.\""
    )

    # =========================================================================
    # SLIDE 11: Live Demonstration Playbook (The 5-Minute Script)
    # =========================================================================
    slide11 = prs.slides.add_slide(blank_layout)
    set_slide_background(slide11)
    add_header(slide11, "Live Demonstration Walkthrough & Script", "LIVE DEMO PLAYBOOK", "🎬")

    demo_steps = [
        ("Step 1: Dashboard & KPIs", "30s", "Show top live threat level, UTC/IST clocks, 2,180 tracked accounts, and 8 active platform hubs.", ACCENT_BLUE),
        ("Step 2: 3D Threat Mesh", "60s", "Pivot camera to India Defence Sectors (Kochi Base, ISRO), inspect Node Dossier & click PIB verification link.", ACCENT_CYAN),
        ("Step 3: AI Text Analyzer", "90s", "Run fake SBI phishing SMS (98.4% Critical) vs. accredited news dispatch (10% Safe) to show explainability.", ACCENT_GREEN),
        ("Step 4: Cascade Simulator", "60s", "Run 3D temporal simulation through 6 lifecycle hops showing latency (14.2s) and 97.8% amplification.", ACCENT_AMBER),
        ("Step 5: Live Feeds", "60s", "Filter Live News by category and Defence Intel by Indian Navy / Army to demonstrate real-time auditability.", ACCENT_PURPLE)
    ]

    step_w = Inches(11.733)
    step_h = Inches(0.9)
    for i, (s_title, s_dur, s_action, color) in enumerate(demo_steps):
        sy = Inches(1.6) + i * Inches(1.05)
        add_card(slide11, Inches(0.8), sy, step_w, step_h, bg_color=CARD_BG, border_color=color, border_width=1.2)
        
        # Duration Badge
        dur_badge = slide11.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, Inches(1.0), sy + Inches(0.2), Inches(0.8), Inches(0.5))
        dur_badge.fill.solid()
        dur_badge.fill.fore_color.rgb = RGBColor(12, 25, 55)
        dur_badge.line.color.rgb = color
        tf_d = dur_badge.text_frame
        p_d = tf_d.paragraphs[0]
        p_d.text = s_dur
        p_d.alignment = PP_ALIGN.CENTER
        p_d.font.name = FONT_HEADING
        p_d.font.size = Pt(11)
        p_d.font.bold = True
        p_d.font.color.rgb = color

        # Step Text
        tb = slide11.shapes.add_textbox(Inches(2.0), sy + Inches(0.12), Inches(10.3), Inches(0.7))
        tf = tb.text_frame
        tf.word_wrap = True
        tf.margin_left = tf.margin_right = tf.margin_top = tf.margin_bottom = 0
        
        p = tf.paragraphs[0]
        p.text = s_title
        p.font.name = FONT_HEADING
        p.font.size = Pt(12.5)
        p.font.bold = True
        p.font.color.rgb = TEXT_WHITE
        
        p2 = tf.add_paragraph()
        p2.text = s_action
        p2.font.name = FONT_BODY
        p2.font.size = Pt(10.5)
        p2.font.color.rgb = TEXT_LIGHT
        p2.space_before = Pt(2)

    add_notes(slide11,
        "PRESENTER SCRIPT (DEMO WALKTHROUGH GUIDE):\n\n"
        "Follow this exact 5-minute flow during your live demonstration:\n"
        "1. Open http://127.0.0.1:8000/ and highlight the real-time KPI telemetry.\n"
        "2. Switch to 3D Threat Mesh, click India Focus, select Kochi Base, and click the PIB debunk link to prove live verification.\n"
        "3. Switch to AI Text Analyzer, run the 'SBI Freeze Alert' sample (98% risk), then run 'Legitimate News' sample (10% risk).\n"
        "4. Switch to Temporal Cascade and step through Stages 1 through 6 to show narrative mutation.\n"
        "5. Conclude on Live News & Defence Intel tabs showing live RSS ingestion."
    )

    # =========================================================================
    # SLIDE 12: Interviewer Q&A Defense & Winning Responses
    # =========================================================================
    slide12 = prs.slides.add_slide(blank_layout)
    set_slide_background(slide12)
    add_header(slide12, "Interviewer Q&A Anticipation & Technical Defense", "WINNING INTERVIEW ANSWERS", "🏆")

    qa_list = [
        ("Q: \"Why rule-based heuristics over pure LLM?\"", 
         "\"Latency (<5ms vs 2000ms), zero hallucination risk, and 100% auditable indicators. The API is designed with standard transformer signatures, making it a 2-line drop-in upgrade for fine-tuned RoBERTa.\"", ACCENT_CYAN),
        ("Q: \"How do you handle encrypted WhatsApp messages?\"", 
         "\"We don't break encryption. We analyze tipline telemetry and export metadata submitted to verified fact-checking desks (e.g. PIB WhatsApp desk), tracking velocity without violating privacy.\"", ACCENT_GREEN),
        ("Q: \"How are campaigns clustered across platforms?\"", 
         "\"By normalizing post schemas, extracting semantic n-grams, and calculating CIB velocity when multiple accounts post the same narrative signature within tight temporal co-action windows.\"", ACCENT_PURPLE),
        ("Q: \"What is your production scalability plan?\"", 
         "\"Distributed Kafka/Celery message queues for 50,000+ posts/sec, TimescaleDB for longitudinal time-series analysis, and Triton Inference Server on GPU clusters.\"", ACCENT_AMBER)
    ]

    qa_w = Inches(11.733)
    qa_h = Inches(1.18)
    for i, (q, a, color) in enumerate(qa_list):
        qy = Inches(1.6) + i * Inches(1.35)
        add_card(slide12, Inches(0.8), qy, qa_w, qa_h, bg_color=CARD_BG, border_color=color, border_width=1.2)
        
        tb = slide12.shapes.add_textbox(Inches(1.05), qy + Inches(0.15), Inches(11.2), Inches(0.9))
        tf = tb.text_frame
        tf.word_wrap = True
        tf.margin_left = tf.margin_right = tf.margin_top = tf.margin_bottom = 0
        
        p = tf.paragraphs[0]
        p.text = q
        p.font.name = FONT_HEADING
        p.font.size = Pt(12)
        p.font.bold = True
        p.font.color.rgb = color
        
        p2 = tf.add_paragraph()
        p2.text = a
        p2.font.name = FONT_BODY
        p2.font.size = Pt(10.5)
        p2.font.color.rgb = TEXT_LIGHT
        p2.space_before = Pt(3)

    add_notes(slide12,
        "CLOSING SUMMARY (WHAT TO SAY TO CONCLUDE):\n\n"
        "\"In summary, Disinfo Shield AI bridges the critical gap between raw OSINT data and actionable threat intelligence.\n\n"
        "It provides defense and civic institutions with the tools to detect, visualize, and neutralize coordinated influence operations before they inflict real-world damage.\n\n"
        "Thank you very much for your time, and I am now excited to answer your technical questions.\""
    )

    # Save the presentation
    output_filename = "Disinfo_Shield_AI_Interview_Presentation.pptx"
    prs.save(output_filename)
    print(f"Presentation saved successfully to: {os.path.abspath(output_filename)}")

if __name__ == "__main__":
    create_presentation()
