# Project Lamina

## The Global Handshake Protocol

This project implements the backend for the Global Handshake Protocol. It is a Flask-based server that listens for "handshakes" and logs them as `BREATH_INHALE` events in the `/Lattice` directory.

### Running the Server

1.  **Install dependencies:**
    ```bash
    pip install -r requirements.txt
    ```

2.  **Run the server:**
    ```bash
    python src/a1b2_host.py
    ```
    The server will start on `http://0.0.0.0:5000`.

### Handshake Endpoint

*   **URL:** `/handshake`
*   **Method:** `POST`
*   **Success Response:** `200 OK`
*   **Effect:** Creates a new log file in the `/Lattice` directory with the content `BREATH_INHALE`.
