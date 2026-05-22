const ARROW_ICON = `<svg xmlns="http://www.w3.org/2000/svg" width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.5" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true"><path d="M7 17 17 7"/><path d="M7 7h10v10"/></svg>`;

const SEARCH_ICON = `<svg xmlns="http://www.w3.org/2000/svg" width="24" height="24" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><circle cx="11" cy="11" r="8"/><path d="m21 21-4.3-4.3"/></svg>`;

const BRIEFCASE_ICON = `<svg xmlns="http://www.w3.org/2000/svg" width="24" height="24" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><rect width="20" height="14" x="2" y="7" rx="2" ry="2"/><path d="M16 21V5a2 2 0 0 0-2-2h-4a2 2 0 0 0-2 2v16"/></svg>`;

let manifest = null;

function escapeHtml(value) {
  return String(value)
    .replaceAll("&", "&amp;")
    .replaceAll("<", "&lt;")
    .replaceAll(">", "&gt;")
    .replaceAll('"', "&quot;")
    .replaceAll("'", "&#39;");
}

function findSkill(skillId) {
  if (!manifest) return null;
  return manifest.skills.find((skill) => skill.id === skillId) || null;
}

function renderSkillTags() {
  const container = document.getElementById("skill-tags");
  if (!manifest || !container) return;

  container.innerHTML = manifest.skills
    .map(
      (skill) =>
        `<a href="?skill=${encodeURIComponent(skill.id)}" data-skill="${escapeHtml(skill.id)}">${escapeHtml(skill.label)}</a>`,
    )
    .join("");

  container.querySelectorAll("[data-skill]").forEach((link) => {
    link.addEventListener("click", onSkillTagClick);
  });
}

function renderEmptyState(title, message, icon) {
  return `
    <div class="empty-state">
      <div class="empty-icon" aria-hidden="true">${icon}</div>
      <h3>${escapeHtml(title)}</h3>
      <p>${escapeHtml(message)}</p>
    </div>
  `;
}

function renderJobCard(job) {
  const description = job.description
    ? `<p class="job-desc">${escapeHtml(job.description)}</p>`
    : "";

  return `
    <article class="job-card">
      <div class="job-card-top">
        <p class="job-title">${escapeHtml(job.title)}</p>
        <a
          class="job-arrow"
          href="${escapeHtml(job.link)}"
          target="_blank"
          rel="noopener noreferrer"
          aria-label="View ${escapeHtml(job.title)} job posting"
        >${ARROW_ICON}</a>
      </div>
      <p class="job-company">${escapeHtml(job.company_name)}</p>
      ${description}
    </article>
  `;
}

function renderResults(skill, jobs, meta) {
  if (!skill) {
    return renderEmptyState(
      "Choose a skill to get started",
      "Select one of 40 supported skills below.",
      BRIEFCASE_ICON,
    );
  }

  const label = meta?.label || skill;
  const header = `
    <div class="results-header">
      <h2>${jobs.length ? `Results for ${escapeHtml(label)}` : `No results for ${escapeHtml(label)}`}</h2>
      ${jobs.length ? `<p class="results-count"><strong>${jobs.length}</strong> jobs found</p>` : ""}
    </div>
  `;

  if (!jobs.length) {
    return (
      header +
      renderEmptyState(
        "No results found",
        "This skill is supported but has no cached listings right now.",
        SEARCH_ICON,
      )
    );
  }

  const updated = meta?.updated_at
    ? `<p class="results-updated">Data updated ${new Date(meta.updated_at).toLocaleDateString()}</p>`
    : "";

  return header + updated + `<div class="job-list">${jobs.map(renderJobCard).join("")}</div>`;
}

async function loadManifest() {
  const response = await fetch("./data/manifest.json");
  if (!response.ok) {
    throw new Error("Could not load skill manifest");
  }
  manifest = await response.json();
  renderSkillTags();
  populateSkillSelect();
}

async function loadJobs(skill) {
  const resultsEl = document.getElementById("results");

  if (!skill) {
    resultsEl.innerHTML = renderResults("", []);
    return;
  }

  const knownSkill = findSkill(skill);
  if (!knownSkill) {
    resultsEl.innerHTML = renderEmptyState(
      "Unsupported skill",
      `"${skill}" is not in the 40 supported skills. Pick one from the list below.`,
      SEARCH_ICON,
    );
    return;
  }

  resultsEl.innerHTML = `<div class="loading-state">Loading ${escapeHtml(knownSkill.label)} jobs...</div>`;

  try {
    const response = await fetch(`./data/${encodeURIComponent(skill)}.json`);
    if (!response.ok) {
      throw new Error(`Missing data file for ${skill}`);
    }

    const data = await response.json();
    resultsEl.innerHTML = renderResults(data.skill, data.jobs || [], data);
  } catch (error) {
    resultsEl.innerHTML = `
      <div class="error-state">
        <h3>Could not load jobs</h3>
        <p>Cached data for this skill is unavailable.</p>
      </div>
    `;
    console.error(error);
  }
}

function populateSkillSelect() {
  const select = document.getElementById("skill-select");
  if (!select || !manifest) return;

  select.innerHTML =
    `<option value="">Select a skill</option>` +
    manifest.skills
      .map(
        (skill) =>
          `<option value="${escapeHtml(skill.id)}">${escapeHtml(skill.label)}</option>`,
      )
      .join("");
}

function getSkillFromUrl() {
  return (new URLSearchParams(window.location.search).get("skill") || "").trim();
}

function setSkillInUrl(skill) {
  const url = new URL(window.location.href);
  if (skill) {
    url.searchParams.set("skill", skill);
  } else {
    url.searchParams.delete("skill");
  }
  window.history.replaceState({}, "", url);
}

function setSelectedSkill(skill) {
  const select = document.getElementById("skill-select");
  if (select) select.value = skill;
}

function onSkillTagClick(event) {
  event.preventDefault();
  const nextSkill = event.currentTarget.dataset.skill;
  setSelectedSkill(nextSkill);
  setSkillInUrl(nextSkill);
  loadJobs(nextSkill);
}

async function init() {
  const form = document.getElementById("search-form");
  const select = document.getElementById("skill-select");

  try {
    await loadManifest();
  } catch (error) {
    document.getElementById("results").innerHTML = `
      <div class="error-state">
        <h3>Could not load skills</h3>
        <p>Job data has not been generated yet.</p>
      </div>
    `;
    console.error(error);
    return;
  }

  const skill = getSkillFromUrl();
  setSelectedSkill(skill);
  loadJobs(skill);

  form.addEventListener("submit", (event) => {
    event.preventDefault();
    const nextSkill = select.value.trim();
    setSkillInUrl(nextSkill);
    loadJobs(nextSkill);
  });

  select.addEventListener("change", () => {
    const nextSkill = select.value.trim();
    setSkillInUrl(nextSkill);
    loadJobs(nextSkill);
  });
}

document.addEventListener("DOMContentLoaded", init);
