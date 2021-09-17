# coding=utf-8

import os
import ddddocr
import onnxruntime

onnxruntime.set_default_logger_severity(3)


def generator(path):
    onnxruntime.set_default_logger_severity(3)
    with open(path, 'rb') as f:
        img_bytes = f.read()
    ocr = ddddocr.DdddOcr()
    code = ocr.classification(img_bytes)
    os.remove(path)
    return code

