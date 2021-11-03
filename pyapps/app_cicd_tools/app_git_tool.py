# coding=utf-8

# dependencies:
# pip install gitpython
# pip install python-gitlab

import datetime
import json
import os
import git
import gitlab
import time
import traceback

from gitlab import exceptions
from loguru import logger
from typing import List, Dict


def cur_dir():
    abs_path = os.path.abspath(__file__)
    return os.path.dirname(abs_path)


def get_dir_from_git_url(git_uri: str):
    return git_uri.split('/')[1].replace('.git', '')


def get_repo_name_from_web_url(web_url: str):
    fields = web_url.rstrip('\n').split('/')
    if len(fields) > 1:
        # (group_name, project_name)
        return fields[-2], fields[-1]
    else:
        raise Exception('invalid web url: ' + web_url)

#
# git tool
#


class GitTool(object):

    """
    api docs: https://gitpython.readthedocs.io/en/stable/reference.html
    """

    def __init__(self, repo_url, repo_path):
        if os.path.exists(repo_path):
            logger.info(f'current git repo set to [{repo_path}]')
            self._repo = git.Repo(repo_path)
        else:
            logger.info(f'clone git repo from [{repo_url}] to [{repo_path}]')
            self._repo = git.Repo.clone_from(url=repo_url, to_path=repo_path)
        self._git = self._repo.git

        self._is_local_debug = True

    @property
    def git(self):
        return self._git

    def create_branch(self, src_branch, dst_branch):
        logger.info(f'create branch: from {src_branch} to {dst_branch}')
        self._git.checkout(src_branch)
        self._git.pull('origin', src_branch)
        self._git.checkout('-b', dst_branch)
        if not self._is_local_debug:
            self._git.push('origin', dst_branch)

    def create_tag_for_commit(self, new_tag, commit_sha):
        logger.info(
            f'create tag [{new_tag}] for commit [{commit_sha}]')
        self._repo.create_tag(new_tag, ref=commit_sha)
        if not self._is_local_debug:
            self._git.push('origin', new_tag)

    def diff_branch_for_name_only(self, src_branch, dst_branch):
        self._git.checkout(src_branch)
        results = self._git.diff(dst_branch, '--name-only')
        return results.split('\n')

    def get_all_remote_branches(self):
        return [ref.name for ref in self._repo.remote().refs]

    def get_branch_head_sha(self, branch_name):
        head = self._repo.commit(branch_name)
        return str(head)[:6]

    def print_commit_info(self, branch_name, commit_sha):
        if len(commit_sha) < 5:
            logger.error(f'commit sha [{commit_sha}] length less than 5.')
            return

        commits = self._repo.iter_commits(branch_name)
        for commit in commits:
            if (commit.hexsha.startswith(commit_sha)):
                print('commit: sha=%s, author=%s, date=%s, message=%s' % (
                    commit.hexsha[:6], commit.author, commit.committed_date, commit.message))
                return

    def print_git_logs(self, num=3):
        print(self._git.log('--oneline', f'-{num}'))

#
# gitlab tool
#


