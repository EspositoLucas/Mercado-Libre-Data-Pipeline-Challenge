# MercadoLibre Data Pipeline Challenge

This project implements a data pipeline using Apache Airflow to gather information about items published on the MercadoLibre ecommerce site, store it in a database, and send email alerts based on specific criteria.

## Table of Contents
1. [Introduction](#introduction)
2. [Prerequisites](#prerequisites)
3. [Project Structure](#project-structure)
4. [Configuration](#configuration)
5. [Airflow DAG](#airflow-dag)
6. [Database Setup](#database-setup)
7. [Running the Pipeline](#running-the-pipeline)
8. [Email Alerts](#email-alerts)
9. [Limitations and Future Improvements](#limitations-and-future-improvements)

## Introduction

This project aims to create a data pipeline that interacts with the MercadoLibre public API to gather item information, save it in a database, and send email alerts based on specific criteria. The pipeline is implemented using Apache Airflow, and the tasks are organized into a Directed Acyclic Graph (DAG).

The 

## Prerequisites

Before running the project, ensure you have the following installed:

- [Apache Airflow](https://airflow.apache.org/)
- [Python](https://www.python.org/) (version specified in `requirements.txt`)
- [Docker](https://www.docker.com/) (optional for database setup)
- [Database (e.g., PostgreSQL)](https://www.postgresql.org/) for storing item information

## Project Structure

```
mercadolibre_data_pipeline/
|-- dags/
|   |-- mercado_pipeline.py
|-- scripts/
|   |-- gather_data.py
|   |-- send_alerts.py
|-- tests/
|   |-- test_gather_data.py
|   |-- test_send_alerts.py
|-- requirements.txt
|-- README.md
```

- **dags/**: Contains the Airflow DAG definition.
- **scripts/**: Contains the Python scripts for gathering data and sending alerts.
- **tests/**: Contains unit and end-to-end tests.
- **requirements.txt**: Lists project dependencies.

## Configuration

Adjust the configuration files in the `scripts/` directory to include your MercadoLibre API key, database connection details, and email settings.

## Airflow DAG

The Airflow DAG (`dags/mercado_pipeline.py`) is responsible for orchestrating the data pipeline. It defines tasks for gathering data and sending alerts, specifying their dependencies and execution order.

## Database Setup

Set up your database by running the necessary SQL scripts found in the `database/` directory. Alternatively, use Docker to run a database container.

## Running the Pipeline

1. Start the Airflow web server: `airflow webserver -p 8080`
2. Start the Airflow scheduler: `airflow scheduler`

Visit `http://localhost:8080` to access the Airflow web UI and trigger the DAG manually or wait for the scheduled run.

## Email Alerts

Email alerts are sent when the data gathering task runs and detects items with a total value exceeding $7,000,000. Configure your email settings in the `send_alerts.py` script.

## Limitations and Future Improvements

While the core functionality of the data pipeline has been implemented, there are certain limitations and areas for future improvements:

- **Bonus Features:** The bonus features, such as deployability, unit/E2E testing, additional metadata, data lineage information, and automation, have not been implemented in this version of the project.

- **Code Quality:** The project code can be further improved for readability, maintainability, and adherence to best coding practices. Consider refactoring and optimizing the code as needed.

- **Enhancements:** Explore opportunities for enhancing the functionality of the data pipeline, adding more features, or integrating with additional services.

- **User Documentation:** Provide comprehensive user documentation for setting up and configuring the pipeline, making it more accessible to a wider audience.

Feel free to contribute to the project by addressing these limitations and implementing new features. Your contributions are welcome!

