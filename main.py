'''
<<<<<<< HEAD
=======
main.py
----------
Matthew Chatham
June 6, 2018

>>>>>>> 7a5082d8ae61d93721d9ec8deb4ddda3d21cfb47
Given a company's landing page on Glassdoor and an output filename, scrape the
following information about each employee review:

Review date
Employee position
Employee location
Employee status (current/former)
Review title
Employee years at company
Number of helpful votes
Pros text
Cons text
Advice to mgmttext
Ratings for each of 5 categories
Overall rating
'''

import time
import pandas as pd
from argparse import ArgumentParser
import argparse
import logging
import logging.config
from selenium import webdriver as wd
import selenium
import numpy as np
from schema import SCHEMA
import json
import urllib
import datetime as dt

start = time.time()

DEFAULT_URL = ('https://www.glassdoor.com/Overview/Working-at-'
               'Premise-Data-Corporation-EI_IE952471.11,35.htm')

parser = ArgumentParser()
parser.add_argument('-u', '--url',
                    help='URL of the company\'s Glassdoor landing page.',
                    default=DEFAULT_URL)
parser.add_argument('-f', '--file', default='glassdoor_ratings.csv',
                    help='Output file.')
parser.add_argument('--headless', action='store_true',
                    help='Run Chrome in headless mode.')
parser.add_argument('--username', help='Email address used to sign in to GD.')
parser.add_argument('-p', '--password', help='Password to sign in to GD.')
parser.add_argument('-c', '--credentials', help='Credentials file')
parser.add_argument('-l', '--limit', default=25,
                    action='store', type=int, help='Max reviews to scrape')
parser.add_argument('--start_from_url', action='store_true',
                    help='Start scraping from the passed URL.')
parser.add_argument(
    '--max_date', help='Latest review date to scrape.\
    Only use this option with --start_from_url.\
    You also must have sorted Glassdoor reviews ASCENDING by date.',
    type=lambda s: dt.datetime.strptime(s, "%Y-%m-%d"))
parser.add_argument(
    '--min_date', help='Earliest review date to scrape.\
    Only use this option with --start_from_url.\
    You also must have sorted Glassdoor reviews DESCENDING by date.',
    type=lambda s: dt.datetime.strptime(s, "%Y-%m-%d"))
args = parser.parse_args()

if not args.start_from_url and (args.max_date or args.min_date):
    raise Exception(
        'Invalid argument combination:\
        No starting url passed, but max/min date specified.'
    )
elif args.max_date and args.min_date:
    raise Exception(
        'Invalid argument combination:\
        Both min_date and max_date specified.'
    )

if args.credentials:
    with open(args.credentials) as f:
        d = json.loads(f.read())
        args.username = d['username']
        args.password = d['password']
else:
    try:
        with open('secret.json') as f:
            d = json.loads(f.read())
            args.username = d['username']
            args.password = d['password']
    except FileNotFoundError:
        msg = 'Please provide Glassdoor credentials.\
        Credentials can be provided as a secret.json file in the working\
        directory, or passed at the command line using the --username and\
        --password flags.'
        raise Exception(msg)


logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)
ch = logging.StreamHandler()
ch.setLevel(logging.INFO)
logger.addHandler(ch)
formatter = logging.Formatter(
    '%(asctime)s %(levelname)s %(lineno)d\
    :%(filename)s(%(process)d) - %(message)s')
ch.setFormatter(formatter)

logging.getLogger('selenium').setLevel(logging.CRITICAL)
logging.getLogger('selenium').setLevel(logging.CRITICAL)


def scrape(field, review, author):

    def scrape_date(review):
        return review.find_element_by_tag_name(
            'time').get_attribute('datetime')

    def scrape_emp_title(review):
        if 'Anonymous Employee' not in review.text:
            try:
                res = author.find_element_by_class_name(
                    'authorJobTitle').text.split('-')[1]
            except Exception:
                logger.warning('Failed to scrape employee_title')
                res = np.nan
        else:
            res = np.nan
        return res

    def scrape_location(review):
        if 'in' in review.text:
            try:
                res = author.find_element_by_class_name(
                    'authorLocation').text
            except Exception:
                res = np.nan
        else:
            res = np.nan
        return res

    def scrape_status(review):
        try:
            res = author.text.split('-')[0]
        except Exception:
            logger.warning('Failed to scrape employee_status')
            res = np.nan
        return res

    def scrape_rev_title(review):
        return review.find_element_by_class_name('summary').text.strip('"')

    def scrape_years(review):
<<<<<<< HEAD
        try:
            first_par = review.find_element_by_class_name(
                'reviewBodyCell').find_element_by_tag_name('p')
            if '(' in first_par.text:
                res = first_par.text[first_par.text.find('(') + 1:-1]
            else:
                res = np.nan
        except Exception:
=======
        first_par = review.find_element_by_class_name(
            'reviewBodyCell').find_element_by_tag_name('p')
        if '(' in first_par.text:
            res = first_par.text[first_par.text.find('(') + 1:-1]
        else:
