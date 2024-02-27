from matcher.core.storage import ImageDataSet, DetectorType
from line_profiler import LineProfiler
from argparse import ArgumentParser

parser = ArgumentParser("fast build")
parser.add_argument("--debug", action="store_true", help="Debug mode")
args = parser.parse_args()

def main():
    ImageDataSet("home", force_update=True, debug=args.debug, detector_type=DetectorType.SIFT)

if __name__ == "__main__":
    profiler = LineProfiler()
    profiler_wrapper = profiler(main)
    profiler_wrapper()
    profiler.print_stats()
    profiler.dump_stats("fast_build.lprof")