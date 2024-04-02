run ocr on a directory of images with python and tesseract

create env

```sh
conda create -y -c conda-forge -n pyocr python=3.12 pytesseract pillow
```

activate env

```sh
conda activate pyocr
```

install [tesseract-ocr](https://tesseract-ocr.github.io/tessdoc/Installation.html)

> YOU MUST SET THE `TESSERACT_PATH` VARIABLE IN THE *ocrdir.py* file

optionally configure the conditional statement to analyze whether an image has qualifying content

`gif2frames.cmd` gives an example of converting a gif frames to jpegs for OCR (e.g. video content with deduplicated frames)

run process

```sh
python ./ocrdir.py
```

drop conda env

```sh
conda deactivate
```

then

```sh
conda remove -y -n pyocr --all
```