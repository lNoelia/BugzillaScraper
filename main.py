from dotenv import load_dotenv
import os

from src.utils import get_resolution_options, get_status_options, choose_resolution_status, ask_user_input_y_or_n
from src.scraper import get_list_issues, get_filtered_issues

#Load DotEnv
load_dotenv()

def main():
 while True:
        try:
            # Prompt the user to enter a number
            number = int(input("Enter a number from 1 to 4 (or 0 to exit): "))
            if number == 1:
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
                result_file='data/list_issues_'+resolution+'_'+status+'.txt'
                # Check if we already have the list of issues 
                if os.path.exists(result_file):
                    get_list_again = ask_user_input_y_or_n()
                    if get_list_again == 'y':
                        get_list_issues(url,resolution, status)
                else:
                    get_list_issues(url,resolution, status)
                # Get the filtered issues    
                get_filtered_issues(resolution, status)
                
            elif number == 2:
                # Print the message if the user enters 2
                print("You entered 2.")
            elif number == 3:
                # Print the message if the user enters 3
                print("You entered 3.")
            elif number == 4:
                # Print the message if the user enters 4
                print("You entered 4.")
            elif number == 0:
                # Exit the program if the user enters 0
                print("Exiting the program.")
                break
        
        except ValueError:
            # Handle the case where the user input is not an integer
            print("Invalid input. Please enter an integer between 1 and 4(or 0 to exit).")

if __name__ == '__main__':
    main()