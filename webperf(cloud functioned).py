import functions_framework
import requests
import random
import time
import re
import os
from google.cloud import bigquery
from google.oauth2 import service_account
import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from datetime import datetime

# Your API Key
api_key = os.getenv('API_KEY')
# api_key = 'AIzaSyBnM6Dowr2CsZ_wVc_EoWpqKS1-yut0TTo'


# URL to test
url = 'https://danubehome.com'


project_id = "analytics-350507"  

# Setup BigQuery client with the specified project ID
client = bigquery.Client(project="analytics-350507")


dataset_id = "analytics-350507.pagespeed"

 

def fetch_performance_data(device_type):  # Accept device_type argument
    # Generate a unique random parameter to bypass caching
    random_param = f"t={random.randint(1, 1000000)}"
    
    # Construct the endpoint based on device_type (either desktop or mobile)
    if device_type == "desktop":
        endpoint = f'https://www.googleapis.com/pagespeedonline/v5/runPagespeed?url={url}&key={api_key}&{random_param}&strategy=desktop'
    elif device_type == "mobile":
        endpoint = f'https://www.googleapis.com/pagespeedonline/v5/runPagespeed?url={url}&key={api_key}&{random_param}&strategy=mobile'
    else:
        raise ValueError(f"Unknown device type: {device_type}")
    
    retries = 3  # Number of retries
    for attempt in range(retries):
        try:
            # Fetch data
            response = requests.get(endpoint)
            if response.status_code == 200:
                data = response.json()
                
                # Extract relevant performance scores
                performance = data['lighthouseResult']['categories']['performance']['score'] * 100
                cls = data['lighthouseResult']['audits']['cumulative-layout-shift']['displayValue']
                fcp = data['lighthouseResult']['audits']['first-contentful-paint']['displayValue']
                ttfb = data['lighthouseResult']['audits']['server-response-time']['displayValue']
                inp = data['lighthouseResult']['audits']['interactive']['displayValue']
                lcp = data['lighthouseResult']['audits']['largest-contentful-paint']['displayValue']
                tbt = data['lighthouseResult']['audits']['total-blocking-time']['displayValue']
                si = data['lighthouseResult']['audits']['speed-index']['displayValue']
                
                # Clean up TTFB to remove "Root document took"
                ttfb_cleaned = re.sub(r'Root document took ', '', ttfb)
                
                # Return the results
                return {
                    device_type: {
                        'performance_score': performance,
                        'cls': cls,
                        'fcp': fcp,
                        'ttfb': ttfb_cleaned,
                        'inp': inp,
                        'lcp': lcp,
                        'tbt': tbt,
                        'si': si
                    }
                }
            else:
                print(f"Error fetching {device_type} data: {response.status_code}")
                time.sleep(2)  # Wait before retrying
        except requests.exceptions.RequestException as e:
            print(f"Error occurred: {e}")
            time.sleep(2)  # Wait before retrying
    
    return None  # Return None if all retries fail

