from iCloudAPI import API
from argparse import ArgumentParser


def parse_args():
    parser = ArgumentParser()
    parser.add_argument("--user", "-user", type=str, default="hlwen.526@yahoo.com", help='iCloud Account')
    parser.add_argument("--password", "-password", type=str, required=True, help='iCloud Password')
    parser.add_argument("--file", "-file", type=str, required=True, help='File to download')
    parser.add_argument("--output", "-output", type=str, default="..", help='Output directory')
    args = parser.parse_args()
    return args


if __name__ == '__main__':
    args = parse_args()
    api = API(args.user, args.password)
    api.download(args.file, args.output)
