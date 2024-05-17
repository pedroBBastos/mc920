import argparse
import sys
import projecaoHorizontal
import transformadaHough

parser = argparse.ArgumentParser()
parser.add_argument('--inputImg', type=str, help='Image to be text aligned')
parser.add_argument('--mode', type=str, help='Alignment mode to be used: PROJECTION or HOUGH')
parser.add_argument('--houghThreshold', type=str, help='Threshold to be used on HOUGH transform')

args = parser.parse_args()
if len(sys.argv[1:]) < 4:
    print(args._get_args())
    parser.print_help()
    exit()

if args.mode == 'PROJECTION':
    projecaoHorizontal.alinhar(args.inputImg)
elif args.mode == 'HOUGH':
    if args.houghThreshold is not None:
        transformadaHough.alinhar(args.inputImg, int(args.houghThreshold))
    else:
        transformadaHough.alinhar(args.inputImg)
else:
    print("Unknown mode '", args.mode, "'. Aborting...")
