import requests
import os
from dotenv import load_dotenv
import csv
import json
import time

load_dotenv()

def get_list_issues(url,resolution,status):
    url = url + '/buglist.cgi?action=wrap&query_format=advanced'
    if(resolution != 'TOTAL'):
        url = url + '&resolution='+resolution
    if(status != 'TOTAL'):
        url = url + '&status='+status
    if(os.getenv('CLASSIFICATION') != ''):
        url = url + '&classification='+os.getenv('CLASSIFICATION')
    if(os.getenv('PRODUCT') != ''):
        url = url + '&product='+os.getenv('PRODUCT')
    if(os.getenv('COMPONENT') != ''):
        url = url + '&component='+os.getenv('COMPONENT')
    url = url + '&ctype=csv&human=1'
    result_file='data/list_issues_'+resolution+'_'+status+'.txt'
    response = requests.get(url)
    if response.status_code == 200:
        with open(result_file, 'wb') as file:
            file.write(response.content)
        print(f"List of issues saved in {result_file})")
    else:
        print("Failed to get issues. Please check the URL provided on the configuration file.")

def get_filtered_issues(resolution,status):
    file = 'data/list_issues_'+resolution+'_'+status+'.txt'
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
                for line in lines[1:]:
                    bug_id = line.split(',')[0]
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
                        print("Failed to get bug information. Please check the URL provided on the configuration file.")

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
                        print("Failed to get bug history. Please try again.")
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
                        print("Failed to get bug comments. Please try again.")
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
                        print("Failed to get bug attachments. Please try again.")
                        row.append("")
                    
                    #Finally, we write all the information for this bug in the result file
                    writer.writerow(row)
                    time.sleep(0.1)## Avoiding to be blocked by the server
        except FileNotFoundError:
            print(f"Error: The file '{file}' was not found.")
        except Exception as e:
            print(f"An error occurred while reading the file: {e}")


            
    print(f"Filtered issues saved in {result_file}")
