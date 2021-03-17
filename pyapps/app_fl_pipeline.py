'''
Wrapped flowengine offline scenario APIs.
'''
import logging
import json
import random
import requests
import uuid

from retrying import retry

# env vars
profile = 'test'  # test, prod
base_url = ''
login_dict = {}

# constants
base_headers = {'Content-Type': 'application/json;charset=utf-8'}
default_timeout = 3  # seconds
default_retry = 3
default_page_size = 10
user_token = ''

logging.basicConfig(level=logging.INFO,
                    format='%(asctime)s - %(levelname)s: %(message)s')
logger = logging.getLogger(__name__)


# -----------------------------------------------
# Init
# -----------------------------------------------


def init_env():
    global base_url, login_dict
    if profile == 'test':
        base_url = 'http://172.27.128.236:40121/'
        login_dict = {'username': 'aaaaa', 'password': 'bbbbb'}
    elif profile == 'prod':
        base_url = 'http://kp.hwwt2.com/'
        login_dict = {'username': 'xxxxx', 'password': 'xxxxx'}


@retry(stop_max_attempt_number=default_retry)
def test_retry():
    url = f'http://127.0.0.1:17891/mocktest/one/3'
    data_dict = {'code': random.choice((200, 403, 502))}
    resp = requests.get(url, params=data_dict)
    logger.info('ret_code=%d, ret_text=%s' % (resp.status_code, resp.text))
    assert(resp.status_code == 200)


@retry(stop_max_attempt_number=default_retry)
def login():
    url = base_url + 'keystone/v1/sessions'

    sess = requests.session()
    sess.headers.update(base_headers)
    resp = sess.post(url, data=json.dumps(login_dict), timeout=default_timeout)
    log_request_info(resp.request)
    assert(resp.status_code == 200)

    cookies_dict = requests.utils.dict_from_cookiejar(resp.cookies)
    logger.info('login with user token: %s' % cookies_dict['User-Token'])
    return sess


# -----------------------------------------------
# Get info and operator for running flowengines
# -----------------------------------------------


@retry(stop_max_attempt_number=default_retry)
def list_running_flowengines(sess, workspace_id, size=default_page_size):
    '''
    List all running flowengine instances.
    '''
    url = base_url + 'automl-manager/v1/appList'
    data_dict = {'workspaceId': workspace_id,
                 'status': 'RUNNING', 'size': size}
    resp = sess.get(url, params=data_dict, timeout=default_timeout)
    assert(resp.status_code == 200)
    if not assert_response_status(resp):
        return []

    fl_list = resp.json()['data']['appList']
    return [{'instanceId': fl['instanceId'], 'status': fl['status'], 'appName': fl['appName']} for fl in fl_list]


@retry(stop_max_attempt_number=default_retry)
def list_fl_pipelines(sess, instance_id, template_id):
    '''
    List all pipelines for a running flowengine.
    '''
    url = base_url + \
        f'automl-engine/{instance_id}/automl/v1/pipeline/{template_id}/list'
    resp = sess.get(url, timeout=default_timeout)
    assert(resp.status_code == 200)
    if not assert_response_status(resp):
        return []

    pipelines = resp.json()['data']
    if profile == 'v2':
        pipelines = pipelines['engineJobPipelineTemplateList']
    return [{'template_id': p['engineTemplateId'], 'id': p['id'], 'status': p['data']['status']}
            for p in pipelines]


@retry(stop_max_attempt_number=default_retry)
def run_fl_pipeline(sess, instance_id, template_id, pipeline_id):
    url = base_url + \
        f'automl-engine/{instance_id}/automl/v1/pipeline/{template_id}/{pipeline_id}/start'
    resp = sess.post(url, data=r'{}', timeout=default_timeout)
    assert(resp.status_code == 200)

    if assert_response_status(resp):
        status = resp.json()['data']['status']
        if status == 'running':
            return True
    return False


@retry(stop_max_attempt_number=default_retry)
def list_fl_pipeline_tasks(sess, instance_id, pipeline_id):
    '''
    List all history tasks of a flowengine pipeline.
    '''
    url = base_url + \
        f'automl-engine/{instance_id}/automl/v1/pipeline/{pipeline_id}/historyList'
    resp = sess.get(url, timeout=default_timeout)
    assert(resp.status_code == 200)
    if not assert_response_status(resp):
        return []

    tasks = resp.json()['data']
    return sorted([{'id': t['id'], 'status':t['status']} for t in tasks], key=lambda x: x['id'])


@retry(stop_max_attempt_number=default_retry)
def stop_fl_pipeline_task(sess, instance_id, pipeline_id, task_id):
    url = base_url + \
        f'automl-engine/{instance_id}/automl/v1/pipeline/{task_id}/stopHistory?engineId={pipeline_id}'
    resp = sess.delete(url, data=r'{}', timeout=default_timeout)
    assert(resp.status_code == 200)

    return True if assert_response_status(resp) else False


