# Julius AI Orchestrator

This project is a FastAPI-based orchestrator for routing tasks to different AI agents. It currently includes a mock `JuliusAgent` and an `OpenAICriticAgent`. The project also includes a command-line tool, `jules`, for interacting with the orchestrator's API.

## Getting Started

### Prerequisites

*   Python 3.8+
*   pip

### Installation

1.  Clone the repository:
    ```bash
    git clone <repository-url>
    cd <repository-directory>
    ```

2.  Install the dependencies:
    ```bash
    pip install -r requirements.txt
    ```

### Running the Server

1.  Set the required environment variables. For now, a dummy token is sufficient.
    ```bash
    export JULIUS_API_TOKEN="dummy_token"
    ```

2.  Start the FastAPI server:
    ```bash
    uvicorn src.main:app --host 127.0.0.1 --port 8000
    ```
    The server will be running at `http://127.0.0.1:8000`.

## Using the `jules` Command-Line Tool

The `jules` command-line tool provides a convenient way to interact with the orchestrator's API from the terminal.

### `remote` commands

The `remote` subcommand is used to interact with remote sessions and repositories.

#### `pull`

Pull the results for a specific session.

```bash
python3 scripts/jules.py remote pull --session <session_id>
```
Example:
```bash
python3 scripts/jules.py remote pull --session 12345
```

#### `list`

List connected repositories or sessions.

```bash
# List repositories
python3 scripts/jules.py remote list --repo

# List sessions
python3 scripts/jules.py remote list --session
```

#### `new`

Start a new session in a repository.

```bash
python3 scripts/jules.py remote new --repo <repository_name> --session "<session_description>"
```
Example:
```bash
python3 scripts/jules.py remote new --repo torvalds/linux --session "write unit tests"
```
