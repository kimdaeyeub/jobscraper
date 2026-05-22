# JobScraper

스킬 키워드로 채용 공고를 검색하는 프로젝트입니다.

Berlin Startup Jobs, We Work Remotely, Web3 Career에서 **40개 개발 스킬**의 공고를 미리 수집해 GitHub Pages에서 보여줍니다.

## 데모

https://kimdaeyeub.github.io/jobscraper/

## 로컬 실행

```bash
uv sync
uv run python main.py
```

브라우저에서 http://127.0.0.1:5000 접속

## 데이터 갱신

```bash
uv run python generate_data.py
```

40개 스킬의 공고를 다시 수집해 `docs/data/`에 JSON으로 저장합니다.  
GitHub Actions가 매주 자동으로 갱신합니다.

## 지원 스킬 (40개)

Python, JavaScript, TypeScript, Java, Go, Rust, PHP, Ruby, Swift, Kotlin, React, Vue, Angular, Node.js, Next.js, Django, Flask, FastAPI, Spring, Rails, SQL, PostgreSQL, MongoDB, Redis, AWS, Docker, Kubernetes, Terraform, DevOps, Machine Learning, Data Science, Android, iOS, Flutter, GraphQL, Elasticsearch, Linux, Git, HTML, CSS
