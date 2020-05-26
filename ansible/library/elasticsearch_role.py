#!/usr/bin/env python

from ansible.module_utils.basic import AnsibleModule
import requests
import json
import sys


class ElasticsearchRolesRepository(object):
    def __init__(self, url, auth=()):
        self.url = url.strip('/')
        self.auth = auth

        self.__check_xpack()

    def __check_xpack(self):
        response = requests.get('{}/_xpack'.format(self.url), auth=self.auth)
        if response.status_code not in [200, 401]:
            raise Exception('No x-pack plugin')

    def __url(self, name=None):
        return '{}/_xpack/security/role/{}'.format(self.url, name)

    def __raise(self, response):
        try:
            output = json.loads(response.text)
            if 'error' in output:
                raise Exception(output['error']['reason'])
            else:
                response.raise_for_status()
        except ValueError as error:
            response.raise_for_status()

    def get(self, name):
        response = requests.get(self.__url(name), auth=self.auth)
        if response.ok:
            return json.loads(response.text)[name]
        elif response.status_code == 404:
            return None
        else:
            self.__raise(response)

    def save(self, name, role):
        data = json.dumps(role)
        response = requests.put(self.__url(name), data=data, auth=self.auth)
        if not response.ok:
            self.__raise(response)

    def delete(self, name):
        response = requests.delete(self.__url(name), auth=self.auth)
        if not response.ok:
            self.__raise(response)


def main():
    module = AnsibleModule(
        argument_spec=dict(
            cluster=dict(type='list', default=None, required=False),
            indices=dict(type='list', default=None, required=False),
            login_password=dict(type='str', required=False,
                                default='changeme', no_log=True),
            login_url=dict(type='str', required=False,
                           default='http://localhost:9200'),
            login_user=dict(type='str', required=False, default='elastic'),
            name=dict(type='str', required=True),
            run_as=dict(type='list', default=None, required=False),
            state=dict(default='present', choices=['present', 'absent']),

        ),
        supports_check_mode=True
    )

    name = module.params['name']
    state = module.params['state']
    changed = False

    try:
        roles = ElasticsearchRolesRepository(
            module.params['login_url'],
            auth=(module.params['login_user'], module.params['login_password'])
        )

        role = roles.get(name)

        if state == 'absent':
            if role is not None:
                changed = True
                if not module.check_mode:
                    roles.delete(name)

        elif state == 'present':
            if role is None:
                role = {'cluster': [], 'indices': [], 'run_as': []}
                changed = True
            for i in ['cluster', 'indices', 'run_as']:
                if module.params[i] is not None:
                    if not role[i] == module.params[i]:
                        changed = True
                    role[i] = module.params[i]
            if not module.check_mode:
                roles.save(name, role)
    except Exception as error:
        module.fail_json(msg=str(error))

    module.exit_json(changed=changed, name=name, state=state)


if __name__ == '__main__':
    reload(sys)
    sys.setdefaultencoding('utf8')
    main()