class GitlabTool(object):

    """
    py api docs: https://python-gitlab.readthedocs.io/en/stable/gl_objects/mrs.html
    rest api docs: https://docs.gitlab.com/ee/api/merge_requests.html
    """

    def __init__(self, project_id=''):
        url = os.getenv('GITLAB_URL')
        if not url:
            raise EnvironmentError('env var [GITLAB_URL] is not set.')
        private_token = os.getenv('GITLAB_PRIVATE_TOKEN')
        if not private_token:
            raise EnvironmentError(
                'env var [GITLAB_PRIVATE_TOKEN] is not set.')

        self._gitlab = gitlab.Gitlab(url, private_token=private_token)
        if len(project_id) > 0:
            self.set_project_by_id(project_id)

    @property
    def gitlab(self):
        return self._gitlab

    #
    # project
    #

    def set_project_by_id(self, project_id):
        self._project = self._gitlab.projects.get(id=project_id)

    def set_project(self, project_name, group_name=''):
        projects = self._gitlab.projects.list(search=project_name)
        matched_pattern = project_name
        if len(group_name) > 0:
            matched_pattern = group_name + '/' + matched_pattern
        matched_projects = []
        for project in projects:
            if project.web_url.endswith(matched_pattern):
                matched_projects.append(project)
        if len(matched_projects) == 0:
            raise Exception(f'no projects found for [{matched_pattern}]')
        if len(matched_projects) > 1:
            found_projects = [(project.name, project.web_url)
                              for project in matched_projects]
            raise Exception(
                f'more than one projects found for {matched_pattern}: {found_projects}')

        self._project = matched_projects[0]

    def get_available_projects(self):
        return [prj.name for prj in self._gitlab.projects.list()]

    def print_project_info(self):
        project = self._project
        info_dict = {
            'name': project.name,
            'web_url': project.web_url,
        }
        print(json.dumps(info_dict))

    #
    # branch
    #

    def get_a_branch(self, branch_name):
        try:
            return self._project.branches.get(branch_name)
        except exceptions.GitlabGetError as e:
            logger.info(e.error_message + ": " + branch_name)

    def get_all_remote_branches(self) -> List[str]:
        return [branch.name for branch in self._project.branches.list(all=True)]

    def create_branch(self, src_branch, dst_branch, is_delete_existing=False):
        logger.info(
            f'repo [{self._project.name}]: create branch from [{src_branch}] to [{dst_branch}].')
        branch = self.get_a_branch(dst_branch)
        if branch:
            if is_delete_existing:
                backup_br = dst_branch+'-backup'
                logger.info(
                    f'branch [{dst_branch}] is exsit, and backup to [{backup_br}]')
                self._project.branches.create(
                    {'branch': backup_br, 'ref': dst_branch})
                self._project.branches.delete(dst_branch)
            else:
                logger.info(f'branch [{dst_branch}] already exists.')
                return

        data = {
            'branch': dst_branch,
            'ref': src_branch,
        }
        return self._project.branches.create(data)

    def protect_branch(self, branch_name, merge_access_level, push_access_level, allowed_user_ids: list):
        """
        Gitlab operation: Settings => Repository => Protected Branches
        """
        try:
            br = self._project.protectedbranches.get(branch_name)
            if br:
                logger.warning('protect branch [%s] is exsit' % branch_name)
                return
        except exceptions.GitlabGetError:
            pass

        data = {
            'name': branch_name,
            'merge_access_level': merge_access_level,
            'push_access_level': push_access_level,
        }
        if branch_name != 'master':
            allowed_users = [{'user_id': user_id}
                             for user_id in allowed_user_ids]
            data['allowed_to_push'] = allowed_users
            data['allowed_to_merge'] = allowed_users
        return self._project.protectedbranches.create(data)

    #
    # tag
    #

    def get_a_tag(self, tag_name):
        """
        return: gitlab.v4.objects.ProjectTag
        properties:
          'commit', 'delete', 'get_id', 'manager', 'message', 'name', 'project_id', 'protected', 'release', 'set_release_description', 'target'
        """
        try:
            return self._project.tags.get(tag_name)
        except exceptions.GitlabGetError as e:
            logger.info(e.error_message + ": " + tag_name)

    def get_tags(self, num=10):
        all_tags = self._project.tags.list()
        return all_tags[:num]

    def get_tag_commit_shortid(self, tag_name):
        commit = self.get_tag_commit(tag_name)
        return commit['short_id']

    def get_tag_commit(self, tag_name) -> Dict[str, str]:
        """
        tag.commit dict:
          'id', 'short_id', 'created_at', 'parent_ids', 'title', 'message', 'author_name', 'author_email', 'authored_date',
          'committer_name', 'committer_email', 'committed_date', 'web_url'
        """
        tag = self.get_a_tag(tag_name)
        return tag.commit

    def create_tag(self, tag_name, commit_sha):
        if self.get_a_tag(tag_name):
            logger.info(f"tag [{tag_name}] already exist.")
            return

        logger.info(f'create tag [{tag_name}] for commit [{commit_sha}].')
        data = {'tag_name': tag_name, 'ref': commit_sha}
        return self._project.tags.create(data)

    def compare_two_tags(self, old_tag, new_tag) -> dict:
        return self._compare_two_repo_object(old_tag, new_tag)

    def _compare_two_repo_object(self, old_obj, new_obj) -> dict:
        """ support compare two branches, tags or commits.

        commit dict:
          'id', 'short_id', 'created_at', 'parent_ids', 'title', 'message', 'author_name', 'author_email', 'authored_date',
          'committer_name', 'committer_email', 'committed_date', 'web_url'

        Note: diff commits results NOT base on given branch.
        """
        result = self._project.repository_compare(old_obj, new_obj)
        return {
            'commits': result['commits'],
            'diffs': result['diffs'],
        }

    def print_tag_info(self, tag):
        data = {
            'name': tag.name,
            'target': tag.target[:8],
            'message': tag.message,
        }
        return print(json.dumps(data))

    #
    # mr
    #

    def get_merge_request_by_id(self, mr_id):
        """
        return: gitlab.v4.objects.ProjectMergeRequest
        properties:
          'approval_rules', 'approvals', 'approvals_before_merge', 'approve', 'assignee', 'assignees',
          'attributes', 'author', 'awardemojis', 'blocking_discussions_resolved', 'cancel_merge_when_pipeline_succeeds',
          'changes', 'closed_at', 'closed_by', 'closes_issues', 'commits', 'created_at', 'delete', 'description', 'diffs',
          'discussion_locked', 'discussions', 'downvotes', 'force_remove_source_branch', 'get_id', 'has_conflicts',
          'id', 'iid', 'labels', 'manager', 'merge', 'merge_commit_sha', 'merge_status', 'merge_when_pipeline_succeeds',
          'merged_at', 'merged_by', 'milestone', 'notes', 'participants', 'pipelines', 'project_id', 'rebase', 'reference', 'references',
          'reset_spent_time', 'reset_time_estimate', 'resourcelabelevents', 'resourcemilestoneevents', 'save', 'sha',
          'should_remove_source_branch', 'source_branch', 'source_project_id', 'squash', 'squash_commit_sha', 'state', 'subscribe',
          'target_branch', 'target_project_id', 'task_completion_status', 'time_estimate', 'time_stats', 'time_stats', 'title',
          'todo', 'unapprove', 'unsubscribe', 'updated_at', 'upvotes', 'user_notes_count', 'web_url', 'work_in_progress'
        """
        return self._project.mergerequests.get(mr_id)

    def get_merge_requests_by_brname(self, state, branch_name, num=10) -> list:
        """
        state:
          all, merged, opened, closed
        """
        all_mrs = self._project.mergerequests.list(
            state=state, target_branch=branch_name, order_by='created_at')
        return all_mrs[:num]

    def get_merge_request_commits(self, mr):
        return mr.commits()

    def get_merged_mrs_from_commits(self, branch_name, commits: Dict[str, str]):
        """
        通过 commit 查询关联的 mr 信息。
        注：直接 push 或 mr 合入生成的 commit 并不会关联 mr.
        """
        branch_mrs = self.get_merge_requests_by_brname(
            'merged', branch_name, 10)
        result_mrs = []
        for mr in branch_mrs:
            mr_commits = self.get_merge_request_commits(mr)
            mr_commit_ids = [mr_commit.short_id for mr_commit in mr_commits]
            result_mrs.append({
                'id': mr.iid,
                'title': mr.title,
                'commits': mr_commit_ids,
            })

        print(f'\nmerged {branch_name} mrs:')
        for mr in result_mrs:
            print(json.dumps(mr))

        # filter mrs by commits
        ret_mrs = {}
        not_match_commit_ids = []
        for commit in commits:
            is_found = False
            for mr in result_mrs:
                if commit['short_id'] in mr['commits']:
                    is_found = True
                    iid = mr['id']
                    if iid not in ret_mrs.keys():
                        ret_mrs[iid] = ({
                            'id': iid,
                            'title': mr['title'],
                        })
                    break
            if not is_found:
                not_match_commit_ids.append(commit['short_id'])

        return list(ret_mrs.values()), not_match_commit_ids

    def print_merge_request_info(self, mr):
        info_dict = {
            'id': mr.id,
            'title': mr.title,
            'assignee': mr.assignee['username'],
            'source_branch': mr.source_branch,
            'target_branch': mr.target_branch,
            'state': mr.state,
            'merge_status': mr.merge_status,
            'pipelines': mr.pipelines(),
        }
        print(json.dumps(info_dict))

    #
    # commit
    #

    def get_a_commit(self, commit_id):
        """
        return: gitlab.v4.objects.ProjectCommit
        properties:
          'attributes', 'author_email', 'author_name', 'authored_date', 'cherry_pick', 'comments', 'committed_date',
          'committer_email', 'committer_name', 'created_at', 'diff', 'discussions', 'get_id', 'id', 'last_pipeline', 'manager',
          'merge_requests', 'message', 'parent_ids', 'project_id', 'refs', 'revert', 'short_id', 'signature',
          'stats', 'status', 'statuses', 'title', 'web_url'
        """
        return self._project.commits.get(commit_id)

    def get_branch_history_commits(self, branch_name, num=10) -> list:
        commits = self._project.commits.list(ref_name=branch_name)
        return commits[:num]

    def get_branch_head_sha(self, branch_name):
        commit = self.get_branch_history_commits(branch_name, 1)
        return commit[0].short_id

    def get_branch_commits_index(self, short_ids: List[str], branch_name, num=10) -> Dict[str, int]:
        commits = self.get_branch_history_commits(branch_name, num)
        ret_dict = {}
        for short_id in short_ids:
            ret_dict[short_id] = -1
            for idx, commit in enumerate(commits):
                if commit.short_id == short_id:
                    ret_dict[short_id] = idx
                    continue
        return ret_dict

    def get_commit_merge_requests(self, commit) -> List[dict]:
        """
        mr dict:
          'id', 'iid', 'project_id', 'title', 'description', 'state', 'created_at', 'updated_at', 'merged_by', 'merged_at',
          'closed_by', 'closed_at', 'target_branch', 'source_branch', 'user_notes_count', 'upvotes', 'downvotes',
          'author', 'assignees', 'assignee', 'source_project_id', 'target_project_id', 'labels', 'work_in_progress', 'milestone',
          'merge_when_pipeline_succeeds', 'merge_status', 'sha', 'merge_commit_sha', 'squash_commit_sha',
          'discussion_locked', 'should_remove_source_branch', 'force_remove_source_branch', 'reference', 'references',
          'web_url', 'time_stats', 'squash', 'task_completion_status', 'has_conflicts', 'blocking_discussions_resolved', 'approvals_before_merge'
        """
        return commit.merge_requests()

    def filter_commits_by_branch(self, commits: Dict[str, str], branch_name) -> Dict[str, str]:
        br_history_commits = self.get_branch_history_commits(branch_name, 50)
        ret_commits = []
        for commit in commits:
            for br_commit in br_history_commits:
                if commit['short_id'] == br_commit.short_id:
                    ret_commits.append(commit)
                    break
        return ret_commits

    def cherry_pick_a_commit(self, commit_sha, dst_branch):
        """
        Note: if code conflict, cherry pick will be failed. Instead, use git cli to manual cherry pick commit.
        """
        commit = self._project.commits.get(commit_sha)
        try:
            commit.cherry_pick(branch=dst_branch)
        except exceptions.GitlabCherryPickError as e:
            logger.error(
                f'gitlab cherry pick error for commit {commit_sha}: {e.error_message}')
            return False
        return True

    def compare_two_commits(self, old_commit_id, new_commit_id) -> dict:
        """
        Note: result diff commits may includes commits to diff branch.
        """
        return self._compare_two_repo_object(old_commit_id, new_commit_id)

    def print_commit_info(self, commit):
        data = {}
        for key in ('short_id', 'title', 'message', 'committer_email', 'committed_date', 'web_url'):
            data[key] = commit[key]
        print(json.dumps(data))

    #
    # file
    #

    def get_a_file(self, file_path, branch_name):
        try:
            return self._project.files.get(file_path=file_path, ref=branch_name)
        except exceptions.GitlabGetError as e:
            logger.warning(e.error_message + ': ' + file_path)

    def commit_a_file(self, commit_data: dict):
        """
        commit_data:
        {
            'file_path': 'testfile.txt',
            'branch': 'master',
            'content': file_content,
            'author_email': 'test@example.com',
            'author_name': 'yourname',
            'commit_message': 'Create testfile'
        }
        """
        f = self.get_a_file(commit_data["file_path"], commit_data["branch"])
        if f:
            logger.info(
                "file [%s] already exist, and not do commit." % commit_data["file_path"])
            return
        logger.info("commit a file [%s]" % commit_data["file_path"])
        return self._project.files.create(commit_data)

    #
    # hook
    #

    def create_project_hook(self, url, enable_events, disable_events):
        """
        Gitlab operation: Settings => Webhooks
        """
        hooks = self._project.hooks.list()
        for hook in hooks:
            if hook.url == url:
                logger.info("hook [%s] already exist." % url)
                return

        data = {
            'url': url,
        }
        for event in enable_events:
            data[event] = 1
        for event in disable_events:
            data[event] = 0
        return self._project.hooks.create(data)

    def print_project_hooks_info(self):
        hooks = self._project.hooks.list()
        for hook in hooks:
            info_dict = {
                'id': hook.id,
                'url': hook.url,
                'push_events': hook.push_events,
                'tag_push_events': hook.tag_push_events,
                'merge_requests_events': hook.merge_requests_events,
            }
            print('project hooks:')
            print(json.dumps(info_dict))

    def format_commit_datetime_to_timestamp(self, input_datetime) -> int:
        items = input_datetime.split('T')
        tmp_date = items[0]
        tmp_time = items[1][:8]

        d = datetime.datetime.strptime(
            f'{tmp_date} {tmp_time}', "%Y-%m-%d %H:%M:%S")
        return int(time.mktime(d.timetuple()))


