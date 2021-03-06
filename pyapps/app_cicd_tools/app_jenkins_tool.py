# coding: utf-8

import os
import json
import re
import requests
import time
import traceback
import xml.dom.minidom as xmldom


class JenkinsTools(object):

    """
    apis:
    http://jenkins-host/job/{job-name}/api
    http://jenkins-host/job/{job-name}/{build-no}/api
    """

    def __init__(self):
        jenkins_host = os.getenv('JENKINS_HOST')
        if not jenkins_host:
            raise EnvironmentError('env JENKINS_HOST is not set.')

        self._jenkins_host = jenkins_host
        self._session = self._build_session()

    def _build_session(self):
        sess = requests.session()
        default_headers = {
            'Content-Type': 'application/json',
            'cookie': os.getenv('JENKINS_COOKIE'),
            'jenkins-crumb': os.getenv('JENKINS_CRUMB')
        }
        sess.headers.update(default_headers)
        return sess

    def close(self):
        if self._session:
            self._session.close()

    def _resp_handler(self, resp):
        # case 404: start a build, and build in queue (not run immediately)
        code = resp.status_code
        assert int(code / 100) == 2 or code == 404, resp.text

    #
    # job
    #

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

    #
    # build
    #

    def get_build_info(self, job_name, build_no, is_print=True):
        '''
        Get jenkins job's build info.
        '''
        url = f'{self._jenkins_host}/job/{job_name}/{build_no}/api/json'
        resp = self._session.get(url)
        self._resp_handler(resp)
        if resp.text.startswith('<html>'):
            return {}

        resp_obj = resp.json()
        if is_print:
            print('build name=%s, building=%s, duration=%s(sec), result=%s' % (
                resp_obj['fullDisplayName'], resp_obj['building'], (int(resp_obj['duration'] / 1000)), resp_obj['result']))

        build_params = []
        actions = resp_obj['actions']
        for action in actions:
            if 'ParametersAction' in action.get('_class', ''):
                build_params = action['parameters']

        params = {}
        for item in ('ENVIRONMENT', 'BRANCH', 'TAG'):
            for param in build_params:
                if param['name'] == item:
                    params[item] = param['value']
        if is_print:
            print('\nbuild parameters:', params)

        remote_urls = ''
        for action in actions:
            if 'BuildData' in action.get('_class', ''):
                remote_urls = action['remoteUrls']
                break
        if is_print and remote_urls:
            print('\nbuild git repo url:', remote_urls[0])

        ret_data = {
            'build_no': build_no,
            'params': params,
        }
        for key in ('building', 'duration', 'result'):
            ret_data[key] = resp_obj[key]
        return ret_data

    def get_lastbuild_number(self, job_name) -> int:
        url = f'{self._jenkins_host}/job/{job_name}/lastBuild/buildNumber'
        resp = self._session.get(url)
        self._resp_handler(resp)
        return int(resp.text)

    def get_nextbuild_number(self, job_name) -> int:
        return self.get_lastbuild_number(job_name) + 1

    def get_build_console_log(self, job_name, build_no):
        url = f'{self._jenkins_host}/job/{job_name}/{build_no}/logText/progressiveText?start=0'
        resp = self._session.get(url)
        self._resp_handler(resp)
        return resp.text

    def get_build_stages_info(self, job_name, build_no):
        """
        apis:
        https://github.com/jenkinsci/pipeline-stage-view-plugin/tree/master/rest-api#get-jobjob-namewfapiruns
        """
        url = f'{self._jenkins_host}/job/{job_name}/{build_no}/wfapi/describe'
        resp = self._session.get(url)
        self._resp_handler(resp)
        build_data = resp.json()

        ret_data = {}
        for key in ('id', 'name', 'status'):
            ret_data[key] = build_data[key]
        ret_data['duration'] = '%.2fs' % (build_data['durationMillis'] / 1000)

        ret_stages = []
        for stage in build_data['stages']:
            node_id = self._get_node_id_from_link(
                stage['_links']['self']['href'])
            ret_log = self.get_build_stage_log_data(
                job_name, build_no, node_id)

            ret_stages.append({
                'name': stage['name'],
                'status': stage['status'],
                'duration': '%.2fs' % (stage['durationMillis'] / 1000),
                'log': ret_log,
            })
        ret_data['stages'] = ret_stages
        return ret_data

    def get_build_stage_log_data(self, job_name, build_no, node_id):
        url = f'{self._jenkins_host}//job/{job_name}/{build_no}/execution/node/{node_id}/wfapi/log'
        resp = self._session.get(url)
        self._resp_handler(resp)
        log_data = resp.json()

        ret_data = {}
        for key in ('length', 'consoleUrl'):
            ret_data[key] = log_data[key]
        return ret_data

    def _get_node_id_from_link(self, link):
        regexp = re.compile(r'node/(\d+)/')
        m = regexp.search(link)
        return m.groups()[0]

    #
    # operation
    #

    def start_job_build_with_params(self, job_name, payload: dict) -> str:
        """
        return queue id from location.
        Location: https://jenkins.i.airpay.com/queue/item/564210/
        """
        url = f'{self._jenkins_host}/job/{job_name}/buildWithParameters'
        resp = self._session.post(url, params=payload)
        self._resp_handler(resp)

        queue_no = self._get_queueno_from_location(resp.headers['Location'])
        return queue_no if queue_no else ''

    def get_executeno_by_queueno(self, queue_no, timeout=10) -> str:
        # note: if use /api/json, no executable data
        url = f'{self._jenkins_host}/queue/item/{queue_no}/api/xml'
        for _ in range(0, timeout):
            resp = self._session.get(url)
            execute_no = self._get_executeno_from_resp(resp.text)
            if execute_no:
                return execute_no
            print(f'wait executable for queue no [{queue_no}] ...')
            time.sleep(1)
        return ''

    def _get_queueno_from_location(self, location) -> str:
        return self._get_key_by_regexp(location, r'item/(\d+)/$')

    def _get_executeno_from_resp(self, body) -> str:
        return self._get_key_by_regexp(body, r'<number>(\d+)</number>')

    def _get_key_by_regexp(self, text, pattern) -> str:
        regexp = re.compile(pattern)
        m = regexp.search(text)
        if not m or (len(m.groups()) == 0):
            return ''
        return m.groups()[0]

    def wait_build_start(self, job_name, build_no, timeout=10) -> bool:
        for _ in range(timeout):
            print(f'wait job [{job_name}] build [{build_no}] start ...')
            if self.is_build_running(job_name, build_no):
                return True
            time.sleep(1)
        return False

    def is_build_running(self, job_name, build_no) -> bool:
        build_info = self.get_build_info(job_name, build_no, is_print=False)
        return bool(build_info['building']) if build_info else False

