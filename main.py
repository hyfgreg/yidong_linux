import json
from datetime import date
from yidong import QueryYidong
import config
from savedata import SaveData
from sendmail import sendmail
from upload_to_qiniu import upload
from apscheduler.schedulers.blocking import BlockingScheduler

def main():
    try:
        yd = QueryYidong()
        yd.saveAll()
    except Exception as e:
        sendmail(str(e),success=False)
        # raise e

    try:
        s = SaveData()
        s.saveSimple()
    except Exception as e:
        sendmail(str(e),success=False)

    try:
        result = upload()
        sendmail(result)
    except:
        sendmail(str(e),success=False)
if __name__ == '__main__':
    sched = BlockingScheduler()
    sched.add_job(main,'cron',hour=22,minute=6)
    sched.start()

    # main()
