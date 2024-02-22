from matcher.core.match import Matcher
from line_profiler import LineProfiler

def main():
    matcher = Matcher("foo", debug=True)
    matcher.match("static/foo/bottom.jpg")

if __name__ == "__main__":
    profiler = LineProfiler()
    profiler_wrapper = profiler(main)
    profiler_wrapper()
    profiler.print_stats()
    profiler.dump_stats("fast_match.lprof")