import argparse
import logging
import os
import zipfile


logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)

log_handler = logging.StreamHandler()
log_handler.setFormatter(logging.Formatter('%(levelname)s: %(message)s'))
logger.addHandler(log_handler)


def unzip_file(zip_path: str, dest_dir: str) -> str:
    zip_file_name = zip_path.lstrip('.').lstrip('/').lstrip('\\').rstrip(".zip")

    try:

        if not os.path.exists(dest_dir):
            logger.warning('Destination directory [%s] not found, creating one...', dest_dir)
            os.makedirs(dest_dir, exist_ok=True)
            logger.warning('Finished making destination directory [%s]!', dest_dir)

        logger.info('Extracting the ZIP file [%s] to [%s]...', zip_path, dest_dir)
        with zipfile.ZipFile(zip_path, 'r') as zip_ref:
            zip_ref.extractall(dest_dir)
        
        # Check if the zip file was extracted to a subdirectory
        sub_dir_path = f'{dest_dir}/{zip_file_name}'

        if os.path.exists(sub_dir_path):
            logger.info('Finished extracting the ZIP file [%s] to [%s]!', zip_path, sub_dir_path)
            return sub_dir_path

        elif os.path.exists(dest_dir):
            logger.info('Finished extracting the ZIP file [%s] to [%s]!', zip_path, dest_dir)
            return dest_dir

    except Exception as e:
        logger.error('Failed to extract the submission ZIP file [%s]: %s', zip_path, e)
    


def parse_arguments() -> argparse.Namespace:
    """
    Parse command line arguments
    """
    parser = argparse.ArgumentParser(description='Extract ZIP files')
    parser.add_argument(
        'path_to_zip_file',
        help='Relative path to the ZIP file from current directory',
        type=str
    )
    parser.add_argument(
        '--dest_dir',
        help='Relative path to the extracted ZIP file contents directory from current directory',
        default='.raw/',
        type=str
    )
    return parser.parse_args()


if __name__ == "__main__":
    args: argparse.Namespace = parse_arguments()
    
    output_path = unzip_file(args.path_to_zip_file, args.dest_dir)
    