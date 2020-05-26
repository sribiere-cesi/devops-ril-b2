#!/usr/bin/python
# -*- coding: utf-8 -*-

from __future__ import absolute_import, division, print_function

__metaclass__ = type

ANSIBLE_METADATA = {
    'metadata_version': '1.1',
    'status': ['stableinterface'],
    'supported_by': 'community'
}

DOCUMENTATION = '''
---
module: postgresql_tablespace
short_description: Adds a tablespace from a PostgreSQL database.
description:
   - Add PostgreSQL tablespaces from a remote host and, optionally,
     update the owner to an existing one.
version_added: "0.1"
options:
  name:
    description:
      - Name of the tablespace to add.
    required: true
  db:
    description:
      - Name of database where tablespace will be created.
  port:
    description:
      - Database port to connect to.
    default: 5432
  login_user:
    description:
      - User (role) used to authenticate with PostgreSQL.
    default: postgres
  login_password:
    description:
      - Password used to authenticate with PostgreSQL.
  login_host:
    description:
      - Host running PostgreSQL.
    default: localhost
  login_unix_socket:
    description:
      - Path to a Unix domain socket for local connections.
  state:
    description:
      - The tablespace state.
    default: present
    choices: ["present", "absent"]
  ssl_mode:
    description:
      - Determines whether or with what priority a secure SSL TCP/IP connection
        will be negotiated with the server.
      - See U(https://www.postgresql.org/docs/current/static/libpq-ssl.html) for
        more information on the modes.
      - Default of C(prefer) matches libpq default.
    default: prefer
    choices: ["disable", "allow", "prefer", "require", "verify-ca", "verify-full"]
    version_added: '2.3'
  ssl_rootcert:
    description:
      - Specifies the name of a file containing SSL certificate authority (CA)
        certificate(s). If the file exists, the server's certificate will be
        verified to be signed by one of these authorities.
    version_added: '2.3'
notes:
   - The default authentication assumes that you are either logging in as or
     sudo'ing to the postgres account on the host.
   - This module uses psycopg2, a Python PostgreSQL database adapter. You must
     ensure that psycopg2 is installed on the host before using this module. If
     the remote host is the PostgreSQL server (which is the default case), then
     PostgreSQL must also be installed on the remote host. For Ubuntu-based
     systems, install the postgresql, libpq-dev, and python-psycopg2 packages
     on the remote host before using this module.
   - The ssl_rootcert parameter requires at least Postgres version 8.4 and
     I(psycopg2) version 2.4.3.
requirements: [ psycopg2 ]
author: "Flowbird"
'''

EXAMPLES = '''
# Create data tablespace with owner sam
- postgresql_tablespace:
    name: data
    owner: sam
    location: /srv/data

# Create data tablespace as default one
- postgresql_tablespace:
    name: data
    owner: sam
    location: /srv/data
    defaultTablespace: yes
'''

import traceback

try:
    import psycopg2
    import psycopg2.extras
except ImportError:
    postgresqldb_found = False
else:
    postgresqldb_found = True

from ansible.module_utils.basic import AnsibleModule
from ansible.module_utils.database import SQLParseError
from ansible.module_utils._text import to_native
from ansible.module_utils.six import iteritems


# ===========================================
# PostgreSQL module specific support methods.
#


def tablespace_exists(cursor, tablespace):
    query = "SELECT spcname FROM pg_tablespace WHERE spcname=%(tablespace)s"
    cursor.execute(query, {'tablespace': tablespace})
    return cursor.rowcount > 0


def tablespace_add(cursor, tablespace, owner, location):
    query = [
        'CREATE TABLESPACE %(tablespace)s OWNER %(owner)s' % {
            "tablespace": tablespace,
            "owner": owner
        }
    ]

    query.append("LOCATION %(location)s")
    query_args = dict(location=location)

    query = ' '.join(query)
    cursor.execute(query, query_args)

    return True


def change_owner(cursor, tablespace, owner):
    query = 'SELECT pg_tablespace.spcname FROM pg_tablespace ' \
            'inner join pg_user on pg_user.usesysid = pg_tablespace.spcowner ' \
            'where pg_tablespace.spcname = %(tablespace)s and pg_user.usename = %(username)s'
    cursor.execute(
        query, {
            'tablespace': tablespace,
            'username': owner
        }
    )
    if cursor.rowcount > 0:
        return False
    else:
        query = [
            'ALTER TABLESPACE %(tablespace)s OWNER TO %(owner)s' % {
                "tablespace": tablespace,
                "owner": owner
            }
        ]
        cursor.execute(query)
        return True


