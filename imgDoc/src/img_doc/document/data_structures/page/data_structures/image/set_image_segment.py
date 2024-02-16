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
    
    def extract_neighbors(self, method: str = "kmean", conf={}):
        self.neigbors = PARENT_SEGMENTS_EXTRACTORS[method].get_index_neighbors_segment(self.segments)
    
    def get_rnd_walk(self, count_step: int, start_node: int = None) -> List[int]:
        rng = np.random.default_rng()
        old_node = rng.integers(len(self.neighbors)) if start_node is None else start_node
        list_walk = []
        for i in range(count_step):
            r = rng.integers(4)
            self.new_node = self.neighbors[old_node][r]
            list_walk.append(old_node)
            self.old_node = self.new_node
        return list_walk
    
    def get_dist(self, index1, index2) -> float:
        return self.segments[index1].get_min_dist(self.segments[index2])

    def get_many_dist(self, index1) -> List[float]:
        return [self.get_dist(index1, n) for n in self.neigbors[index1]]

    def get_angle(self, index1, index2) -> float:
        return self.segments[index1].get_angle_center(self.segments[index2])

    def get_many_angle(self, index1) -> List[float]:
        return [self.get_angle(index1, n) for n in self.neigbors[index1]]

    def get_bold(self) -> np.ndarray:
        pass