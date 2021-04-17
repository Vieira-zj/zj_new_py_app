# coding: utf-8
import json
import logging
import requests
import time


class JiraTools(object):

    _jira_host = 'https://jira.xxxxx.io'
    _jira_rest_api_url = f'{_jira_host}/rest/api/latest'
    _jira_webhook_url = f'{_jira_host}/rest/webhooks/1.0/webhook'
    # token: echo -n 'username:password' | base64
    _auth_token = 'base64_token'

    def __init__(self):
        self._sess = requests.session()
        default_headers = {'Authorization': 'Basic ' +
                           self._auth_token, 'Content-Type': 'application/json'}
        self._sess.headers.update(default_headers)

    '''
    query issues
    '''

    def search(self, query: str, limit=3, fields=['id', 'key']):
        url = f'{self._jira_rest_api_url}/search'
        query_dict = {
            'jql': query,
            'maxResults': limit,
            'fields': fields,
        }
        resp = self._sess.post(url, json=query_dict)
        assert(resp.status_code >= 200)
        print('ret_code=%d, ret_text=%s' % (resp.status_code, resp.text))

    def get_issue(self, issue_id, expand_fields: list):
        expend = ','.join(expand_fields)
        url = f'{self._jira_rest_api_url}/issue/{issue_id}?expand={expend}'
        resp = self._sess.get(url)
        assert(resp.status_code >= 200)

        json_text = resp.text
        json_object = json.loads(json_text)
        label = json_object['fields']['labels']
        desc = json_object['renderedFields']['description']
        resolution = json_object['names']['resolution']
        print(
            f'issue [{issue_id}] info: label={label}, description={desc}, resolution={resolution}')

    '''
    remote issue link api:
    https://developer.atlassian.com/server/jira/platform/jira-rest-api-for-remote-issue-links/
    '''

    def add_remote_issue_link(self, issue_id, link, title):
        url = f'{self._jira_rest_api_url}/issue/{issue_id}/remotelink'
        favicon_url = 'https://git.xxxxx.com/assets/favicon-7901bd695fb93edb07975966062049829afb56cf11511236e61bcf425070e36e.png'
        link_data = {
            'object': {
                'url': link,
                'title': title,
                'icon': {
                    'url16x16': favicon_url,
                    'title': 'Gitlab'
                }
            }
        }
        resp = self._sess.post(url, json=link_data)
        self.resp_handler(resp)

    def get_remote_issue_links(self, issue_id):
        url = f'{self._jira_rest_api_url}/issue/{issue_id}/remotelink'
        resp = self._sess.get(url)
        self.resp_handler(resp)

    def delete_remote_issue_link(self, issue_id, link_id):
        url = f'{self._jira_rest_api_url}/issue/{issue_id}/remotelink/{link_id}'
        resp = self._sess.delete(url)
        self.resp_handler(resp)

    '''
    webhook api:
    https://developer.atlassian.com/server/jira/platform/webhooks/
    '''

    def query_webhook(self):
        resp = self._sess.get(self._jira_webhook_url)
        self.resp_handler(resp)

    def register_a_webhook(self, wh_data: dict):
        resp = self._sess.post(self._jira_webhook_url, json=wh_data)
        self.resp_handler(resp)

    def unregister_a_webhook(self, wh_id):
        url = f'{self._jira_webhook_url}/{wh_id}'
        resp = self._sess.delete(url)
        self.resp_handler(resp)

    def resp_handler(self, resp):
        assert(resp.status_code >= 200)
        print(resp.text)

    def close(self):
        if self._sess is not None:
            self._sess.close()


def get_issues_test(jira):
    # get a issue
    issue_id = 'issue-xxxxx'
    expand_fields = ['names', 'renderedFields']
    jira.get_issue(issue_id, expand_fields)

    # search issues by query
    jql = 'assignee="jin.zheng@xxxxx.com" AND resolution=Unresolved'
    jira.search(jql)


def remote_issue_link_test(jira):
    # add issue link
    issue_id = 'issue-xxxxx'
    link = 'https://git.xxxxx.com/jin.zheng/zhengjin_worksapce/-/merge_requests/1'
    title = f'[Merge Request] - {issue_id} / Update workspace readme.'
    jira.add_remote_issue_link(issue_id, link, title)

    # get issue links
    time.sleep(1)
    jira.get_remote_issue_links(issue_id)

    # delete issue link
    # link_id = '1194974'
    # jira.delete_remote_issue_link(issue_id, link_id)


def webhook_test(jira):
    jira.query_webhook()

    webhook_data_dict = {
        "name": "zj webhook test via rest",
        "url": "http://www.xxxxx.com/webhooks",
        "events": [
            "jira:issue_created",
                "jira:issue_updated"
        ],
        "filters": {
            "issue-related-events-section": "assignee=\"jin.zheng@xxxxx.com\" AND resolution=Unresolved"
        },
        "excludeBody": False
    }
    jira.register_a_webhook(webhook_data_dict)


if __name__ == '__main__':

    jira = JiraTools()
    try:
        # get_issues_test(jira)
        # remote_issue_link_test(jira)
        webhook_test(jira)
    finally:
        if jira:
            jira.close()

    print('jira demo done.')