#
# tag version
#


class TagVersion(object):

    """
    Regular: {module}-v{major}.{minor}.{patch}
    Hotfix and Ad hoc:
    {module}-v{major}.{minor}.{patch}-{type}

    Example:
    current version: rm-v1.2.0
    next regular: rm-v1.3.0
    next adhoc after regular: rm-v1.3.1-adhoc
    next hotfix after regular: rm-v1.3.1-hotfix
    """

    def __init__(self, version_name: str):
        fields = version_name.split('-')
        if len(fields) == 2:
            self._type = None
        elif len(fields) == 3:
            self._type = fields[2]
            if self._type not in ('hotfix', 'adhoc'):
                raise Exception('invalid version type: ' + self._type)
        else:
            raise Exception('invalid version name.')

        self._module = fields[0]
        self._version_number = VersionNumber(fields[1])

    def add_tag_version(self, number=1):
        if self._type:
            # emergency
            self._version_number.add_version_number_for_patch(number)
        else:
            self._version_number.add_version_number_for_regular(number)

    def __str__(self):
        if self._type:
            return '-'.join((self._module, str(self._version_number), self._type))
        return '-'.join((self._module, str(self._version_number)))


class VersionNumber(object):

    def __init__(self, version_number: str):
        if version_number.startswith('v'):
            version_number = version_number[1:]
        fields = version_number.split('.')
        if len(fields) != 3:
            raise Exception('invalid version number.')
        self._major = int(fields[0])
        self._minor = int(fields[1])
        self._patch = int(fields[2])

    def set_major_number(self, number):
        self._major = number

    def set_minor_number(self, number):
        self._minor = number

    def set_patch_number(self, number):
        self._patch = number

    def add_version_number_for_regular(self, number):
        self._minor += number

    def add_version_number_for_patch(self, number):
        self._patch += number

    def __str__(self):
        return 'v%d.%d.%d' % (self._major, self._minor, self._patch)