>>>>>>> 7a5082d8ae61d93721d9ec8deb4ddda3d21cfb47
            res = np.nan
        return res

    def scrape_helpful(review):
        try:
<<<<<<< HEAD
            #helpful = review.find_element_by_class_name('count')
            helpful = review.find_element_by_class_name('voteHelpful').find_element_by_class_name('count').find_element_by_tag_name('span')
=======
            helpful = review.find_element_by_class_name('helpfulCount')
>>>>>>> 7a5082d8ae61d93721d9ec8deb4ddda3d21cfb47
            res = helpful[helpful.find('(') + 1: -1]
        except Exception:
            res = 0
        return res

    def expand_show_more(section):
        try:
            more_content = section.find_element_by_class_name('moreContent')
            more_link = more_content.find_element_by_class_name('moreLink')
            more_link.click()
        except Exception:
            pass

    def scrape_pros(review):
<<<<<<< HEAD
        #try:
        return review.find_elements_by_class_name('mt-md')[0].find_elements_by_tag_name('p')[1].text
            #expand_show_more(pros)
            #res = pros.text.replace('\nShow Less', '')
        #except Exception:
        #return np.nan

    def scrape_cons(review):
        try:
            return review.find_elements_by_class_name('mt-md')[1].find_elements_by_tag_name('p')[1].text
            #expand_show_more(pros)
            #res = pros.text.replace('\nShow Less', '')
        except Exception:
            return np.nan

    def scrape_advice(review):
        
        try:
            return review.find_elements_by_class_name('mt-md')[2].find_elements_by_tag_name('p')[1].text
            #expand_show_more(pros)
            #res = pros.text.replace('\nShow Less', '')
        except Exception:
            return np.nan

=======
        try:
            pros = review.find_element_by_class_name('pros')
            expand_show_more(pros)
            res = pros.text.replace('\nShow Less', '')
        except Exception:
            res = np.nan
        return res

    def scrape_cons(review):
        try:
            cons = review.find_element_by_class_name('cons')
            expand_show_more(cons)
            res = cons.text.replace('\nShow Less', '')
        except Exception:
            res = np.nan
        return res

    def scrape_advice(review):
        try:
            advice = review.find_element_by_class_name('adviceMgmt')
            expand_show_more(advice)
            res = advice.text.replace('\nShow Less', '')
        except Exception:
            res = np.nan
        return res
>>>>>>> 7a5082d8ae61d93721d9ec8deb4ddda3d21cfb47

    def scrape_overall_rating(review):
        try:
            ratings = review.find_element_by_class_name('gdStars')
            overall = ratings.find_element_by_class_name(
                'rating').find_element_by_class_name('value-title')
            res = overall.get_attribute('title')
        except Exception:
            res = np.nan
        return res

    def _scrape_subrating(i):
        try:
            ratings = review.find_element_by_class_name('gdStars')
            subratings = ratings.find_element_by_class_name(
                'subRatings').find_element_by_tag_name('ul')
            this_one = subratings.find_elements_by_tag_name('li')[i]
            res = this_one.find_element_by_class_name(
                'gdBars').get_attribute('title')
        except Exception:
            res = np.nan
        return res

    def scrape_work_life_balance(review):
        return _scrape_subrating(0)

    def scrape_culture_and_values(review):
        return _scrape_subrating(1)

    def scrape_career_opportunities(review):
        return _scrape_subrating(2)

    def scrape_comp_and_benefits(review):
        return _scrape_subrating(3)

    def scrape_senior_management(review):
        return _scrape_subrating(4)

    funcs = [
        scrape_date,
        scrape_emp_title,
        scrape_location,
        scrape_status,
        scrape_rev_title,
        scrape_years,
        scrape_helpful,
        scrape_pros,
        scrape_cons,
        scrape_advice,
        scrape_overall_rating,
        scrape_work_life_balance,
        scrape_culture_and_values,
        scrape_career_opportunities,
        scrape_comp_and_benefits,
        scrape_senior_management
    ]

    fdict = dict((s, f) for (s, f) in zip(SCHEMA, funcs))

    return fdict[field](review)


def extract_from_page():

    def is_featured(review):
        try:
            review.find_element_by_class_name('featuredFlag')
            return True
        except selenium.common.exceptions.NoSuchElementException:
            return False

    def extract_review(review):
        author = review.find_element_by_class_name('authorInfo')
        res = {}
        # import pdb;pdb.set_trace()
        for field in SCHEMA:
            res[field] = scrape(field, review, author)

        assert set(res.keys()) == set(SCHEMA)
        return res

    logger.info(f'Extracting reviews from page {page[0]}')

    res = pd.DataFrame([], columns=SCHEMA)

    reviews = browser.find_elements_by_class_name('empReview')
    logger.info(f'Found {len(reviews)} reviews on page {page[0]}')

    for review in reviews:
        if not is_featured(review):
            data = extract_review(review)
            logger.info(f'Scraped data for "{data["review_title"]}"\
({data["date"]})')
            res.loc[idx[0]] = data
        else:
            logger.info('Discarding a featured review')
        idx[0] = idx[0] + 1

    if args.max_date and \
        (pd.to_datetime(res['date']).max() > args.max_date) or \
            args.min_date and \
            (pd.to_datetime(res['date']).min() < args.min_date):
        logger.info('Date limit reached, ending process')
        date_limit_reached[0] = True

    return res


