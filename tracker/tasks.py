#from celery.task import task
#from tracker.utils import update_twitter, update_facebook

#@task
def twitter_task():
    for batch in range(1,6):
        update_twitter('house', official=True, batch=batch)
        update_twitter('house', official=False, batch=batch)
    update_twitter('senate')
    
#@task
def facebook_task():
    update_facebook('house')
    update_facebook('senate')