# tesseract_reader

[install tesseract](https://tesseract-ocr.github.io/tessdoc/Installation.html)

```python
from tesseract_reader.tesseract_reader import TesseractReader, TesseractReaderConfig

config = TesseractReaderConfig(lang="rus")
reader = TesseractReader(config)


# img:np.ndarray = ...
bboxes = reader.read(img)

```

```commandline
docker run -p 1286:1236 my_image/tesseract
```