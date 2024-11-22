import argparse
import logging
import multiprocessing
import os
import shutil


logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)

log_handler = logging.StreamHandler()
log_handler.setFormatter(logging.Formatter('%(levelname)s: %(message)s'))
logger.addHandler(log_handler)


def move_file_to_dir(file_name: str, src_dir: str, dest_dir: str) -> None:
    """
    Copy a file from the source directory to the destination directory
    """
    try:
        source_path = f'{src_dir}/{file_name}'
        destination_path = f'{dest_dir}/{file_name}'
        logger.debug('Copying %s from %s to %s', file_name, src_dir, dest_dir)
        shutil.copy(source_path, destination_path)
        logger.debug('Finished copying %s from %s to %s', file_name, src_dir, dest_dir)
    except Exception as e:
        logger.error('Failed to copy %s from %s to %s: %s', file_name, src_dir, dest_dir, e)


def filter_directory(file_type: str, src_dir: str, dest_dir: str) -> None:
    """
    Filter files from the source directory to the destination directory
    """

    target_file_names: List[str] = []

    if not os.path.exists(dest_dir):
        logger.warning('Destination directory [%s] not found, creating one...', dest_dir)
        os.makedirs(dest_dir, exist_ok=True)
        logger.warning('Finished making destination directory [%s]!', dest_dir)

    file_names: List[str] = os.listdir(src_dir)
    
    logger.info('Found %s files in [%s]', len(file_names), src_dir)

    for file_name in file_names:
        if file_name.endswith(file_type):
            target_file_names.append(file_name)
    
    logger.info('Extracting %s [%s] files to [%s]...', len(target_file_names), file_type, dest_dir)

    with multiprocessing.Pool() as pool:
        args = [(tfn, src_dir, dest_dir) for tfn in target_file_names]
        pool.starmap(move_file_to_dir, args)
    
    logger.info('Finished extracting %s [%s] files to [%s]!', len(target_file_names), file_type, dest_dir)


def parse_arguments() -> argparse.Namespace:
    """
    Parse command line arguments
    """
    parser = argparse.ArgumentParser(description='Filter submission files')
    parser.add_argument(
        'extracted_zip_contents_dir',
        help='Relative path to the extracted submissions ZIP file directory from current directory',
        type=str
    )
    parser.add_argument(
        '--dest_dir',
        help='Relative path to the filtered submissions directory from current directory',
        default='.filtered',
        type=str
    )
    return parser.parse_args()


if __name__ == "__main__":

    args: argparse.Namespace = parse_arguments()
    source_directory = args.extracted_zip_contents_dir
    destination_directory = args.dest_dir

    filter_directory(
        file_type='.css', 
        src_dir=source_directory, 
        dest_dir=destination_directory + '/css'
    )
    filter_directory(
        file_type='.zip', 
        src_dir=source_directory, 
        dest_dir=destination_directory +'/zip'
    )
