import datetime
import subprocess

# Set the log file name
log_file_name = 'daily_run_log.txt'

# Open the log file for appending
with open(log_file_name, 'a') as log_file:
    # Get the current date and time
    now = datetime.datetime.now()

    # Write the date and time to the log file
    log_file.write('Script run at {:%Y-%m-%d %H:%M:%S}\n'.format(now))

    # Run the daily scripts
    subprocess.run(['python','gmail_parse.py'])
    
    # Write the end of the log entry to the log file
    log_file.write('Script run complete.\n\n')