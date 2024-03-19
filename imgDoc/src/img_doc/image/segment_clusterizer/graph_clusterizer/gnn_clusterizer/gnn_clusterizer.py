from typing import Dict, List
from img_doc.image import ImageSegment
from ..k_mean_clusterizer import KMeanClusterizer
import numpy as np


class GNNClusterizer(KMeanClusterizer):
    def cluster(self, segments: List[ImageSegment], conf: Dict = ...) -> List[ImageSegment]:
        if len(segments) == 0:
            return []
        elif len(segments) == 1:
            segment = ImageSegment(dict_2p=segments[0].get_segment_2p())
            return [segment]

       

    def get_vecs(self, segments: List[ImageSegment]):
        neighbors = self.get_index_neighbors_segment(segments)
        cords = [seg.get_center() for seg in segments]
        
        xs = np.array([c[0] for c in cords])
        xs = xs/max(xs)
        
        ys = np.array([c[1] for c in cords])
        ys = ys/max(ys)
        
        vecs = [[] for s in segments]
        
        for i, nodes in enumerate(neighbors):
            x = sum([xs[n] for n in nodes])/4
            y = sum([ys[n] for n in nodes])/4
            vecs[i].append(x)
            vecs[i].append(y)

        for layear in range(4):
            for i, nodes in enumerate(neighbors):
                x = sum([vecs[n][-1] for n in nodes])/4
                y = sum([vecs[n][-2] for n in nodes])/4
                vecs[i].append(x)
                vecs[i].append(y)
        return vecs
