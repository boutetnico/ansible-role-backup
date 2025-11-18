[![tests](https://github.com/boutetnico/ansible-role-backup/workflows/Test%20ansible%20role/badge.svg)](https://github.com/boutetnico/ansible-role-backup/actions?query=workflow%3A%22Test+ansible+role%22)
[![Ansible Galaxy](https://img.shields.io/badge/galaxy-boutetnico.backup-blue.svg)](https://galaxy.ansible.com/boutetnico/backup)

ansible-role-backup
===================

This role configures backups.

Requirements
------------

Ansible 2.10 or newer.

Supported Platforms
-------------------

- [Debian - 11 (Bullseye)](https://wiki.debian.org/DebianBullseye)
- [Debian - 12 (Bookworm)](https://wiki.debian.org/DebianBookworm)
- [Ubuntu - 22.04 (Jammy Jellyfish)](http://releases.ubuntu.com/22.04/)
- [Ubuntu - 24.04 (Noble Numbat)](http://releases.ubuntu.com/24.04/)

Role Variables
--------------

| Variable                     | Required | Default                         | Choices | Comments                                     |
|------------------------------|----------|---------------------------------|---------|----------------------------------------------|
| backup_user                  | yes      | `backupd`                       | string  | User who runs backup scripts.                |
| backup_group                 | yes      | `backupd`                       | string  |                                              |
| backup_extra_groups          | yes      | `[]`                            | list    | Add `backup_user` to additional groups.      |
| backup_home_dir              | yes      | `/home/{{ backup_user }}`       | string  |                                              |
| backup_scripts_dir           | yes      | `{{ backup_home_dir }}/scripts` | string  |                                              |
| backup_temp_dir              | yes      | `{{ backup_home_dir }}/temp`    | string  |                                              |
| backup_extra_dir             | yes      | `[]`                            | list    | Create additional directories if needed.     |
| backup_dependencies          | yes      |                                 | list    | See `defaults/main.yml`.                     |
| backup_env                   | yes      | `{}`                            | dict    |                                              |
| backup_archive_enabled       | yes      | `true`                          | bool    | Wether or not to pack files into an archive. |
| backup_compression_enabled   | yes      | `true`                          | bool    | Wether or not to compress the archive file.  |
| backup_compressor            | yes      | `gzip`                          | string  |                                              |
| backup_compression_level     | yes      | `1`                             | int     |                                              |
| backup_encryption_enabled    | yes      | `false`                         | bool    | Wether or not to encrypt the archive file.   |
| backup_encryption_key        | yes      | `my_secure_key`                 | string  | Encryption key.                              |
| backup_encryption_algo       | yes      | `aes-256-cbc`                   | string  | Encryption algorithm.                        |
| backup_aws_command           | yes      | `aws`                           | string  |                                              |
| backup_aws_upload_enabled    | yes      | `false`                         | bool    |                                              |
| backup_aws_bucket_name       | yes      | `mybucket`                      | string  |                                              |
| backup_aws_region            | yes      | `us-east-1`                     | string  |                                              |
| backup_gcloud_command        | yes      | `gsutil`                        | string  |                                              |
| backup_gcloud_upload_enabled | yes      | `false`                         | bool    |                                              |
| backup_gcloud_bucket_name    | yes      | `mybucket`                      | string  |                                              |
| backup_b2_command            | yes      | `b2`                            | string  |                                              |
| backup_b2_upload_enabled     | yes      | `false`                         | bool    | Enable Backblaze B2 upload.                  |
| backup_b2_bucket_name        | yes      | `mybucket`                      | string  | Backblaze B2 bucket name.                    |
| backup_restic_command        | yes      | `restic`                        | string  |                                              |
| backup_restic_enabled        | yes      | `false`                         | bool    |                                              |
| backup_restic_forget_options | yes      | `--keep-daily 90 --prune`       | string  | See (all options)[https://restic.readthedocs.io/en/latest/060_forget.html#removing-snapshots-according-to-a-policy]. |
| backup_restic_check_enabled  | yes      | `false`                         | bool    |                                              |
| backup_cron_syslog_enabled   | yes      | `true`                          | bool    | Log script output to syslog.                 |
| backup_cron_syslog_tag       | yes      | `cron_backup_`                  | string  |                                              |
| backup_services              | yes      | `[]`                            | list    | Scripts to install. See `defaults/main.yml`. |

Dependencies
------------

- `backup_aws_*` options require [`awscli` package](https://github.com/boutetnico/ansible-role-awscli).
- `backup_gcloud_*` options require `gcloud` package.
- `backup_restic_*` options require [`restic` package](https://github.com/boutetnico/ansible-role-restic).
- `backup_b2_*` options require [`b2` package](https://github.com/boutetnico/ansible-role-b2).

Example Playbook
----------------

    - hosts: all
      roles:
        - ansible-role-backup
          backup_aws_upload_enabled: true
          backup_aws_bucket_name: backup
          backup_aws_region: us-east-1
          backup_services:
            - name: site-files
              script: files.sh
              vars:
                files_path: /var/www/site/data
              cron:
                day: 1
                hour: 6
                minute: 0
            - name: site-mysql
              script: mysqldump.sh
              vars:
                mysql_user: backup
                mysql_password: backup
                mysql_endpoint: localhost
                mysql_databases:
                  - site
                mysqldump_options: "--get-server-public-key"
              cron:
                hour: "*/6"
                minute: 30
            - name: photos-bucket
              script: s3_bucket.sh
              vars:
                bucket_name: photos
                s3_sync_path: "/mnt/photos-s3-mirror"
                s3_sync_options: "--follow-symlinks"
              cron:
                hour: 5
                minute: 20
                weekday: 0
            - name: site-mongodb
              script: mongodump.sh
              vars:
                mongodb_user: backup
                mongodb_password: backup
                mongodb_endpoint: localhost
              cron:
                hour: 7
                minute: 45
            - name: site-mysql-xtrabackup
              script: xtrabackup.sh
              vars:
                mysql_user: backup
                mysql_password: backup
                xtrabackup_backup_options: --slave-info
                xtrabackup_prepare_options: --use-memory=1G
            - name: logs-bucket
              script: s3_bucket.sh
              vars:
                bucket_name: logs
                s3_sync_path: "/mnt/logs-s3-mirror"
                restic_enabled: true
                restic_check_enabled: true
                archive_enabled: false
                compression_enabled: false
              cron:
                hour: 14
                minute: 30
            - name: docker_mariabackup
              script: docker_mariabackup.sh
              vars:
                mysql_container_name: project_mysql_1
                mysql_network_name: project_backend
                mysql_host: mysql
                mysql_user: backup
                mysql_password: backup
                mariabackup_docker_image: mariadb:latest
                mariabackup_options: --no-lock
              cron:
                hour: "*/1"
                minute: 27
            - name: influxdb
              script: influxdb.sh
              vars:
                influxdb_host: localhost:8086
                influxdb_token: influxdb-root-token-created-at-setup
              cron:
                hour: 21
                minute: 06

Testing
-------

    molecule test

License
-------

MIT

Author Information
------------------

[@boutetnico](https://github.com/boutetnico)
