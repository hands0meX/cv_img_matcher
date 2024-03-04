from matcher.core.storage import ImageDataSet, DetectorType
from line_profiler import LineProfiler
from argparse import ArgumentParser

parser = ArgumentParser("fast build")
parser.add_argument("--debug", action="store_true", help="Debug mode")
parser.add_argument("--force", action="store_true", help="Force update dataset")
args = parser.parse_args()

def main():
    ImageDataSet("foo", force_update=args.force, debug=args.debug, detector_type=DetectorType.ORB)

if __name__ == "__main__":
    profiler = LineProfiler()
    profiler_wrapper = profiler(main)
    profiler_wrapper()
    profiler.print_stats()
    profiler.dump_stats("fast_build.lprof")