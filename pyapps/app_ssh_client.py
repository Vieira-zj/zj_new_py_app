# coding=utf-8

import paramiko


class SSHClient(object):

    def __init__(self, host, port, user, pkey_file_path):
        private_key = paramiko.RSAKey.from_private_key_file(pkey_file_path)
        self.ssh = paramiko.SSHClient()
        self.ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy)
        self.ssh.connect(hostname=host, port=port,
                         username=user, pkey=private_key, timeout=10)

    def execute_command(self, command):
        _, stdout, stderr = self.ssh.exec_command(command)
        out = stdout.read
        err = stderr.read
        return out, err

    def close(self):
        self.ssh.close()
