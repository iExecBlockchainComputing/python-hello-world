import json
import os
import sys

from pyfiglet import Figlet


def do_some_computation():
    """
    This function simulates some computation in an iExec application. Script
    arguments (if provided) are accessible via "sys.argv" array. In this case,
    if the first argument is present, it is used in the greeting message.
    """
    name = sys.argv[1] if len(sys.argv) > 1 else "World"
    greeting = f'Hello, {name}!'
    # Let's add some art for e.g.
    art = Figlet().renderText(greeting)
    return art + greeting


def handle_dataset():
    """
    This function shows how to read a dataset file from an iExec application.
    Datasets are public in standard mode and confidential in TEE mode.
    The dataset location and filename are needed to be able to read it. Both
    of which are provided in the following environment variables:
        - IEXEC_IN: the path to the folder where the dataset is located.
        - IEXEC_DATASET_FILENAME: the name of the dataset file.
    """
    iexec_in = os.environ['IEXEC_IN']
    dataset_filename = os.environ['IEXEC_DATASET_FILENAME']
    dataset_filepath = iexec_in + '/' + dataset_filename
    text = f'\nDataset ({dataset_filepath}): '
    if os.path.isfile(dataset_filepath):
        with open(dataset_filepath) as f:
            text = text + f.read()
    return text


def handle_input_files():
    """
    This function demonstrates how to use input files in an iExec application.
    The following environment variables are used:
        - IEXEC_IN: the path to the folder where input files are located.
        - IEXEC_INPUT_FILES_NUMBER: number of available input files.
        - IEXEC_INPUT_FILE_NAME_N: the name of the Nth input file. N is between
          1 and IEXEC_INPUT_FILES_NUMBER.
    If IEXEC_INPUT_FILES_NUMBER is 0 then no input file is available.
    """
    iexec_in = os.environ['IEXEC_IN']
    iexec_input_files_number = int(os.environ['IEXEC_INPUT_FILES_NUMBER'])
    text = ''
    for i in range(1, iexec_input_files_number + 1):
        file_path = iexec_in + "/" \
                    + os.environ['IEXEC_INPUT_FILE_NAME_' + str(i)]
        if os.path.isfile(file_path):
            with open(file_path) as f:
                text += f'\nInput file [{i}] ({file_path}): {f.read()}'
    return text


def handle_app_developer_secrets():
    """
    This function demonstrates how to use application-developer secrets in an
    iExec application.
    The following environment variables are used:
        - IEXEC_APP_DEVELOPER_SECRET: first secret set by the application
        developer
    """
    iexec_app_developer_secret = os.getenv('IEXEC_APP_DEVELOPER_SECRET', '')
    if iexec_app_developer_secret == '':
        return ''
    return f'\nApp developer secret: {iexec_app_developer_secret}'


def handle_requester_secrets():
    """
    This function demonstrates how to use requester secrets in an
    iExec application.
    The following environment variables are used:
        - IEXEC_REQUESTER_SECRET_1: first secret set by the requester
        - IEXEC_REQUESTER_SECRET_2: second secret set by the requester
        - IEXEC_REQUESTER_SECRET_3: third secret set by the requester
    """
    iexec_requester_secrets = ''
    for idx in range(1, 4):
        iexec_requester_secret = os.getenv(f'IEXEC_REQUESTER_SECRET_{idx}', '')
        if iexec_requester_secret != '':
            iexec_requester_secrets += f'\nRequester secret {idx}: {iexec_requester_secret}'
    return iexec_requester_secrets


def write_stderr():
    """
    This function writes some text to stderr.
    This text will be saved after task execution. It can be retrieved in result.zip or through
    the scheduler's dedicated endpoints `/tasks/{chainTaskId}/logs`
    or `/tasks/{chainTaskId}/replicates/{walletAddress}/logs`.
    """
    iexec_task_id = os.environ['IEXEC_TASK_ID']
    text = f'Here is a line for stderr of task {iexec_task_id}'
    print(text, file=sys.stderr)


def save_result(text):
    """
    This function shows how to save a result in an iExec application. The result
    file(s) should be written in the folder indicated by the environment
    variable IEXEC_OUT. After saving the result, the file "computed.json" must
    be created in the same folder. It must contain, at least, the path to the
    determinism file (deterministic-output-path).
    """
    iexec_out = os.environ['IEXEC_OUT']
    result_filepath = iexec_out + '/result.txt'
    with open(result_filepath, 'w+') as f:
        f.write(text)
    computed_file_content = {"deterministic-output-path": result_filepath}
    print(computed_file_content)
    with open(iexec_out + '/computed.json', 'w+') as f:
        json.dump(computed_file_content, f)


if __name__ == '__main__':
    computation_text = do_some_computation()
    print(computation_text)
    dataset_text = handle_dataset()
    print(dataset_text)
    input_files_text = handle_input_files()
    print(input_files_text)
    app_developer_secrets_text = handle_app_developer_secrets()
    print(app_developer_secrets_text)
    requester_secrets_text = handle_requester_secrets()
    print(requester_secrets_text)
    write_stderr()
    result = f'{computation_text}\n' \
             f'{dataset_text}\n' \
             f'{input_files_text}\n' \
             f'{app_developer_secrets_text}\n' \
             f'{requester_secrets_text}\n'
    save_result(result)