#
# main
#


repo_urls = [
    os.getenv('GITLAB_SSH_ADDR') + ':jin.zheng/zhengjin_worksapce.git',
]


def main_create_deploy_branches_by_git():
    """
    steps:
    1. create deploy branches
    2. add a tag on new release branch
    """
    root_path = '/tmp/test/repos'
    new_tag_name = 'v1.0.1-test'
    for repo_url in repo_urls:
        repo_path = get_dir_from_git_url(repo_url)
        tool = GitTool(repo_url, os.path.join(root_path, repo_path))
        for branch in ('master-backup', 'staging', 'release'):
            tool.create_branch('master', branch)
        commit_sha = tool.get_branch_head_sha('release')
        tool.create_tag_for_commit(new_tag_name, commit_sha)


def main_create_deploy_branches_by_gitlab():
    """
    steps:
    1. create deploy branches
    2. add a tag on new release branch
    """
    repo_names = ['zhengjin_worksapce', 'goc']
    new_tag_name = 'v1.0.1-test'
    tool = GitlabTool(repo_names[0])
    for repo in repo_names:
        tool.set_project(repo)
        for branch in ('master-backup', 'staging', 'release'):
            tool.create_branch('master', branch)
        head_sha = tool.get_branch_head_sha('release')
        tool.create_tag(new_tag_name, head_sha)


