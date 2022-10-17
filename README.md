
# Ansible Role:  `389ds`

This role will fully configure and install [389ds](https://icinga.com/docs/icinga-db).

[![GitHub Workflow Status](https://img.shields.io/github/workflow/status/bodsch/ansible-389ds/CI)][ci]
[![GitHub issues](https://img.shields.io/github/issues/bodsch/ansible-389ds)][issues]
[![GitHub release (latest by date)](https://img.shields.io/github/v/release/bodsch/ansible-389ds)][releases]

[ci]: https://github.com/bodsch/ansible-389ds/actions
[issues]: https://github.com/bodsch/ansible-389ds/issues?q=is%3Aopen+is%3Aissue
[releases]: https://github.com/bodsch/ansible-389ds/releases


## Requirements & Dependencies

### supported operating systems

* ArchLinux
* Debian based
    - Debian 10 / 11
    - Ubuntu 20.04

## usage

```yaml
ds389_server_uri: "ldap://localhost:{{ ds389_init_slapd.port }}"

ds389_init_general: {}

ds389_init_slapd: {}

ds389_init_backend: {}

ds389_tls: {}

ds389_sasl_plain_enabled: true

ds389_allow_anonymous_binds: 'rootdse'
ds389_simple_auth_enabled: true

ds389_password_storage_scheme: "PBKDF2_SHA256"
ds389_install_examples: false
ds389_ldapi_enabled: true

ds386_plugins_dynamic_load: true

# https://access.redhat.com/documentation/en-us/red_hat_directory_server/11/html-single/administration_guide/index#listing_the_available_plug-ins
# https://possiblelossofprecision.net/?p=2534
ds389_plugins_enabled: {}

ds389_custom_schema: []

ds389_install_additional_ldif: []

# Cannot use /tmp, see https://github.com/lvps/389ds-server/issues/18
ds389_install_additional_ldif_dir: "/var/lib/dirsrv/slapd-{{ ds389_init_slapd.instance_name }}/ldif"

ds389_logging:
  audit:
    enabled: false
    logrotationtimeunit: day
    logmaxdiskspace: 400
    maxlogsize: 200
    maxlogsperdir: 7
    mode: 600
  access:
    enabled: true
    logrotationtimeunit: day
    logmaxdiskspace: 400
    maxlogsize: 200
    maxlogsperdir: 7
    mode: 600
  error:
    enabled: true
    logrotationtimeunit: day
    logmaxdiskspace: 400
    maxlogsize: 200
    maxlogsperdir: 7
    mode: 600

ds389_dna_plugin:
  gid_min: 2000
  gid_max: 2999
  uid_min: 2000
  uid_max: 2999
```

### `ds389_init_general`

```yaml
ds389_init_general:
  machine_name: "{{ ansible_nodename }}"
```

### `ds389_init_slapd`

```yaml
ds389_init_slapd:
  instance_name: default
  listen: 127.0.0.1
  secure_listen: 127.0.0.1
  port: 389
  root_dn: cn=Directory Manager
  root_password: "Bwmo5xqKeXDg2xkhFwhNLG1k8G9fUfS9q5FQ70I8uD"
  self_sign_cert: true
  self_sign_cert_valid_months: 4
  db_home_dir: ""
  run_dir: "/run"
```

### `ds389_init_backend`

```yaml
ds389_init_backend:
  example.com:
    name: exampleRoot
    sample_entries: true
    suffix: dc=example,dc=com
    create_suffix_entry: true
```

### `ds389_tls`

```yaml
ds389_tls:
ds389_tls:
  enabled: true
  enforced: true
  key_file: "{{ snakeoil_local_tmp_directory }}/{{ snakeoil_domain }}/{{ snakeoil_domain }}.key"
  cert_file: "{{ snakeoil_local_tmp_directory }}/{{ snakeoil_domain }}/{{ snakeoil_domain }}.pem"
```

### `ds389_plugins_enabled`

```yaml
ds389_plugins_enabled:
  MemberOf Plugin: true
```

### `ds389_custom_schema`

```yaml
ds389_custom_schema:
  - "98-ssh.ldif"
  - "98-telegram.ldif"
```

### defaults

[see](vars/main.yml)

```yaml
ds389_defaults_init_general:
  version: ""
  machine_name: "{{ ansible_nodename }}"

ds389_defaults_init_slapd:
  instance_name: default
  listen: 0.0.0.0
  secure_listen: 0.0.0.0
  port: 389
  root_dn: cn=Directory Manager
  root_password: "Bwmo5xqKeXDg2xkhFwhNLG1k8G9fUfS9q5FQ70I8uD"
  self_sign_cert: true
  self_sign_cert_valid_months: 4
  db_home_dir: ""
  run_dir: "/run"

ds389_defaults_init_backend:
  example.com:
    name: exampleRoot
    sample_entries: true
    suffix: dc=example,dc=com
    create_suffix_entry: true

#  - name: userRoot
#    sample_entries: true
#    suffix: dc=example,dc=com
#    create_suffix_entry: true
#    # - name: next
#    #   sample_entries: true
#    #   suffix: dc=next,dc=lan
#    #   create_suffix_entry: true

ds389_defaults_tls:
  enabled: false
  enforced: false
  #key: ""
  #cert: ""
  key_file: tls_test_local.key
  cert_file: tls_test_local_cert.pem
  files_remote: false
  # As in, "publicly trusted because it's signed by a public and recognized CA"
  validate_certs: false
  enforced_initially_binds:
  min_version: "1.2"
  # Ansible is not secure enough for a SSF of 256 for 389DS 1.4.X
  # Unfortunately we don't yet have access to dirsrv_legacy or the
  # installed version so we need to base the condition on the CentOS version
  min_ssf: 256


```


## Contribution

Please read [Contribution](CONTRIBUTING.md)

## Development,  Branches (Git Tags)

The `master` Branch is my *Working Horse* includes the "latest, hot shit" and can be complete broken!

If you want to use something stable, please use a [Tagged Version](https://github.com/bodsch/ansible-389ds/tags)!

---

## Author

- Bodo Schulz

## License

[Apache](LICENSE)

`FREE SOFTWARE, HELL YEAH!`
