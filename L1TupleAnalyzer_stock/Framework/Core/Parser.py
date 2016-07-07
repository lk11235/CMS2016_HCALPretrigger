
import argparse

parser = argparse.ArgumentParser(description='parser for BTagResult class')

parser.add_argument('--inputDir',action="store",help="input directory")
parser.add_argument('--outputDir',action="store",help="output directory")
parser.add_argument('--inputPath',action="store",help="input path")
parser.add_argument('--outputPath',action="store",help="output path")


option = parser.parse_args()
