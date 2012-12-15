import paramiko

def add(host, user, key_file, instance_name, port):
	ssh_client = None
	sftp_client = None
	nginx_config = None
	try:
		ssh_client = paramiko.SSHClient()
		ssh_client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
		ssh_client.connect(hostname=host, username=user, key_filename=key_file)

		sftp_client = ssh_client.open_sftp()
		nginx_config = sftp_client.open('/etc/nginx/conf.d/default.conf', 'a')
		nginx_config.write('''server {
  listen 176.9.66.108:80;
  server_name ''' + instance_name + '''.jtalks.org;

  location / {
    proxy_pass http://5.9.40.180:''' + port + ''';

    proxy_set_header Host $host;
    proxy_set_header X-Forwarded-For $remote_addr;
    proxy_set_header X-Real-IP $remote_addr;
    proxy_redirect off;
  }
}

''')

	finally:
		if ssh_client is not None:
			ssh_client.close()
		if sftp_client is not None:
			sftp_client.close()
		if nginx_config is not None:
			nginx_config.close()

def restart(host, user, key_file):
	ssh_client = None
	try:
		ssh_client = paramiko.SSHClient()
		ssh_client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
		ssh_client.connect(hostname=host, username=user, key_filename=key_file)

		stdin, stdout, stderr = ssh_client.exec_command('sudo /etc/init.d/nginx restart')
		data = stdout.read() + stderr.read()
		print data

	finally:
		if ssh_client is not None:
			ssh_client.close()

