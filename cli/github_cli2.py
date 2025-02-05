import json

import click
import requests
from decouple import config

# https://docs.github.com/en/rest/reference/issues#create-an-issue

# Autenticação
REPO_USERNAME = config('REPO_USERNAME')
REPO_PASSWORD = config('REPO_PASSWORD')

# O repositório para adicionar a issue
REPO_OWNER = config('REPO_OWNER')
REPO_NAME = config('REPO_NAME')

@click.command()
@click.option('--title', prompt='Title', help='Type the title.')
@click.option('--body', prompt='Description', help='Type the description.')
@click.option('--assignee', prompt='Assignee', help='Type the assignee.')
@click.option('--labels', prompt='Labels', help='Type the labels.')
def make_github_issue(title, body=None, assignee=None, milestone=None, labels=None):
    '''
    Create an issue on github.com using the given parameters.
    '''
    url = 'https://api.github.com/repos/%s/%s/issues' % (REPO_OWNER, REPO_NAME)
    session = requests.Session()
    session.auth = (REPO_USERNAME, REPO_PASSWORD)
    # Create our issue
    issue = {
        'title': title,
        'body': body,
        'assignee': assignee,
        'milestone': milestone,
        'labels': [labels]
    }
    # Add the issue to our repository
    r = session.post(url, json.dumps(issue))
    if r.status_code == 201:
        print('Successfully created Issue "%s"' % title)
    else:
        print('Could not create Issue "%s"' % title)
        print('Response:', r.content)


if __name__ == '__main__':
    make_github_issue()
