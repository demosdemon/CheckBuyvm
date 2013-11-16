#!/usr/bin/env python2.7

# pip install pymongo

from contextlib import closing
from urllib2 import urlopen, URLError
from pymongo import MongoClient
import json, sys

BUYVM_JSON = 'http://www.doesbuyvmhavestock.com/automation.json'

def main():
    with closing(urlopen(BUYVM_JSON)) as fp:
        data = json.load(fp)
        
    alerts = {
        'newstock': [],
        'depleted': []
    }
    
    conn = MongoClient()
    db = conn.buyvm.instances
    
    for vm in data:
        try:
            res = db.find_one({'pid': vm['pid']})
        except KeyError:
            continue
        
        if res is None:
            if vm['qty'] > 0:
                alerts['newstock'].append(vm)
            res = vm
        else:
            if res['qty'] == 0 and vm['qty'] > 0:
                alerts['newstock'].append(vm)
            elif res['qty'] > 0 and vm['qty'] == 0:
                alerts['depleted'].append(vm['name'] + "\n")
            res.update(vm)
        
        db.save(res)
        
    if alerts['newstock']:
        sys.stdout.write("New Stock:\n")
        sys.stdout.writelines("%(name)17s %(qty)3d\n" % vm for vm in alerts['newstock'])
    
    if alerts['newstock'] and alerts['depleted']:
        sys.stdout.write("\n")
    
    if alerts['depleted']:
        sys.stdout.write("Depleted Stock:\n")
        sys.stdout.writelines("%(name)s\n" % vm for vm in alerts['depleted'])
        
    
if __name__ == '__main__':
    main()
