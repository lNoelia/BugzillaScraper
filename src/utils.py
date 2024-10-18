import requests

def get_resolution_options(url):
    url = url + '/resolution'
    response = requests.get(url)
    resolution_options = []
    if response.status_code == 200:
        data = response.json()
        resolutions = get_field_by_name(data, 'resolution')
        resolutions_values = resolutions.get('values', [])
        for value in resolutions_values:
            if value.get('name') == '':
                resolution_options.append('---')
            else:
                resolution_options.append(value.get('name'))
        resolution_options.append('TOTAL')
    else: 
        print("Failed to get resolution options. Please check the URL provided on the configuration file.")
    return resolution_options

def get_status_options(url):
    url = url + '/bug_status'
    response = requests.get(url)
    status_options = []
    if response.status_code == 200:
        data = response.json()
        status = get_field_by_name(data, 'bug_status')
        status_values = status.get('values', [])
        for value in status_values:
            status_options.append(value.get('name'))
        status_options.append('TOTAL')
    else: 
        print("Failed to get status options. Please check the URL provided on the configuration file.")
    return status_options

def get_field_by_name(data, field_name):
    for field in data.get('fields', []):
        if field.get('name') == field_name:
            return field
    return None

def choose_resolution_status(resolution_options, status_options):
    print("Resolution Options:")
    for i, option in enumerate(resolution_options):
        print(f"{i+1}. {option}")
    resolution = input("Select a resolution option: ")
    print("Status Options:")
    for i, option in enumerate(status_options):
        print(f"{i+1}. {option}")
    status = input("Select a status option: ")
    return resolution, status