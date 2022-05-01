from operator import sub
import paramiko
from scp import SCPClient
import os

class Main:
    
    def scp_teransfer_file(sef,remote_addr:str,user:str,password:str,fileaddres:str,remoteaddres:str) -> None:
        with paramiko.SSHClient() as ssh:
            ssh = paramiko.SSHClient()
            ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
            ssh.connect(hostname=remote_addr, username=user, password=password, look_for_keys=False, allow_agent=False)

            with SCPClient(ssh.get_transport()) as scp:
                scp.put(fileaddres, remoteaddres)
                
               
    
    def scp_transfer_directory(self,remote_addr:str,user:str,password:str,fileaddres:str,remoteaddres:str) -> None:
        file_list = os.listdir(fileaddres)
        for i in file_list:
            self.scp_teransfer_file(remote_addr,user,password,f"{fileaddres}/{i}",remoteaddres)

      
        


