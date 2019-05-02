import os
from scheduler import SchedulerServer

if __name__ == "__main__":
    schedulerServer = SchedulerServer.SchedulerServer()
    schedulerServer.start()