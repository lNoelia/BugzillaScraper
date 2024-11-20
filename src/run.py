import os
from src.utils import (
    get_resolution_options,
    get_status_options,
    choose_resolution_status,
    ask_user_input_y_or_n
)
from src.scraper import get_list_issues, get_dataset_issues


def run_scrapper(resolution=None, status=object()):  # Usamos object() como valor sentinela
    # Obtener la URL principal desde el entorno
    url = os.getenv('MAIN_PAGE')
    if not url:
        raise ValueError("MAIN_PAGE environment variable is not set.")
    if url.endswith('/'):
        url = url[:-1]

    field_url = f"{url}/rest/field/bug"

    # Obtener las opciones de resolución y estado
    resolution_options = get_resolution_options(field_url)
    status_options = get_status_options(field_url)

    # Si resolution o status no están definidos, entra en modo interactivo
    if resolution is None or status is object():  # Usamos el sentinela para detectar valores ausentes
        print("Resolution or status not provided, entering interactive mode...")
        print("Resolution Options:")
        for i, opt in enumerate(resolution_options, start=1):
            print(f"{i}. {opt}")
        resolution_index = int(input("Select a resolution option: ")) - 1
        resolution = resolution_options[resolution_index]

        print("Status Options:")
        for i, opt in enumerate(status_options, start=1):
            print(f"{i}. {opt}")
        status_index = int(input("Select a status option: ")) - 1
        status = status_options[status_index]

    # Validar que los valores proporcionados sean válidos
    else:
        if resolution not in resolution_options:
            raise ValueError(f"Invalid resolution: {resolution}. Valid options: {resolution_options}")
        if status not in status_options and status is not None:
            raise ValueError(f"Invalid status: {status}. Valid options: {status_options}")

    print(f"Resolution and Status selected: {resolution} and {status}")

    # Crear la carpeta 'data' si no existe
    if not os.path.exists('data'):
        os.makedirs('data')

    result_file = f"data/list_issues_{resolution}_{status}.csv"

    # Comprobar si el archivo ya existe
    if os.path.exists(result_file):
        print(f"The file {result_file} already exists.")
        get_list_again = ask_user_input_y_or_n("Do you want to regenerate the list of issues? (y/n): ")
        if get_list_again.lower() == 'y':
            get_list_issues(url, resolution, status)
    else:
        get_list_issues(url, resolution, status)

    # Obtener el conjunto de datos de issues
    get_dataset_issues(resolution, status)
    print(f"The list of issues has been saved in the file: {result_file}")

if __name__ == '__main__':
    run_scrapper()
