import pytest

import os

import testinfra.utils.ansible_runner

testinfra_hosts = testinfra.utils.ansible_runner.AnsibleRunner(
    os.environ['MOLECULE_INVENTORY_FILE']).get_hosts('all')


@pytest.mark.parametrize('group', [
  ('backupd')
])
def test_backup_group_exists(host, group):
    backup_group = host.group(group)
    assert backup_group.exists


@pytest.mark.parametrize('user,group,home', [
  ('backupd', 'backupd', '/home/backupd')
])
def test_backup_user_exists(host, user, group, home):
    backup_user = host.user(user)
    assert backup_user.name == user
    assert backup_user.group == group
    assert backup_user.home == home


@pytest.mark.parametrize('name', [
  ('cron'),
  ('gzip'),
  ('tar'),
  ('util-linux')
])
def test_packages_are_installed(host, name):
    package = host.package(name)
    assert package.is_installed


@pytest.mark.parametrize('path,user,group,mode', [
  ('/home/backupd/scripts', 'backupd', 'backupd', 0o750),
  ('/home/backupd/temp', 'backupd', 'backupd', 0o750),
  ('/home/backupd/storage', 'backupd', 'backupd', 0o750)
])
def test_directories_exist(host, path, user, group, mode):
    directory = host.file(path)
    assert directory.exists
    assert directory.is_directory
    assert directory.user == user
    assert directory.group == group
    assert directory.mode == mode


@pytest.mark.parametrize('path,user,group,mode', [
  ('/home/backupd/scripts/files.sh', 'backupd', 'backupd', 0o750),
  ('/home/backupd/scripts/mysql.sh', 'backupd', 'backupd', 0o750),
  ('/home/backupd/scripts/s3_bucket.sh', 'backupd', 'backupd', 0o750),
  ('/home/backupd/scripts/mongodb.sh', 'backupd', 'backupd', 0o750),
  ('/home/backupd/scripts/xtrabackup.sh', 'backupd', 'backupd', 0o750)
])
def test_scripts_exist(host, path, user, group, mode):
    directory = host.file(path)
    assert directory.exists
    assert directory.is_file
    assert directory.user == user
    assert directory.group == group
    assert directory.mode == mode


@pytest.mark.parametrize('job,user', [
  ('0 6 1 * * /home/backupd/scripts/files.sh 2>&1 | \
/usr/bin/logger -t cron_backup_files', 'backupd'),
  ('30 */6 * * * /home/backupd/scripts/mysql.sh 2>&1 | \
/usr/bin/logger -t cron_backup_mysql', 'backupd'),
  ('20 5 * * 0 /home/backupd/scripts/s3_bucket.sh 2>&1 | \
/usr/bin/logger -t cron_backup_s3_bucket', 'backupd'),
  ('45 7 * * * /home/backupd/scripts/mongodb.sh 2>&1 | \
/usr/bin/logger -t cron_backup_mongodb', 'backupd')
])
def test_cron_jobs_exist(host, job, user):
    jobs = host.check_output('crontab -u ' + user + ' -l')
    assert job in jobs
