from AVSpider import AVSpider


START_YEAR = 2001  # first year to be scraped

END_YEAR = 2016  # last year to be scraped

YEARS = list(range(START_YEAR, END_YEAR + 1))  # list of years to be scraped

WEBDRIVER_PATH = "../chromedriver"  # path to the webdriver

av_spider = AVSpider(WEBDRIVER_PATH, allowed_webpage_response_period=60)  # initialize the AVSpider object

for year in YEARS:  # for every year

    CSV_FILENAME = "../AV Data/" + str(year) + ".csv"  # specify the output path and unique csv filename

    av_spider.deploy(CSV_FILENAME, year, offset=0, resume=False)  # deploy spider