def main_check_all_projects():
    web_urls = None
    with open('/tmp/test/repos.txt', 'r') as f:
        web_urls = [line for line in f.readlines() if all(
            ('http' in line, not line.startswith('#')))]
    repos = [get_repo_name_from_web_url(url) for url in web_urls]

    tool = GitlabTool()
    failed_repos = []
    for repo in repos:
        try:
            tool.set_project(repo[1], group_name=repo[0])
        except Exception as e:
            logger.error(e)
            failed_repos.append('%s/%s' % (repo[0], repo[1]))
            continue
        tool.print_project_info()
        branches = [br for br in tool.get_all_remote_branches()
                    if 'pay' not in br.lower()]
        print('branches:', branches)
        tool.print_project_hooks_info()

    if len(failed_repos) > 0:
        logger.error("check failed gitlab repos: " + failed_repos)

#
# test
#


def test_tag_version():
    cur_tag_vers = ['rm-v1.2.0', 'rm-v1.3.0-hotfix', 'rm-v1.3.0-ad']
    for version in cur_tag_vers:
        print('current tag version:', version)
        tag_version = TagVersion(version)
        tag_version.add_tag_version()
        print('next tag version:', tag_version)


def test_gitlab_rest_api():
    import requests

    gitlab_url = os.getenv('GITLAB_URL')
    private_token = os.getenv('GITLAB_PRIVATE_TOKEN')

    url = f'{gitlab_url}api/v4/users/4902/projects'
    header = {'PRIVATE-TOKEN': private_token}
    resp = requests.get(url, headers=header)
    print(resp.status_code)
    print('get a project:', resp.json()[0]['name'])


