Check BuyVM Script

This script uses MongoDB to store json information retrieved from
http://doesbuyvmhavestock.com It outputs when a unit changes from 0 to >0 or
from >0 to 0. This is particularly useful if you have cron run this script every
hour or so and have cron email you the stdout/stderr from the cronjob.

Why MongoDB?

Because I'm already using it for other reasons, and it's quick and easy and 
schema-less, which is particularly useful since there's other data in the json
output from DBVMHS.


CronJob:

8 * * * * /path/to/buyvm.py