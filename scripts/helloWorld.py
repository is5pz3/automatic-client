from apscheduler.schedulers.blocking import BlockingScheduler

sched = BlockingScheduler()

@sched.scheduled_job('interval', seconds=2)
def hello_world_job():
    print("Hello, World!")

sched.start()