# Initialize lists to store the values from each iteration for Desktop and Mobile
def executePageSpeed ():
    # Desktop Metrics
    desktop_performance_scores = []
    desktop_cls_values = []
    desktop_fcp_values = []
    desktop_ttfb_values = []
    desktop_inp_values = []
    desktop_lcp_values = []
    desktop_tbt_values = []
    desktop_si_values = []

    # Mobile Metrics
    mobile_performance_scores = []
    mobile_cls_values = []
    mobile_fcp_values = []
    mobile_ttfb_values = []
    mobile_inp_values = []
    mobile_lcp_values = []
    mobile_tbt_values = []
    mobile_si_values = []





    # Run 3 iterations and collect results for both Desktop and Mobile
    for iteration in range(1, 4):
        print(f"\nIteration {iteration}:")


        # Fetch the performance data for Desktop
        desktop_results = fetch_performance_data("desktop")  # Pass 'desktop' as argument
        
        # Fetch the performance data for Mobile
        mobile_results = fetch_performance_data("mobile")  # Pass 'mobile' as argument
        
        if desktop_results:
            # Print the results for Desktop for the current iteration
            print("\nDesktop Performance Results:")
            print(f"Performance: {desktop_results['desktop']['performance_score']}%")
            print(f"CLS: {desktop_results['desktop']['cls']}")
            print(f"FCP: {desktop_results['desktop']['fcp']}")
            print(f"TTFB: {desktop_results['desktop']['ttfb']}")
            print(f"INP: {desktop_results['desktop']['inp']}")
            print(f"LCP: {desktop_results['desktop']['lcp']}")
            print(f"TBT: {desktop_results['desktop']['tbt']}")
            print(f"Speed Index: {desktop_results['desktop']['si']}")
            
            # Append the Desktop results to the respective lists
            desktop_performance_scores.append(desktop_results['desktop']['performance_score'])
            desktop_cls_values.append(float(desktop_results['desktop']['cls'].split()[0]))  # Assuming CLS is a numeric value with a unit
            desktop_fcp_values.append(float(desktop_results['desktop']['fcp'].split()[0]))  # Assuming FCP is a numeric value with a unit
            ttfb_cleaned_value = desktop_results['desktop']['ttfb'].split()[0].replace(',', '')  # Remove commas
            desktop_ttfb_values.append(float(ttfb_cleaned_value))  # Convert to float
            desktop_inp_values.append(float(desktop_results['desktop']['inp'].split()[0]))  # Assuming INP is a numeric value with a unit
            desktop_lcp_values.append(float(desktop_results['desktop']['lcp'].split()[0]))  # Assuming LCP is a numeric value with a unit
            desktop_tbt_values.append(float(desktop_results['desktop']['tbt'].split()[0].replace(',', '')))  # Remove commas from TBT
            desktop_si_values.append(float(desktop_results['desktop']['si'].split()[0].replace(',', '')))  # Remove commas from Speed Index
        else:
            print("Failed to retrieve Desktop data for this iteration.")
        
        if mobile_results:
            # Print the results for Mobile for the current iteration
            print("\nMobile Performance Results:")
            print(f"Performance: {mobile_results['mobile']['performance_score']}%")
            print(f"CLS: {mobile_results['mobile']['cls']}")
            print(f"FCP: {mobile_results['mobile']['fcp']}")
            print(f"TTFB: {mobile_results['mobile']['ttfb']}")
            print(f"INP: {mobile_results['mobile']['inp']}")
            print(f"LCP: {mobile_results['mobile']['lcp']}")
            print(f"TBT: {mobile_results['mobile']['tbt']}")
            print(f"Speed Index: {mobile_results['mobile']['si']}")
            
            # Append the Mobile results to the respective lists
            mobile_performance_scores.append(mobile_results['mobile']['performance_score'])
            mobile_cls_values.append(float(mobile_results['mobile']['cls'].split()[0]))  # Assuming CLS is a numeric value with a unit
            mobile_fcp_values.append(float(mobile_results['mobile']['fcp'].split()[0]))  # Assuming FCP is a numeric value with a unit
            ttfb_cleaned_value = mobile_results['mobile']['ttfb'].split()[0].replace(',', '')  # Remove commas
            mobile_ttfb_values.append(float(ttfb_cleaned_value))  # Convert to float
            mobile_inp_values.append(float(mobile_results['mobile']['inp'].split()[0]))  # Assuming INP is a numeric value with a unit
            mobile_lcp_values.append(float(mobile_results['mobile']['lcp'].split()[0]))  # Assuming LCP is a numeric value with a unit
            mobile_tbt_values.append(float(mobile_results['mobile']['tbt'].split()[0].replace(',', '')))  # Remove commas from TBT
            mobile_si_values.append(float(mobile_results['mobile']['si'].split()[0].replace(',', '')))  # Remove commas from Speed Index
        else:
            print("Failed to retrieve Mobile data for this iteration.")
        
        # Delay of 10 seconds between iterations
        if iteration < 3:  # Don't delay after the last iteration
            print("\nWaiting for 10 seconds before the next iteration...\n")
            

    # Round the values to 2 decimal places for Desktop and Mobile performance data

    # For Desktop metrics
    desktop_performance_scores = [round(x, 2) for x in desktop_performance_scores]
    desktop_cls_values = [round(x, 2) for x in desktop_cls_values]
    desktop_fcp_values = [round(x, 2) for x in desktop_fcp_values]
    desktop_ttfb_values = [round(x, 2) for x in desktop_ttfb_values]
    desktop_inp_values = [round(x, 2) for x in desktop_inp_values]
    desktop_lcp_values = [round(x, 2) for x in desktop_lcp_values]
    desktop_tbt_values = [round(x, 2) for x in desktop_tbt_values]  # Round TBT values
    desktop_si_values = [round(x, 2) for x in desktop_si_values]    # Round Speed Index values

    # For Mobile metrics
    mobile_performance_scores = [round(x, 2) for x in mobile_performance_scores]
    mobile_cls_values = [round(x, 2) for x in mobile_cls_values]
    mobile_fcp_values = [round(x, 2) for x in mobile_fcp_values]
    mobile_ttfb_values = [round(x, 2) for x in mobile_ttfb_values]
    mobile_inp_values = [round(x, 2) for x in mobile_inp_values]
    mobile_lcp_values = [round(x, 2) for x in mobile_lcp_values]
    mobile_tbt_values = [round(x, 2) for x in mobile_tbt_values]  # Round TBT values
    mobile_si_values = [round(x, 2) for x in mobile_si_values]    # Round Speed Index values

    # Calculate the averages of all the metrics for Desktop and round them to 2 decimal places
    average_desktop_performance = round(sum(desktop_performance_scores) / len(desktop_performance_scores), 2) if desktop_performance_scores else 0
    average_desktop_cls = round(sum(desktop_cls_values) / len(desktop_cls_values), 2) if desktop_cls_values else 0
    average_desktop_fcp = round(sum(desktop_fcp_values) / len(desktop_fcp_values), 2) if desktop_fcp_values else 0
    average_desktop_ttfb = round(sum(desktop_ttfb_values) / len(desktop_ttfb_values), 2) if desktop_ttfb_values else 0
    average_desktop_inp = round(sum(desktop_inp_values) / len(desktop_inp_values), 2) if desktop_inp_values else 0
    average_desktop_lcp = round(sum(desktop_lcp_values) / len(desktop_lcp_values), 2) if desktop_lcp_values else 0
    average_desktop_tbt = round(sum(desktop_tbt_values) / len(desktop_tbt_values), 2) if desktop_tbt_values else 0  # Average for TBT
    average_desktop_si = round(sum(desktop_si_values) / len(desktop_si_values), 2) if desktop_si_values else 0  # Average for Speed Index

    # Calculate the averages of all the metrics for Mobile and round them to 2 decimal places
    average_mobile_performance = round(sum(mobile_performance_scores) / len(mobile_performance_scores), 2) if mobile_performance_scores else 0
    average_mobile_cls = round(sum(mobile_cls_values) / len(mobile_cls_values), 2) if mobile_cls_values else 0
    average_mobile_fcp = round(sum(mobile_fcp_values) / len(mobile_fcp_values), 2) if mobile_fcp_values else 0
    average_mobile_ttfb = round(sum(mobile_ttfb_values) / len(mobile_ttfb_values), 2) if mobile_ttfb_values else 0
    average_mobile_inp = round(sum(mobile_inp_values) / len(mobile_inp_values), 2) if mobile_inp_values else 0
    average_mobile_lcp = round(sum(mobile_lcp_values) / len(mobile_lcp_values), 2) if mobile_lcp_values else 0
    average_mobile_tbt = round(sum(mobile_tbt_values) / len(mobile_tbt_values), 2) if mobile_tbt_values else 0  # Average for TBT
    average_mobile_si = round(sum(mobile_si_values) / len(mobile_si_values), 2) if mobile_si_values else 0  # Average for Speed Index

    # Print the averages for Desktop
    print("\nAverages of the Desktop performance metrics over the 3 iterations:")
    print(f"Average Desktop Performance Score: {average_desktop_performance:.2f}%")
    print(f"Average Desktop CLS: {average_desktop_cls:.2f}")
    print(f"Average Desktop FCP: {average_desktop_fcp:.2f} s")  # FCP in seconds
    print(f"Average Desktop TTFB: {average_desktop_ttfb:.2f} ms")  # TTFB in milliseconds
    print(f"Average Desktop INP: {average_desktop_inp:.2f} s")  # INP in seconds
    print(f"Average Desktop LCP: {average_desktop_lcp:.2f} s")  # LCP in seconds
    print(f"Average Desktop TBT: {average_desktop_tbt:.2f} ms")
    print(f"Average Desktop Speed Index: {average_desktop_si:.2f} s")

    # Print the averages for Mobile
    print("\nAverages of the Mobile performance metrics over the 3 iterations:")
    print(f"Average Mobile Performance Score: {average_mobile_performance:.2f}%")
    print(f"Average Mobile CLS: {average_mobile_cls:.2f}")
    print(f"Average Mobile FCP: {average_mobile_fcp:.2f} s")  # FCP in seconds
    print(f"Average Mobile TTFB: {average_mobile_ttfb:.2f} ms")  # TTFB in milliseconds
    print(f"Average Mobile INP: {average_mobile_inp:.2f} s")  # INP in seconds
    print(f"Average Mobile LCP: {average_mobile_lcp:.2f} s")  # LCP in seconds
    print(f"Average Mobile TBT: {average_mobile_tbt:.2f} ms")
    print(f"Average Mobile Speed Index: {average_mobile_si:.2f} s")


   
    mobile_table_id = f"{dataset_id}.page_speed_mobile_tbl"
    desktop_table_id = f"{dataset_id}.page_speed_desktop_tbl"

    # Prepare the data to insert into BigQuery for Mobile
    created_at = datetime.now().strftime('%Y-%m-%d %H:%M:%S')

    mobile_rows_to_insert = [
        {
            "created_at": created_at,
            "iteration_1": {
                "performance_score": mobile_performance_scores[0],
                "cls": mobile_cls_values[0],
                "fcp": mobile_fcp_values[0],
                "ttfb": mobile_ttfb_values[0],
                "inp": mobile_inp_values[0],
                "lcp": mobile_lcp_values[0],
                "tbt": mobile_tbt_values[0],
                "si": mobile_si_values[0]
            },
            "iteration_2": {
                "performance_score": mobile_performance_scores[1],
                "cls": mobile_cls_values[1],
                "fcp": mobile_fcp_values[1],
                "ttfb": mobile_ttfb_values[1],
                "inp": mobile_inp_values[1],
                "lcp": mobile_lcp_values[1],
                "tbt": mobile_tbt_values[1],
                "si": mobile_si_values[1]
            },
            "iteration_3": {
                "performance_score": mobile_performance_scores[2],
                "cls": mobile_cls_values[2],
                "fcp": mobile_fcp_values[2],
                "ttfb": mobile_ttfb_values[2],
                "inp": mobile_inp_values[2],
                "lcp": mobile_lcp_values[2],
                "tbt": mobile_tbt_values[2],
                "si": mobile_si_values[2]
            },
            "average": {
                "performance_score": average_mobile_performance,
                "cls": average_mobile_cls,
                "fcp": average_mobile_fcp,
                "ttfb": average_mobile_ttfb,
                "inp": average_mobile_inp,
                "lcp": average_mobile_lcp,
                "tbt": average_mobile_tbt,  # Include average TBT
                "si": average_mobile_si     # Include average Speed Index
            }
        }
    ]

    # Insert data into BigQuery for Mobile
    errors_mobile = client.insert_rows_json(mobile_table_id, mobile_rows_to_insert)

    # Check for errors and output accordingly for Mobile
    if errors_mobile:
        print("Error inserting data into Mobile table in BigQuery:", errors_mobile)
    else:
        print("Data inserted successfully into Mobile table in BigQuery.")

    # Prepare the data to insert into BigQuery for Desktop
    desktop_rows_to_insert = [
        {
            "created_at": created_at,
            "iteration_1": {
                "performance_score": desktop_performance_scores[0],
                "cls": desktop_cls_values[0],
                "fcp": desktop_fcp_values[0],
                "ttfb": desktop_ttfb_values[0],
                "inp": desktop_inp_values[0],
                "lcp": desktop_lcp_values[0],
                "tbt": desktop_tbt_values[0],
                "si": desktop_si_values[0]
            },
            "iteration_2": {
                "performance_score": desktop_performance_scores[1],
                "cls": desktop_cls_values[1],
                "fcp": desktop_fcp_values[1],
                "ttfb": desktop_ttfb_values[1],
                "inp": desktop_inp_values[1],
                "lcp": desktop_lcp_values[1],
                "tbt": desktop_tbt_values[1],
                "si": desktop_si_values[1]
            },
            "iteration_3": {
                "performance_score": desktop_performance_scores[2],
                "cls": desktop_cls_values[2],
                "fcp": desktop_fcp_values[2],
                "ttfb": desktop_ttfb_values[2],
                "inp": desktop_inp_values[2],
                "lcp": desktop_lcp_values[2],
                "tbt": desktop_tbt_values[2],
                "si": desktop_si_values[2]
            },
            "average": {
                "performance_score": average_desktop_performance,
                "cls": average_desktop_cls,
                "fcp": average_desktop_fcp,
                "ttfb": average_desktop_ttfb,
                "inp": average_desktop_inp,
                "lcp": average_desktop_lcp,
                "tbt": average_desktop_tbt,  # Include average TBT
                "si": average_desktop_si     # Include average Speed Index
            }
        }
    ]

    # Insert data into BigQuery for Desktop
    errors_desktop = client.insert_rows_json(desktop_table_id, desktop_rows_to_insert)

    # Check for errors and output accordingly for Desktop
    if errors_desktop:
        print("Error inserting data into Desktop table in BigQuery:", errors_desktop)
    else:
        print("Data inserted successfully into Desktop table in BigQuery.")
    

