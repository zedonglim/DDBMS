# DDBMS
Distributed Database Management System for THUACP2023

## When running a large script in mysql workbence
### SET GLOBAL max_allowed_packet=1000000

```
SELECT * FROM dmbs1.user 
WHERE find_in_set(uid, (SELECT readUidList FROM dmbs1.be_read  WHERE aid=9));
```
## We app demo for DDBMS project

### 1. First start the mysql dataset and minio
 A. Start MYSQL Sever

 - To start mysql server, just open mysql workbench and open the instance where database is stored

 B. Start minio server 
  - navigate to where minio.exe is located (i.e., datastore folder) and then run the following command
 ```bash
 minio.exe server .
 ```

### 2. Start the web app
```bash
cd web
flask --app newsapp --debug run
```

