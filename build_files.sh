print "bulid Start"

pip install -r requirements.txt
python manage.py collectstatic

print "bulid End"