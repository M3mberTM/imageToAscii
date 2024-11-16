import argparse

parser = argparse.ArgumentParser(description='Adjusting the image to ascii converter.')

parser.add_argument('integers', metavar='N', type=int, nargs='+',
                    help='an integer for the accumulator')
parser.add_argument('--sum', dest='accumulate', action='store_const',
                    const=sum, default=max,
                    help='sum the integers (default: find the max)')

args = parser.parse_args()
print(args.accumulate(args.integers))

# TODO make the arguments for switching between modes. As well as arguments for color in the Image version. Make arguments for adjusting the ascii gradient.


