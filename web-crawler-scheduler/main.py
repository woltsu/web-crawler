import sys
from scheduler import SchedulerServer

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Please provide a root url as the first argument")
        exit(1)
    schedulerServer = SchedulerServer.SchedulerServer()
    schedulerServer.start()