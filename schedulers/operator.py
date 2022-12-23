from apscheduler.schedulers.background import BackgroundScheduler
from schedulers.task.change_weather import change_weather


def start():
    scheduler = BackgroundScheduler()
    # 혹시 빠르게 메일을 받고싶다면 hours를 seconds로 바꾸고 10초정도로 해주세요.
    scheduler.add_job(change_weather, "interval", hours=1)
    print("스케줄링 시작")
    scheduler.start()
