from git import Repo
from os.path import isdir
from os import environ
from sys import stderr, stdout
from pathlib import Path
from .types import RegionReport

import csv
import pendulum

REPO_TARGET = environ.get("REPO_TARGET", "./.stats_repo")

# The format (which is unfortunate) used by the csv files
FILE_DATE_FORMAT = "MM-DD-YYYY"

def today():
    """
    Return the current day in DD-MM-YYYY format.
    """
    dt = pendulum.now()
    return (dt.year, dt.month, dt.day)

def clone_repo():
    """
    Clone the covid-19 data repo.
    """
    if not isdir(REPO_TARGET):
        stdout.write(f"Cloning repo to {REPO_TARGET}\n")
        Repo.clone_from("https://github.com/CSSEGISandData/COVID-19.git", REPO_TARGET)

def pull_repo():
    """
    Pull the latest from the repo.
    """
    clone_repo()
    repo = Repo(REPO_TARGET)
    stdout.write(f"Pulling latest from origin\n")
    repo.remotes.origin.pull()

def case_reports_by_day(year, month, day):
    """
    Given a timestamp, get an iterator over data from that day.
    If it does not exist, the iterator will yield zero values.
    """

    timestamp = pendulum.datetime(year, month, day).format(FILE_DATE_FORMAT)
    reports_subpath = Path("csse_covid_19_data/csse_covid_19_daily_reports")

    case_reports_path = Path(".") / Path(REPO_TARGET) / Path(reports_subpath) / Path(f"{timestamp}.csv")

    if case_reports_path.exists():
        with case_reports_path.open() as reportsfile:
            reports_reader = csv.reader(reportsfile, delimiter=",")
            # skip the headers
            next(reports_reader)
            for row in reports_reader:
                yield RegionReport(*row)

def current_case_reports():
    """
    Get an iterator of all case reports for today. If they exist.
    Otherwise decrement day until we find one that does exist.
    """
    return case_reports_by_day(*today())
