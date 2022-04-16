import schedule
import time

def job():
    print("I'm working...")
def job2():
    print("I'm Babou...")
def job3():
    print("I'm Mbaye...")

schedule.every(1).minutes.do(job)
schedule.every().hour.do(job)
schedule.every().day.at("10:28").do(job2)
schedule.every().monday.do(job)
schedule.every().thursday.at("10:27").do(job3)
schedule.every().minute.at(":17").do(job)

while True:
    schedule.run_pending()
    time.sleep(1)