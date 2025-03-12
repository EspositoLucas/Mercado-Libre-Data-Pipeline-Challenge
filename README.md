# Mercado Libre Data Pipeline Challenge

This project implements a data pipeline using Apache Airflow to gather information about items published on the MercadoLibre ecommerce site, store it in a database, and send email alerts based on specific criteria.

## Table of Contents
- [Mercado Libre Data Pipeline Challenge](#mercado-libre-data-pipeline-challenge)
  - [Table of Contents](#table-of-contents)
  - [Introduction](#introduction)
  - [Prerequisites](#prerequisites)
  - [Project Structure](#project-structure)
  - [Configuration](#configuration)
  - [Database Setup](#database-setup)
  - [Running the Pipeline](#running-the-pipeline)
  - [Pipeline Tasks](#pipeline-tasks)
  - [Email Alerts](#email-alerts)
  - [Limitations and Future Improvements](#limitations-and-future-improvements)

## Introduction

This project implements an automated data pipeline that:
- Fetches product data from MercadoLibre's API
- Stores the data in a PostgreSQL database
- Sends email alerts for high-value inventory items
- Uses Apache Airflow for orchestration

## Prerequisites

- Docker and Docker Compose
- Python 3.8+
- MercadoLibre API credentials
- Gmail account with App Password for email notifications

## Project Structure

```
Mercado-Libre-Data-Pipeline-Challenge/
├── dags/
│   └── postgres.py              # Main Airflow DAG definition
├── plugins/
│   ├── operators/
│   │   └── PostgresFileOperator.py  # Custom Airflow operator
│   └── tmp/
│       ├── api_fetch.py         # MercadoLibre API interaction script
│       └── file.tsv            # Temporary data storage
├── docker-compose.yaml          # Docker services configuration
├── .env                        # Environment variables
└── README.md
```

## Configuration

1. Create a `.env` file with the following variables:
```
BEARER_TOKEN=your_mercadolibre_token
EMAIL_PASSWORD=your_gmail_app_password
```

2. Set up Airflow variables in the UI:
- `project_path`: `/opt/airflow`
- `BEARER_TOKEN`: Your MercadoLibre API token
- `EMAIL_PASSWORD`: Your Gmail app password

## Database Setup

The project uses PostgreSQL for data storage. Tables are created automatically by the pipeline.

Schema:
```sql
create table if not exists mercado_libre_data (
    id varchar(100), 
    site_id varchar(100), 
    title varchar(100),
    price varchar(100),
    available_quantity varchar(100),
    thumbnail varchar(100),
    created_date varchar(100),
    primary key(id, created_date)
);
```

## Running the Pipeline

1. Start the Docker containers:
```bash
docker-compose up -d
```

2. Access Airflow UI:
```
http://localhost:8080
```
Default credentials:
- Username: airflow
- Password: airflow

3. Enable the "postgres" DAG in the Airflow UI

## Pipeline Tasks

The pipeline consists of four main tasks:

1. `create_table`: Creates the PostgreSQL table if it doesn't exist
2. `consulting_API`: Fetches data from MercadoLibre API
3. `insert_data`: Loads the fetched data into PostgreSQL
4. `reading_data`: Queries high-value items and sends email alerts

Task Dependencies:
```
create_table >> consulting_API >> insert_data >> reading_data
```

## Email Alerts

The pipeline sends email alerts for items with:
- Available quantity > 0
- Total value (price × quantity) > 7,000,000

Email Configuration:
- Sender: Gmail account with App Password
- Protocol: SMTP over SSL (port 465)
- Content: List of matching items with details

## Limitations and Future Improvements

While the core functionality of the data pipeline has been implemented, there are certain limitations and areas for future improvements:

- **Bonus Features:** The bonus features, such as deployability, unit/E2E testing, additional metadata, data lineage information, and automation, have not been implemented in this version of the project.

- **Code Quality:** The project code can be further improved for readability, maintainability, and adherence to best coding practices. Consider refactoring and optimizing the code as needed.

- **Enhancements:** Explore opportunities for enhancing the functionality of the data pipeline, adding more features, or integrating with additional services.

- **User Documentation:** Provide comprehensive user documentation for setting up and configuring the pipeline, making it more accessible to a wider audience.

