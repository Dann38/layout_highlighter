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
        self.neighbors = PARENT_SEGMENTS_EXTRACTORS[method].get_index_neighbors_segment(self.segments)
    
    def get_rnd_walk(self, count_step: int, start_node: int = None) -> List[int]:
        rng = np.random.default_rng()
        self.old_node = rng.integers(len(self.neighbors)) if start_node is None else start_node
        list_walk = []
        for i in range(count_step):
            r = rng.integers(4)
            self.new_node = self.neighbors[self.old_node][r]
            list_walk.append(self.old_node)
            self.old_node = self.new_node
        return list_walk
    
    def get_list_random_node(self, count_node: int) -> List[int]:
        rng = np.random.default_rng()
        list_rnd = [rng.integers(len(self.neighbors)) for i in range(count_node)]
        return list_rnd
    
    def get_dist(self, index1, index2) -> float:
        return self.segments[index1].get_min_dist(self.segments[index2])

    def get_many_dist(self, index1) -> List[float]:
        return [self.get_dist(index1, n) for n in self.neighbors[index1]]

    def get_angle(self, index1, index2) -> float:
        return self.segments[index1].get_angle_center(self.segments[index2])

    def get_many_angle(self, index1) -> List[float]:
        return [self.get_angle(index1, n) for n in self.neighbors[index1]]
    
    def get_height(self, index1) -> List[float]:
        mean_ = self.get_mean_height()
        return [self.segments[index1].get_height()/mean_]

    def get_info_segment(self, index1, key_info) -> List[float]:
        rez = self.segments[index1].get_info(key_info)
        return list(rez)
    
    def get_dist_hist(self)-> List[float]:
        dists = np.array([x for i in range(len(self.segments)) for x in self.get_many_dist(i)])
        rez = np.histogram(dists, bins=11)[0]
        max_ = rez.max()
        if max_ != 0:
            rez = rez/max_
        return rez        
    
    def get_ang_hist(self)-> List[float]:
        angs = np.array([x for i in range(len(self.segments)) for x in self.get_many_angle(i)])
        rez = np.histogram(angs, bins=11)[0]
        max_ = rez.max()
        if max_ != 0:
            rez = rez/max_
        return rez 