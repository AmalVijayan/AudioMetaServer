# Django Audio Metadata Server

### System requirements:
- Python 3.7

### Local setup:

Clone  
```bash
git clone https://github.com/AmalVijayan/AudioMetaServer.git
```

Create virtualenv
```bash
cd AudioMetaServer
python3 -m venv ve #or virtualenv ve
source ve/bin/activate #or ve\Scripts\acivate for windows
```

Install dependencies
```bash
pip install -r requirements.txt
```

Run existing migrations (creates a local sqlite3 DB file with tables)  
```bash
python manage.py migrate
```

Run Unit-tests:
```bash
python manage.py test audio_files
python manage.py test audio_files_api

or 

python manage.py test
```

Load sample data:
```bash
python manage.py loaddata sampledata.json
```


Run server  
```bash
python manage.py runserver 8000
```

Django automatic admin    
- [http://localhost:8000/admin/]()  
- username: admin
- password: admin123

### Postman API Collections:  
Download and import into postman:  
  [AudioServer.postman_collection.json](https://drive.google.com/file/d/1I6XiQ1mvoJBGoDA0gpfw8k9F6tUGBkQZ/view?usp=sharing)  