# Function to fetch the latest and previous averages for both Mobile and Desktop
def fetch_averages_from_bigquery():
    # Define the query to get the latest and previous row for Mobile data
    mobile_query = f"""
        SELECT *
        FROM `{dataset_id}.page_speed_mobile_tbl`
        ORDER BY created_at DESC
        LIMIT 2
    """
    
    # Define the query to get the latest and previous row for Desktop data
    desktop_query = f"""
        SELECT *
        FROM `{dataset_id}.page_speed_desktop_tbl`
        ORDER BY created_at DESC
        LIMIT 2
    """
    
    # Execute the queries
    try:
        mobile_query_job = client.query(mobile_query)
        desktop_query_job = client.query(desktop_query)
        
        # Fetch the results for both queries
        mobile_result = mobile_query_job.result()
        desktop_result = desktop_query_job.result()
        
        # Convert the result to list of rows
        mobile_rows = list(mobile_result)
        desktop_rows = list(desktop_result)
        
        # Initialize variables to store the latest and previous averages
        latest_mobile_averages = None
        previous_mobile_averages = None
        latest_desktop_averages = None
        previous_desktop_averages = None
        
        # Check if we have at least 2 rows in Mobile data
        if len(mobile_rows) >= 2:
            latest_mobile_row = mobile_rows[0]
            previous_mobile_row = mobile_rows[1]
            
            # Extract averages for Mobile
            latest_mobile_averages = {
                "performance_score": latest_mobile_row["average"]["performance_score"],
                "cls": latest_mobile_row["average"]["cls"],
                "fcp": latest_mobile_row["average"]["fcp"],
                "ttfb": latest_mobile_row["average"]["ttfb"],
                "inp": latest_mobile_row["average"]["inp"],
                "lcp": latest_mobile_row["average"]["lcp"],
                "tbt": latest_mobile_row["average"]["tbt"],
                "si": latest_mobile_row["average"]["si"],
                "created_at": latest_mobile_row["created_at"].strftime('%d/%m/%Y %H:%M:%S')
            }

            previous_mobile_averages = {
                "performance_score": previous_mobile_row["average"]["performance_score"],
                "cls": previous_mobile_row["average"]["cls"],
                "fcp": previous_mobile_row["average"]["fcp"],
                "ttfb": previous_mobile_row["average"]["ttfb"],
                "inp": previous_mobile_row["average"]["inp"],
                "lcp": previous_mobile_row["average"]["lcp"],
                "tbt": previous_mobile_row["average"]["tbt"],
                "si": previous_mobile_row["average"]["si"],
                "created_at": previous_mobile_row["created_at"].strftime('%d/%m/%Y %H:%M:%S')
            }

        # Check if we have at least 2 rows in Desktop data
        if len(desktop_rows) >= 2:
            latest_desktop_row = desktop_rows[0]
            previous_desktop_row = desktop_rows[1]
            
            # Extract averages for Desktop
            latest_desktop_averages = {
                "performance_score": latest_desktop_row["average"]["performance_score"],
                "cls": latest_desktop_row["average"]["cls"],
                "fcp": latest_desktop_row["average"]["fcp"],
                "ttfb": latest_desktop_row["average"]["ttfb"],
                "inp": latest_desktop_row["average"]["inp"],
                "lcp": latest_desktop_row["average"]["lcp"],
                "tbt": latest_desktop_row["average"]["tbt"],
                "si": latest_desktop_row["average"]["si"],
                "created_at": latest_desktop_row["created_at"].strftime('%d/%m/%Y %H:%M:%S')
            }

            previous_desktop_averages = {
                "performance_score": previous_desktop_row["average"]["performance_score"],
                "cls": previous_desktop_row["average"]["cls"],
                "fcp": previous_desktop_row["average"]["fcp"],
                "ttfb": previous_desktop_row["average"]["ttfb"],
                "inp": previous_desktop_row["average"]["inp"],
                "lcp": previous_desktop_row["average"]["lcp"],
                "tbt": previous_desktop_row["average"]["tbt"],
                "si": previous_desktop_row["average"]["si"],
                "created_at": previous_desktop_row["created_at"].strftime('%d/%m/%Y %H:%M:%S')
            }

        # Return both mobile and desktop averages
        return (latest_mobile_averages, previous_mobile_averages, latest_desktop_averages, previous_desktop_averages)

    except Exception as e:
        print(f"Error fetching averages: {e}")
        return None, None, None, None  # Return None if there's an error
    

