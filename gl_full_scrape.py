import pandas as pd
import requests
from scrapy import Selector


def create_urls(first_event, last_event):
    """Create urls to scrape across from the first event specified to the last"""
    results_urls = {}
    for i in range(first_event, last_event + 1):
        results_urls[i] = f"https://www.parkrun.org.uk/greatlines/results/{i}/"
    return results_urls


def create_sel_object(url):
    header = {'User-Agent': 'Mozilla/5.0 (Intel Mac OS X 10_15_7) '
                               'AppleWebKit/605.1.15 (KHTML, like Gecko) '
                               'Version/14.1.1 Safari/605.1.15',
                 'Accept': 'text/html,application/xhtml+xml,application/xml '
                           'q=0.9,image/webp,image/apng,*/*;q=0.8'}
    html = requests.get(url, headers=header).content
    return Selector(text=html)


def scrape_page(fields_dict, page_url, max_css, css_path):
    results_dict = {key: [] for (key, value) in fields_dict.items()}
    sel = create_sel_object(page_url)
    for i in range(1, max_css + 1):
        for key, value in fields_dict.items():
            path = css_path + str(i) + value
            results_dict[key].append(sel.css(path).get(default="None"))
    return results_dict


def scrape_pages_to_ind_csv(fields_dict, page_urls, history_dict, css_path, save_loc):
    for event_num, page_url in page_urls.items():
        max_css = history_dict[event_num][1]
        results_dict = scrape_page(fields_dict, page_url, max_css, css_path)
        results_df = pd.DataFrame(results_dict)
        results_df["event_num"] = event_num
        results_df["date"] = history_dict[event_num][0]
        results_df.to_csv(f"{save_loc}{event_num}.csv")


gl_history_dict = {"event": ") > td.Results-table-td.Results-table-td--position > a::text",
                   "date": ") > td:nth-child(2) > div.compact > a > span::text",
                   "num_runners": ") > td:nth-child(3)::text",
                   "num_vols": ") > td:nth-child(4)::text"}
gl_history_css = "#content > div.Results.Results--eventHistory > table > tbody > tr:nth-child("

gl_history_url = "https://www.parkrun.org.uk/greatlines/results/eventhistory/"

# FIRST: Uncomment and run below to scrape history data and save to csv
# gl_history_info = scrape_page(gl_history_dict, gl_history_url, 436, gl_history_css)
# gl_history_df = pd.DataFrame(gl_history_info)
# gl_history_df.to_csv('gl-event-details-1-436.csv')

# Uncomment after running above
# gl_history_df = pd.read_csv("gl-event-details-1-436.csv", index_col=0)
# gl_history_df.set_index("event", inplace=True)

# runner_fields_dict = {'runner_id': ") > td.Results-table-td.Results-table-td--name > div.compact > a ::attr(href)",
#                        'position': ") > td.Results-table-td.Results-table-td--position ::text",
#                        'name': ") > td.Results-table-td.Results-table-td--name > div.compact > a ::text",
#                        'age_cat': ") > td.Results-table-td.Results-table-td--name > div.Results-tablet > div > a ::text",
#                        'age_grade': ") > td.Results-table-td.Results-table-td--ageGroup > div.detailed ::text",
#                        'time': ") > td.Results-table-td.Results-table-td--time > div.compact ::text",
#                        'achievement': ") > td.Results-table-td.Results-table-td--time > div.detailed > span ::text"
#                        }
#
# css_path_runners = "#content > div.Results > table > tbody > tr:nth-child("
# runners_save_loc = "RunnerDataAll/runner-data-"
# runner_nums_dict = gl_history_df[["date", "num_runners"]].T.to_dict("list")

# Uncomment and run below to scrape runner data and save to csv files
# pages_to_scrape = create_urls(1, 436)
# scrape_pages_to_ind_csv(runner_fields_dict, pages_to_scrape, runner_nums_dict, css_path_runners, runners_save_loc)

# vol_fields_dict = {'volunteer_id': ") ::attr(href)",
#                    "volunteer_name": ") ::text"}
# css_path_vols = "#content > div.paddedt.left > p:nth-child(2) > a:nth-child("
# vol_save_loc = "VolunteerDataAll/volunteer-data-"
# vol_nums_dict = gl_history_df[["date", "num_vols"]].T.to_dict("list")

# Uncomment and run below to scrape volunteer data and save to csv files
# pages_to_scrape = create_urls(1, 436)
# scrape_pages_to_ind_csv(vol_fields_dict, pages_to_scrape, vol_nums_dict, css_path_vols, vol_save_loc)





