# Web Performance Monitoring System

This project monitors the web performance of a specified URL using **Google PageSpeed Insights API**, stores results in **Google BigQuery**, and sends email notifications if performance metrics degrade.

---

## Features

- Fetches performance metrics for both **Desktop** and **Mobile** devices.
- Collects metrics such as:
  - Performance Score (%)
  - Cumulative Layout Shift (CLS)
  - First Contentful Paint (FCP)
  - Time to First Byte (TTFB)
  - Interaction to Next Paint (INP)
  - Largest Contentful Paint (LCP)
  - Total Blocking Time (TBT)
  - Speed Index (SI)
- Runs multiple iterations (default: 3) and calculates averages.
- Stores results in **BigQuery** tables:
  - `page_speed_desktop_tbl`
  - `page_speed_mobile_tbl`
- Sends email alerts if any metrics worsen compared to the previous run.
- Can be deployed as a **Google Cloud Function**.

---

## Prerequisites

- Python 3.8+
- Google Cloud Project with:
  - BigQuery API enabled
  - Service account with access to BigQuery
- PageSpeed Insights API key
- SMTP credentials for sending email

---

## Environment Variables

Set the following environment variables:

| Variable | Description |
|----------|-------------|
| `API_KEY` | Google PageSpeed Insights API key |
| `SENDER_EMAIL` | Email address to send notifications from |
| `RECEIVER_EMAIL` | Recipient email address |
| `EMAIL_PASSWORD` | Password or app-specific password for the sender email |
| `SMTP_SERVER` | SMTP server address (e.g., `smtp.gmail.com`) |
| `SMTP_PORT` | SMTP server port (e.g., `587`) |

---

## Installation

1. Clone the repository:

```bash
git clone https://github.com/Raheesraha/Web-Performance-Monitoring-System.git
cd Web-Performance-Monitoring-System

