import requests
import os
from dotenv import load_dotenv
import csv
import json
import time
from io import StringIO

load_dotenv()


def fetch_bugzilla_issues(base_url, resolution, status, limit_per_query=0):
    start = 0
    
    result_file = f'data/list_issues_{resolution}_{status}.csv'
    with open(result_file, 'w', newline='', encoding='utf-8') as csvfile:
        csvwriter = None
        
        while True:
            # Build the full URL with pagination parameters
            url = f"{base_url}/buglist.cgi?action=wrap&query_format=advanced&ctype=csv&human=1&limit={limit_per_query}&offset={start}"
            
            if resolution != 'TOTAL':
                url += f'&resolution={resolution}'
            if status != 'TOTAL':
                url += f'&status={status}'
            if os.getenv('CLASSIFICATION'):
                url += f'&classification={os.getenv('CLASSIFICATION')}'
            if os.getenv('PRODUCT'):
                url += f'&product={os.getenv('PRODUCT')}'
            if os.getenv('COMPONENT'):
                url += f'&component={os.getenv('COMPONENT')}'
            
            print(f"Getting list of issues from {url}...")
            
            response = requests.get(url)
            response.raise_for_status()
            
            # Read the CSV content
            csv_content = StringIO(response.text)
            csvreader = csv.reader(csv_content)
            
            # Write the headers only once
            if start == 0:
                headers = next(csvreader)
                csvwriter = csv.writer(csvfile)
                csvwriter.writerow(headers)
            else:
                next(csvreader)  # Skip headers for subsequent batches
            
            rows = list(csvreader)
            
            if not rows:
                break
            
            # Write the rows to the CSV file
            csvwriter.writerows(rows)

            if start == 0 and limit_per_query == 0:
                # Set the limit per query based on the number of rows in the first batch
                limit_per_query = len(rows)
                print(f"Determined limit per query: {limit_per_query}")

            if len(rows) < limit_per_query:
                break
            
            start += limit_per_query

def get_list_issues(base_url, resolution, status):
    print(f"Getting list of issues from {base_url} with resolution={resolution} and status={status}...")
    
    fetch_bugzilla_issues(base_url, resolution, status)
    
    result_file = f'data/list_issues_{resolution}_{status}.csv'
    print(f"List of issues saved in {result_file}")

