from matcher.core.match import Matcher, MatcherNumMethod, MatcherType
from line_profiler import LineProfiler

from matcher.core.storage import DetectorType
from argparse import ArgumentParser

parser = ArgumentParser(description="Fast match")
parser.add_argument("--show", action="store_true", help="Show matches picture")
parser.add_argument("--debug", action="store_true", help="Debug mode")
args = parser.parse_args()

def main():
    matcher = Matcher("foo", debug=args.debug, match_method=MatcherType.BF, match_num_method=MatcherNumMethod.KNN, detector_type=DetectorType.ORB)
    matcher.show_matches_pic = args.show

    matcher.match("toy.jpg")

if __name__ == "__main__":
    profiler = LineProfiler()
    profiler_wrapper = profiler(main)
    profiler_wrapper()
    profiler.print_stats()
    profiler.dump_stats("fast_match.lprof")