@retry(stop_max_attempt_number=default_retry)
def resume_fl_pipeline_task(sess, instance_id, pipeline_id, task_id):
    url = base_url + \
        f'automl-engine/{instance_id}/automl/v1/pipeline/{task_id}/resumeHistory?engineId={pipeline_id}'
    resp = sess.post(url, data=r'{}', timeout=default_timeout)
    assert(resp.status_code == 200)

    return True if assert_response_status(resp) else False


def update_and_run_pipeline_demo(sess):
    '''
    Update param of a pipeline node, and run pipeline.
    '''
    fl_id = 60
    data_dict = {'page': 1, 'size': 20}
    url = base_url + f'automl-engine/{fl_id}/automl/v1/pipeline/1/list'
    resp = sess.get(url, params=data_dict, timeout=default_timeout)
    assert(resp.status_code == 200)

    # get pipeline
    pipeline_id = 1
    pipeline = {}
    pipelines = resp.json()['data']['engineJobPipelineTemplateList']
    for p in pipelines:
        if p['id'] == pipeline_id:
            pipeline = p
    assert(pipeline is not None)

    # get node (job)
    node_name = 'offline_job01'
    node = {}
    nodes = pipeline['data']['nodes']
    for n in nodes:
        if n['name'] == node_name:
            node = n
    assert(node is not None)

    # get node param
    key_name = 'param1'
    param = {}
    params = node['params']['values']
    for p in params:
        if p['key'] == key_name:
            param = p
    assert(param is not None)
    logger.info('to update: ' + str(param))

    # update node param of pipeline
    # url = base_url + f'automl-engine/{fl_id}/automl/v1/pipeline/template/1/update'


# -----------------------------------------------
# Get info and operator for flowengine template
# -----------------------------------------------


@retry(stop_max_attempt_number=default_retry)
def list_template_pipelines(sess, template_id, size=default_page_size):
    '''
    List all pipelines of template.
    '''
    url = base_url + \
        f'template-market/v1/pipeline/template/{template_id}/list/byPage?size={size}'
    resp = sess.get(url, timeout=default_timeout)
    assert(resp.status_code == 200)
    if not assert_response_status(resp):
        return []

    return [{'id': template['id'], 'describe': template['data']['describe']}
            for template in resp.json()['data']['engineJobPipelineTemplateList']]


@retry(stop_max_attempt_number=default_retry)
def list_template_jobs(sess, template_id, size=default_page_size):
    '''
    List all jobs of template.
    '''
    url = base_url + \
        f'template-market/v1/job/template/{template_id}/list/byPage?page=1&size={size}'
    resp = sess.get(url, timeout=default_timeout)
    assert(resp.status_code == 200)
    if not assert_response_status(resp):
        return []

    return [{'id': job['id'], 'name': job['name']}
            for job in resp.json()['data']['engineJobTemplateList']]


def list_template_pipeline_jobs(sess, template_id, pipeline_id, size=default_page_size):
    data = get_template_pipeline_data(sess, template_id, pipeline_id, size)
    return [{'name': node['name']} for node in data['data']['nodes']] if len(data) > 0 else []


@retry(stop_max_attempt_number=default_retry)
def get_template_pipeline_data(sess, template_id, pipeline_id, size=10):
    '''
    Get meta data of a pipeline.
    '''
    url = base_url + \
        f'template-market/v1/pipeline/template/{template_id}/list/byPage?size={size}'
    resp = sess.get(url, timeout=default_timeout)
    assert(resp.status_code == 200)
    if not assert_response_status(resp):
        return {}

    pipelines = [p for p in resp.json()['data']['engineJobPipelineTemplateList']
                 if str(p['id']) == pipeline_id]
    return pipelines[0] if len(pipelines) > 0 else {}


@retry(stop_max_attempt_number=default_retry)
def get_template_job_data(sess, template_id, job_id, size=default_page_size):
    '''
    Get meta data of a job.
    '''
    url = base_url + \
        f'template-market/v1/job/template/{template_id}/list/byPage?page=1&size={size}'
    resp = sess.get(url, timeout=default_timeout)
    assert(resp.status_code == 200)
    if not assert_response_status(resp):
        return {}

    jobs = [job for job in resp.json()['data']['engineJobTemplateList']
            if str(job['id']) == job_id]
    return jobs[0] if len(jobs) > 0 else {}


@retry(stop_max_attempt_number=default_retry)
def create_template_pipeline_job(sess, template_id, pipeline_template_name):
    '''
    Create a pipeline job of template.
    '''
    url = base_url + \
        f'template-market/v1/job/template/{template_id}/create'
    data = build_pipeline_job_data(template_id, pipeline_template_name)
    resp = sess.post(url, data=json.dumps(data), timeout=default_timeout)
    assert(resp.status_code == 200)
    return True if assert_response_status(resp) else False


