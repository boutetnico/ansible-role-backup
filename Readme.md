ansible-role-backup
===================

This role configures backups.

Requirements
------------

Ansible 2.6 or newer.

Supported Platforms
-------------------

- [Debian - 9 (Stretch)](https://wiki.debian.org/DebianStretch)
- [Debian - 10 (Buster)](https://wiki.debian.org/DebianBuster)
- [Ubuntu - 18.04 (Bionic Beaver)](http://releases.ubuntu.com/18.04/)
- [Ubuntu - 20.04 (Focal Fossa)](http://releases.ubuntu.com/20.04/)

Role Variables
--------------

| Variable                     | Required | Default                         | Choices | Comments                                    |
|------------------------------|----------|---------------------------------|---------|---------------------------------------------|
| backup_user                  | yes      | `backupd`                       | string  | User who runs backup scripts                |
| backup_group                 | yes      | `backupd`                       | string  |                                             |
| backup_extra_groups          | yes      | `[]`                            | list    | Add `backup_user` to additional groups      |
| backup_home_dir              | yes      | `/home/{{ backup_user }}`       | string  |                                             |
| backup_scripts_dir           | yes      | `{{ backup_home_dir }}/scripts` | string  |                                             |
| backup_temp_dir              | yes      | `{{ backup_home_dir }}/temp`    | string  |                                             |
| backup_extra_dir             | yes      | `[]`                            | list    | Create additional directories if needed     |
| backup_dependencies          | yes      | `[cron, gzip, tar, util-linux]` | list    |                                             |
| backup_env                   | yes      | `[]`                            | list    |                                             |
| backup_archive_enabled       | yes      | `true`                          | bool    | Wether or not to pack files into an archive |
| backup_compression_enabled   | yes      | `true`                          | bool    | Wether or not to compress the archive file  |
| backup_compressor            | yes      | `gzip`                          | string  |                                             |
| backup_compression_level     | yes      | `1`                             | int     |                                             |
| backup_aws_upload_enabled    | yes      | `false`                         | bool    |                                             |
| backup_aws_bucket_name       | yes      | `mybucket`                      | string  |                                             |
| backup_aws_region            | yes      | `us-east-1`                     | string  |                                             |
| backup_gcloud_upload_enabled | yes      | `false`                         | bool    |                                             |
| backup_gcloud_bucket_name    | yes      | `mybucket`                      | string  |                                             |
| backup_restic_enabled        | yes      | `false`                         | bool    |                                             |
| backup_restic_forget_options | yes      | `--keep-daily 90 --prune`       | string  | See (all options)[https://restic.readthedocs.io/en/latest/060_forget.html#removing-snapshots-according-to-a-policy]. |
| backup_restic_check_enabled  | yes      | `false`                         | bool    |                                             |
| backup_cron_syslog_enabled   | yes      | `true`                          | bool    | Log script output to syslog                 |
| backup_cron_syslog_tag       | yes      | `cron_backup_`                  | string  |                                             |
| backup_services              | yes      | `[]`                            | list    | Scripts to install. See `defaults/main.yml` |

Dependencies
------------

- `backup_aws_*` options require `awscli` package.
- `backup_gcloud_*` options require `gcloud` package.
- `backup_restic_*` options require [`restic` package](https://github.com/boutetnico/ansible-role-restic).

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
              cron:
                hour: "*/6"
                minute: 30
            - name: photos-bucket
              script: s3_bucket.sh
              vars:
                bucket_name: photos
                s3_sync_path: "/mnt/photos-s3-mirror"
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

Testing
-------

    molecule test

License
-------

MIT

Author Information
------------------

[@boutetnico](https://github.com/boutetnico)
