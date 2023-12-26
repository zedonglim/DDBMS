## We app demo for DDBS project

### 1. First start the mysql dataset and minio
 1. Start minio server 

  To start mysql server, just open mysql workbench and open the instance where database is stored
  -> navigate to where minio.exe is located (data store folder)
 ```bash
 minio.exe server .
 ```

### 2. Start the web app
```bash
flask --app newsapp --debug run
```

