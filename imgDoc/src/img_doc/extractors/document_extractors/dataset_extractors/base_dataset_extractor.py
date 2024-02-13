from img_doc.data_structures.document import Document
from abc import ABC, abstractmethod
from ..base_document_extractor import BaseDocumentExtractor
from typing import List

class BaseDatasetDocExtractor(BaseDocumentExtractor):
    @abstractmethod
    def dataset_extractor(self, path_dataset) -> List[Document]:
        pass
        

    
