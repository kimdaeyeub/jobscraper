import logging
from urllib.parse import urljoin

import requests
from bs4 import BeautifulSoup

logger = logging.getLogger(__name__)


def get_rework(skill):
    url = "https://weworkremotely.com"
    full_url = f"{url}/remote-jobs/search?utf8=%E2%9C%93&term={skill}"

    try:
        response = requests.get(full_url, timeout=10)
        response.raise_for_status()
    except requests.RequestException as e:
        logger.warning("We Work Remotely request failed: %s", e)
        return []

    soup = BeautifulSoup(response.content, "html.parser")
    jobs_section = soup.find("section", class_="jobs")
    if not jobs_section:
        return []

    all_jobs = []
    for job in jobs_section.find_all("li"):
        try:
            title = job.find("h3", class_="new-listing__header__title")
            if not title:
                continue

            company_el = job.find("p", class_="new-listing__company-name")
            desc_el = job.find("p", class_="new-listing__company-headquarters")
            link = job.find("a", class_="listing-ad-url")
            if not link or "href" not in link.attrs:
                continue

            all_jobs.append(
                {
                    "title": title.get_text(strip=True),
                    "description": desc_el.get_text(strip=True) if desc_el else "",
                    "link": urljoin(f"{url}/", link["href"]),
                    "company_name": company_el.get_text(strip=True)
                    if company_el
                    else "",
                }
            )
        except (AttributeError, KeyError, TypeError) as e:
            logger.debug("We Work Remotely job parse skipped: %s", e)
            continue

    return all_jobs
