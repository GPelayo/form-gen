from datetime import datetime


class TimedTest:
    @staticmethod
    def start(gaddery):
        start_time = datetime.now()
        print("Started Scraping...")
        gaddery.collect_data()
        print("Scraping Finished after {}".format(datetime.now() - start_time))
