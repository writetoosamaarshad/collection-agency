# Collection Agency

This project is a collection agency management system built with Django. It provides functionalities for managing accounts, loading data from CSV files, and querying accounts using various filters.

## Requirements

- Python 3.10

## Setup Instructions

### Step 1: Create a Virtual Environment

Before starting, it's recommended to create a virtual environment to manage dependencies.

```bash
python3.10 -m venv venv
```

### Step 2: Activate the Virtual Environment

Activate the environment you just created.

- On Windows:

```bash
venv\Scripts\activate
```

- On macOS/Linux:

```bash
source venv/bin/activate
```

### Step 3: Install Requirements

Install all the necessary packages using the provided `requirements.txt` file.

```bash
pip install -r requirements.txt
```

## Data Loading

You can load data into the system in two ways:

### Option 1: Using a Custom Management Command

Run the following command, replacing `[file_path]`, `[agency_name]`, and `[agency_reference_no]` with your actual values:

```bash
python manage.py load_data "[file_path]" "[agency_name]" "[agency_reference_no]"
```

### Option 2: Using the `/upload-csv/` API Endpoint

You can also use the `/upload-csv/` API endpoint to upload your data via a POST request.

## Utilizing API Endpoints

You can query accounts using various filters through the `/accounts/` endpoint. Below is a summary of the parameters you can use:

### Query Parameters

- **min_balance**: Filter accounts with a minimum balance.
- **max_balance**: Filter accounts with a maximum balance.
- **consumer_name**: Filter accounts by consumer name.
- **status**: Filter accounts by status. Available values: `IN_COLLECTION`, `PAID_IN_FULL`, `INACTIVE`.
- **page**: Paginate the results by specifying a page number.

### Example API Call

```http
GET /accounts/?min_balance=100&max_balance=500&status=IN_COLLECTION
```

### API Response Example

```json
{
  "count": 1,
  "next": null,
  "previous": null,
  "results": [
    {
      "client": {...},
      "consumer": {...},
      "balance": {...},
      "status": "IN_COLLECTION"
    }
  ]
}
```

You can interact with and explore these endpoints using the provided Swagger documentation.

## Running Tests

You can run the test suite to ensure everything is working as expected.

```bash
python manage.py test
```
