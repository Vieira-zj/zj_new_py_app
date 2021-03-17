# coding=utf-8

# dependencies:
# pip install gitpython
# pip install python-gitlab

import json
import os

import git
import gitlab
from gitlab.exceptions import GitlabCherryPickError
from loguru import logger


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
    api docs: https://python-gitlab.readthedocs.io/en/stable/gl_objects/mrs.html
    """

    def __init__(self, url, private_token, project_name, group_name=''):
        self._gitlab = gitlab.Gitlab(url, private_token=private_token)
        self.set_project(project_name, group_name)

    @property
    def gitlab(self):
        return self._gitlab

    # project

    def set_project(self, project_name, group_name=''):
        projects = self._gitlab.projects.list(search=project_name)
        if len(projects) == 0:
            raise Exception(f'no projects found for [{project_name}]')
        if len(projects) == 1:
            self._project = projects[0]
            return

        matched_pattern = project_name
        if len(group_name) > 0:
            matched_pattern = group_name + '/' + matched_pattern
        matched_projects = []
        for project in projects:
            if all((project.name == project_name, matched_pattern in project.web_url)):
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

    # branch

    def get_all_remote_branches(self):
        return [branch.name for branch in self._project.branches.list()]

    def create_branch(self, src_branch, dst_branch, is_delete_existing=False):
        logger.info(f'create branch from {src_branch} to {dst_branch}.')
        data = {
            'branch': dst_branch,
            'ref': src_branch,
        }
        branch = self._project.branches.get(dst_branch)
        if branch:
            if is_delete_existing:
                logger.warning(
                    f'backup old branch [{dst_branch}], and create new.')
                self._project.branches.create(
                    {'branch': dst_branch+'-backup', 'ref': dst_branch})
                self._project.branches.delete(dst_branch)
            else:
                logger.warning(
                    f'create branch [{dst_branch}] failed, already exists.')
                return

        return self._project.branches.create(data)

    # tag

    def get_tags(self):
        return self._project.tags.list()

    def create_tag(self, tag_name, commit_sha):
        logger.info(f'create tag [{tag_name}] for commit [{commit_sha}].')
        data = {'tag_name': tag_name, 'ref': commit_sha}
        return self._project.tags.create(data)

    def print_tag_info(self, tag):
        data = {
            'name': tag.name,
            'message': tag.message,
            'target': tag.target[:6],
            'commit_msg': tag.commit['message'],
        }
        return print(json.dumps(data))

    # mr

    def get_open_merge_requests(self):
        return self.get_merge_requests('opened')

    def get_merge_requests(self, state):
        return self._project.mergerequests.list(state=state, order_by='updated_at')

    def get_merge_request_by_id(self, mr_id):
        return self._project.mergerequests.get(mr_id)

    def print_merge_request_info(self, mr):
        info_dict = {
            'title': mr.title,
            'assignee': mr.assignee['username'],
            'source_branch': mr.source_branch,
            'target_branch': mr.target_branch,
            'state': mr.state,
            'merge_status': mr.merge_status,
            'pipelines': mr.pipelines(),
        }
        print(json.dumps(info_dict))

    # commit

    def get_branch_head_sha(self, branch_name):
        commits = self._project.commits.list(ref_name=branch_name)
        return commits[0].short_id

    def cherry_pick_a_commit(self, commit_sha, dst_branch):
        """
        Note: if code conflict, cherry pick will be failed. Instead, use git cli to manual cherry pick commit.
        """
        commit = self._project.commits.get(commit_sha)
        try:
            commit.cherry_pick(branch=dst_branch)
        except GitlabCherryPickError as e:
            logger.error(
                f'gitlab cherry pick error for commit {commit_sha}: {e.error_message}')
            return False
        return True

    # file

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
        return self._project.files.create(commit_data)

    # hook

    def create_project_hook(self, url, enable_events, disable_events):
        data = {
            'url': url,
        }
        for event in enable_events:
            data[event] = 1
        for event in disable_events:
            data[event] = 0
        self._project.hooks.create(data)

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
    'gitlab@git.xxxxx.com:jin.zheng/zhengjin_worksapce.git',
]
gitlab_url = 'https://git.xxxxx.com/'
private_token = 'token'


def test_git_tool():
    root_path = '/tmp/test/repos'
    for repo_url in repo_urls:
        repo_path = get_dir_from_git_url(repo_url)
        tool = GitTool(repo_url, os.path.join(root_path, repo_path))
        print(tool.get_all_remote_branches())


def test_gitlab_tool():
    group_name = ''
    project_names = ['zhengjin_worksapce']
    for prj_name in project_names:
        tool = GitlabTool(gitlab_url, private_token,
                          prj_name, group_name=group_name)
        tool.print_project_info()

        if False:
            # create br
            print(tool.get_all_remote_branches())
            tool.create_branch('master', 'release', is_delete_existing=True)

            # mr
            mr = tool.get_merge_request_by_id(4)
            tool.print_merge_request_info(mr)

            for tag in tool.get_tags():
                tool.print_tag_info(tag)

            # tag
            print(tool.get_branch_head_sha('master'))
            tool.cherry_pick_a_commit('dab8b78', 'master')

            # add a web hook
            hook_url = 'http://qa-test/webhook'
            enable_events = ['tag_push_events', 'merge_requests_events']
            disable_events = ['push_events']
            tool.create_project_hook(hook_url, enable_events, disable_events)
            tool.print_project_hooks_info()

            # commit a file
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
    tool = GitlabTool(gitlab_url, private_token, repo_names[0])
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

    for repo in repos:
        tool = GitlabTool(gitlab_url, private_token,
                          repo[1], group_name=repo[0])
        tool.print_project_info()
        branches = [br for br in tool.get_all_remote_branches()
                    if 'label' not in br.lower()]
        print('branches:', branches)
        tool.print_project_hooks_info()


def test_tag_version():
    cur_tag_vers = ['rm-v1.2.0', 'rm-v1.3.0-hotfix', 'rm-v1.3.0-ad']
    for version in cur_tag_vers:
        print('current tag version:', version)
        tag_version = TagVersion(version)
        tag_version.add_tag_version()
        print('next tag version:', tag_version)


if __name__ == '__main__':

    # test_git_tool()
    # main_create_deploy_branches_by_git()

    # test_gitlab_tool()
    # main_create_deploy_branches_by_gitlab()

    # main_check_all_projects()

    test_tag_version()
    print('git tool test done.')
