# -*- coding: utf-8 -*-

import os
import uuid

import pdfrw
import pytest

from PyPDFForm.core.constants import Merge as MergeCoreConstants
from PyPDFForm.core.constants import Template as TemplateCoreConstants
from PyPDFForm.core.template import Template as TemplateCore
from PyPDFForm.middleware.element import Element, ElementType
from PyPDFForm.middleware.exceptions.template import InvalidTemplateError
from PyPDFForm.middleware.template import Template as TemplateMiddleware


@pytest.fixture
def pdf_samples():
    return os.path.join(os.path.dirname(__file__), "..", "..", "pdf_samples")


@pytest.fixture
def template_stream(pdf_samples):
    with open(os.path.join(pdf_samples, "sample_template.pdf"), "rb+") as f:
        return f.read()


@pytest.fixture
def template_with_radiobutton_stream(pdf_samples):
    with open(
        os.path.join(pdf_samples, "sample_template_with_radio_button.pdf"), "rb+"
    ) as f:
        return f.read()


@pytest.fixture
def data_dict():
    return {
        "test": False,
        "check": False,
        "radio_1": False,
        "test_2": False,
        "check_2": False,
        "radio_2": False,
        "test_3": False,
        "check_3": False,
        "radio_3": False,
    }


def test_validate_template():
    bad_inputs = [""]

    try:
        TemplateMiddleware().validate_template(*bad_inputs)
        assert False
    except InvalidTemplateError:
        assert True


def test_validate_template_stream(template_stream):
    try:
        TemplateMiddleware().validate_stream(b"")
        assert False
    except InvalidTemplateError:
        assert True

    TemplateMiddleware().validate_stream(template_stream)
    assert True


def test_remove_all_elements(template_stream):
    result = TemplateCore().remove_all_elements(template_stream)
    assert not TemplateCore().iterate_elements(result)


def test_iterate_elements_and_get_element_key(
    template_with_radiobutton_stream, data_dict
):
    for each in TemplateCore().iterate_elements(template_with_radiobutton_stream):
        data_dict[TemplateCore().get_element_key(each)] = True

    for k in data_dict.keys():
        assert data_dict[k]


def test_iterate_elements_and_get_element_key_v2(
    template_with_radiobutton_stream, data_dict
):
    assert TemplateCore().get_element_key_v2(pdfrw.PdfDict()) is None
    for each in TemplateCore().iterate_elements(template_with_radiobutton_stream):
        data_dict[TemplateCore().get_element_key_v2(each)] = True

    for k in data_dict.keys():
        assert data_dict[k]


def test_iterate_elements_and_get_element_key_sejda(sejda_template, sejda_data):
    data_dict = {key: False for key in sejda_data.keys()}
    for each in TemplateCore().iterate_elements(sejda_template, sejda=True):
        data_dict[TemplateCore().get_element_key(each, sejda=True)] = True

    for k in data_dict.keys():
        assert data_dict[k]


def test_iterate_elements_and_get_element_key_v2_sejda(sejda_template, sejda_data):
    data_dict = {key: False for key in sejda_data.keys()}
    for each in TemplateCore().iterate_elements(sejda_template, sejda=True):
        data_dict[TemplateCore().get_element_key_v2(each)] = True

    for k in data_dict.keys():
        assert data_dict[k]


def test_get_elements_by_page_sejda(sejda_template):
    expected = {
        1: {
            "date": False,
            "year": False,
            "buyer_name": False,
            "buyer_address": False,
            "seller_name": False,
            "seller_address": False,
            "make": False,
            "model": False,
            "caliber": False,
            "serial_number": False,
            "purchase_option": False,
            "date_of_this_bill": False,
            "at_future_date": False,
            "other": False,
            "other_reason": False,
            "future_date": False,
            "future_year": False,
            "exchange_for": False,
        },
        2: {
            "buyer_name_printed": False,
            "seller_name_printed": False,
            "buyer_signed_date": False,
            "seller_signed_date": False,
            "buyer_dl_number": False,
            "seller_dl_number": False,
            "buyer_dl_state": False,
            "seller_dl_state": False,
        },
    }

    for page, elements in (
        TemplateCore().get_elements_by_page(sejda_template, sejda=True).items()
    ):
        for each in elements:
            expected[page][TemplateCore().get_element_key(each, sejda=True)] = True

    for page, elements in expected.items():
        for k in elements.keys():
            assert expected[page][k]


