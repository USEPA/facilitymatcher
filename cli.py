from main import main
import click

@click.command()
@click.option('--verbose', is_flag=True, help="Produces program logs, slows down the program considerably")
@click.option('--no-log', default=False, help="Skip logging the current run of the program")
@click.option('--skip-rows', default=0, help="Given an integer count {N}, skips N rows of first input file for processing. Used when an output is already partially created and you wish to continue a broken process")
@click.option('--skip-chunks', default=0, help="Given an integer count {N}, skips first N chunks, based on chunksize in config.json. Used when an output is already partially created and you wish to continue a broken process")
@click.option('--output', default="./output.csv", help="Output file path")
def cli(verbose, no_log, skip_rows, skip_chunks, output):
    """
    A tool that compares two CSV files and finds matches based on input fields.

    Use config.json for FRS filepath, EIA filepath, the fields to match,
    threshold to be set, chunk_size

    chunksize refers to how much of the FRS file is read per iteration. If you have a large RAM, you can increase
    chunksize and speed up processing slightly.
    """
    if skip_rows > 0 and skip_chunks > 0:
        raise ValueError("--skip-rows and --skip-chunks options cannot be used together")
    main(verbose, no_log, skip_rows, skip_chunks, output)

if __name__ == '__main__':
    cli()