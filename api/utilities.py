"""
Errors 500
Last modification: 24-04-2023 - Giovanni Junco
"""
import sys
from apscheduler.schedulers.background import BackgroundScheduler
from logs import do_log
from api.models import driver, session


# Creates a default Background Scheduler
sched = BackgroundScheduler()


def get_error(point,error):
    """ log and response error handling 500
        Required attributes:
            point (String): endpoint or resolve
            error(object): data error
        Return: 
            response: to graphql
    """
    do_log(str(error),point,
            error[2].tb_lineno
            ,'error')
    return {"status":500,
            "message": 'internal_error',
            "error": f'Point : {point}, Error: {str(error)}' }

def prompt():
    try:   
        session.close()
        driver.close()
        sched.remove_all_jobs()
        print(" -Executing Task...")
    except:
        return get_error('prompt, utilies',sys.exc_info())

def begin_job():
    sched.remove_all_jobs()
    sched.add_job(prompt,'interval', seconds=30, id='job_close_DB') 
    # Starts the Scheduled jobs
    if sched.state ==0:
        sched.start()