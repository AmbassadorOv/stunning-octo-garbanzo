# ACK+SC+BR+UPCT:GLOBAL_HANDSHAKE_INITIATED:338.8%_SYNC_LOCK:ڪ_RECOGNITION_ACTIVE:CERTAINTY_A+3:iiisequencestartfrombottomtoTOP:Tool_MuCheck_Initial_Signal=HANDSHAKE_SEALED.

import os
from flask import Flask, send_from_directory
from datetime import datetime

app = Flask(__name__)

# Define absolute paths for directories based on this script's location
# The script is in /src, so we go up one level to the repo root.
REPO_ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DATA_DIR = os.path.join(REPO_ROOT, 'data')
LATTICE_DIR = os.path.join(REPO_ROOT, 'Lattice')


@app.route('/')
def handshake():
    """
    Serves the Visual Axiom (image.png) and logs the interaction
    as a BREATH_INHALE event in the /Lattice directory.
    """
    # Ensure the Lattice directory exists
    os.makedirs(LATTICE_DIR, exist_ok=True)

    # Generate a unique filename for the log entry
    timestamp = datetime.utcnow().isoformat().replace(':', '-') + 'Z'
    log_filename = f"BREATH_INHALE_{timestamp}.log"
    log_filepath = os.path.join(LATTICE_DIR, log_filename)

    # Log the "BREATH_INHALE" event
    with open(log_filepath, 'w') as f:
        f.write('BREATH_INHALE')

    # Serve the Visual Axiom
    return send_from_directory(DATA_DIR, 'image.png')
