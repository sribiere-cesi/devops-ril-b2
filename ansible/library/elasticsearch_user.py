#!/usr/bin/env python

import sys
import json
import requests
from ansible.module_utils.basic import AnsibleModule


class ElasticsearchUserResource(object):

    def __init__(self, url, auth=()):
        self.url = url.strip('/')
        self.auth = auth

        self.__check_xpack()

    def __check_xpack(self):
        url = '{}/_xpack'.format(self.url)
        response = requests.get(url, auth=self.auth)
        if response.status_code not in [200, 401]:
            raise Exception('No x-pack plugin')

    def __get_user_url(self, username=None):
        return '%s/_xpack/security/user/%s' % (self.url, username)

    def __raise(self, response):
        try:
            output = json.loads(response.text)
            raise Exception(output['error']['reason'])
        except ValueError as error:
            raise Exception(
                requests.status_codes._codes[response.status_code][0])

    def check_authentication(self, username, password):
        url = '{}/'.format(self.url)
        response = requests.get(url, auth=(username, password))
        if response.status_code in [200, 403]:
            return True
        elif response.status_code == 401:
            return False
        else:
            self.__raise(response)

    def get(self, username):
        url = self.__get_user_url(username)
        response = requests.get(url, auth=self.auth)
        if response.status_code == 200:
            return json.loads(response.text)[username]
        elif response.status_code == 404:
            return None
        else:
            self.__raise(response)

    def save(self, username, data):
        url = self.__get_user_url(username)
        data = json.dumps(data)
        response = requests.post(url, data=data, auth=self.auth)
        if not response.ok:
            self.__raise(response)

    def delele(self, username):
        url = self.__get_user_url(username)
        response = requests.delete(url, auth=self.auth)
        if not response.ok:
            self.__raise(response)

    def password(self, username, password):
        url = self.__get_user_url('%s/_password' % username)
        data = json.dumps({'password': password})
        response = requests.put(url, data=data, auth=self.auth)
        if response.status_code == 200:
            return True
        elif response.status_code == 401:
            return False
        else:
            self.__raise(response)


def main():
    module = AnsibleModule(
        argument_spec=dict(
            email=dict(type='str', required=False),
            enabled=dict(type='bool', required=False),
            full_name=dict(type='str', required=False),
            login_password=dict(type='str', required=False,
                                default='changeme', no_log=True),
            login_url=dict(type='str', required=False,
                           default='http://localhost:9200'),
            login_user=dict(type='str', required=False, default='elastic'),
            metadata=dict(type='dict', required=False),
            name=dict(type='str', required=True),
            password=dict(type='str', required=False, no_log=True),
            password_update=dict(
                default='always', choices=['always', 'on_create']),
            roles=dict(type='list', required=False),
            state=dict(default='present',
                       choices=['present', 'absent', 'password_update']),
        ),
        supports_check_mode=True
    )

    state = module.params['state']
    name = module.params['name']
    changed = False
    user = None

    try:
        users = ElasticsearchUserResource(
            module.params['login_url'], (module.params['login_user'], module.params['login_password']))

        if state == 'absent':
            user = users.get(name)

            if user is not None:
                if module.check_mode is not True:
                    users.delele(name)
                changed = True

        elif state == 'present':
            user = users.get(name) or {}

            if module.params['password_update'] == 'always' or not user:
                if module.params['password']:
                    if not users.check_authentication(name, module.params['password']):
                        changed = True
                    user['password'] = module.params['password']

            for index in ['email', 'enabled', 'full_name', 'metadata', 'roles']:
                if module.params[index]:
                    if index not in user or user[index] != module.params[index]:
                        changed = True
                    user[index] = module.params[index]

            if module.check_mode is False:
                users.save(name, user)

        elif state == 'password_update':
            if module.params['password']:
                changed = not users.check_authentication(
                    name, module.params['password'])
                if module.check_mode is not True:
                    users.password(name, module.params['password'])

    except Exception as error:
        module.fail_json(msg=str(error))

    module.exit_json(changed=changed, name=name, state=state, user=user)


if __name__ == '__main__':
    reload(sys)
    sys.setdefaultencoding('utf8')
    main()
