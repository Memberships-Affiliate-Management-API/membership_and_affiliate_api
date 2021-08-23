***REMOVED***
    **scheduler**
        used to dynamically add jobs on a separate thread to complete tasks that should not interfere
        with requests, or requests that takes a long time to complete
***REMOVED***

from apscheduler.schedulers.background import BackgroundScheduler
schedule = BackgroundScheduler()