def send_email(latest_mobile_averages, previous_mobile_averages, latest_desktop_averages, previous_desktop_averages):
    # Function to determine the color based on the comparison
    def compare_metrics(latest, previous, metric_name, unit=None):
        if metric_name == 'performance_score':
            if latest < previous:  # Performance score should not go up
                return 'red', f"{metric_name}: {latest}% (Should go up)"
            elif latest > previous:  # Performance score improved
                return 'green', f"{metric_name}: {latest}% (dropped)"
            else:  # No change
                return 'default', f"{metric_name}: {latest}% (No change)"
        
        # For all other metrics
        if latest > previous:  # If the value went up, it's a violation (red)
            return 'red', f"{metric_name}: {latest} {unit} (Should not go up)"
        elif latest < previous:  # If the value improved, it's a good change (green)
            return 'green', f"{metric_name}: {latest} {unit} (Improved)"
        else:  # If no change (default)
            return 'default', f"{metric_name}: {latest} {unit} (No change)"
    
    # Define units for each metric
    metric_units = {
        'performance_score': '%',  # Performance score in percentage
        'cls': '',                 # CLS is a dimensionless score
        'fcp': 's',                # Seconds
        'ttfb': 'ms',              # Milliseconds
        'lcp': 's',                # Seconds
        'tbt': 'ms',               # Milliseconds
        'si': 's'                  
    }
    
    # Email content
    email_content = f"""
<html>
<head>
    <style>
        table {{border-collapse: collapse; width: 100%;}}
        th, td {{border: 1px solid black; padding: 8px; text-align: left;}}
        th {{background-color: #f2f2f2;}}
        th {{ text-transform: uppercase; }} 
        .red {{color: red;}}
        .green {{color: green;}}
        .default {{color: black;}}
    </style>
</head>
<body>
    <h3>Performance Metrics Report [Mobile]</h3>
    <table>
        <tr>
            <th>Metric</th>
            <th>Latest Average Value [{latest_mobile_averages['created_at']}]</th>
            <th>Previous Average Value [{previous_mobile_averages['created_at']}]</th>
        </tr>
    """
    
    # List of metrics to compare
    metrics = [
        'performance_score', 'cls', 'fcp', 'ttfb', 'lcp', 'tbt', 'si'
    ]
    
    # Variable to check if any violation occurred
    send_email_flag = False

    # Compare mobile metrics
    for metric in metrics:
        unit = metric_units.get(metric, '')  # Get the unit for each metric
        color, result = compare_metrics(latest_mobile_averages[metric], previous_mobile_averages[metric], metric, unit)
        if color == 'red':  # Violation found
            send_email_flag = True
        
        email_content += f"""
        <tr>
            <td>{metric.replace('_', ' ').title()}</td>
            <td class="{color}">{latest_mobile_averages[metric]} {unit}</td>
            <td class="default">{previous_mobile_averages[metric]} {unit}</td>
        </tr>
        """
    
    email_content += f"""
    </table>
    <h3>Performance Metrics Report [Desktop]</h3>
    <table>
        <tr>
            <th>Metric</th>
            <th>Latest Average Value [{latest_desktop_averages['created_at']}]</th>
            <th>Previous Average Value [{previous_desktop_averages['created_at']}]</th>
        </tr>
    """
    
    # Compare desktop metrics
    for metric in metrics:
        unit = metric_units.get(metric, '')  # Get the unit for each metric
        color, result = compare_metrics(latest_desktop_averages[metric], previous_desktop_averages[metric], metric, unit)
        if color == 'red':  # Violation found
            send_email_flag = True
        
        email_content += f"""
        <tr>
            <td>{metric.replace('_', ' ').title()}</td>
            <td class="{color}">{latest_desktop_averages[metric]} {unit}</td>
            <td class="default">{previous_desktop_averages[metric]} {unit}</td>
        </tr>
        """

    email_content += """
    </table>
</body>
</html>
"""

    # If no violations found, return without sending email
    if not send_email_flag:
        print("No violations found, email will not be sent.")
        return

    # Email setup
    sender_email = os.getenv("SENDER_EMAIL")
    receiver_email = os.getenv("RECEIVER_EMAIL")
    password = os.getenv("EMAIL_PASSWORD")  # Use an app password if using Gmail
    # sender_email = 'noreply@danubehome.com'
    # receiver_email = 'raheesraha31@gmail.com'
    # password = 'Mission@700m2023$$'

    # Create a MIME object
    msg = MIMEMultipart()
    msg['From'] = sender_email
    msg['To'] = receiver_email
    msg['Subject'] = "Performance Metric Change Report"
    
    # Attach the email content
    msg.attach(MIMEText(email_content, 'html'))
    
    # Send the email via SMTP server
    SMTP_SERVER = os.getenv('SMTP_SERVER')
    SMTP_PORT = os.getenv('SMTP_PORT')
    try:
        with smtplib.SMTP(SMTP_SERVER,SMTP_PORT) as server:
            server.starttls()
            server.login(sender_email, password)
            server.sendmail(sender_email, receiver_email, msg.as_string())
        print("Email sent successfully.")
    except Exception as e:
        print(f"Failed to send email: {e}")


# Fetch the latest and previous averages from BigQuery


@functions_framework.http
def my_http_function(request):
    executePageSpeed() 
    latest_mobile_averages, previous_mobile_averages, latest_desktop_averages, previous_desktop_averages = fetch_averages_from_bigquery()

    if latest_mobile_averages and previous_mobile_averages and latest_desktop_averages and previous_desktop_averages:
        # Send the email with the averages
        send_email(latest_mobile_averages, previous_mobile_averages, latest_desktop_averages, previous_desktop_averages)
                   
    else:
        print("Not enough data to compare the latest and previous metrics.")
    return f"execution finished"