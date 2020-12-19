import datetime
import os
import subprocess
import glob
from PIL import Image

def media_resize():
    wsize=700
    extensions = ["/*.jpg", "/*.JPG", "/*.jpeg", "/*.JPEG", "/*.png", "/*.PNG"]
    files = []
    for extension in extensions:
        files.extend(glob.glob('media' + extension))

    for f in files:
        img = Image.open(f)
        if wsize >= img.width:
            continue
        rate = wsize / img.width
        hsize = int(img.height * rate)
        img_resize = img.resize((wsize, hsize))
        imgdir = os.path.dirname(f)
        imgname = os.path.basename(f)
        newfname = imgdir + "/" + imgname
        img_resize.save(newfname)

def backup_command():
    backup_directory = 'backup/'
    today = datetime.date.today()
    delete_date = today - datetime.timedelta(days=3)
    today_file = today.strftime('%Y%m%d')
    delete_file = backup_directory + delete_date.strftime('%Y%m%d')
    file_path = backup_directory + today_file +'/' + today_file
    os.makedirs(backup_directory, exist_ok=True)
    os.makedirs(backup_directory+ today_file, exist_ok=True)

    sqlite_file_path = file_path + '_db.sqlite3'
    migration_file_path = file_path + '_migrations'
    media_path = file_path + '_media'
    dumpdata_path = file_path + '_dumpdata.json'
    subprocess.run(['cp', 'db/db.sqlite3', sqlite_file_path], stdout=subprocess.PIPE)
    subprocess.run(['cp', '-r', 'todo/migrations', migration_file_path], stdout=subprocess.PIPE)
    subprocess.run(['cp', '-r', 'media', media_path], stdout=subprocess.PIPE)
    dumpdata = subprocess.run(['python3', 'manage.py', 'dumpdata'], stdout=subprocess.PIPE)
    with open(dumpdata_path, 'w') as f:
        print(dumpdata.stdout.decode('utf8'), file=f)
    subprocess.run(['rm', '-rf', delete_file], stdout=subprocess.PIPE)

media_resize()
backup_command()
