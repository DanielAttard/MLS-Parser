import sys
from MLS import MLS

if len(sys.argv) > 0:
        for link in sys.argv[1:]:
                mls = MLS(link)
                print mls.parse()