def test_git_tool():
    root_path = '/tmp/test/repos'
    for repo_url in repo_urls:
        repo_path = get_dir_from_git_url(repo_url)
        tool = GitTool(repo_url, os.path.join(root_path, repo_path))
        print(tool.get_all_remote_branches())


def test_gitlab_tool():
    prj_name = os.getenv('GITLAB_REPO')
    group_name = os.getenv('GITLAB_GROUP')

    tool = GitlabTool()
    tool.set_project(prj_name, group_name=group_name)
    tool.print_project_info()

    def test_create_br():
        print(tool.get_all_remote_branches())
        tool.create_branch('master', 'release', is_delete_existing=True)

    def test_project_mr():
        mr = tool.get_merge_request_by_id(4)
        tool.print_merge_request_info(mr)

    def test_project_tag():
        for tag in tool.get_tags():
            tool.print_tag_info(tag)

    def test_project_commit():
        print(tool.get_branch_head_sha('master'))
        tool.cherry_pick_a_commit('dab8b78', 'master')

    def test_add_webhook():
        hook_url = 'http://qa-test/webhook'
        enable_events = ['tag_push_events', 'merge_requests_events']
        disable_events = ['push_events']
        tool.create_project_hook(hook_url, enable_events, disable_events)
        tool.print_project_hooks_info()

    def test_commit_a_file():
        file_content = None
        with open('/tmp/test/gitlab-ci.yml', 'r') as f:
            file_content = f.read()
        commit_data = {
            'file_path': '.gitlab-ci.yml',
            'branch': 'master',
            'content': file_content,
            'author_email': 'jin.zheng@xxxxx.com',
            'author_name': 'zhengjin',
            'commit_message': 'Create gitlab ci file.'
        }
        print(tool.commit_a_file(commit_data))

    if False:
        test_create_br()
        test_project_mr()
        test_project_tag()
        test_project_commit()
        test_add_webhook()
        test_commit_a_file()

    test_project_tag()


