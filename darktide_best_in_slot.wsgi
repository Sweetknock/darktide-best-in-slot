import sys
import logging

logging.basicConfig(level=logging.DEBUG, filename='/var/www/html/darktide-best-in-slot/darktide_best_in_slot.log',
					format='%(asctime)s %(message)s')
sys.path.insert(0, '/var/www/html/darktide_best_in_slot')
sys.path.insert(0, '/var/www/html/darktide_best-in_slot/.venv/lib/python3.9/site-packages')
from app import app as application
