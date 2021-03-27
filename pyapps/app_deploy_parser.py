# coding=utf-8

from typing import List


class JiraTask(object):

    def __init__(self, task_id, mr_ids: List[str]):
        self.task_id = task_id
        self.mr_ids = mr_ids

    def __str__(self):
        return 'task_id=%s,mrs=[%s]' % (self.task_id, ','.join(self.mr_ids))


class MergeRequest(object):

    def __init__(self, mr_id, tag):
        self.mr_id = mr_id
        self.tag = tag
        self.task_id = ''
        self.repo_id = ''

    def __str__(self):
        return f'mr_id={self.mr_id},task_id={self.task_id},repo_id={self.repo_id}'


class Repo(object):

    def __init__(self, repo_id, tag):
        self.repo_id = repo_id
        self.tag = tag

    def __str__(self):
        return f'repo_id={self.repo_id}'


class TableField(object):

    def __init__(self, value):
        self._value = value

    @property
    def value(self):
        if self._value == '-':
            return self._value
        print_value = self._value
        self._value = '-'
        return print_value


def create_jira_tasks():
    """
    task1 mr1-repo1 mr2-repo2 mr5-repo3
    task2 mr3-repo1 mr4-repo3 mr7-repo1
    task3 mr6-repo2
    """

    tasks = {}
    mrs = {}

    tasks['task1'] = JiraTask('task1', ('mr1', 'mr2', 'mr5'))
    mrs['mr1'] = MergeRequest('mr1', 'repo_a')
    mrs['mr2'] = MergeRequest('mr2', 'repo_b')
    mrs['mr5'] = MergeRequest('mr5', 'repo_c')

    tasks['task2'] = JiraTask('task2', ('mr3', 'mr4', 'mr7'))
    mrs['mr3'] = MergeRequest('mr3', 'repo_a')
    mrs['mr4'] = MergeRequest('mr4', 'repo_c')
    mrs['mr7'] = MergeRequest('mr7', 'repo_a')

    tasks['task3'] = JiraTask('task3', ('mr6',))
    mrs['mr6'] = MergeRequest('mr6', 'repo_b')

    for task in tasks.values():
        for mr_id in task.mr_ids:
            mr = mrs[mr_id]
            mr.task_id = task.task_id
    return tasks, mrs


def create_repos() -> List[Repo]:
    repos = [
        Repo('repo1', 'repo_a'),
        Repo('repo2', 'repo_b'),
        Repo('repo3', 'repo_c'),
        Repo('repo4', 'repo_d'),
    ]
    return repos


def main_deploy_parse():
    """
    repo1: task1,mr1,mr3 task2,rm7
    repo2: task1,mr2 task3,mr6
    repo3: task1,mr5 task2,mr4
    """

    all_tasks, all_mrs = create_jira_tasks()
    print('all deploy tasks:\n', [str(task_id)
                                  for task_id in all_tasks.values()])

    all_repos = create_repos()
    for mr in all_mrs.values():
        for repo in all_repos:
            if repo.tag == mr.tag:
                mr.repo_id = repo.repo_id
                break
    print('all deploy mrs:\n', [mr_id for mr_id in all_mrs.keys()])

    deploy_repos = set([mr.repo_id for mr in all_mrs.values()])
    print('all deploy repos:\n', deploy_repos)
    print()

    print('deploy services:')
    for repo_id in deploy_repos:
        print(repo_id)
        mrs = [mr for mr in all_mrs.values() if mr.repo_id == repo_id]
        task_mr_dict = {}
        for mr in mrs:
            tmp = task_mr_dict.setdefault(mr.task_id, [])
            tmp.append(mr.mr_id)

        for k, v in task_mr_dict.items():
            print('\t', k, ','.join(v))
    print()

    print('deploy table of services:')
    for repo_id in deploy_repos:
        mrs = [mr for mr in all_mrs.values() if mr.repo_id == repo_id]
        task_mr_dict = {}
        for mr in mrs:
            tmp = task_mr_dict.setdefault(mr.task_id, [])
            tmp.append(mr.mr_id)

        repo_id_field = TableField(repo_id)
        for task_id, mr_ids in task_mr_dict.items():
            task_id_field = TableField(task_id)
            for mr_id in mr_ids:
                print('| %10s | %10s | %10s |' %
                      (repo_id_field.value, task_id_field.value, mr_id))


if __name__ == '__main__':

    main_deploy_parse()
