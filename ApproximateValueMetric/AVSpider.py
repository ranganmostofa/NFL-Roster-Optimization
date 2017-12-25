from time import sleep
from FileIO import FileIO
from selenium import webdriver
from selenium.common.exceptions import NoSuchElementException


# create a global registry of all unique "data-stat" web element values for every web row
WEB_DATA_FIELDS = \
    [
        "ranker",
        "player",
        "year_id",
        "age",
        "psl_draft_info",
        "team",
        "league_id",
        "g",
        "gs",
        "seasons",
        "pro_bowls",
        "all_pros_first_team",
        "av"
    ]


class AVSpider:
    """
    Web spider class that houses all necessary code to crawl www.pro-football-reference.com,
    retrieve and store Approximate Value data for a user-specified season
    """
    def __init__(self, webdriver_path, allowed_webpage_response_period=60):
        """
        Constructor for the AVSpider class - used to initialize all necessary fields of the
        AVSpider object
        """
        self.webdriver_path = webdriver_path  # initialize all necessary fields
        self.allowed_webpage_response_period = allowed_webpage_response_period
        self.base_url = "https://www.pro-football-reference.com/play-index/"

    def deploy(self, csv_filename, year, offset=0, resume=False):
        """
        Given a csv filename and the start year of an NFL season, deploys the spider to extract all
        relevant Approximate Value data pertaining to specified season and finally, stores retrieved
        data in a csv file
        """
        if resume:  # if resume capabilities are switched on
            csv_matrix = FileIO.read_csv(csv_filename)  # read in data that has been scraped so far
        else:
            csv_matrix = \
                list([
                    AVSpider.build_csv_data_fields()  # otherwise, start anew
                ])

        current_offset = offset  # set the current offset as the input offset

        driver = webdriver.Chrome(self.get_webdriver_path())  # initialize the webdriver

        while True:  # infinite loop - should break out of loop once all data has been scraped (see below)

            print("\nCurrent Offset: " + str(current_offset) + "\n")  # print current offset

            # build query based on year and offset
            current_query = AVSpider.build_branch_url(year, current_offset)
            current_target_url = self.get_base_url() + current_query  # build target url

            driver.get(current_target_url)  # visit target url

            sleep(self.get_allowed_webpage_response_period())  # allow time for webpage to load

            # retrieve table of web rows
            table_outer_container = driver.find_element_by_xpath('.//div[@class="table_outer_container"]')
            table_body = table_outer_container.find_element_by_xpath(".//tbody")

            for web_row in table_body.find_elements_by_xpath(".//tr"):  # for every web row
                csv_data_row = AVSpider.retrieve_web_row_data(web_row)  # extract relevant information
                if csv_data_row:  # if csv data row is not empty
                    csv_matrix.append(list(csv_data_row))  # append csv row to data matrix
                    print(csv_data_row)  # print csv row to console

            FileIO.write_csv(csv_filename, csv_matrix)  # write data that has been scraped so far to memory

            current_offset = len(csv_matrix) - 1  # compute updated offset

            # if a "Next Page" button does not exist, break out of infinite loop
            if not driver.find_elements_by_xpath('.//div[@class="prevnext"]'):
                break

        driver.close()  # terminate spider once all data has been acquired

    @staticmethod
    def retrieve_web_row_data(web_row):
        """
        Given a web row element, extracts and returns all relevant textual information in a list
        """
        csv_data_row = list()  # initialize csv row
        try:  # surround operations with a try-catch block
            # extract rank field
            csv_data_row.append(str(web_row.find_element_by_xpath('.//th[@data-stat="ranker"]').text))
            for field in WEB_DATA_FIELDS[1:]:  # for all fields other than rank
                # use the global registry defined at the top of this module
                csv_data_row.append(str(web_row.find_element_by_xpath('.//td[@data-stat="' + str(field) + '"]').text))
            csv_data_row = AVSpider.preprocess_player_names(csv_data_row)  # preprocess player names
        except NoSuchElementException:  # in the event of an exception
            csv_data_row.clear()  # clear the csv row in order to avoid storage of bad data
        return csv_data_row  # return final csv data row

    @staticmethod
    def preprocess_player_names(csv_data_row):
        """
        Given a csv data row, preprocesses the player name contained within to remove any trailing
        asterisks and returns the formatted row
        """
        # strip the right side of the player name of any asterisks
        return list([csv_data_row[0]]) + list([str(csv_data_row[1]).rstrip("*")]) + list(csv_data_row[2:])

    @staticmethod
    def build_csv_data_fields():
        """
        Static method that returns the header row prefacing all csv file outputs
        """
        return \
            list([
                'Rank', 'Player', 'Year', 'Age', 'Draft', 'Team', 'League', 'Games Played',
                'Games Started', 'Years', 'Pro-Bowl Selections', 'First-Team All-Pro Selections', 'Approximate Value'
            ])

    @staticmethod
    def build_branch_url(year, offset=0):
        """
        Given the NFL season start year and the offset, i.e. the number of rows to skip, builds
        and returns a suitable query to access the relevant Approximate Value information from the
        pro-football reference website
        """
        # build and return the query
        return \
            "psl_finder.cgi?request=1&match=single" + \
            "&year_min=" + str(year) + \
            "&year_max=" + str(year) + \
            "&season_start=1&season_end=-1&age_min=0&age_max=0" + \
            "&pos=qb&pos=rb&pos=wr&pos=te&pos=e&pos=t&pos=g&pos=c&pos=ol&pos=dt" + \
            "&pos=de&pos=dl&pos=ilb&pos=olb&pos=lb&pos=cb&pos=s&pos=db&pos=k&pos=p" + \
            "&c1stat=choose&c1comp=gt&c2stat=choose&c2comp=gt&c3stat=choose&c3comp=gt" + \
            "&c4stat=choose&c4comp=gt&c5comp=choose&c5gtlt=lt&c6mult=1.0&c6comp=choose" + \
            "&order_by=av" + \
            "&draft=0&draft_year_min=1936&draft_year_max=2016&draft_slot_min=1&draft_slot_max=500" + \
            "&draft_pick_in_round=pick_overall&conference=any&draft_pos=qb&draft_pos=rb&draft_pos=wr&draft_pos=te" + \
            "&draft_pos=e&draft_pos=t&draft_pos=g&draft_pos=c&draft_pos=ol&draft_pos=dt&draft_pos=de&draft_pos=dl" + \
            "&draft_pos=ilb&draft_pos=olb&draft_pos=lb&draft_pos=cb&draft_pos=s&draft_pos=db&draft_pos=k&draft_pos=p" +\
            "&utm_source=direct&utm_medium=Share&utm_campaign=ShareTool" + \
            "&offset=" + str(offset)

    def get_webdriver_path(self):
        """
        Returns the webdriver path of the web spider
        """
        return self.webdriver_path  # return the webdriver path

    def get_allowed_webpage_response_period(self):
        """
        Returns the amount of time, in seconds, that the spider allows the webpage to load before
        initiating data extraction
        """
        return self.allowed_webpage_response_period  # return the response period

    def get_base_url(self):
        """
        Returns the base url of the web spider
        """
        return self.base_url  # return the base url

    def set_webdriver_path(self, webdriver_path):
        """
        Given a new webdriver path, sets the input as the current webdriver path
        """
        self.webdriver_path = webdriver_path  # overwrite the existing webdriver path with the input webdriver path

    def set_allowed_webpage_response_period(self, allowed_webpage_response_period):
        """
        Given a new response period, sets the input as the current allowed response period
        """
        self.allowed_webpage_response_period = allowed_webpage_response_period