def set_default(cursor, tablespace):
    query = [
        'SET DEFAULT_TABLESPACE = %(tablespace)s' % {
            'tablespace': tablespace
        }
    ]
    cursor.execute(query)
    return True


# ===========================================
# Module execution.
#


def main():
    module = AnsibleModule(
        argument_spec=dict(
            login_user=dict(default="postgres"),
            login_password=dict(default="", no_log=True),
            login_host=dict(default=""),
            login_unix_socket=dict(default=""),
            ssl_mode=dict(default='prefer', choices=['disable', 'allow', 'prefer', 'require', 'verify-ca', 'verify-full']),
            ssl_rootcert=dict(default=None),
            db=dict(default=''),
            port=dict(default='5432'),

            tablespace=dict(required=True, aliases=['name']),
            state=dict(default="present", choices=["absent", "present"]),
            owner=dict(required=True),
            location=dict(required=True),
            defaultTablespace=dict(type='bool', default='no')
        ),
        supports_check_mode=True
    )

    tablespace = module.params["tablespace"]
    owner = module.params["owner"]
    location = module.params["location"]
    state = module.params["state"]
    defaultTablespace = module.params["defaultTablespace"]

    if not postgresqldb_found:
        module.fail_json(msg="the python psycopg2 module is required")

    # To use defaults values, keyword arguments must be absent, so
    # check which values are empty and don't include in the **kw
    # dictionary
    params_map = {
        "login_host": "host",
        "login_user": "user",
        "login_password": "password",
        "port": "port",
        "db": "database",
        "ssl_mode": "sslmode",
        "ssl_rootcert": "sslrootcert"
    }
    kw = dict((params_map[k], v) for (k, v) in iteritems(module.params)
              if k in params_map and v != "" and v is not None)

    # If a login_unix_socket is specified, incorporate it here.
    is_localhost = "host" not in kw or kw["host"] == "" or kw["host"] == "localhost"
    if is_localhost and module.params["login_unix_socket"] != "":
        kw["host"] = module.params["login_unix_socket"]

    sslrootcert = module.params["ssl_rootcert"]

    if psycopg2.__version__ < '2.4.3' and sslrootcert is not None:
        module.fail_json(
            msg='psycopg2 must be at least 2.4.3 in order to user the ssl_rootcert parameter')

    try:
        db_connection = psycopg2.connect(**kw)
        db_connection.set_session(autocommit=True)
        cursor = db_connection.cursor(cursor_factory=psycopg2.extras.DictCursor)
    except TypeError as e:
        if 'sslrootcert' in e.args[0]:
            module.fail_json(msg='Postgresql server must be at least version 8.4 to support sslrootcert')
        module.fail_json(msg="unable to connect to database: %s" % to_native(e), exception=traceback.format_exc())
    except Exception as e:
        module.fail_json(msg="unable to connect to database: %s" % to_native(e), exception=traceback.format_exc())

    kw = dict(tablespace=tablespace)
    changed = False

    if state == "present":
        if tablespace_exists(cursor, tablespace):
            changed = False
        else:
            try:
                changed = tablespace_add(cursor, tablespace, owner, location)
            except psycopg2.ProgrammingError as e:
                module.fail_json(msg="Unable to add tablespace with given requirement due to : %s" % to_native(e), exception=traceback.format_exc())
            except SQLParseError as e:
                module.fail_json(msg=to_native(e), exception=traceback.format_exc())
        try:
            changed = change_owner(cursor, tablespace, owner) or changed
        except SQLParseError as e:
            module.fail_json(msg=to_native(e), exception=traceback.format_exc())
        if defaultTablespace:
            try:
                changed = set_default(cursor, tablespace) or changed
            except SQLParseError as e:
                module.fail_json(msg=to_native(e), exception=traceback.format_exc())
    else:
        module.fail_json(msg="Unsupported tablespace deletion operation")

    if changed:
        if module.check_mode:
            db_connection.rollback()
        else:
            db_connection.commit()

    kw['changed'] = changed
    module.exit_json(**kw)


if __name__ == '__main__':
    main()
