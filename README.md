# PropScout | Unlocking the Potential of Property Investment

`PropScout` is a real estate investment app designed to assist budding property investors with identifying potentially lucrative markets as well provide them with a framework for systematic real estate investment deal analysis.

## Project Overview

PropScout is a real estate investment app that helps property investors identify promising markets and offers a systematic framework for real estate deal analysis. It leverages data extraction, storage, and analysis to streamline the property analysis workflow and enable users to make informed investment decisions. Building on previous projects, PropScout focuses on collecting and storing property listings to create a comprehensive database for analysis, with plans to incorporate additional features in the future.

PropScout builds upon the foundation established in two key projects: [analysing_south_african_property_markets](https://github.com/CoenMeintjes/analysing_south_african_property_markets) and [property_investment_analysis_framework](https://github.com/CoenMeintjes/property_investment_analysis_framework). These projects have laid the groundwork for future feature improvements and serve as valuable references for the development of PropScout.

## Features

- **Gmail Parsing**: Extract property listing notifications from a Gmail inbox using the Gmail API. The `gmail_parse.py` script locates these notifications, accesses the property listings, and saves the links and listing webpages in a SQLite database.

- **Property Data Extraction**: The `extract_prop_specs.py` script extracts relevant property listing information from the stored webpages. The extracted data is then saved in JSON format in the same SQLite database.

- **Data Analysis and Exploration**: The `notebook.ipynb` Jupyter Notebook provides a platform for exploring and analyzing the JSON data stored in the database. It offers various data manipulation, visualization, and analysis techniques to gain insights into property markets and make informed investment decisions.

## Installation and Setup

To get started with `PropScout`, follow these steps:

1. Clone the repository: `git clone https://github.com/your-username/prop_scout.git`

2. Install the required Python packages: `pip install -r requirements.txt`

3. Set up Gmail API access:
   - Follow the instructions in the [Gmail API Python Quickstart](https://developers.google.com/gmail/api/quickstart/python) to enable the API and download the `credentials.json` file.
   - Place the `credentials.json` file in the project directory.

4. Run the scripts:
   - Execute `gmail_parse.py` to extract property listing data from Gmail messages and store it in the SQLite database.
   - Run `extract_prop_specs.py` to parse the stored webpages and extract property information in JSON format.

5. Open and run the `notebook.ipynb` Jupyter Notebook to perform data analysis and exploration.

## Usage Instructions

### Script 1 | `gmail_parse.py`

The script `gmail_parse.py` is designed to extract relevant information from Gmail messages and store them in a SQLite database for further analysis. For more information regarding the Gmail API: https://developers.google.com/gmail/api/quickstart/python

Follow the instructions below to use the `gmail_parse.py` script effectively:

1. Make sure you have the necessary dependencies installed. You can install them by running the following command:

   ```python
   pip install -r requirements.txt
   ```

2. Set up the required credentials:
   - Create a file named `credentials.json` with your Google API credentials. Make sure it is in the same directory as the script.
   
   ```python
   {
    "installed": {
        "client_id": "...",
        "project_id": "...",
        "auth_uri": "https://accounts.google.com/o/oauth2/auth",
        "token_uri": "https://oauth2.googleapis.com/token",
        "auth_provider_x509_cert_url": "https://www.googleapis.com/oauth2/v1/certs",
        "client_secret": "...",
        "redirect_uris": ["http://localhost"]
      }
   }
   ````
   - If you have already authorized the script before, make sure the `token.json` file is present in the same directory. Otherwise, the script will prompt you to authorize it and generate the `token.json` file.

3. Run the script:
   ```python
   python gmail_parse.py
   ```

   The script `gmail_parse.py` performs the following steps:

   1. **Connects to the Gmail API:** The script establishes a connection to the Gmail API using the provided credentials. This allows it to access your Gmail account and retrieve the necessary data.

   2. **Retrieves messages:** The script retrieves a list of messages from the specified Gmail label or folder. It searches for messages that contain property analysis alerts.

   3. **Extracts property listing URLs:** For each message, the script extracts property listing URLs. It searches for URLs within the message content, specifically looking for links related to property listings.

   4. **Stores URLs in the SQLite database:** The extracted property listing URLs are stored in the SQLite database. The database table named `Urls` is used for this purpose. If the table doesn't exist, the script creates it automatically.

   5. **Fetches listing pages:** The script follows each URL and retrieves the corresponding property listing page. It downloads the HTML content of each listing page.

   6. **Stores listing pages in the SQLite database:** The downloaded HTML content of the listing pages is stored in the SQLite database. Each listing page is associated with its respective URL in the `Urls` table.

   By performing these steps, the script allows you to gather property listing URLs and their corresponding HTML pages for further processing and analysis.

   Note: The script uses the `BeautifulSoup` library to parse HTML content and the `base64` library to decode encoded email bodies.

4. Check the database:
   - The script creates a SQLite database file named `property_analysis_db.sqlite` in the same directory.
   - You can access the database using any SQLite-compatible tool or integrate it into your own analysis workflow.

### Script 2 | `extract_prop_specs.py`

This script, `extract_prop_specs.py`, extracts property specifications from HTML content stored in the SQLite database and stores them in a JSON format in the database itself. It also maintains an updated `all_properties.json` file with the complete list of properties' JSON data.

1. Make sure you have the necessary dependencies installed. You can install them by running the following command:

   ```python
   pip install -r requirements.txt
   ```

2. Ensure that you have the `property_analysis_db.sqlite` file in the same directory as the script. 

3. Run the script using the following command:
   ```
   python extract_prop_specs.py
   ```

4. The script will prompt you to enter the number of properties you want to process. Enter the desired number and press Enter. If you want to process all available properties, leave the input blank and press Enter. `need to update this in the script`

5. The script will fetch HTML content from the SQLite database and parse it to extract relevant property specifications.

6. The extracted property specifications will be stored in a JSON format in the `json` column of the `Urls` table for each property in the SQLite database. Additionally, a complete list of all properties' JSON data will be kept updated in the `all_properties.json` file. If the file does not already exist, the script will create it and append the data to it.

7. `improve how the script ends this is not good` The final JSON data will be printed on the console. You can also find the updated `all_properties.json` file in the script's directory.

Note: This script assumes that you have already populated the SQLite database with HTML content. If you haven't done so, please make sure to run the appropriate script `gmail_parse.py` to populate the database before running this script.

### Script 3 | `daily_script.py`

This script is designed to be used with Task Scheduler to automate the process of running the PropScout scripts and update the database at a chosen desired interval.

1. Set Up the Script:
   - Customize the log file name (optional):
     - Modify the `log_file_name` variable in the script to set a desired name for the log file.
   - Save the changes to the script file.

2. Configure Task Scheduler:
   - Open Task Scheduler on your system.
   - Create a new task or import an existing task.
   - Configure the task settings, including the desired schedule for script execution.
   - In the "Actions" tab, add a new action to "Start a program".
   - Specify the path to the Python executable as the program/script, e.g., `C:\Python\python.exe`.
   - Enter the script file name as the argument, e.g., `daily_script.py`.
   - Set the working directory to the location of the script file.
   - Save the task configuration.

3. Execution:
   - Task Scheduler will automatically run the script based on the configured schedule.
   - The script will open the log file specified and append the log entries to it.
   - The current date and time will be written to the log file.
   - The script will execute the daily scripts by running the `gmail_parse.py` script using the `subprocess.run()` function.
   - Once the daily scripts have finished running, the end of the log entry will be written to the log file.
   - The script execution is now complete.

4. Verification:
   - Check the log file (`daily_run_log.txt`) to view the log entries and verify the script's execution time.
   - Review the database to ensure that it has been updated as expected.

Note: Ensure that you have the necessary permissions and access rights to write to the log file, execute the required scripts, and configure Task Scheduler accordingly.

## Data Analysis

*Provide an overview of the types of data analysis being performed in the Jupyter Notebook. still need to develop this feature*

## Contributing

Contributions to PropScout are welcome! If you encounter any issues or have suggestions for improvements, please create an issue or submit a pull request.