def build_pipeline_job_data(template_id, template_name):
    data = {'name': template_name, 'engineTemplateId': template_id,
            'indexType': 'DAG', 'type': 'TASK', 'system': False}

    outputCfg = data['outputConfig'] = {}
    outputCfg['outputType'] = 'Table'

    execCfg = data['executionConfig'] = {}
    execCfg['runMode'] = 'SINGLE'
    execCfg['interval'] = 0
    execCfg['intervalUnit'] = 'MINUTE'
    execCfg['trigger'] = 'ModelTrainFinishEvent'
    return data


@retry(stop_max_attempt_number=default_retry)
def delete_template_pipeline_job(sess, template_id, job_id):
    '''
    Delete a pipeline job of template.
    '''
    url = base_url + \
        f'template-market/v1/job/template/{template_id}/{job_id}/delete'
    resp = sess.delete(url, data=r'{}', timeout=default_timeout)
    assert(resp.status_code == 200)
    return True if assert_response_status(resp) else False


@retry(stop_max_attempt_number=default_retry)
def delete_template_pipeline(sess, template_id, pipeline_id):
    '''
    Delete a pipeline of template.
    '''
    url = base_url + \
        f'template-market/v1/pipeline/template/{template_id}/{pipeline_id}/delete'
    resp = sess.delete(url, data=r'{}', timeout=default_timeout)
    assert(resp.status_code == 200)
    return True if assert_response_status(resp) else False


# -----------------------------------------------
# Copy and edit pipeline and job of template
# -----------------------------------------------


@retry(stop_max_attempt_number=default_retry)
def copy_template_pipeline(sess, template_id, src_pipeline_id, pipeline_name):
    '''
    Create a new pipeline of template from a source pipeline.
    '''
    url = base_url + \
        f'template-market/v1/pipeline/template/{template_id}/create'

    data = get_template_pipeline_data(sess, template_id, src_pipeline_id)
    if len(data) == 0:
        logger.error(f'srouce pipeline(id={src_pipeline_id}) is not found!')
        return False
    else:
        data = data['data']

    data['name'] = pipeline_name
    data['describe'] = f'pipeline copied from pipelineID={src_pipeline_id}.'

    req_data = {'engineTemplateId': template_id,
                'pipelineKey': pipeline_name + '_' + str(uuid.uuid1())[:8]}
    req_data['data'] = data

    resp = sess.post(url, data=json.dumps(req_data), timeout=default_timeout)
    assert(resp.status_code == 200)
    return True if assert_response_status(resp) else False


@retry(stop_max_attempt_number=default_retry)
def copy_template_job(sess, template_id, src_job_id, job_name):
    '''
    Create a new job of template from a source job.
    '''
    url = base_url + f'template-market/v1/job/template/{template_id}/create'

    req_data = get_template_job_data(sess, template_id, src_job_id)
    if len(req_data) == 0:
        logger.error(f'srouce job(id={src_job_id}) is not found!')
        return False

    req_data['id'] = None
    req_data['name'] = job_name
    req_data['desc'] = f'job copied from jobID={src_job_id}.'

    resp = sess.post(url, data=json.dumps(req_data), timeout=default_timeout)
    assert(resp.status_code == 200)
    return True if assert_response_status(resp) else False


@retry(stop_max_attempt_number=default_retry)
def update_template_pipeline(sess, template_id, pipeline_id):
    '''
    Update existing pipeline of template.
    Example: update pipeline context key value.
    '''
    url = base_url + \
        f'template-market/v1/pipeline/template/{template_id}/update'

    req_data = get_template_pipeline_data(sess, template_id, pipeline_id)
    context_kv = req_data['data']['pipelineParams']['values']
    # for test
    if len(context_kv) > 0:
        context_kv[0]['describe'] = 'new test kv desc.'

    resp = sess.put(url, data=json.dumps(req_data), timeout=default_timeout)
    assert(resp.status_code == 200)
    return True if assert_response_status(resp) else False


@retry(stop_max_attempt_number=default_retry)
def update_template_job(sess, template_id, job_id, params):
    '''
    Update existing job of template.
    Example: update job name and description.
    '''
    url = base_url + f'template-market/v1/job/template/{template_id}/update'

    req_data = get_template_job_data(sess, template_id, job_id)
    for k, v in params.kv_map.items():
        req_data[k] = v

    resp = sess.put(url, data=json.dumps(req_data), timeout=default_timeout)
    assert(resp.status_code == 200)
    return True if assert_response_status(resp) else False


