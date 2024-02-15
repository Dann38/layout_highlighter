from .image_segment import ImageSegment
from typing import List
from .segment_clusterizer import KMeanClusterizer
import numpy as np

PARENT_SEGMENTS_EXTRACTORS = {
    "kmean": KMeanClusterizer()
}

class SetImageSegment:
    def __init__(self, list_segment: List[ImageSegment]):
        self.segments = list_segment
        self.parent_segments: List[ImageSegment]

    def extract_parant_segment(self, method: str = "kmean", conf={}):
        self.parent_segments = PARENT_SEGMENTS_EXTRACTORS[method].cluster(self.segments, conf)

    def get_mean_height(self):
        if len(self.segments) == 0:
            return None
        
        return np.mean([seg.get_height() for seg in self.segments])