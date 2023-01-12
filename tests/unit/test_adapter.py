# -*- coding: utf-8 -*-

import os

import pytest

from PyPDFForm.middleware import adapter


@pytest.fixture
def pdf_samples():
    return os.path.join(os.path.dirname(__file__), "..", "..", "pdf_samples")


@pytest.fixture
def template_stream(pdf_samples):
    with open(os.path.join(pdf_samples, "sample_template.pdf"), "rb+") as f:
        return f.read()


def test_readable(pdf_samples):
    path = os.path.join(pdf_samples, "sample_template.pdf")
    assert not adapter.readable(path)
    with open(path, "rb+") as f:
        assert adapter.readable(f)
        stream = f.read()
        assert not adapter.readable(stream)


def test_file_adapter_fp_or_f_obj_or_stream_to_stream(pdf_samples, template_stream):
    path = os.path.join(pdf_samples, "sample_template.pdf")
    _read = adapter.fp_or_f_obj_or_stream_to_stream(path)
    assert len(_read) == len(template_stream)
    assert _read == template_stream
    with open(path, "rb+") as f:
        _read = adapter.fp_or_f_obj_or_stream_to_stream(f)
        assert len(_read) == len(template_stream)
        assert _read == template_stream
        f.seek(0)
        _read = adapter.fp_or_f_obj_or_stream_to_stream(f.read())
        assert len(_read) == len(template_stream)
        assert _read == template_stream
