from dotenv import load_dotenv
import os

from src.utils import get_resolution_options, get_status_options, choose_resolution_status, ask_user_input_y_or_n
from src.scraper import get_list_issues, get_dataset_issues

#Load DotEnv
load_dotenv()

def main():
    url = os.getenv('MAIN_PAGE')
    if(url.endswith('/')):
        url = url[:-1]
    field_url = url + '/rest/field/bug'
    resolution_options = get_resolution_options(field_url)
    status_options = get_status_options(field_url)
    resolution_status = choose_resolution_status(resolution_options, status_options)
    resolution = resolution_options[int(resolution_status[0])-1]
    status = status_options[int(resolution_status[1])-1]

    print("Resolution and Status selected:"+ resolution+ " and "+ status)
    result_file='data/list_issues_'+resolution+'_'+status+'.csv'

    # Check if we already have the list of issues 
    if os.path.exists(result_file):
        get_list_again = ask_user_input_y_or_n()
        if get_list_again == 'y':
            get_list_issues(url,resolution, status)
    else:
        get_list_issues(url,resolution, status)
    
    # Obtain the dataset of issues    
    get_dataset_issues(resolution, status)
    print("The list of issues has been saved in the file: "+result_file)
if __name__ == '__main__':
    main()