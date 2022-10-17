#!/usr/bin/env python3
# -*- coding: utf-8 -*-

# (c) 2020-2022, Bodo Schulz <bodo@boone-schulz.de>

from __future__ import print_function

import os
import re

from ansible.module_utils.basic import AnsibleModule

__metaclass__ = type

ANSIBLE_METADATA = {
    'metadata_version': '0.1',
    'status': ['preview'],
    'supported_by': 'community'
}

DOCUMENTATION = """
---
module: java_version.py
author:
    - 'Bodo Schulz'
short_description: Detect installed java Version
description: Detect installed java Version
"""

EXAMPLES = """

"""

"""
usage: dsconf [-h] [-v] [-D BINDDN] [-w BINDPW] [-W] [-y PWDFILE] [-b BASEDN] [-Z] [-j]
              instance
              {backend,backup,chaining,config,directory_manager,monitor,plugin,pwpolicy,localpwp,replication,repl-agmt,repl-winsync-agmt,repl-tasks,sasl,security,schema,repl-conflict}
              ...

positional arguments:
  instance              The instance name OR the LDAP url to connect to, IE localhost, ldap://mai.example.com:389
  {backend,backup,chaining,config,directory_manager,monitor,plugin,pwpolicy,localpwp,replication,repl-agmt,repl-winsync-agmt,repl-tasks,sasl,security,schema,repl-conflict}
                        resources to act upon
    backend             Manage database suffixes and backends
    backup              Manage online backups
    chaining            Manage database chaining/database links
    config              Manage server configuration
    directory_manager   Manage the directory manager account
    monitor             Monitor the state of the instance
    plugin              Manage plugins available on the server
    pwpolicy            Get and set the global password policy settings
    localpwp            Manage local (user/subtree) password policies
    replication         Configure replication for a suffix
    repl-agmt           Manage replication agreements
    repl-winsync-agmt   Manage Winsync Agreements
    repl-tasks          Manage replication tasks
    sasl                Query and manipulate SASL mappings
    security            Query and manipulate security options
    schema              Query and manipulate schema
    repl-conflict       Manage replication conflicts

optional arguments:
  -h, --help            show this help message and exit
  -v, --verbose         Display verbose operation tracing during command execution
  -D BINDDN, --binddn BINDDN
                        The account to bind as for executing operations
  -w BINDPW, --bindpw BINDPW
                        Password for binddn
  -W, --prompt          Prompt for password for the bind DN
  -y PWDFILE, --pwdfile PWDFILE
                        Specifies a file containing the password for the binddn
  -b BASEDN, --basedn BASEDN
                        Basedn (root naming context) of the instance to manage
  -Z, --starttls        Connect with StartTLS
  -j, --json            Return result in JSON object
"""


class DSConf(object):
    """
        Main Class
    """
    module = None

    def __init__(self, module):
        """
        """
        self.module = module
        # self.state = self.module.params.get("state")
        self.instance = self.module.params.get("instance")
        self.resources = self.module.params.get("resources")
        self.verbose = self.module.params.get("verbose")
        self.binddn = self.module.params.get("binddn")
        self.bindpw = self.module.params.get("bindpw")
        self.pwdfile = self.module.params.get("pwdfile")
        self.basedn = self.module.params.get("basedn")
        self.starttls = self.module.params.get("starttls")

        self.dsconf = self.module.get_bin_path('dsconf', False)


    def run(self):
        """
        """
        result = dict(
            failed=False,
            msg="initial error",
        )

        if(not self.dsconf):
            return dict(
                failed = True,
                msg = "no valid dsconf found"
            )

        if self.from_file is not None and os.path.isfile(self.from_file):

            args = []
            args.append(self.dsconf)
            args.append(self.instance)

            for arg in self.resources:
                args.append(arg)

            self.module.log(msg=f" - args {args}")

            rc, out, err = self._exec(args)

            if rc == 0:
                _changed = True



                return dict(
                    rc=rc,
                    cmd=" ".join(args),
                    failed=True,
                    changed=False,
                    msg=err
                )

            else:
                return dict(
                    failed=False,
                    changed=False
                )


        else:
            return dict(
                failed=True,
                changed=False,
                msg=f"missing configuration file {self.from_file}"
            )


    def _exec(self, args):
        '''   '''
        # self.module.log(msg="cmd: {}".format(args))
        rc, out, err = self.module.run_command(args, check_rc=True)
        self.module.log(msg=f"  rc : '{rc}'")
        self.module.log(msg=f"  out: '{out}'")
        self.module.log(msg=f"  err: '{err}'")
        return rc, out, err

# ===========================================
# Module execution.
#


def main():
    """

    """
    module = AnsibleModule(
        argument_spec=dict(
            # state=dict(
            #     required=True,
            #     default = "instance",
            #     choose = [
            #         'backend',
            #         'backup',
            #         'chaining',
            #         'config',
            #         'directory_manager',
            #         'monitor',
            #         'plugin',
            #         'pwpolicy',
            #         'localpwp',
            #         'replication',
            #         'repl-agmt',
            #         'repl-winsync-agmt',
            #         'repl-tasks',
            #         'sasl',
            #         'security',
            #         'schema',
            #         'repl-conflict'
            #     ]
            # ),
            # The instance name OR the LDAP url to connect to, IE localhost, ldap://mai.example.com:389
            instance = dict(
                required = True,
                type = str
            ),
            resources = dict(
                required = True,
                type = list
            ),
            verbose = dict(
                required = False,
                type = bool,
                default = False
            ),
            # The account to bind as for executing operations
            binddn = dict(
                required = False,
                type = str
            ),
            # Password for binddn
            bindpw = dict(
                required = False,
                type = str
            ),
            # Specifies a file containing the password for the binddn
            pwdfile = dict(
                required = False,
                type = str
            ),
            # Basedn (root naming context) of the instance to manage
            basedn = dict(
                required = False,
                type = str
            ),
            # Connect with StartTLS
            starttls = dict(
                required = False,
                type = bool,
                default = False
            )
        ),
        supports_check_mode=True
    )

    client = DSConf(module)
    result = client.run()

    module.exit_json(**result)


if __name__ == '__main__':
    main()
