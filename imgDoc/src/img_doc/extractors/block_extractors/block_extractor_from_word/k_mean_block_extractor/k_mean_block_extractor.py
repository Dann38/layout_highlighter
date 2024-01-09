from ..base_block_extractor_from_word import *
from img_doc.data_structures import ImageSegment, Word, Block, Graph
import numpy as np
from typing import Dict

class KMeanBlockExtractor(BaseBlockExtractorFromWord):
    def extract_from_word(self, words: List[Word], history: Dict) -> List[Block]:
        """
        history:
        join_blocks,
        neighbors,
        distans,
        dist_word,
        graph,
        no_join_blocks
        """
        neighbors = self.get_index_neighbors_word(words)
        distans = self.get_distans(neighbors, words)
        dist_word, dist_row = self.get_standart_distant(distans)
        graph = self.get_graph_words(words, neighbors, dist_word, dist_row, distans)

        list_block = []
        for r in graph.get_related_graphs():
            block = Block()
            words_r = [words[n.index-1] for n in r.get_nodes()]
            block.set_words(words_r)
            list_block.append(block)

        join_intersect_block = self.join_intersect_blocks(list_block)

        if "join_blocks" in history.keys():
            history["join_blocks"] = join_intersect_block
        if "neighbors" in history.keys():
            history["neighbors"] = neighbors
        if "distans" in history.keys():
            history["distans"] = distans
        if "dist_word" in history.keys():
            history["dist_word"] = dist_word
        if "dist_row" in history.keys():
            history["dist_word"] = dist_row
        if "graph" in history.keys():
            history["graph"] = graph
        if "no_join_blocks" in history.keys():
            history["no_join_blocks"] = list_block
        return join_intersect_block

    def get_index_neighbors_word(self, words, max_level=3):
        hash_matrix, fun_hashkey = self.get_hash_matrix(words)
        neighbors = []
        for k in range(len(words)):
            top_right_bottom_left = [k, k, k, k]
            for i, vec in enumerate(["top", "right", "bottom", "left"]):
                top_right_bottom_left[i] = self.get_neighbor_fun(words, k, hash_matrix,
                                                                 fun_hashkey, max_level, vec)

            neighbors.append(top_right_bottom_left)
        return neighbors

    def get_hash_matrix(self, words):
        n = len(words)

        segment_words = ImageSegment(0, 0, 0, 0)
        segment_words.set_segment_max_segments([word.segment for word in words])

        h = segment_words.get_height()
        w = segment_words.get_width()

        coef = w / h

        m_width = round((n * coef) ** 0.5)
        m_height = round(m_width / coef)

        dh = h / m_height
        dw = w / m_width
        ch = segment_words.y_top_left
        cw = segment_words.x_top_left
        hashkey = lambda word: self.get_index_hash(word, dh, dw, ch, cw)

        hash_matrix = [[[] for i in range(m_width)] for j in range(m_height)]

        for i, word in enumerate(words):
            hash_i, hash_j = hashkey(word)
            hash_matrix[hash_i][hash_j].append(i)

        return hash_matrix, hashkey

    def get_index_hash(self, word, dh, dw, ch, cw):
        x_c, y_c = word.segment.get_center()
        hash_i = int((y_c - ch) / dh)
        hash_j = int((x_c - cw) / dw)
        return hash_i, hash_j

    def get_words_hash_cell(self, hash_matrix, hash_i, hash_j):

        return hash_matrix[hash_i][hash_j]

    def get_word_index_level(self, words, k, hash_matrix, fun_hashkey, level, vec):
        index_h, index_w = fun_hashkey(words[k])

        index_h_max = len(hash_matrix)
        index_w_max = len(hash_matrix[0])

        if vec in ("left", "right"):
            new_index_w = index_w - level if vec == "left" else index_w + level
            new_index_h = index_h

            new_index_h0 = max(0, index_h - level)
            new_index_h1 = min(index_h_max - 1, index_h + level)
            # word_ = words[k].segment.x_top_left if vec == "left" else words[k].segment.x_bottom_right
        elif vec in ("top", "bottom"):
            new_index_h = index_h - level if vec == "top" else index_h + level
            new_index_w = index_w
            new_index_w0 = max(0, index_w - level)
            new_index_w1 = min(index_w_max - 1, index_w + level)
            # word_ = words[k].segment.y_top_left if vec == "top" else words[k].segment.y_bottom_right

        if new_index_w < 0 or new_index_w >= index_w_max or new_index_h < 0 or new_index_h >= index_h_max:
            return k
        else:
            neighbors = []
            if vec in ("left", "right"):
                # for new_index_h_i in range(new_index_h0, new_index_h1 + 1):
                #     neighbors += self.get_words_hash_cell(hash_matrix, new_index_h_i, new_index_w)  #
                neighbors += self.get_words_hash_cell(hash_matrix, new_index_h, new_index_w)
            else:
                # for new_index_w_i in range(new_index_w0, new_index_w1 + 1):  #
                #     neighbors += self.get_words_hash_cell(hash_matrix, new_index_h, new_index_w_i)  #
                neighbors += self.get_words_hash_cell(hash_matrix, new_index_h, new_index_w)

        min_distance = np.inf
        min_index = k

        for neighbor_index_word in neighbors:
            # if vec in ("left", "right"):
            #     neighbors_word_ = words[neighbor_index_word].segment.x_bottom_right if vec == "left" \
            #         else words[neighbor_index_word].segment.x_top_left
            # else:
            #     neighbors_word_ = words[neighbor_index_word].segment.y_bottom_right if vec == "top" \
            #         else words[neighbor_index_word].segment.y_top_left
            #
            # distance = word_ - neighbors_word_ if vec in ("left", "top") else neighbors_word_ - word_
            if vec == "left":
                neighbor_ = words[neighbor_index_word].segment.x_bottom_right
                word_ = words[k].segment.x_top_left
                nc_, nc = words[neighbor_index_word].segment.get_center()
                wc_, wc = words[k].segment.get_center()
                delta = word_-neighbor_
                # delta = abs(nc_-wc_)
                distance = delta**2+(nc-wc)**2
            elif vec == "right":
                neighbor_ = words[neighbor_index_word].segment.x_top_left
                word_ = words[k].segment.x_bottom_right
                nc_, nc = words[neighbor_index_word].segment.get_center()
                wc_, wc = words[k].segment.get_center()
                delta = neighbor_-word_
                # delta = abs(nc_ - wc_)
                distance = delta**2+(nc-wc)**2
            elif vec == "top":
                neighbor_ = words[neighbor_index_word].segment.y_bottom_right
                word_ = words[k].segment.y_top_left
                nc, nc_ = words[neighbor_index_word].segment.get_center()
                wc, wc_ = words[k].segment.get_center()
                delta = word_ - neighbor_
                # delta = abs(nc_ - wc_)
                distance = delta ** 2 + (nc - wc) ** 2
            elif vec == "bottom":
                neighbor_ = words[neighbor_index_word].segment.y_top_left
                word_ = words[k].segment.y_bottom_right
                nc, nc_ = words[neighbor_index_word].segment.get_center()
                wc, wc_ = words[k].segment.get_center()
                delta = neighbor_ - word_
                # delta = abs(nc_ - wc_)
                distance = delta ** 2 + (nc - wc) ** 2
            if (delta > 0) and (distance < min_distance):
                min_distance = distance
                min_index = neighbor_index_word
        return min_index

    def get_neighbor_fun(self, words, k, hash_matrix, fun_hashkey, max_level, vec):
        for level in range(max_level):
            min_index_word = self.get_word_index_level(words, k, hash_matrix, fun_hashkey, level, vec)
            if min_index_word != k:
                return min_index_word
        return k

    def get_distans(self, neighbors, words):
        distans = []

        for i, ed_k in enumerate(neighbors):
            top_dist = words[i].segment.y_top_left - words[ed_k[0]].segment.y_bottom_right
            right_dist = words[ed_k[1]].segment.x_top_left - words[i].segment.x_bottom_right
            bottom_dist = words[ed_k[2]].segment.y_top_left - words[i].segment.y_bottom_right
            left_dist = words[i].segment.x_top_left - words[ed_k[3]].segment.x_bottom_right
            distans.append([top_dist, right_dist, bottom_dist, left_dist])

        return distans

    def get_standart_distant(self, distans):
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
        return dist_word, dist_row

    def get_graph_words(self, words, neighbors, dist_word, dist_row, distans):
        graph = Graph()
        edges = []

        for n1, ed_k in enumerate(neighbors):
            for vec, n2 in enumerate(ed_k):
                set_n = {n1, n2}
                if n1 != n2 and not (set_n in edges):
                    if (vec in (0, 2)) and (distans[n1][vec] < dist_row) and (distans[n1][vec] > 0):
                        edges.append(set_n)
                    elif (vec in (1, 3)) and (distans[n1][vec] < dist_word) and (distans[n1][vec] > 0):
                        edges.append(set_n)
        for i, word in enumerate(words):
            c1x, c1y = word.segment.get_center()
            index = graph.add_node(c1x, c1y)  # index_word+1

        for edge in edges:
            n_list = list(edge)
            n1, n2 = n_list[0] + 1, n_list[1] + 1
            graph.add_edge(n1, n2)

        return graph
