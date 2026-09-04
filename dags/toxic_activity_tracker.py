from datetime import datetime, timedelta

from airflow.sdk import dag, task
from airflow.providers.github.hooks.github import GithubHook
from github.Event import Event
from github.PaginatedList import PaginatedList
from github import Github

from include.discord import send_to_discord

# ===============================================================
# DIRECTED ACYCLIC GRAPH
# ===============================================================

@dag(
    schedule=None, # I'm changing this to run every 20:00 PM ig
    catchup=False
)
def toxic_activity_tracker():
    """
    It connects to my GitHub and observes how many commits did I submit today
    """

    @task
    def get_commits() -> list:
        client = GithubHook(github_conn_id='github-conn').get_conn() or None

        if client:
            return _get_commits_task(client)
        else:
            err_msg = 'LOGIC ERROR: client cannot be authorized'

            send_to_discord(err_msg + ' @everyone')
            print(err_msg)
            raise

    @task
    def send_toxic_message(commits: list):

        return _send_toxic_message_task(commits)

    # call tasks
    commits = get_commits()
    send_toxic_message(commits)


# ===============================================================
# TASK FUNCTIONS
# ===============================================================


def _get_commits_task(client: Github):
    events: PaginatedList[Event] = client.get_user().get_events()
    yesterday = datetime.now() - timedelta(hours=10)

    commit_list = []
    for event in events[:20]:
        if event.type == 'PushEvent' and event.created_at > yesterday:
            commits = event.payload.get("commits", [])

            for commit in commits:
                commit_list.append(commit.message)
    
    return commit_list


def _send_toxic_message_task(commits: list):
    if commits:
        # he roasts my commits
        pass
    else:
        # he roasts me anyways because I didn't do shi
        pass


# INIT DAG
toxic_activity_tracker()