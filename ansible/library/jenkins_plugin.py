#!/usr/bin/env python

from ansible.module_utils.basic import AnsibleModule, get_exception
import requests
import urlparse

class JenkinsPlugin(object):
    def __init__(self, url = 'http://localhost:8080', username = None, password = None):
        self._url = url
        self._username = username
        self._password = password

    def _get_url(self, path):
        return '%s%s' % (self._url, path)

    def _get_auth(self):
        if not self._username:
            return None
        return (self._username, self._password)

    def _check_response_status(self, response, message = 'Invalid response code'):
        if response.status_code == 403:
            raise Exception(
                'Authentication required, You are authenticated as: %s',
                response.headers['X-You-Are-Authenticated-As']
            )
        elif response.status_code != 200:
            raise Exception(message)

    def _get_config(self):
        url = self._get_url('/api/json')
        response = requests.get( url, auth = self._get_auth())
        self._check_response_status(response, 'Failed to get configuration')
        return response.json()

    def _use_crumbs(self):
        config = self._get_config()
        return 'useCrumbs' in config and config['useCrumbs']

    def _get_plugins(self):
        url = self._get_url('/pluginManager/api/json?depth=1')
        response = requests.get(url, auth = self._get_auth())
        self._check_response_status(response, 'Failed to get plugins list')
        data = response.json()
        if not 'plugins' in data:
            raise Exception('Response missing plugins list')
        return data['plugins']

    def _get_plugin(self, name, version = None):
        plugins = self._get_plugins()
        for plugin in plugins:
            if plugin['shortName'] == name:
                if version and plugin['version'] != version:
                    continue
                return plugin
        return None

    def _get_crumb(self):
        url = self._get_url('/crumbIssuer/api/json')
        response = requests.get(url, auth = self._get_auth())
        self._check_response_status(response, 'Failed to get crumb')
        return response.json()

    def _get_plugin_name(self, name, version = None):
        if not version:
            version = 'latest'
        return '%s@%s' % (name, version)

    def _install_plugin(self, name, version):
        url = self._get_url('/pluginManager/installNecessaryPlugins/json')
        plugin = self._get_plugin_name(name, version)
        payload = '<install plugin="%s"/>' % plugin
        headers = {'Content-Type': 'application/xml'}
        if self._use_crumbs():
            crumb = self._get_crumb()
            headers[crumb['crumbRequestField']] = crumb['crumb']
        auth = self._get_auth()
        response = requests.post(url, data = payload, headers = headers, auth = auth)
        self._check_response_status(response, 'Failed to install plugin %s' % plugin)

    def install(self, name, version = None):
        changed = False
        plugin = self._get_plugin(name, version)
        if plugin == None:
            self._install_plugin(name, version)
            changed = True
        return changed

    def uninstall(self, name):
        raise Exception('Not implemented')

def main():
    module = AnsibleModule(
        argument_spec = dict(
            state     = dict(default='present', choices=['present', 'absent']),
            name      = dict(required=True),
            version   = dict(default=None, required=False),
            jenkins   = dict(type='dict')
        )
    )

    state = module.params['state']
    name = module.params['name']
    version = module.params['version']

    jenkins = module.params['jenkins']
    url = jenkins['url'] or 'http://localhost:8080'
    username = jenkins['username'] or None
    if 'password' in jenkins:
        password = jenkins['password']
    elif 'password_file' in jenkins:
        password = str.strip(open(jenkins['password_file'], 'r').read().strip())
    else:
        password = None

    try:
        changed = False
        jenkins_plugin = JenkinsPlugin(url, username, password)
        if state == 'present':
            changed = jenkins_plugin.install(name, version)
        elif state == 'absent':
            changed = jenkins_plugin.uninstall(name)
    except Exception:
        e = get_exception()
        module.fail_json(msg=e.message)

    module.exit_json(changed=changed, name=name, state=state)

if __name__ == '__main__':
    main()
