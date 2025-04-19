import os

bind = f"0.0.0.0:{os.getenv('PORT', '10000')}"
workers = 4
timeout = 120
accesslog = '-'
errorlog = '-'



