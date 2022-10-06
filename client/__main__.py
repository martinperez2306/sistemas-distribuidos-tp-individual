#!/usr/bin/env python3

import csv
import json
import logging
import pathlib
import os
from dependencies.commons.VideosQuery import VideosQuery

from dependencies.commons.base_app import initialize_config, initialize_log
from dependencies.commons.constants import *
from dependencies.commons.message import Message
from dependencies.commons.video import Video
from dependencies.middleware_client.middleware_client import MiddlewareClient

CONFIG_PATH = "/root/client/config/config.ini"
VIDEOS_PATH = "/root/client/videos"
CATEGORIES_PATH = "/root/client/categories"
FILEPATH_SEPARATOR = "_"

RESULTS_PENDING = "PENDING"
THUMBNAILS_STORAGE = "/root/client/thumbnails"

def main():
    config_params = initialize_config(CONFIG_PATH)
    initialize_log(config_params["logging_level"])
    middleware_client = initialize_middleware_client()
    total_countries = get_total_countries()
    categories = get_categories()
    query = VideosQuery(categories, total_countries)
    request_id = process_videos(middleware_client, query)
    results: Message = get_results(middleware_client, request_id)
    while RESULTS_PENDING == results.body:
        results = get_results(middleware_client, request_id)
    download_thumbnails(middleware_client, request_id)
    shutdown_middleware_client(middleware_client)
    show_results(results)

def initialize_middleware_client():
    logging.info("Initializing Middleware Client")
    return MiddlewareClient(RABBITMQ_HOST, MIDDLEWARE_QUEUE, THUMBNAILS_STORAGE)
    
def get_total_countries():
    logging.info("Getting total countries")
    countries = 0
    for path in pathlib.Path(VIDEOS_PATH).iterdir():
        if path.is_file():
            countries += 1
    logging.info("Total Countries = {}".format(countries))
    return countries

def get_categories():
    logging.info("Getting categories Videos")
    categories = dict()
    for path in pathlib.Path(CATEGORIES_PATH).iterdir():
        if path.is_file():
            country = extract_country_from_path(path)
            with open(path, 'r') as file:
                categories[country] = create_country_categories(json.load(file))
    logging.info("Categories [{}]".format(categories))
    return categories

def create_country_categories(json_category):
    items = json_category['items']
    country_categories = dict()
    for item in items:
        id = item['id']
        title = item['snippet']['title']
        country_categories[id] = title
    return country_categories

def process_videos(middleware_client: MiddlewareClient, query: VideosQuery):
    logging.info("Processing Videos")
    print("Processing Videos. Please wait...")
    middleware_client.connect()
    request_id = middleware_client.call_start_data_process(query)
    for path in pathlib.Path(VIDEOS_PATH).iterdir():
        if path.is_file():
            country = extract_country_from_path(path)
            process_csv(path, middleware_client, request_id, country)
    middleware_client.call_end_data_process(request_id)
    logging.info("Processing video Request ID [{}]".format(request_id))
    return request_id

def extract_country_from_path(path):
    basename = str(os.path.basename(path))
    split = basename.split(FILEPATH_SEPARATOR)
    return split[0]

def process_csv(path, middleware_client, request_id, country):
    with open(path, 'r') as file:
        csvreader = csv.reader(file)
        header = next(csvreader, None)
        logging.info("CSV Header [{}]".format(header))
        while True:
          try:
               row = next(csvreader)
               process_video(row, middleware_client, request_id, country)
          except csv.Error:
               continue
          except StopIteration:
               break

def process_video(video_str: 'list[str]', middleware_client: MiddlewareClient, request_id: int, country: str):
    logging.debug("Processing Video STR: [{}] in Request with ID [{}]".format(video_str, request_id))
    video = __parse_video_from_csv(video_str, country)
    middleware_client.call_process_data(request_id, video)

def __parse_video_from_csv(video_str: 'list[str]', country):
    id = video_str[0].strip("''")
    title = video_str[1].strip("''")
    published_at = video_str[2].strip("''")
    channel_id = video_str[3].strip("''")
    channel_title = video_str[4].strip("''")
    category_id = video_str[5].strip("''")
    trending_date = video_str[6].strip("''")
    tags = video_str[7].strip("''")
    view_count = 0
    try:
        view_count = int(video_str[8].strip("''"))
    except ValueError:
        pass
    likes = 0
    try:
        likes = int(video_str[9].strip("''"))
    except ValueError:
        pass
    dislikes = 0
    try:
        dislikes = int(video_str[10].strip("''"))
    except ValueError:
        pass
    comment_count = 0
    try:
        comment_count = int(video_str[11].strip("''"))
    except ValueError:
        pass
    thumbnail_link = video_str[12].strip("''")
    comments_disabled = video_str[13].strip("''")
    ratings_disabled = video_str[14].strip("''")
    description = video_str[15].strip("''")
    return Video(id, title, published_at, channel_id, channel_title, category_id, trending_date, tags, view_count, likes, dislikes,
                    comment_count, thumbnail_link, comments_disabled, ratings_disabled, description, country)

def get_results(middleware_client: MiddlewareClient, request_id: str):
    logging.info("Getting Results for Request with ID [{}]".format(request_id))
    print("Waiting for system processing. This may take a few minutes.")
    results_message: Message = middleware_client.wait_get_results(request_id)
    logging.info("Results for Request with ID [{}]: [{}]".format(request_id, results_message.to_string()))
    return results_message

def download_thumbnails(middleware_client: MiddlewareClient, request_id: str):
    logging.info("Download Thumbnails for Request with ID [{}]".format(request_id))
    print("Downloading files...")
    middleware_client.call_download_thumbnails(request_id)
    middleware_client.wait_get_results(request_id)

def show_results(results):
    print("Processing complete!!")
    print(results.to_string())

def shutdown_middleware_client(middleware_client: MiddlewareClient):
    middleware_client.close()

if __name__ == "__main__":
    main()