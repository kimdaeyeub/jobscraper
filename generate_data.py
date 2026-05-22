import json
import logging
from datetime import UTC, datetime
from pathlib import Path

from jobs import fetch_jobs
from skills import SKILLS

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

DATA_DIR = Path(__file__).parent / "docs" / "data"


def generate_all():
    DATA_DIR.mkdir(parents=True, exist_ok=True)
    manifest = {
        "updated_at": datetime.now(UTC).isoformat(),
        "skills": [],
    }

    for skill in SKILLS:
        skill_id = skill["id"]
        logger.info("Scraping jobs for %s", skill_id)
        jobs = fetch_jobs(skill_id)
        payload = {
            "skill": skill_id,
            "label": skill["label"],
            "count": len(jobs),
            "updated_at": datetime.now(UTC).isoformat(),
            "jobs": jobs,
        }
        output_path = DATA_DIR / f"{skill_id}.json"
        output_path.write_text(json.dumps(payload, ensure_ascii=False, indent=2))
        manifest["skills"].append(
            {
                "id": skill_id,
                "label": skill["label"],
                "count": len(jobs),
            }
        )
        logger.info("Saved %d jobs to %s", len(jobs), output_path)

    manifest_path = DATA_DIR / "manifest.json"
    manifest_path.write_text(json.dumps(manifest, ensure_ascii=False, indent=2))
    logger.info("Wrote manifest with %d skills", len(manifest["skills"]))


if __name__ == "__main__":
    generate_all()
