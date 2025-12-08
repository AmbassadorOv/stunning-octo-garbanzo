import click
import httpx
import json

BASE_URL = "http://127.0.0.1:8000"

@click.group()
def jules():
    """A command-line tool to interact with the Julius AI."""
    pass

@jules.group()
def remote():
    """Commands for interacting with remote sessions and repositories."""
    pass

@remote.command()
@click.option('--session', required=True, help='The ID of the session to pull results for.')
def pull(session):
    """Pull the results for a specific session."""
    try:
        with httpx.Client() as client:
            response = client.post(f"{BASE_URL}/remote/pull", json={"session_id": session})
            response.raise_for_status()
            click.echo(json.dumps(response.json(), indent=2))
    except httpx.RequestError as e:
        click.echo(f"Error: {e}", err=True)

@remote.command('list')
@click.option('--repo', is_flag=True, help='List all connected repositories.')
@click.option('--session', is_flag=True, help='List all active and past sessions.')
def list_items(repo, session):
    """List connected repositories or sessions."""
    if not repo and not session:
        click.echo("Please specify what to list: --repo or --session.", err=True)
        return

    params = {}
    if repo:
        params["list_repos"] = True
    if session:
        params["list_sessions"] = True

    try:
        with httpx.Client() as client:
            response = client.post(f"{BASE_URL}/remote/list", json=params)
            response.raise_for_status()
            click.echo(json.dumps(response.json(), indent=2))
    except httpx.RequestError as e:
        click.echo(f"Error: {e}", err=True)


@remote.command()
@click.option('--repo', required=True, help="The repository to start a new session in (e.g., 'torvalds/linux').")
@click.option('--session', required=True, help='A description for the new session.')
def new(repo, session):
    """Start a new session in a repository."""
    try:
        with httpx.Client() as client:
            response = client.post(f"{BASE_URL}/remote/new", json={"repo": repo, "session_description": session})
            response.raise_for_status()
            click.echo(json.dumps(response.json(), indent=2))
    except httpx.RequestError as e:
        click.echo(f"Error: {e}", err=True)

if __name__ == "__main__":
    jules()
