# 🧠 AuraSight: AI-Powered Strategic Intelligence Pipeline

![Python](https://img.shields.io/badge/Python-3.10%2B-blue)
![License](https://img.shields.io/badge/License-MIT-green)
![Status](https://img.shields.io/badge/Status-Active-success)

**AuraSight** is an automated strategic intelligence tool designed to scrape, analyze, and structure corporate data from unstructured web content. It leverages **Asynchronous Web Scraping** and **Large Language Models (LLMs)** via OpenRouter to generate actionable insights about companies, exporting the results into a structured Excel database.

## 🚀 Key Features

* **🕵️‍♂️ Asynchronous Scouting:** Uses `Crawl4AI` for high-speed, non-blocking web scraping of target corporate websites.
* **🧠 Multi-Model Intelligence:** Integrates with **OpenRouter** to access state-of-the-art LLMs (Claude 3.5 Sonnet, Llama 3, etc.) for processing raw HTML and extracting semantic meaning.
* **🛡️ Structured Data Enforcement:** Utilizes `Instructor` and `Pydantic` to force LLMs to output strict JSON schemas, eliminating hallucinated formats.
* **💾 Incremental Database:** Features a built-in duplicate prevention system. It checks the existing Excel database before scanning, ensuring only new targets are processed (Cost & Time efficient).
* **📊 Automated Reporting:** Exports findings (Company Summary, Hiring Status, Key Products, etc.) directly to an Excel file (`strategic_report.xlsx`).
* **🧩 Modular Architecture:** Clean, maintainable codebase separated into specialized modules (Scraper, Analyzer, Utils).

## 🛠️ Tech Stack

* **Core Logic:** Python 3.11+
* **Web Scraping:** `crawl4ai` (Async/Await pattern)
* **LLM Gateway:** `OpenRouter` (Universal API)
* **Structured Output:** `instructor` & `pydantic`
* **Data Manipulation:** `Pandas`

## 📂 Project Structure

```bash
AuraSight/
├── main.py               # Manages the pipeline workflow
├── scraper.py            # Handles async web scraping logic
├── analyzer.py           # Manages LLM interaction & Pydantic models
├── utils.py              # Handles database (Excel) & file operations
├── requirements.txt      # Dependency list
├── .env                  # API Keys (Not included in repo)
├── .gitignore            # Security rules
└── strategic_report.xlsx # Output database (Generated automatically)