#
# test
#


def test_get_job_info(tool: JenkinsTools, job: str):
    print(f'job [{job}] info:')
    tool.get_job_info(job)

    if False:
        print(f'\njob [{job}] config data:')
        tool.get_job_config(job)


def test_get_build_info(tool: JenkinsTools, job: str):
    build_no = tool.get_lastbuild_number(job)
    if False:
        print(f'job [{job}] build info for {build_no}:')
        tool.get_build_info(job, build_no)

        print(f'\njob [{job}] build [{build_no}] console log:')
        logs = tool.get_build_console_log(job, build_no)
        logs = [log for log in logs.split('\r\n') if len(log.strip()) > 0]
        for log in logs[-10:]:
            print(log)

    print(f'\njob [{job}] build [{build_no}] stages info:')
    print(tool.get_build_stages_info(job, build_no))


def test_run_a_build(tool: JenkinsTools, job: str):
    """
    refer:
    https://stackoverflow.com/questions/28311030/check-jenkins-job-status-after-triggering-a-build-remotely
    https://wiki.jenkins-ci.org/display/JENKINS/Jenkins+CLI
    """
    build_no = tool.get_nextbuild_number(job)
    print(f'job [{job}]: start build [{build_no}]')

    # start build
    payload = {
        'ENVIRONMENT': 'test',
        'BRANCH': 'origin/master',
    }
    queue_no = tool.start_job_build_with_params(job, payload)
    execute_no = tool.get_executeno_by_queueno(queue_no, timeout=30)
    print(f'job [{job}]: start execute [{execute_no}]')
    assert execute_no == str(
        build_no), f'execute no [{execute_no} is not equal to build no {build_no}]'

    if not tool.wait_build_start(job, build_no, timeout=30):
        raise EnvironmentError(
            f'job [{job}]: no running build [{build_no}] found')

    # check build
    build_info = tool.get_build_info(job, build_no)
    build_params = build_info['params']
    for k in payload.keys():
        assert build_params[k] == payload[
            k], f'running build [{build_no}] parameters [{k}] are not matched'

    # wait build done
    while tool.is_build_running(job, build_no):
        print(f'\njob [{job}]: wait build [{build_no}] done ...')
        print(tool.get_build_stages_info(job, build_no))
        time.sleep(3)

    # get build info
    res = tool.get_build_info(job, build_no, is_print=False)
    print('job [%s] build [%s] finished: duration=%.2f(s),result=%s' %
          (job, build_no, (res['duration'] / 1000), res['result']))


if __name__ == '__main__':

    job = 'test-dev-grpc-swagger'
    tool = None
    try:
        tool = JenkinsTools()
        # test_get_job_info(tool, job)
        # test_get_build_info(tool, job)
        test_run_a_build(tool, job)
    except Exception:
        traceback.print_exc()
    finally:
        if tool:
            tool.close()
