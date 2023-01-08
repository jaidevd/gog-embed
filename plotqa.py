import os
from argparse import ArgumentParser
from PIL import Image
import re

op = os.path


def match_template(s, tmpls):
    matches = [re.search(pat, s) for pat in tmpls]
    matches = [m.groupdict() if m else {} for m in matches]
    return max(matches, key=len)


class PlotQA(object):
    def __init__(self, root):
        self.root = root

    def load_qa(self, by="chart-id"):
        pass

    def show(self, chart_id):
        path = op.join(self.root, "png", f"{chart_id}.png")
        with Image.open(path) as im:
            im.show()


if __name__ == "__main__":
    ROOT = "/media/jaidevd/motherbox/archive/plotqa/"
    parser = ArgumentParser()
    parser.add_argument("--path", dest="root", default=ROOT, action="store")
    parser.add_argument("--id", type=int)
    # args = parser.parse_args()
    # ds = PlotQA(args.root)
    # ds.show(args.id)
