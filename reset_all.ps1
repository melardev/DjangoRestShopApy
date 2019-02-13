ls */migrations/*.py -exclude __init__.py | foreach {Remove-Item -Path $_.FullName}
ls */migrations/*.pyc  | foreach {Remove-Item -Path $_.FullName}

Remove-Item .\db.sqlite3

python3 manage.py makemigrations
python3 manage.py migrate
python3 seed_db.py