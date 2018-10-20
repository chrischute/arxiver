import argparse
import fileinput

from arxiver import ArXiver


def main(args):
    arxiver = ArXiver(output_dir=args.output_dir)
    url_fh = fileinput.input([args.input_file])
    for url in url_fh:
        arxiver.get_paper(url)


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Download Papers from ArXiv')
    parser.add_argument('--output_dir', type=str, default='papers',
                        help='Output directory for writing papers.')
    parser.add_argument('--input_file', '-i', type=str, default='-',
                        help='Input file with one URL per line. Use "-" for stdin.')
    main(parser.parse_args())