def get_filtered_issues(resolution,status):
    file = 'data/list_issues_'+resolution+'_'+status+'.csv'
    result_file='data/filtered_issues_'+resolution+'_'+status+'.csv'

    ## Headers for all request:
    headers = {
        'Accept': 'application/json'  # Especifica que esperas una respuesta en JSON
    }
    with open(result_file, 'w', encoding='utf-8',newline='', errors='surrogateescape') as res_file:
        writer = csv.writer(res_file, escapechar='\\', quoting=csv.QUOTE_MINIMAL)
        #Header of result file
        ## bug_url, id, alias, classification, component, product, version, platform, op_sys, status, resolution, depends_on, dupe_of, blocks, groups, flags, severity, priority, deadline, target_milestone, creator, creator_detail , creation_time, assigned_to, assigned_to_detail,cc ,cc_detail,is_cc_acessible, is_confirmed, is_open, is_creator_accessible, summary, description, url(something related to bug),whiteboard, keywords, see_also, last_change_time, qa_contact
        header = [
            "Issue URL", "ID", "Alias", "Classification", "Component", "Product", "Version", "Platform", "Op sys", 
            "Status", "Resolution", "Depends on", "Dupe of", "Blocks", "Groups", "Flags", "Severity", "Priority", 
            "Deadline", "Target Milestone", "Creator", "Creator Detail", "Creation time", "Assigned to", 
            "Assigned to detail", "CC", "CC detail", "Is CC accessible", "Is confirmed", "Is open", 
            "Is creator accessible", "Summary", "Description", "URL", "Whiteboard", "Keywords", "See also", 
            "Last change time", "QA contact","History/Activity Log", "Comments", "Attachments"
        ]

        writer.writerow(header)

        try:
            with open(file, 'r',encoding='utf-8', errors='surrogateescape') as f:
                lines = f.readlines()
                print(f"Total lines in input file: {len(lines)}")  # Debugging: print total number of lines
                for line_number, line in enumerate(lines[1:], start=1):
                    try:
                        parts = line.strip().split(',')
                        if len(parts) < 1:
                            raise ValueError(f"Line {line_number} does not have the expected format: {line}")

                        bug_id = parts[0].strip().strip()
                        if not bug_id.isdigit():
                            raise ValueError(f"Extracted bug ID is not a digit on line {line_number}: {bug_id}")
                        base_url = os.getenv('MAIN_PAGE') + '/rest/bug/' + bug_id

                        ## Base information
                        response = requests.get(base_url, headers=headers)
                        if response.status_code == 200:
                            data = response.json()
                            bug = data.get('bugs', [])[0]
                            bug_url = os.getenv('MAIN_PAGE') + 'show_bug.cgi?id=' + str(bug.get('id'))
                            row = [
                                bug_url, bug.get('id'), bug.get('alias'), bug.get('classification'), bug.get('component'), 
                                bug.get('product'), bug.get('version'), bug.get('platform'), bug.get('op_sys'), 
                                bug.get('status'), bug.get('resolution'), bug.get('depends_on'), bug.get('dupe_of'), 
                                bug.get('blocks'), bug.get('groups'), bug.get('flags'), bug.get('severity'), 
                                bug.get('priority'), bug.get('deadline'), bug.get('target_milestone'), bug.get('creator'), 
                                bug.get('creator_detail'), bug.get('creation_time'), bug.get('assigned_to'), 
                                bug.get('assigned_to_detail'), bug.get('cc'), bug.get('cc_detail'), 
                                bug.get('is_cc_accessible'), bug.get('is_confirmed'), bug.get('is_open'), 
                                bug.get('is_creator_accessible'), bug.get('summary'), "BUG_DESCRIPTION", bug.get('url'), 
                                bug.get('whiteboard'), bug.get('keywords'), bug.get('see_also'), bug.get('last_change_time'), 
                                bug.get('qa_contact')
                            ]
                        else:
                            print(f"Failed to get bug information for bug ID {bug_id}. Please check the URL provided on the configuration file.")
                            continue #Skip to next issue
                        
                        ## Bug HISTORY (Activity log)
                        history_url = base_url + '/history'
                        response = requests.get(history_url, headers=headers)
                        if response.status_code == 200:
                            history_data = response.json()
                            # Get all the bug history
                            history = history_data.get('bugs', {})[0].get("history", {})
                            # Convert history to JSON string
                            history_json = json.dumps(history)
                            row.append(history_json)
                        else:
                            print(f"Failed to get bug history for bug ID {bug_id} on line {line_number}.")
                            row.append("")
                        
                        ## Comments and description
                        comment_url = base_url + '/comment'
                        response = requests.get(comment_url, headers=headers)
                        if response.status_code == 200:
                            comment_data = response.json()
                            # Get all the bug comments
                            bug_comments = comment_data.get('bugs', {}).get(bug_id, {})
                            description = ""
                            bug_comments_split = bug_comments.get('comments', [])
                            # Find the description (count=0)
                            for comment in bug_comments_split:
                                if comment.get('count') == 0:
                                    description = comment.get('text').replace('\n', '\\n').replace('\r', '\\r').replace('\"', '\\\"')
                            # Convert bug_comments to JSON string
                            bug_comments_json = json.dumps(bug_comments)
                            row[32] = description
                            row.append(bug_comments_json)
                        else:
                            print(f"Failed to get bug comments for bug ID {bug_id} on line {line_number}.")
                            row.append("")

                        ## Attachments
                        attachment_url = base_url + '/attachment'
                        response = requests.get(attachment_url, headers=headers)
                        if response.status_code == 200:
                            attachment_data = response.json()
                            # Get all the bug attachments
                            attachments = attachment_data.get('bugs', {}).get(bug_id, [])
                            # Convert attachments to JSON string
                            attachments_json = json.dumps(attachments)
                            row.append(attachments_json)
                        else:
                            print(f"Failed to get bug attachments for bug ID {bug_id}. Please try again.")
                            row.append("")
                    
                        #Finally, we write all the information for this bug in the result file
                        writer.writerow(row)
                    #time.sleep(0.1)## Avoiding to be blocked by the server
                    except ValueError as val_err:
                        print(f"Value error on line {line_number}: {val_err}")
                    except requests.exceptions.HTTPError as http_err:
                        print(f"HTTP error occurred for bug ID {bug_id} on line {line_number}: {http_err}")
                    except requests.exceptions.RequestException as req_err:
                        print(f"Request exception occurred for bug ID {bug_id} on line {line_number}: {req_err}")
                    except Exception as e:
                        print(f"An unexpected error occurred on line {line_number}: {e}")
                    
        except FileNotFoundError:
            print(f"Error: The file '{file}' was not found.")
        except Exception as e:
            print(f"An error occurred while reading the file: {e}")
    print(f"Filtered issues saved in {result_file}")
