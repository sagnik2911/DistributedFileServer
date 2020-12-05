# DistributedFileServer : EEL5737 - Fall 2020
Unix FS distributed across multiple server, mocking RAID5 approach. Redundancy and Fault Tolerance.
##How to Run the Program?
1. Download the files. 
2. Open terminals separately and start server like below commands: 

  python3 memoryfs_server.py 8000
  
  python3 memoryfs_server.py 8001
  
  python3 memoryfs_server.py 8002
  
  python3 memoryfs_server.py 8003
  
  python3 memoryfs_server.py 8004 2
  
  The 4th argument onwards specifies the corrupted blocks. The same corrupt block number can't be in different servers. Parity works only when 1 server is faulty for a particular block
  
3. Open another terminal and begin shell. 

  python3 memoryfs_shell_rpc.py 5 localhost:8000 localhost:8001 localhost:8002 localhost:8003 localhost:8004
  
  The third argument specifies the number of servers. Followed by the server names to connect to. 

##How to Check what's working?

Check the file generated memoryfs_log
