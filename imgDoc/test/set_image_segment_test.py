import unittest
from img_doc.image import ImageSegment, SetImageSegment, PositionException, TypeArgError
from img_doc.image.segment_clusterizer import KMeanClusterizer


class TestSetImageSegment(unittest.TestCase):
    def test_arg_create_segment(self):
        segment1 = ImageSegment(x_top_left=1, x_bottom_right=9, y_bottom_right=10, y_top_left=0)
        segment2 = ImageSegment(1,0,9,10)
        rez1 = segment1.get_segment_2p()
        rez2 = segment2.get_segment_2p()
        self.assertEqual(rez1["x_top_left"], rez2["x_top_left"])
        self.assertEqual(rez1["x_bottom_right"], rez2["x_bottom_right"])
        self.assertEqual(rez1["y_bottom_right"], rez2["y_bottom_right"])
        self.assertEqual(rez1["y_top_left"], rez2["y_top_left"])
    
    def test_invalid_create_segment(self):
        with self.assertRaises(PositionException):
            s = ImageSegment(9, 0, 1, 10)
        with self.assertRaises(PositionException):
            s = ImageSegment(1, 10, 9, 0)
        with self.assertRaises(TypeArgError):
            s = ImageSegment(1.3, 0, 9, 10)

    def test_center_segment(self):
        segment= ImageSegment(1,0,9,10)
        x, y = segment.get_center()
        self.assertEqual(x, 5)
        self.assertEqual(y, 5)


    def test_clusterizer(self):
        kmean = KMeanClusterizer()
        segment1 = ImageSegment(1,0,25,10)
        segment2 = ImageSegment(1,13,30,23)
        segment3 = ImageSegment(60,40,89,50)
        segment4 = ImageSegment(93,40,108,50)
        self.assertEqual(len(kmean.cluster([])), 0)
        self.assertEqual(len(kmean.cluster([segment1])), 1)
        self.assertEqual(len(kmean.cluster([segment1, segment2])), 1)
        self.assertEqual(len(kmean.cluster([segment1, segment2, segment3, segment4])), 2)


if __name__ == "__main__":
    unittest.main(verbosity=2)