def more_pages():
    paging_control = browser.find_element_by_class_name('pagingControls')
    next_ = paging_control.find_element_by_class_name('next')
    try:
        next_.find_element_by_tag_name('a')
        return True
    except selenium.common.exceptions.NoSuchElementException:
        return False


def go_to_next_page():
    logger.info(f'Going to page {page[0] + 1}')
<<<<<<< HEAD
    paging_control = browser.find_element_by_class_name('pagination__PaginationStyle__next')
    next_ = paging_control.find_element_by_class_name('pagination__ArrowStyle__nextArrow  ')
=======
    paging_control = browser.find_element_by_class_name('pagingControls')
    next_ = paging_control.find_element_by_class_name(
        'next').find_element_by_tag_name('a')
>>>>>>> 7a5082d8ae61d93721d9ec8deb4ddda3d21cfb47
    browser.get(next_.get_attribute('href'))
    time.sleep(1)
    page[0] = page[0] + 1


def no_reviews():
    return False
    # TODO: Find a company with no reviews to test on


def navigate_to_reviews():
    logger.info('Navigating to company reviews')

    browser.get(args.url)
    time.sleep(1)

    if no_reviews():
        logger.info('No reviews to scrape. Bailing!')
        return False

    reviews_cell = browser.find_element_by_xpath(
        "//*[@id='EmpLinksWrapper']/div//a[2]")
    reviews_path = reviews_cell.get_attribute('href')
    browser.get(reviews_path)
    time.sleep(1)

    return True


def sign_in():
    logger.info(f'Signing in to {args.username}')

    url = 'https://www.glassdoor.com/profile/login_input.htm'
    browser.get(url)

    # import pdb;pdb.set_trace()

    email_field = browser.find_element_by_name('username')
    password_field = browser.find_element_by_name('password')
    submit_btn = browser.find_element_by_xpath('//button[@type="submit"]')

    email_field.send_keys(args.username)
    password_field.send_keys(args.password)
    submit_btn.click()

    time.sleep(1)


def get_browser():
    logger.info('Configuring browser')
    chrome_options = wd.ChromeOptions()
    if args.headless:
        chrome_options.add_argument('--headless')
    chrome_options.add_argument('log-level=3')
    browser = wd.Chrome(options=chrome_options)
    return browser


def get_current_page():
    logger.info('Getting current page number')
    paging_control = browser.find_element_by_class_name('pagingControls')
    current = int(paging_control.find_element_by_xpath(
        '//ul//li[contains\
        (concat(\' \',normalize-space(@class),\' \'),\' current \')]\
        //span[contains(concat(\' \',\
        normalize-space(@class),\' \'),\' disabled \')]')
        .text.replace(',', ''))
    return current


def verify_date_sorting():
    logger.info('Date limit specified, verifying date sorting')
    ascending = urllib.parse.parse_qs(
        args.url)['sort.ascending'] == ['true']

    if args.min_date and ascending:
        raise Exception(
            'min_date required reviews to be sorted DESCENDING by date.')
    elif args.max_date and not ascending:
        raise Exception(
            'max_date requires reviews to be sorted ASCENDING by date.')


browser = get_browser()
page = [1]
idx = [0]
date_limit_reached = [False]


def main():
<<<<<<< HEAD
    count=0
=======

>>>>>>> 7a5082d8ae61d93721d9ec8deb4ddda3d21cfb47
    logger.info(f'Scraping up to {args.limit} reviews.')

    res = pd.DataFrame([], columns=SCHEMA)

    sign_in()

    if not args.start_from_url:
        reviews_exist = navigate_to_reviews()
        if not reviews_exist:
            return
    elif args.max_date or args.min_date:
        verify_date_sorting()
        browser.get(args.url)
        page[0] = get_current_page()
        logger.info(f'Starting from page {page[0]:,}.')
        time.sleep(1)
    else:
        browser.get(args.url)
        page[0] = get_current_page()
        logger.info(f'Starting from page {page[0]:,}.')
        time.sleep(1)

    reviews_df = extract_from_page()
    res = res.append(reviews_df)

    # import pdb;pdb.set_trace()

<<<<<<< HEAD
    while(count<(args.limit//10)):
        go_to_next_page()
        reviews_df = extract_from_page()
        res = res.append(reviews_df)
        count+=1
=======
    while more_pages() and\
            len(res) < args.limit and\
            not date_limit_reached[0]:
        go_to_next_page()
        reviews_df = extract_from_page()
        res = res.append(reviews_df)
>>>>>>> 7a5082d8ae61d93721d9ec8deb4ddda3d21cfb47

    logger.info(f'Writing {len(res)} reviews to file {args.file}')
    res.to_csv(args.file, index=False, encoding='utf-8')

    end = time.time()
    logger.info(f'Finished in {end - start} seconds')


if __name__ == '__main__':
    main()
