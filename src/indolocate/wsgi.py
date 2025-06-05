"""
File            : indolocate/wsgi.py  
Description     : Indolocate's wsgi file.  
"""

from indolocate.web import webserver

app = webserver() 
server = app.server