# Reservation Slot Monitor

A lightweight Python monitor that checks appointment availability through the Calendesk API and sends a notification by creating a GitHub Issue when a new slot appears.

The project is designed to run automatically with GitHub Actions, so it does not require a local machine to stay online.

## Features

- Checks reservation availability automatically
- Uses the Calendesk API directly
- Detects newly available time slots
- Avoids duplicate notifications
- Creates a GitHub Issue for every newly detected slot
- Can trigger GitHub email notifications
- Runs automatically with GitHub Actions
- No browser automation required
- No private email credentials stored in the repository

## How it works

The monitor follows a simple flow:

```text
GitHub Actions
      ↓
Calendesk API
      ↓
Check available slots
      ↓
Any new slot?
   ↓        ↓
  No       Yes
   ↓        ↓
 Finish   Check if already reported
              ↓
          Create GitHub Issue
              ↓
       GitHub notification / email
```

The GitHub Issue contains the detected appointment date and time together with a link to the reservation page.

## Project structure

```text
Reservation_Scraper/
├── .github/
│   └── workflows/
│       └── monitor.yml
├── .gitignore
├── calendesk.py
├── main.py
├── notifier.py
├── requirements.txt
└── README.md
```

### `calendesk.py`

Handles communication with the Calendesk API and retrieves appointment slot data.

### `main.py`

Contains the main application logic:

- retrieves appointment data
- extracts available slots
- checks whether a slot has already been reported
- triggers notifications for newly detected slots

### `notifier.py`

Uses the GitHub REST API to:

- check previously created Issues
- prevent duplicate notifications
- create a new Issue when a new appointment slot is detected

### `monitor.yml`

GitHub Actions workflow responsible for running the monitor automatically.

## Installation

Clone the repository:

```bash
git clone https://github.com/Karol-Polak/Reservation_Scraper.git
cd Reservation_Scraper
```

Create a virtual environment:

```bash
python -m venv venv
```

Activate it.

macOS / Linux:

```bash
source venv/bin/activate
```

Windows:

```bash
venv\Scripts\activate
```

Install dependencies:

```bash
pip install -r requirements.txt
```

Run the monitor locally:

```bash
python main.py
```

If there are currently no available appointments, the output will look similar to:

```text
INFO | Sprawdzam dostępne terminy...
INFO | Brak wolnych terminów.
```

## GitHub Actions

The monitor is configured to run automatically using GitHub Actions.

Example schedule:

```yaml
on:
  schedule:
    - cron: "*/10 * * * *"
```

This schedules the monitor approximately every 10 minutes.

GitHub Actions scheduled workflows are not guaranteed to start at the exact scheduled second and may occasionally be delayed.

The workflow can also be triggered manually from:

```text
Repository → Actions → Reservation Monitor → Run workflow
```

## Notifications

When a new appointment slot is detected, the application creates a GitHub Issue.

Example:

```text
🚨 Available appointment: 2026-10-15 12:30
```

The Issue body contains the appointment details and a link to the reservation page.

To receive email notifications:

1. Watch the repository on GitHub.
2. Enable notifications for Issues.
3. Enable email notifications in your GitHub notification settings.

## Duplicate prevention

Each detected slot is stored inside the generated Issue using an invisible marker:

```html
<!-- SLOT_ID:2026-10-15|12:30 -->
```

Before creating a new notification, the application checks existing Issues.

If the slot has already been reported, no new Issue is created.

This prevents repeated notifications when the same appointment remains available across multiple monitoring runs.

## Requirements

- Python 3.12+
- `requests`
- GitHub Actions

Dependencies are defined in:

```text
requirements.txt
```

## Security

The project does not require storing personal email credentials.

GitHub Actions provides the built-in:

```text
GITHUB_TOKEN
```

which is used to create Issues through the GitHub API.

The workflow requires:

```yaml
permissions:
  contents: read
  issues: write
```

Sensitive data such as `.env` files should never be committed.

Example `.gitignore`:

```gitignore
.env
venv/
.venv/
__pycache__/
.idea/
.DS_Store
```

## Disclaimer

This project is intended as a personal availability monitoring tool.

It does not automatically book appointments and does not attempt to bypass authentication, access controls, rate limits, or other protections.

The monitor only checks availability exposed by the reservation system.

Use responsibly and respect the terms and conditions of the reservation service.

## License

This project is provided for educational and personal-use purposes.
