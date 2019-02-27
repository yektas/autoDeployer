import configparser
import paramiko

config = configparser.ConfigParser()
config.read("config.properties")

hostIp = config["SETTINGS"]["hostIp"]
username = config["SETTINGS"]["username"]
password = config["SETTINGS"]["password"]

def scp(local_path, remote_path):

    client = paramiko.SSHClient()
    client.set_missing_host_key_policy(paramiko.AutoAddPolicy())

    client.connect(hostname=hostIp,
                   port=22,
                   username=username,
                   password=password)
    sftp = client.open_sftp()
    sftp.put(local_path, remote_path)
    print("File is deployed.")
    sftp.close()