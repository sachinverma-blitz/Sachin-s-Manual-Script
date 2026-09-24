# Copilot Instructions for this repository

- This repository is a collection of standalone Python automation scripts, not a packaged application.
- Each script lives in the repo root and is usually run directly with the local virtualenv Python interpreter:
  - `/Users/sachinverma/Documents/Scripts/.venv/bin/python <script.py>`
- Many filenames include spaces and uppercase letters, for example `FO ACCESS.py`, `delete FO user.py`, and `trip complete.py`.

## Common repo patterns

- Scripts commonly read local Excel or JSON input files and write Excel output files.
  - `pandas.read_excel(...)`, `DataFrame.to_excel(...)`
  - Examples: `pickup.py`, `tripcomplete.py`, `bank2.py`, `FO ACCESS.py`
- HTTP integration is central.
  - Most scripts use `requests` with `Content-Type: application/json`.
  - Headers frequently include custom fields such as `rider_id`, `name`, `orgId`, `pool`, or `x-api-key`.
  - Example endpoint style: `https://...execute-api.ap-south-1.amazonaws.com/V1/...`
- Typical work steps in code:
  1. read input file
  2. normalize row data / build payload
  3. send API call
  4. print status
  5. save results locally

## Development guidance

- Preserve the existing script-first model; do not turn this into a package project unless the user asks.
- Keep changes minimal and consistent with the current style: top-level execution, row loops, print status, save Excel outputs.
- Use `requests.post(..., headers=headers, json=payload)` or `requests.get(..., params=params)` as in existing files.
- When adding new automation, mirror the payload and header conventions used by the matching existing script.

## Environment and dependencies

- The repo uses a `.venv` virtual environment with Python 3.9.6.
- Installed packages include `requests`, `pandas`, `openpyxl`, `numpy`.
- There is no visible `requirements.txt` or package manifest in this repo.

## What to avoid

- Avoid assuming a full backend/service architecture or tests are present.
- Avoid renaming files or paths unless explicitly requested, especially because many filenames contain spaces.
- Avoid introducing unrelated frameworks or packaging layers.

## When uncertain

- Ask for the intended input file, the exact API endpoint URL, and whether the change should stay as a standalone script.
- If extending an existing workflow, choose the most closely related file as the template:
  - `tripcomplete.py` / `trip_complete.py` for trip completion flows
  - `pickup.py` for pickup + trip actions
  - `FO ACCESS.py` / `foaccess.py` for front-office access operations
  - `bank2.py` for bank detail batch fetches
