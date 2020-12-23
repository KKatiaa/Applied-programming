import os, sys

sys.path.insert(0, os.getcwd())

from app import app, db, ma
from app.users_notes import *

try:
    db.create_all()
except Exception as e:
    print(e)
    sys.exit(1)

try:
    app.run(debug = True, host='0.0.0.0', port=5000)
except Exception as e:
    print(e)
    sys.exit(1)