def test_get_elements_by_page_sejda_v2(sejda_template):
    expected = {
        1: {
            "date": False,
            "year": False,
            "buyer_name": False,
            "buyer_address": False,
            "seller_name": False,
            "seller_address": False,
            "make": False,
            "model": False,
            "caliber": False,
            "serial_number": False,
            "purchase_option": False,
            "date_of_this_bill": False,
            "at_future_date": False,
            "other": False,
            "other_reason": False,
            "future_date": False,
            "future_year": False,
            "exchange_for": False,
        },
        2: {
            "buyer_name_printed": False,
            "seller_name_printed": False,
            "buyer_signed_date": False,
            "seller_signed_date": False,
            "buyer_dl_number": False,
            "seller_dl_number": False,
            "buyer_dl_state": False,
            "seller_dl_state": False,
        },
    }

    for page, elements in (
        TemplateCore().get_elements_by_page_v2(sejda_template).items()
    ):
        for each in elements:
            expected[page][TemplateCore().get_element_key(each, sejda=True)] = True

    for page, elements in expected.items():
        for k in elements.keys():
            assert expected[page][k]


def test_get_elements_by_page(template_with_radiobutton_stream):
    expected = {
        1: {
            "test": False,
            "check": False,
            "radio_1": False,
        },
        2: {
            "test_2": False,
            "check_2": False,
            "radio_2": False,
        },
        3: {
            "test_3": False,
            "check_3": False,
            "radio_3": False,
        },
    }

    for page, elements in (
        TemplateCore().get_elements_by_page(template_with_radiobutton_stream).items()
    ):
        for each in elements:
            expected[page][TemplateCore().get_element_key(each)] = True

    for page, elements in expected.items():
        for k in elements.keys():
            assert expected[page][k]


def test_get_elements_by_page_v2(template_with_radiobutton_stream):
    expected = {
        1: {
            "test": False,
            "check": False,
            "radio_1": False,
        },
        2: {
            "test_2": False,
            "check_2": False,
            "radio_2": False,
        },
        3: {
            "test_3": False,
            "check_3": False,
            "radio_3": False,
        },
    }

    for page, elements in (
        TemplateCore().get_elements_by_page_v2(template_with_radiobutton_stream).items()
    ):
        for each in elements:
            expected[page][TemplateCore().get_element_key(each)] = True

    for page, elements in expected.items():
        for k in elements.keys():
            assert expected[page][k]


def test_get_element_type_sejda(sejda_template):
    type_mapping = {
        "date": ElementType.text,
        "year": ElementType.text,
        "buyer_name": ElementType.text,
        "buyer_address": ElementType.text,
        "seller_name": ElementType.text,
        "seller_address": ElementType.text,
        "make": ElementType.text,
        "model": ElementType.text,
        "caliber": ElementType.text,
        "serial_number": ElementType.text,
        "purchase_option": ElementType.radio,
        "date_of_this_bill": ElementType.checkbox,
        "at_future_date": ElementType.checkbox,
        "other": ElementType.checkbox,
        "other_reason": ElementType.text,
        "payment_amount": ElementType.text,
        "future_date": ElementType.text,
        "future_year": ElementType.text,
        "exchange_for": ElementType.text,
        "buyer_name_printed": ElementType.text,
        "seller_name_printed": ElementType.text,
        "buyer_signed_date": ElementType.text,
        "seller_signed_date": ElementType.text,
        "buyer_dl_number": ElementType.text,
        "seller_dl_number": ElementType.text,
        "buyer_dl_state": ElementType.text,
        "seller_dl_state": ElementType.text,
    }

    for each in TemplateCore().iterate_elements(sejda_template, sejda=True):
        assert type_mapping[
            TemplateCore().get_element_key(each, sejda=True)
        ] == TemplateCore().get_element_type(each, sejda=True)

    read_template_stream = pdfrw.PdfReader(fdata=sejda_template)

    for each in TemplateCore().iterate_elements(read_template_stream):
        assert type_mapping[
            TemplateCore().get_element_key(each, sejda=True)
        ] == TemplateCore().get_element_type(each, sejda=True)


