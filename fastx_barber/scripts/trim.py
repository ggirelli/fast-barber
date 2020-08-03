"""
@author: Gabriele Girelli
@contact: gigi.ga90@gmail.com
"""

import argparse
from fastx_barber.scripts import common as com
from fastx_barber.const import logfmt, log_datefmt
from fastx_barber.match import FastxMatcher
from fastx_barber.seqio import FastxSimpleRecord, FastxChunkedParser
from fastx_barber.trim import get_fastx_trimmer, ABCTrimmer
import joblib  # type: ignore
import logging
import regex  # type: ignore
from typing import Tuple

logging.basicConfig(level=logging.INFO, format=logfmt, datefmt=log_datefmt)


def init_parser(subparsers: argparse._SubParsersAction) -> argparse.ArgumentParser:
    parser = subparsers.add_parser(
        __name__.split(".")[-1],
        description="Trim FASTX file.",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        help="Trim a FASTX file.",
    )

    parser.add_argument(
        "input",
        type=str,
        metavar="in.fastx[.gz]",
        help="""Path to the fasta/q file to trim.""",
    )
    parser.add_argument(
        "output",
        type=str,
        metavar="out.fastx[.gz]",
        help="""Path to fasta/q file where to write
                        trimmed records. Format will match the input.""",
    )

    default_pattern = "^(?<UMI>.{8})(?<BC>CATCACGC){s<2}(?<CS>GATC){s<2}"
    parser.add_argument(
        "--pattern",
        type=str,
        default=default_pattern,
        help=f"""Pattern to match to reads and trim.
        Remember to use quotes. Default: '{default_pattern}'""",
    )

    parser = com.add_version_option(parser)

    advanced = parser.add_argument_group("advanced arguments")
    advanced = com.add_unmatched_output_option(advanced)
    advanced = com.add_compress_level_option(advanced)
    advanced = com.add_log_file_option(advanced)

    advanced = com.add_chunk_size_option(advanced)
    advanced = com.add_threads_option(advanced)

    parser.set_defaults(parse=parse_arguments, run=run)

    return parser


def parse_arguments(args: argparse.Namespace) -> argparse.Namespace:
    args.regex = regex.compile(args.pattern)
    args.threads = com.check_threads(args.threads)

    if args.log_file is not None:
        com.add_log_file_handler(args.log_file)

    return args


def trim_record(
    record: FastxSimpleRecord, matcher: FastxMatcher, trimmer: ABCTrimmer
) -> Tuple[FastxSimpleRecord, bool]:
    match, matched = matcher.match(record)
    if matched:
        record = trimmer.trim_re(record, match)
    return (record, matched)


def run(args: argparse.Namespace) -> None:
    logging.info(f"Threads: {args.threads}")
    logging.info(f"Chunk size: {args.chunk_size}")
    logging.info(f"Pattern: {args.pattern}")

    fmt, IH, OH = com.get_io_handlers(args.input, args.output, args.compress_level)
    IH = FastxChunkedParser(IH, args.chunk_size)
    UH = com.get_unmatched_handler(fmt, args.unmatched_output, args.compress_level)
    foutput = com.get_output_fun(OH, UH)

    matcher = FastxMatcher(args.regex)
    trimmer = get_fastx_trimmer(fmt)

    logging.info("Trimming...")
    parsed_counter = 0
    trimmed_counter = 0
    for chunk in IH:
        parsed_counter += len(chunk)
        output = joblib.Parallel(n_jobs=args.threads, verbose=0)(
            joblib.delayed(trim_record)(record, matcher, trimmer) for record in chunk
        )
        for record, matched in output:
            trimmed_counter += matched
            foutput[matched](record)
        logging.info(f"Parsed {parsed_counter} records...")

    logging.info(f"{trimmed_counter}/{parsed_counter} records trimmed.")

    OH.close()
    if args.unmatched_output is not None and UH is not None:
        UH.close()
    logging.info("Done.")
