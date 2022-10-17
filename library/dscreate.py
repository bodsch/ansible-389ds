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
usage: dscreate [-h] [-v] [-j] {from-file,interactive,create-template} ...

positional arguments:
  {from-file,interactive,create-template}
                        action
    from-file           Create an instance of Directory Server from an inf answer file
    interactive         Start interactive installer for Directory Server installation
    create-template     Display an example inf answer file, or provide a file name to write it to disk.

optional arguments:
  -h, --help            show this help message and exit
  -v, --verbose         Display verbose operation tracing during command execution
  -j, --json            Return the result as a json message
"""

class DSCreate(object):
    """
        Main Class
    """
    module = None

    def __init__(self, module):
        """
        """
        self.module = module
        self.from_file = self.module.params.get("from_file")
        self.verbose = self.module.params.get('verbose')

        self.dscreate = self.module.get_bin_path('dscreate', False)



    def run(self):
        """
        """
        result = dict(
            failed=False,
            msg="initial error",
        )

        if(not self.dscreate):
            return dict(
                failed = True,
                msg = "no valid dscreate found"
            )

        if self.from_file is not None and os.path.isfile(self.from_file):

            args = []
            args.append(self.dscreate)

            if self.verbose:
                args.append("--verbose")

            args.append("--json")

            if self.from_file:
                args.append("from-file")
                args.append(self.from_file)

            self.module.log(msg=f" - args {args}")

            rc, out, err = self._exec(args)

            if rc == 0:
                _changed = True

                msg = "The 389 Directory Server are successfully created."

                return dict(
                    rc=rc,
                    cmd=" ".join(args),
                    failed=False,
                    changed=True,
                    msg=msg
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
        """
        """
        rc, out, err = self.module.run_command(args, check_rc=True)
        # self.module.log(msg=f"  rc : '{rc}'")
        # self.module.log(msg=f"  out: '{out}'")
        # self.module.log(msg=f"  err: '{err}'")
        return rc, out, err

# ===========================================
# Module execution.
#


def main():
    """

    """
    module = AnsibleModule(
        argument_spec=dict(
            from_file=dict(
                required=True,
                type=str
            ),
            verbose = dict(
                required = False,
                type = bool,
                default = False
            )
        ),
        supports_check_mode=True
    )

    client = DSCreate(module)
    result = client.run()

    module.exit_json(**result)


if __name__ == '__main__':
    main()