def test_get_element_type_v2_sejda(sejda_template):
    type_mapping = {
        "date": ElementType.text,
        "year": ElementType.text,
        "buyer_name": ElementType.text,
        "buyer_address": ElementType.text,
        "seller_name": ElementType.text,
        "seller_address": ElementType.text,
        "make": ElementType.text,
        "model": ElementType.text,
        "caliber": ElementType.text,
        "serial_number": ElementType.text,
        "purchase_option": ElementType.radio,
        "date_of_this_bill": ElementType.checkbox,
        "at_future_date": ElementType.checkbox,
        "other": ElementType.checkbox,
        "other_reason": ElementType.text,
        "payment_amount": ElementType.text,
        "future_date": ElementType.text,
        "future_year": ElementType.text,
        "exchange_for": ElementType.text,
        "buyer_name_printed": ElementType.text,
        "seller_name_printed": ElementType.text,
        "buyer_signed_date": ElementType.text,
        "seller_signed_date": ElementType.text,
        "buyer_dl_number": ElementType.text,
        "seller_dl_number": ElementType.text,
        "buyer_dl_state": ElementType.text,
        "seller_dl_state": ElementType.text,
    }

    for each in TemplateCore().iterate_elements(sejda_template, sejda=True):
        assert type_mapping[
            TemplateCore().get_element_key_v2(each)
        ] == TemplateCore().get_element_type_v2(each)

    read_template_stream = pdfrw.PdfReader(fdata=sejda_template)

    for each in TemplateCore().iterate_elements(read_template_stream):
        assert type_mapping[
            TemplateCore().get_element_key_v2(each)
        ] == TemplateCore().get_element_type_v2(each)


def test_get_element_type(template_stream):
    type_mapping = {
        "test": ElementType.text,
        "check": ElementType.checkbox,
        "test_2": ElementType.text,
        "check_2": ElementType.checkbox,
        "test_3": ElementType.text,
        "check_3": ElementType.checkbox,
    }

    for each in TemplateCore().iterate_elements(template_stream):
        assert type_mapping[
            TemplateCore().get_element_key(each)
        ] == TemplateCore().get_element_type(each)

    read_template_stream = pdfrw.PdfReader(fdata=template_stream)

    for each in TemplateCore().iterate_elements(read_template_stream):
        assert type_mapping[
            TemplateCore().get_element_key(each)
        ] == TemplateCore().get_element_type(each)


def test_get_element_type_v2(template_stream):
    assert TemplateCore().get_element_type_v2(pdfrw.PdfDict()) is None

    type_mapping = {
        "test": ElementType.text,
        "check": ElementType.checkbox,
        "test_2": ElementType.text,
        "check_2": ElementType.checkbox,
        "test_3": ElementType.text,
        "check_3": ElementType.checkbox,
    }

    for each in TemplateCore().iterate_elements(template_stream):
        assert type_mapping[
            TemplateCore().get_element_key_v2(each)
        ] == TemplateCore().get_element_type_v2(each)

    read_template_stream = pdfrw.PdfReader(fdata=template_stream)

    for each in TemplateCore().iterate_elements(read_template_stream):
        assert type_mapping[
            TemplateCore().get_element_key_v2(each)
        ] == TemplateCore().get_element_type_v2(each)


def test_get_element_type_radiobutton(template_with_radiobutton_stream):
    type_mapping = {
        "test": ElementType.text,
        "check": ElementType.checkbox,
        "test_2": ElementType.text,
        "check_2": ElementType.checkbox,
        "test_3": ElementType.text,
        "check_3": ElementType.checkbox,
        "radio_1": ElementType.radio,
        "radio_2": ElementType.radio,
        "radio_3": ElementType.radio,
    }

    for each in TemplateCore().iterate_elements(template_with_radiobutton_stream):
        assert type_mapping[
            TemplateCore().get_element_key(each)
        ] == TemplateCore().get_element_type(each)

    read_template_stream = pdfrw.PdfReader(fdata=template_with_radiobutton_stream)

    for each in TemplateCore().iterate_elements(read_template_stream):
        assert type_mapping[
            TemplateCore().get_element_key(each)
        ] == TemplateCore().get_element_type(each)


