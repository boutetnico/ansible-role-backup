ansible-role-backup
===================

This role configures backups.

[![Build Status](https://travis-ci.org/boutetnico/ansible-role-backup.svg?branch=master)](https://travis-ci.org/boutetnico/ansible-role-backup)

Requirements
------------

Ansible 2.6 or newer.

Supported Platforms
-------------------
- [Debian - 9 (Stretch)](https://wiki.debian.org/DebianStretch)
- [Debian - 10 (Buster)](https://wiki.debian.org/DebianBuster)
- [Ubuntu - 16.04 (Xenial Xerus)](http://releases.ubuntu.com/16.04/)
- [Ubuntu - 18.04 (Bionic Beaver)](http://releases.ubuntu.com/18.04/)


Role Variables
--------------

| Variable                     | Required | Default                         | Choices   | Comments                                    |
|------------------------------|----------|---------------------------------|-----------|---------------------------------------------|
| backup_user                  | yes      | `backupd`                       | string    | User who runs backup scripts                |
| backup_group                 | yes      | `backupd`                       | string    |                                             |
| backup_extra_groups          | yes      | `[]`                            | list      | Add `backup_user` to additional groups      |
| backup_home_dir              | yes      | `/home/{{ backup_user }}`       | string    |                                             |
| backup_scripts_dir           | yes      | `{{ backup_home_dir }}/scripts` | string    |                                             |
| backup_temp_dir              | yes      | `{{ backup_home_dir }}/temp`    | string    |                                             |
| backup_extra_dir             | yes      | `[]`                            | list      | Create additional directories if needed     |
| backup_dependencies          | yes      | `[cron, gzip, tar, util-linux]` | list      |                                             |
| backup_compression_enabled   | yes      | `true`                          | bool      |                                             |
| backup_compressor            | yes      | `gzip`                          | string    |                                             |
| backup_compression_level     | yes      | `1`                             | int       |                                             |
| backup_aws_upload_enabled    | yes      | `false`                         | bool      |                                             |
| backup_aws_bucket_name       | yes      | `mybucket`                      | string    |                                             |
| backup_aws_region            | yes      | `us-east-1`                     | string    |                                             |
| backup_gcloud_upload_enabled | yes      | `false`                         | bool      |                                             |
| backup_gcloud_bucket_name    | yes      | `mybucket`                      | string    |                                             |
| backup_cron_syslog_enabled   | yes      | `true`                          | bool      | Log script output to syslog                 |
| backup_cron_syslog_tag       | yes      | `cron_backup_`                  | string    |                                             |
| backup_services              | yes      | `[]`                            | list      | Scripts to install. See `defaults/main.yml` |

Dependencies
------------

`backup_aws_*` options require `awscli` package.
`backup_gcloud_*` options require `gcloud` package.

Example Playbook
----------------

    - hosts: all
      roles:
         - ansible-role-backup

Testing
-------

## Debian

`molecule --base-config molecule/shared/base.yml test --scenario-name debian`

## Ubuntu

`molecule --base-config molecule/shared/base.yml test --scenario-name ubuntu`

License
-------

MIT

Author Information
------------------

[@boutetnico](https://github.com/boutetnico)
