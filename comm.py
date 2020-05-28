import argparse


argparser = argparse.ArgumentParser()
argparser.add_argument('--data', type=str, default=False)
argparser.add_argument('--out', type=str, default="./")
argparser.add_argument('--okved', type=str, default="68:31")
args = argparser.parse_args()