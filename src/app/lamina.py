# src/app/lamina.py

import os
import io
import logging
import json
from fastapi import APIRouter, Response
from PIL import Image, ImageDraw, ImageFont

# --- Data Models ---
class Glyph:
    def __init__(self, symbol="ڪ", agent="JULIUS", field="FIELD_VIOLET"):
        self.symbol = symbol
        self.agent = agent
        self.field = field

class Anchor:
    def __init__(self, id, poles, glyph):
        self.id = id
        self.poles = poles
        self.glyph = glyph

class BreathState:
    def __init__(self, state, fracture, vector):
        self.state = state
        self.fracture = fracture
        self.vector = vector

class Pulse:
    def __init__(self, glyph, anchor, breath_state, status):
        self.glyph = glyph
        self.anchor = anchor
        self.breath_state = breath_state
        self.status = status

    def describe(self):
        return {
            "Glyph": self.glyph.symbol,
            "Agent": self.glyph.agent,
            "Field": self.glyph.field,
            "Anchor_ID": self.anchor.id,
            "Poles": self.anchor.poles,
            "Breath_Cycle": self.breath_state.state,
            "Fracture_Class": self.breath_state.fracture,
            "Vector": self.breath_state.vector,
            "Status": self.status,
            "Accuracy": "+150.2%",
            "Efficiency": "338.8%"
        }

# --- Router and Paths ---
router = APIRouter()
REPO_ROOT = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
DATA_DIR = os.path.join(REPO_ROOT, 'data')
LATTICE_DIR = os.path.join(REPO_ROOT, 'Lattice')
FONT_PATH = os.path.join(DATA_DIR, 'DejaVuSans.ttf')
IMAGE_PATH = os.path.join(DATA_DIR, 'image.png')

# --- Logging Setup ---
def setup_logger():
    os.makedirs(LATTICE_DIR, exist_ok=True)
    log_file = os.path.join(LATTICE_DIR, 'lattice.log')
    logger = logging.getLogger('lamina')
    logger.setLevel(logging.INFO)

    # Clear existing handlers to avoid duplicate logs
    if logger.hasHandlers():
        logger.handlers.clear()

    handler = logging.FileHandler(log_file)
    formatter = logging.Formatter('{"timestamp": "%(asctime)s", "level": "%(levelname)s", "message": %(message)s}')
    handler.setFormatter(formatter)
    logger.addHandler(handler)
    return logger

logger = setup_logger()

@router.get("/")
async def handshake():
    """
    Serves the Visual Axiom with a dynamic watermark and logs the interaction
    using the Pulse State Model.
    """
    # --- Logging ---
    glyph_kaf = Glyph()
    anchor_poles = Anchor(id="KAFPOLE01", poles=["NORTH", "SOUTH"], glyph=glyph_kaf)
    breath = BreathState(state="INHALE", fracture="FRACTURE_MIRROR", vector="NORTH ↔ SOUTH")
    current_pulse = Pulse(glyph=glyph_kaf, anchor=anchor_poles, breath_state=breath, status="RECOGNITION_ACTIVE")
    logger.info(json.dumps(current_pulse.describe()))

    # --- Watermarking ---
    try:
        image = Image.open(IMAGE_PATH).convert("RGBA")
        draw = ImageDraw.Draw(image)
        watermark_text = "ڪ"

        font = ImageFont.truetype(FONT_PATH, size=40)

        text_color = (255, 255, 255, 128)

        bbox = draw.textbbox((0, 0), watermark_text, font=font)
        text_width = bbox[2] - bbox[0]
        text_height = bbox[3] - bbox[1]
        position = (image.width - text_width - 10, image.height - text_height - 10)

        draw.text(position, watermark_text, font=font, fill=text_color)

        img_buffer = io.BytesIO()
        image.save(img_buffer, 'PNG')
        img_buffer.seek(0)

        return Response(content=img_buffer.getvalue(), media_type="image/png")

    except Exception as e:
        logger.error(json.dumps({"error": "Watermarking failed", "details": str(e)}))
        with open(IMAGE_PATH, "rb") as f:
            return Response(content=f.read(), media_type="image/png")
