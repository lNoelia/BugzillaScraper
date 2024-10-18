import requests
import os
from dotenv import load_dotenv

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
    result_file='data/filtered_issues_'+resolution+'_'+status+'.txt'

    with open(result_file, 'w') as res_file:
        #Header of result file
        res_file.write("ID,Summary,Status,Resolution,Classification\n")
        try:
            with open(file, 'r',encoding='utf-8') as f:
                lines = f.readlines()
                print(f"Total lines in input file: {len(lines)}")  # Debugging: print total number of lines
                for line in lines[1:]:
                    base_url = os.getenv('MAIN_PAGE') + '/rest/bug/' + line.split(',')[0]
                    ##Base information
                    response = requests.get(base_url)
                    if response.status_code == 200:
                        data = response.json()
                        bug = data.get('bugs', [])[0]
                        res_file.write(f"{bug.get('id')},{bug.get('summary')},{bug.get('status')},{bug.get('resolution')},{bug.get('classification')}\n")
                    else:
                        print("Failed to get bug information. Please check the URL provided on the configuration file.")
        except FileNotFoundError:
            print(f"Error: The file '{file}' was not found.")
        except Exception as e:
            print(f"An error occurred while reading the file: {e}")


            
    print(f"Filtered issues saved in {result_file}")
