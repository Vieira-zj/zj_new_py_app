# coding: utf-8
import json
import requests
import xml.dom.minidom as xmldom


class JenkinsTools(object):

    def __init__(self, jenkins_host, is_debug=False):
        self._jenkins_host = jenkins_host
        self._is_debug = is_debug
        self._session = self._build_session()

    def _build_session(self):
        sess = requests.session()
        default_headers = {
            'Content-Type': 'application/json',
            'cookie': 'JSESSIONID.9a305488=node0xr3i86qyhr782hvo5qlbd5gw87464.abcde',
            'jenkins-crumb': '7fa30d61e7d9530f52d9ef46f26bb56e40b0029ff8b77608192e951da53bcdef'
        }
        sess.headers.update(default_headers)
        return sess

    def close(self):
        if self._session:
            self._session.close()

    def _resp_handler(self, resp):
        assert(resp.status_code >= 200)
        if self._is_debug:
            print(resp.text)

    def get_job_info(self, job_name):
        '''
        Get jenkins job info.
        '''
        # url = f'{self._jenkins_host}/view/{view_name}job/{job_name}/api/json'
        url = f'{self._jenkins_host}/job/{job_name}/api/json'
        resp = self._session.get(url)
        self._resp_handler(resp)
        resp_obj = resp.json()
        print('job name=%s, desc=%s color=%s' %
              (resp_obj['fullName'], resp_obj['description'], resp_obj['color']))

        last_build = resp_obj['lastBuild']
        print('\nlast build: number=%s, url=%s' %
              (last_build['number'], last_build['url']))
        next_build = resp_obj['nextBuildNumber']
        print('next build number:', next_build)

        print('\njob parameters:')
        params = None
        properties = resp_obj['property']
        for p in properties:
            if 'ParametersDefinitionProperty' in p['_class']:
                params = p['parameterDefinitions']
                break
        for p in params:
            print('param_name=%s, param_type=%s' % (p['name'], p['type']))

    def get_job_config(self, job_name):
        '''
        Get jenkins job xml config.
        '''
        url = f'{self._jenkins_host}/job/{job_name}/config.xml'
        resp = self._session.get(url)
        self._resp_handler(resp)
        config_dom = xmldom.parseString(resp.text)
        root_element = config_dom.documentElement

        desc = root_element.getElementsByTagName('description')[0]
        print('job description:', desc.firstChild.data)

        remote_cfg = root_element.getElementsByTagName(
            'hudson.plugins.git.UserRemoteConfig')[0]
        git_repo_url = remote_cfg.getElementsByTagName('url')[0]
        print('git repo url:', git_repo_url.firstChild.data)

    def get_build_info(self, job_name, build_no):
        '''
        Get jenkins job's build info.
        '''
        url = f'{self._jenkins_host}/job/{job_name}/{build_no}/api/json'
        resp = self._session.get(url)
        self._resp_handler(resp)
        resp_obj = resp.json()

        print('build name=%s, building=%s, duration=%s(sec), result=%s' % (
            resp_obj['fullDisplayName'], resp_obj['building'], (int(resp_obj['duration'] / 1000)), resp_obj['result']))

        actions = resp_obj['actions']
        build_data = None
        for action in actions:
            if 'BuildData' in action.get('_class', ''):
                build_data = action
                break
        print('git repo url:', build_data['remoteUrls'][0])

    def get_running_builds(self, job_name):
        '''
        Get running builds in a jenkins job.
        '''
        last_build_no = self.get_lastbuild_number(job_name)
        print(f'job [{job_name}] running builds:')
        for i in range(last_build_no, 0, -1):
            build_name, is_running = self.is_build_running(job_name, i)
            if not is_running:
                print('no running builds')
                break
            print(f'#{i} {build_name}')

    def get_lastbuild_number(self, job_name):
        url = f'{self._jenkins_host}/job/{job_name}/lastBuild/buildNumber'
        resp = self._session.get(url)
        self._resp_handler(resp)
        return int(resp.text)

    def is_build_running(self, job_name, build_no):
        url = f'{self._jenkins_host}/job/{job_name}/{build_no}/api/json'
        resp = self._session.get(url)
        self._resp_handler(resp)
        resp_obj = resp.json()
        return resp_obj['fullDisplayName'], bool(resp_obj['building'])

    def get_lastbuild_console_log(self, job_name):
        url = f'{self._jenkins_host}/job/{job_name}/lastBuild/logText/progressiveText'
        resp = self._session.get(url)
        self._resp_handler(resp)
        print(f'job [{job_name}] last build console log:')
        print(resp.text)

    def start_job_build_with_params(self, job_name, playload: dict):
        url = f'{self._jenkins_host}/job/{job_name}/buildWithParameters'
        resp = self._session.post(url, params=playload)
        self._resp_handler(resp)
        print(resp.text)


if __name__ == '__main__':

    jenkins_host = 'https://jenkins.i.xxxxx.com'
    job = 'qa-dev-goc-feature-ci'
    build_no = '30'

    tool = None
    try:
        tool = JenkinsTools(jenkins_host, is_debug=False)
        # tool.get_job_info(job)
        # tool.get_job_config(job)

        # tool.get_build_info(job, build_no)
        print(tool.get_lastbuild_number(job))
        # tool.get_lastbuild_console_log(job)

        # job = 'apa_deploy_server_pipeline'
        # tool.get_running_builds(job)

        # playload = {
        #     'FEATURE_BRANCH': 'origin/feature-20201209',
        #     'BASE_BRANCH': 'remotes/origin/master',
        # }
        # tool.start_job_build_with_params(job, playload)
    finally:
        if tool:
            tool.close()
