from .image_segment import ImageSegment

class SegmentInformation:
    def __init__(self, segment:ImageSegment, info: dict) -> None:
        self.segment = segment
        self.info = info
        