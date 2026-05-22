import logging
from urllib.parse import urljoin

import requests
from bs4 import BeautifulSoup

logger = logging.getLogger(__name__)


def get_web3_career(skill):
    url = "https://web3.career"
    full_url = f"{url}/{skill}-jobs"

    try:
        response = requests.get(full_url, timeout=10)
        response.raise_for_status()
    except requests.RequestException as e:
        logger.warning("Web3 Career request failed: %s", e)
        return []

    soup = BeautifulSoup(response.content, "html.parser")
    tbody = soup.find("tbody", class_="tbody")
    if not tbody:
        return []

    all_jobs = []
    for job in tbody.find_all(class_="table_row"):
        try:
            title = job.find("h2")
            if not title:
                continue

            link_el = job.find("a")
            company_el = job.find("h3")
            if not link_el or "href" not in link_el.attrs:
                continue

            description = ""
            tds = job.find_all("td")
            if tds:
                for category in tds[-1].find_all("a"):
                    description += f" {category.get_text(strip=True)}"

            all_jobs.append(
                {
                    "title": title.get_text(strip=True),
                    "link": urljoin(f"{url}/", link_el["href"]),
                    "company_name": company_el.get_text(strip=True)
                    if company_el
                    else "",
                    "description": description.strip(),
                }
            )
        except (AttributeError, KeyError, TypeError, IndexError) as e:
            logger.debug("Web3 Career job parse skipped: %s", e)
            continue

    return all_jobs
