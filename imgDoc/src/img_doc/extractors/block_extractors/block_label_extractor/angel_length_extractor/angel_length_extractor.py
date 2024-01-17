from typing import List
import numpy as np
from img_doc.extractors.block_extractors.block_extractor_from_word import KMeanBlockExtractor
from ..base_block_label_extractor import BaseBlockLabelExtractor, Block, LABEL

class AngleLengthExtractor(BaseBlockLabelExtractor):
    def __init__(self):
        self.kmean_ext = KMeanBlockExtractor()
    def extract(self, blocks: List[Block]) -> None:
        for block in blocks:
            try:
                words = block.words
                if len(words) < 4:
                    block.label = LABEL["text"]
                    continue
                neighbors = self.kmean_ext.get_index_neighbors_word(words)
                distans = self.kmean_ext.get_distans(neighbors, words)
                dist_word, dist_row, std_word, std_row = self._get_stat_from_dist(distans)
                mean_word_h, mean_word_w, std_word_h, std_word_w = self._get_stat_from_words(words)

                is_exist_col = dist_word > mean_word_w
                is_exist_row = dist_row > mean_word_h

                is_homogeneous_col = std_word < mean_word_w + std_word_w
                is_homogeneous_row = std_row < mean_word_h + std_word_h

                if is_homogeneous_row or is_homogeneous_col:
                    block.label = LABEL["multiple_blocks"]
                else:
                    block.label = LABEL["text"]
            except :
                block.label = LABEL["no_struct"]

    # LABEL = {
    #     "no_struct": 0,
    #     "multiple_blocks": 1,
    #     "text": 2,
    #     "header": 3,
    #     "list": 4,
    #     "table": 5,
    # }

    def _get_stat_from_dist(self, distans):
        distribution_h = []
        distribution_w = []

        for dist in distans:
            if dist[0] > 0:
                distribution_h.append(dist[0])
            if dist[1] > 0:
                distribution_w.append(dist[1])
            if dist[2] > 0:
                distribution_h.append(dist[2])
            if dist[3] > 0:
                distribution_w.append(dist[3])
        dist_row = np.mean(distribution_h)
        dist_word = np.mean(distribution_w)

        std_row = np.std(distribution_h)
        std_word = np.std(distribution_w)

        return dist_word, dist_row, std_word, std_row

    def _get_stat_from_words(self, words):
        size_h_word = [word.segment.get_height() for word in words]
        size_w_word = [word.segment.get_width() for word in words]
        mean_word_h = np.mean(size_h_word)
        mean_word_w = np.mean(size_w_word)
        std_word_h = np.std(size_h_word)
        std_word_w = np.std(size_w_word)
        return mean_word_h, mean_word_w, std_word_h, std_word_w