def test_get_element_type_v2_radiobutton(template_with_radiobutton_stream):
    type_mapping = {
        "test": ElementType.text,
        "check": ElementType.checkbox,
        "test_2": ElementType.text,
        "check_2": ElementType.checkbox,
        "test_3": ElementType.text,
        "check_3": ElementType.checkbox,
        "radio_1": ElementType.radio,
        "radio_2": ElementType.radio,
        "radio_3": ElementType.radio,
    }

    for each in TemplateCore().iterate_elements(template_with_radiobutton_stream):
        assert type_mapping[
            TemplateCore().get_element_key_v2(each)
        ] == TemplateCore().get_element_type_v2(each)

    read_template_stream = pdfrw.PdfReader(fdata=template_with_radiobutton_stream)

    for each in TemplateCore().iterate_elements(read_template_stream):
        assert type_mapping[
            TemplateCore().get_element_key_v2(each)
        ] == TemplateCore().get_element_type_v2(each)


def test_build_elements(template_with_radiobutton_stream, data_dict):
    for k, v in (
        TemplateMiddleware().build_elements(template_with_radiobutton_stream).items()
    ):
        if k in data_dict and k == v.name:
            data_dict[k] = True

    for k in data_dict.keys():
        assert data_dict[k]


def test_build_elements_v2(template_with_radiobutton_stream, data_dict):
    for k, v in (
        TemplateMiddleware().build_elements_v2(template_with_radiobutton_stream).items()
    ):
        if k in data_dict and k == v.name:
            data_dict[k] = True

    for k in data_dict.keys():
        assert data_dict[k]


def test_build_elements_sejda(sejda_template, sejda_data):
    data_dict = {key: False for key in sejda_data.keys()}

    for k, v in TemplateMiddleware().build_elements(sejda_template, sejda=True).items():
        if k in data_dict and k == v.name:
            data_dict[k] = True

    for k in data_dict.keys():
        assert data_dict[k]


def test_build_elements_v2_sejda(sejda_template, sejda_data):
    data_dict = {key: False for key in sejda_data.keys()}

    for k, v in TemplateMiddleware().build_elements_v2(sejda_template).items():
        if k in data_dict and k == v.name:
            data_dict[k] = True

    for k in data_dict.keys():
        assert data_dict[k]


def test_build_elements_v2_with_comb_text_field(
    sample_template_with_max_length_text_field, sample_template_with_comb_text_field
):
    result = TemplateMiddleware().build_elements_v2(
        sample_template_with_max_length_text_field
    )
    assert result["LastName"].max_length == 8
    assert result["LastName"].comb is None

    result = TemplateMiddleware().build_elements_v2(
        sample_template_with_comb_text_field
    )
    assert result["LastName"].max_length == 7
    assert result["LastName"].comb is True


def test_get_draw_checkbox_radio_coordinates(sejda_template):
    for element in TemplateCore().iterate_elements(sejda_template):
        assert TemplateCore().get_draw_checkbox_radio_coordinates(element) == (
            (
                float(element[TemplateCoreConstants().annotation_rectangle_key][0])
                + float(element[TemplateCoreConstants().annotation_rectangle_key][2])
            )
            / 2
            - 5,
            (
                float(element[TemplateCoreConstants().annotation_rectangle_key][1])
                + float(element[TemplateCoreConstants().annotation_rectangle_key][3])
            )
            / 2
            - 4,
        )


def test_assign_uuid(template_with_radiobutton_stream, data_dict):
    for element in TemplateCore().iterate_elements(
        TemplateCore().assign_uuid(template_with_radiobutton_stream)
    ):
        key = TemplateCore().get_element_key(element)
        assert MergeCoreConstants().separator in key

        key, _uuid = key.split(MergeCoreConstants().separator)

        assert len(_uuid) == len(uuid.uuid4().hex)
        data_dict[key] = True

    for k in data_dict.keys():
        assert data_dict[k]


def test_traverse_pattern(template_with_radiobutton_stream):
    _data_dict = {
        "test": "text",
        "check": "check",
        "radio_1": "radio",
        "test_2": "text",
        "check_2": "check",
        "radio_2": "radio",
        "test_3": "text",
        "check_3": "check",
        "radio_3": "radio",
    }

    type_to_pattern = {
        "text": {TemplateCoreConstants().annotation_field_key: True},
        "check": {TemplateCoreConstants().annotation_field_key: True},
        "radio": {
            TemplateCoreConstants().parent_key: {
                TemplateCoreConstants().annotation_field_key: True
            }
        },
    }

    for each in TemplateCore().iterate_elements(template_with_radiobutton_stream):
        key = TemplateCore().get_element_key(each)
        pattern = type_to_pattern[_data_dict[key]]
        assert TemplateCore().traverse_pattern(pattern, each)[1:-1] == key