def test_gitlab_compare_two_commits():
    prj_name = os.getenv('GITLAB_REPO')
    if not prj_name:
        raise Exception('env var [GITLAB_REPO] is not set')
    group_name = os.getenv('GITLAB_GROUP')
    tool = GitlabTool()
    tool.set_project(prj_name, group_name=group_name)
    tool.print_project_info()

    def test_get_br_head_commit():
        latest_commit_short_id = tool.get_branch_head_sha('staging')
        print('latest commit for staging branch:', latest_commit_short_id)

    def test_get_br_commit_index():
        br_name = 'master'
        commits = tool.get_branch_history_commits(br_name, num=10)
        for cm in commits:
            print(
                f'short id: {cm.short_id}, title: {cm.title}, commit date: {cm.committed_date}')

        short_ids = ['00f5b4cb', '00f5b4xx', 'e95cffa2']
        res = tool.get_branch_commits_index(short_ids, br_name)
        for k, v in res.items():
            print(f'commit {k}, index: {v}')

    def test_get_tag_commit():
        test_tag = 'release-2021.10.v2'
        release_tag = tool.get_a_tag(test_tag)
        if release_tag:
            tool.print_tag_info(release_tag)
            commit = tool.get_tag_commit(test_tag)
            tool.print_commit_info(commit)

    def test_diff_tags():
        print('get history commits by diff tag:')
        test_tag = 'release-2021.10.v2'
        result = tool.compare_two_tags(test_tag, f'{test_tag}-hotfix')
        diff_commits = result['commits']
        print('diff commits count:', len(diff_commits))
        for commit in diff_commits:
            tool.print_commit_info(commit)

    def test_diff_commits():
        print('get history commits by diff commits:')
        result = tool.compare_two_commits('1dd9122e', '7a0add46')
        diff_commits = result['commits']
        diff_files = result['diffs']
        print('diff commits count %d, diff files count %d' %
              (len(diff_commits), len(diff_files)))
        for commit in diff_commits:
            print(commit['short_id'], commit['title'])

    def test_get_to_uat_mrs():
        uat_mrs = tool.get_merge_requests_by_brname('merged', 'uat', num=5)
        print('top 10 uat merged mrs:')
        for mr in uat_mrs:
            print(mr.iid, mr.title)
            commits = tool.get_merge_request_commits(mr)
            print('\ttotal:', commits.total)
            for commit in commits:
                print('\t\t', commit.short_id, commit.title)

    def test_compare_commits_by_date():
        import time
        import datetime
        new_commit = tool.get_a_commit('5d15c4ef')
        old_commit = tool.get_a_commit('9ed45ae3')

        new_ts = tool.format_commit_datetime_to_timestamp(
            new_commit.committed_date)
        old_ts = tool.format_commit_datetime_to_timestamp(
            old_commit.committed_date)
        print('compare commit date:', new_ts > old_ts)

    if False:
        test_get_br_head_commit()
        test_get_br_commit_index()
        test_get_tag_commit()
        test_diff_tags()
        test_diff_commits()
        test_get_to_uat_mrs()
        test_compare_commits_by_date()
    test_get_br_head_commit()


def test_gitlab_filter_commits_by_branch():
    prj_name = os.getenv('GITLAB_REPO')
    tool = GitlabTool()
    tool.set_project(prj_name)
    tool.print_project_info()

    # get history commits between two commits
    result = tool.compare_two_commits('36ddb7eb', '12aa2338')
    diff_commits = result['commits']
    print('src diff commits count:', len(diff_commits))

    # get history commits for uat branch
    uat_commits = tool.filter_commits_by_branch(diff_commits, 'uat')
    uat_commits = [
        commit for commit in uat_commits if not commit['title'].startswith('Merge branch')]
    print(f'\nuat history commits count: {len(uat_commits)}')
    print('commits:', [commit['short_id'] for commit in uat_commits])

    # get commits linked master mrs
    print('\nmaster')
    ret_mrs, not_match_commit_ids = tool.get_merged_mrs_from_commits(
        uat_commits, 'master')
    print('mr data:', json.dumps(ret_mrs))
    print('not matched commit ids:', not_match_commit_ids)

    # get commits linked staging mrs
    print('\nstaging')
    uat_commits = [
        commit for commit in uat_commits if commit['short_id'] in not_match_commit_ids]
    ret_mrs, not_match_commit_ids = tool.get_merged_mrs_from_commits(
        uat_commits, 'staging')
    print('\nmr data:', json.dumps(ret_mrs))

    # commits push to uat directly, and no mr linked
    print('not matched commit ids:', not_match_commit_ids)


if __name__ == '__main__':

    try:
        # main_check_all_projects()
        # main_create_deploy_branches_by_git()
        # main_create_deploy_branches_by_gitlab()

        # test_tag_version()

        # test_git_tool()

        # test_gitlab_rest_api()
        # test_gitlab_tool()
        # test_gitlab_compare_two_commits()
        # test_gitlab_filter_commits_by_branch()
        pass
    except:
        traceback.print_exc()

    print('git tool test done.')
