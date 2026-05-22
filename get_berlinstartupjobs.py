# BLUEPRINT | DONT EDIT

import logging

import requests
from bs4 import BeautifulSoup

HEADERS = "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36"

logger = logging.getLogger(__name__)


def _parse_berlin_jobs(soup):
    all_jobs = []
    jobs_list = soup.find("ul", class_="jobs-list-items")
    if not jobs_list:
        return all_jobs

    for job in jobs_list.find_all("li", class_="bjs-jlid"):
        try:
            title_el = job.find("h4", class_="bjs-jlid__h")
            link_el = title_el.find("a") if title_el else None
            desc_el = job.find("div", class_="bjs-jlid__description")
            company_el = job.find("a", class_="bjs-jlid__b")
            if not link_el or not company_el:
                continue

            all_jobs.append(
                {
                    "title": link_el.get_text(strip=True),
                    "description": desc_el.get_text(strip=True) if desc_el else "",
                    "link": link_el["href"],
                    "company_name": company_el.get_text(strip=True),
                }
            )
        except (AttributeError, KeyError, TypeError) as e:
            logger.debug("Berlin job parse skipped: %s", e)
            continue

    return all_jobs


def _fetch_soup(url, headers):
    response = requests.get(url, headers={"User-Agent": headers}, timeout=10)
    response.raise_for_status()
    return BeautifulSoup(response.content, "html.parser")


def get_berlinstartupjobs(url, headers):
    try:
        soup = _fetch_soup(url, headers)
    except requests.RequestException as e:
        logger.warning("Berlin Startup Jobs request failed: %s", e)
        return []

    pagination_nav = soup.find("ul", class_="bsj-nav")
    pages = []
    if pagination_nav:
        for btn in pagination_nav.find_all(class_="page-numbers"):
            if not btn:
                continue
            content = btn.get_text(strip=True)
            try:
                float(content)
                pages.append(content)
            except ValueError:
                pass

    if pages:
        all_jobs = []
        for i in pages:
            try:
                page_soup = _fetch_soup(url + f"page/{i}", headers)
                all_jobs.extend(_parse_berlin_jobs(page_soup))
            except requests.RequestException as e:
                logger.warning("Berlin Startup Jobs page %s failed: %s", i, e)
                continue
        return all_jobs

    return _parse_berlin_jobs(soup)