def test_traverse_pattern_sejda(sejda_template):
    pattern = {
        TemplateCoreConstants().parent_key: {
            TemplateCoreConstants().annotation_field_key: True
        }
    }

    for each in TemplateCore().iterate_elements(sejda_template):
        key = TemplateCore().get_element_key(each)
        assert TemplateCore().traverse_pattern(pattern, each)[1:-1] == key


def test_find_pattern_match(template_with_radiobutton_stream):
    _data_dict = {
        "test": "text",
        "check": "check",
        "radio_1": "radio",
        "test_2": "text",
        "check_2": "check",
        "radio_2": "radio",
        "test_3": "text",
        "check_3": "check",
        "radio_3": "radio",
    }

    type_to_pattern = {
        "text": (
            {
                TemplateCoreConstants()
                .element_type_key: TemplateCoreConstants()
                .text_field_identifier
            },
        ),
        "check": (
            {
                TemplateCoreConstants()
                .element_type_key: TemplateCoreConstants()
                .selectable_identifier
            },
        ),
        "radio": (
            {
                TemplateCoreConstants().parent_key: {
                    TemplateCoreConstants()
                    .element_type_key: TemplateCoreConstants()
                    .selectable_identifier
                }
            },
        ),
    }

    for each in TemplateCore().iterate_elements(template_with_radiobutton_stream):
        key = TemplateCore().get_element_key(each)
        patterns = type_to_pattern[_data_dict[key]]
        check = True
        for pattern in patterns:
            check = check and TemplateCore().find_pattern_match(pattern, each)
        assert check


def test_find_pattern_match_sejda(sejda_template, sejda_data):
    _data_dict = {}
    for key, value in sejda_data.items():
        _type = None
        if isinstance(value, str):
            _type = "text"
        if isinstance(value, int):
            _type = "radio"
        if isinstance(value, bool):
            _type = "check"
        _data_dict[key] = _type

    type_to_pattern = {
        "text": (
            {
                TemplateCoreConstants().parent_key: {
                    TemplateCoreConstants()
                    .element_type_key: TemplateCoreConstants()
                    .text_field_identifier
                }
            },
        ),
        "check": (
            {
                TemplateCoreConstants().parent_key: {
                    TemplateCoreConstants()
                    .element_type_key: TemplateCoreConstants()
                    .selectable_identifier
                }
            },
            {
                TemplateCoreConstants().parent_key: {
                    TemplateCoreConstants()
                    .subtype_key: TemplateCoreConstants()
                    .widget_subtype_key
                }
            },
        ),
        "radio": (
            {
                TemplateCoreConstants().parent_key: {
                    TemplateCoreConstants()
                    .element_type_key: TemplateCoreConstants()
                    .selectable_identifier
                }
            },
        ),
    }

    for each in TemplateCore().iterate_elements(sejda_template):
        key = TemplateCore().get_element_key(each, sejda=True)
        patterns = type_to_pattern[_data_dict[key]]
        check = True
        for pattern in patterns:
            check = check and TemplateCore().find_pattern_match(pattern, each)
        assert check


def test_get_text_field_max_length(sample_template_with_max_length_text_field):
    for _page, elements in (
        TemplateCore()
        .get_elements_by_page_v2(sample_template_with_max_length_text_field)
        .items()
    ):
        for element in elements:
            assert TemplateCore().get_text_field_max_length(element) is (
                8 if TemplateCore().get_element_key_v2(element) == "LastName" else None
            )


def test_is_text_field_comb(sample_template_with_comb_text_field):
    for _page, elements in (
        TemplateCore()
        .get_elements_by_page_v2(sample_template_with_comb_text_field)
        .items()
    ):
        for element in elements:
            assert TemplateCore().get_text_field_max_length(element) is (
                7 if TemplateCore().get_element_key_v2(element) == "LastName" else None
            )
            if TemplateCore().get_element_key_v2(element) == "LastName":
                assert TemplateCore().is_text_field_comb(element) is True


def test_font_size_for_text_field_with_max_length(sample_template_with_comb_text_field):
    for _page, elements in (
        TemplateCore()
        .get_elements_by_page_v2(sample_template_with_comb_text_field)
        .items()
    ):
        for element in elements:
            if TemplateCore().get_element_key_v2(element) == "LastName":
                assert isinstance(
                    TemplateCore().font_size_for_text_field_with_max_length(element, 7),
                    float,
                )
