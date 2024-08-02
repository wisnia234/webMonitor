import schedule
import time
import webRequest

schedule.every(10).seconds.do(webRequest.run)

while True:
    schedule.run_pending()
    time.sleep(1)