import paramiko
def sftp_put(host, port, user, password, local_bytes: bytes, remote_path: str):
    t=paramiko.Transport((host,port)); t.connect(username=user, password=password)
    s=paramiko.SFTPClient.from_transport(t)
    with s.file(remote_path,'wb') as f: f.write(local_bytes)
    s.close(); t.close()