class JobParams(object):
    '''
    Job parameters for create and update a job of template.
    '''

    def __init__(self):
        self.kv_map = {}

    def set_name(self, name):
        self.kv_map['name'] = name
        return self

    def set_desc(self, text):
        self.kv_map['desc'] = text
        return self


# -----------------------------------------------
# Common
# -----------------------------------------------


def log_request_info(req):
    logger.debug('request url: %s' % req.url)
    logger.debug('request headers: %s' % req.headers)
    logger.debug('request method: %s' % req.method)
    logger.debug('request body: %s' % req.body)


def assert_response_status(resp):
    cond = (str(resp.json()['status']) == '0')
    if not cond:
        logger.error('***** assert response status FAILED.')
        logger.error('***** response:\n' + resp.text)
    return cond


class MyRequest(object):
    '''
    Http request with common logs and assert.
    '''

    def get(self, *args, **kwargs):
        resp = requests.get(*args, **kwargs)
        self._log_request_info(resp)
        self._log_response_info(resp)
        self._assert_success(resp)

    def post(self, *args, **kwargs):
        resp = requests.post(*args, **kwargs)
        self._log_request_info(resp.request)
        self._log_response_info(resp)
        self._assert_success(resp)

    def _log_request_info(self, request):
        title_line = "| " + "*" * 30 + "REQUEST" + "*" * 30
        logger.info(title_line)

        logger.info("|  Method: " + request.method)
        logger.info("|  Url: " + request.url)
        logger.info("|  Headers:")
        for k, v in request.headers.items():
            logger.info("|    %s: %s" % (k, v))

        data = request.body
        if data and len(data) > 0:
            logger.info("|  Request Data:")
            logger.info("|    " + data)
        self._print_divide_line(len(title_line))

    def _log_response_info(self, response):
        title_line = "| " + "*" * 30 + "RESPONSE" + "*" * 30
        logger.info(title_line)
        logger.info("|  Status Code: " + str(response.status_code))
        logger.info("|  Headers:")
        for k, v in response.headers.items():
            logger.info("|    %s: %s" % (k, v))

        data = response.content
        if data and len(data) > 0:
            logger.info("|  Response Data:")
            logger.info("|    " + str(data))
        self._print_divide_line(len(title_line))

    def _assert_success(self, response):
        assert "status code not equal to 200", response.status_code == 200
        # validate json
        # json_object = json.loads(response.content)

    def _print_divide_line(self, length=60):
        logger.info("|" + "*" * length)


# -----------------------------------------------
# Main
# -----------------------------------------------


def test_fl_main(sess):
    workspace_id = '47'
    instance_id = '371'
    running_template_id = '1'
    running_pipeline_id = '3'
    # pipeline_task_id = '19'

    logger.info(list_running_flowengines(sess, workspace_id))

    logger.info(list_fl_pipelines(sess, instance_id, running_template_id))
    # ret = run_fl_pipeline(sess, instance_id, running_template_id, running_pipeline_id)

    logger.info(list_fl_pipeline_tasks(sess, instance_id, running_pipeline_id))
    # ret = resume_fl_pipeline_task(sess, instance_id, running_pipeline_id, pipeline_task_id)
    # ret = stop_fl_pipeline_task(sess, instance_id, running_pipeline_id, pipeline_task_id)
    # assert(ret)
    logger.info('flowengine pipeline api demo done.')


def test_template_main(sess):
    template_id = '10027'
    pipeline_id = '33'
    # job_id = '147'

    logger.info(list_template_pipelines(sess, template_id))
    logger.info(list_template_jobs(sess, template_id))
    logger.info(list_template_pipeline_jobs(sess, template_id, pipeline_id))

    # ret = create_template_pipeline_job(sess, template_id, 'offline_job05')
    # ret = delete_template_pipeline_job(sess, template_id, job_id)
    # ret = delete_template_pipeline(sess, template_id, pipeline_id)
    logger.info('flowengine template api demo done.')


def test_template_copy_edit_main(sess):
    # template_id = '10032'
    # pipeline_id = '65'
    # job_id = '147'

    # pipeline_key = 'copied_pipeline_test04'
    # ret = copy_template_pipeline(sess, template_id, pipeline_id, pipeline_key)

    # job_name = 'copied_job_test04'
    # ret = copy_template_job(sess, template_id, job_id, job_name)

    # params = JobParams()
    # params.set_name('new_job_test04').set_desc('new job desc.')
    # ret = update_template_job(sess, template_id, job_id, params)

    # ret = update_template_pipeline(sess, template_id, pipeline_id)
    # assert(ret)
    logger.info('flowengine template api demo done.')


if __name__ == '__main__':

    # test_retry()

    init_env()
    sess = login()
    try:
        # test_fl_main(sess)
        # test_template_main(sess)
        # test_template_copy_edit_main(sess)
        update_and_run_pipeline_demo(sess)
    finally:
        sess.close()
