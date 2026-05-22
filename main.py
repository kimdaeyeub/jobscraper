import json
import logging
from pathlib import Path

from flask import Flask, render_template, request
from skills import SKILLS, SKILL_IDS, SKILL_LABELS

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

app = Flask("jobscraper")

DATA_DIR = Path(__file__).parent / "docs" / "data"


def load_cached_jobs(skill):
    if skill not in SKILL_IDS:
        return None

    path = DATA_DIR / f"{skill}.json"
    if not path.exists():
        return None

    data = json.loads(path.read_text(encoding="utf-8"))
    return data.get("jobs", [])


@app.route("/")
def home():
    skill = request.args.get("skill", "").strip().lower()
    unsupported = bool(skill and skill not in SKILL_IDS)
    jobs = []

    if skill and not unsupported:
        jobs = load_cached_jobs(skill) or []

    logger.info("Loaded %d cached jobs for skill=%r", len(jobs), skill or None)
    return render_template(
        "home.html",
        jobs=jobs,
        skill=skill or None,
        skills=SKILLS,
        unsupported=unsupported,
    )


if __name__ == "__main__":
    app.run(host="127.0.0.1", port=5000, debug=True)
