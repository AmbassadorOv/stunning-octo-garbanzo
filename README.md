# Julius Thinking Machine Orchestrator (V3)

This project provides a containerized, deployable multi-agent orchestrator service that can query different AI models (specifically OpenAI and Gemini) in parallel and aggregate their responses.

## Features

-   **Multi-Model Orchestration:** Queries OpenAI (gpt-4-turbo, gpt-4o) and Gemini (gemini-1.5-pro, gemini-1.5-flash) models in parallel.
-   **Epistemic Aggregation:** Aggregates responses from different models to provide a consensus answer with a confidence score.
-   **Hex 6F Workflow:** Implements a core formula for calculating an "action estimate" based on the consensus confidence.
-   **Reverse Audit Logic:** Includes an `/audit` endpoint for reverse auditing of logs and incidents.
-   **Containerized:** The application is fully containerized with Docker for easy deployment.

## Getting Started

### Prerequisites

-   Docker and Docker Compose
-   OpenAI API Key
-   Gemini API Key

### Running the Application

1.  **Create a `.env` file:**
    ```bash
    cp .env.template .env
    ```
2.  **Edit the `.env` file:**
    -   Add your `OPENAI_API_KEY` and `GEMINI_API_KEY`.
3.  **Build and run the Docker container:**
    ```bash
    docker-compose up --build
    ```

### API Endpoints

-   **`/orchestrate` (POST):**
    -   The main endpoint for querying the orchestrator.
    -   Accepts a JSON payload with a `prompt` and other parameters.
    -   Returns an aggregated response with a consensus answer and confidence score.
-   **`/audit` (GET):**
    -   An endpoint for triggering the reverse audit logic.

### Example Usage

```bash
curl -sS -X POST http://localhost:8080/orchestrate \
  -H "Content-Type: application/json" \
  -d '{
    "context_id":"test-001",
    "prompt":"Database write errors on service payments since 03:00 UTC. Show root-cause hypotheses and minimal remediation steps.",
    "goal":"restore payment writes within 15 minutes",
    "max_tokens":400,
    "temperature":0.1,
    "hex_step":"A",
    "reverse_sequence":true
  }' | jq .
```
