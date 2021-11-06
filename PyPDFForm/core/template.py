# -*- coding: utf-8 -*-
"""Contains helpers for template."""

import uuid
from typing import Dict, List, Tuple, Union

import pdfrw

from ..middleware.element import ElementType
from .constants import Merge as MergeConstants
from .constants import Template as TemplateCoreConstants
from .patterns import ELEMENT_KEY_PATTERNS, ELEMENT_TYPE_PATTERNS
from .utils import Utils


class Template:
    """Contains methods for interacting with a pdfrw parsed PDF form."""

    @staticmethod
    def remove_all_elements(pdf: bytes) -> bytes:
        """Removes all elements from a pdfrw parsed PDF form."""

        pdf = pdfrw.PdfReader(fdata=pdf)

        for i in range(len(pdf.pages)):
            elements = pdf.pages[i][TemplateCoreConstants().annotation_key]
            if elements:
                for j in reversed(range(len(elements))):
                    elements.pop(j)

        return Utils().generate_stream(pdf)

    @staticmethod
    def iterate_elements(
        pdf: Union[bytes, "pdfrw.PdfReader"], sejda: bool = False
    ) -> List["pdfrw.PdfDict"]:
        """Iterates through a PDF and returns all elements found."""

        if isinstance(pdf, bytes):
            pdf = pdfrw.PdfReader(fdata=pdf)

        result = []

        for i in range(len(pdf.pages)):
            elements = pdf.pages[i][TemplateCoreConstants().annotation_key]
            if elements:
                for element in elements:
                    if not sejda:
                        if (
                            element[TemplateCoreConstants().subtype_key]
                            == TemplateCoreConstants().widget_subtype_key
                            and element[TemplateCoreConstants().annotation_field_key]
                        ):
                            result.append(element)
                        elif (
                            element[TemplateCoreConstants().checkbox_field_value_key]
                            and element[TemplateCoreConstants().parent_key]
                        ):
                            result.append(element)
                    else:
                        if (
                            element[TemplateCoreConstants().parent_key]
                            and element[TemplateCoreConstants().parent_key][
                                TemplateCoreConstants().element_type_key
                            ]
                        ):
                            result.append(element)

        return result

    @staticmethod
    def get_elements_by_page(
        pdf: Union[bytes, "pdfrw.PdfReader"], sejda: bool = False
    ) -> Dict[int, List["pdfrw.PdfDict"]]:
        """Iterates through a PDF and returns all elements found grouped by page."""

        if isinstance(pdf, bytes):
            pdf = pdfrw.PdfReader(fdata=pdf)

        result = {}

        for i in range(len(pdf.pages)):
            elements = pdf.pages[i][TemplateCoreConstants().annotation_key]
            result[i + 1] = []
            if elements:
                for element in elements:
                    if not sejda:
                        if (
                            element[TemplateCoreConstants().subtype_key]
                            == TemplateCoreConstants().widget_subtype_key
                            and element[TemplateCoreConstants().annotation_field_key]
                        ):
                            result[i + 1].append(element)
                        elif (
                            element[TemplateCoreConstants().checkbox_field_value_key]
                            and element[TemplateCoreConstants().parent_key]
                        ):
                            result[i + 1].append(element)
                    else:
                        if (
                            element[TemplateCoreConstants().parent_key]
                            and element[TemplateCoreConstants().parent_key][
                                TemplateCoreConstants().element_type_key
                            ]
                        ):
                            result[i + 1].append(element)

        return result

    def get_elements_by_page_v2(
        self, pdf: Union[bytes, "pdfrw.PdfReader"]
    ) -> Dict[int, List["pdfrw.PdfDict"]]:
        """Iterates through a PDF and returns all elements found grouped by page."""

        if isinstance(pdf, bytes):
            pdf = pdfrw.PdfReader(fdata=pdf)

        result = {}

        for i in range(len(pdf.pages)):
            elements = pdf.pages[i][TemplateCoreConstants().annotation_key]
            result[i + 1] = []
            if elements:
                for element in elements:
                    for each in ELEMENT_TYPE_PATTERNS:
                        patterns = each[0]
                        check = True
                        for pattern in patterns:
                            check = check and self.find_pattern_match(pattern, element)
                        if check:
                            result[i + 1].append(element)
                            break

        return result

    @staticmethod
    def get_element_key(element: "pdfrw.PdfDict", sejda: bool = False) -> str:
        """Returns its annotated key given a PDF form element."""

        if sejda:
            return element[TemplateCoreConstants().parent_key][
                TemplateCoreConstants().annotation_field_key
            ][1:-1]

        if not element[TemplateCoreConstants().annotation_field_key]:
            return element[TemplateCoreConstants().parent_key][
                TemplateCoreConstants().annotation_field_key
            ][1:-1]

        return element[TemplateCoreConstants().annotation_field_key][1:-1]

    def traverse_pattern(
        self, pattern: dict, element: "pdfrw.PdfDict"
    ) -> Union[str, None]:
        """Traverses down a PDF dict pattern and find the value."""

        for key, value in element.items():
            result = None
            if key in pattern:
                if isinstance(pattern[key], dict) and isinstance(value, pdfrw.PdfDict):
                    result = self.traverse_pattern(pattern[key], value)
                else:
                    if pattern[key] is True and value:
                        return value
            if result:
                return result
        return None

    def get_element_key_v2(self, element: "pdfrw.PdfDict") -> Union[str, None]:
        """Finds a PDF element's annotated key by pattern matching."""

        for pattern in ELEMENT_KEY_PATTERNS:
            value = self.traverse_pattern(pattern, element)
            if value:
                return value[1:-1]

        return None

    @staticmethod
    def get_element_type(
        element: "pdfrw.PdfDict", sejda: bool = False
    ) -> Union["ElementType", None]:
        """Returns its annotated type given a PDF form element."""

        if sejda:
            if (
                element[TemplateCoreConstants().parent_key][
                    TemplateCoreConstants().element_type_key
                ]
                == TemplateCoreConstants().text_field_identifier
            ):
                return ElementType.text
            if (
                element[TemplateCoreConstants().parent_key][
                    TemplateCoreConstants().element_type_key
                ]
                == TemplateCoreConstants().selectable_identifier
            ):
                if (
                    element[TemplateCoreConstants().parent_key][
                        TemplateCoreConstants().subtype_key
                    ]
                    == TemplateCoreConstants().widget_subtype_key
                ):
                    return ElementType.checkbox
                return ElementType.radio

        element_type_mapping = {
            TemplateCoreConstants().selectable_identifier: ElementType.checkbox,
            TemplateCoreConstants().text_field_identifier: ElementType.text,
        }

        result = element_type_mapping.get(
            str(element[TemplateCoreConstants().element_type_key])
        )

        if not result and element[TemplateCoreConstants().parent_key]:
            return ElementType.radio

        return result or ElementType.text

    def find_pattern_match(self, pattern: dict, element: "pdfrw.PdfDict") -> bool:
        """Checks if a PDF dict pattern exists in a PDF element."""

        for key, value in element.items():
            result = False
            if key in pattern:
                if isinstance(pattern[key], dict) and isinstance(value, pdfrw.PdfDict):
                    result = self.find_pattern_match(pattern[key], value)
                else:
                    result = pattern[key] == value
            if result:
                return result
        return False

    def get_element_type_v2(
        self, element: "pdfrw.PdfDict"
    ) -> Union["ElementType", None]:
        """Finds a PDF element's annotated type by pattern matching."""

        for each in ELEMENT_TYPE_PATTERNS:
            patterns, _type = each
            check = True
            for pattern in patterns:
                check = check and self.find_pattern_match(pattern, element)
            if check:
                return _type

        return None

    @staticmethod
    def get_draw_checkbox_radio_coordinates(
        element: "pdfrw.PdfDict",
    ) -> Tuple[Union[float, int], Union[float, int]]:
        """Returns coordinates to draw at given a PDF form checkbox/radio element."""

        return (
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

    @staticmethod
    def get_draw_checkbox_radio_coordinates_v2(
        element: "pdfrw.PdfDict",
        font_size: Union[float, int],
    ) -> Tuple[Union[float, int], Union[float, int]]:
        """Returns coordinates to draw at given a PDF form checkbox/radio element."""

        side = font_size * 96 / 72
        c_half_width = (
            float(element[TemplateCoreConstants().annotation_rectangle_key][0])
            + float(element[TemplateCoreConstants().annotation_rectangle_key][2])
        ) / 2
        c_half_height = (
            float(element[TemplateCoreConstants().annotation_rectangle_key][1])
            + float(element[TemplateCoreConstants().annotation_rectangle_key][3])
        ) / 2

        return (
            (c_half_width - side / 2 + c_half_width) / 2,
            (c_half_height - side / 2 + c_half_height) / 2,
        )

    @staticmethod
    def get_draw_text_coordinates(
        element: "pdfrw.PdfDict",
    ) -> Tuple[Union[float, int], Union[float, int]]:
        """Returns coordinates to draw text at given a PDF form text element."""

        return (
            float(element[TemplateCoreConstants().annotation_rectangle_key][0]),
            (
                float(element[TemplateCoreConstants().annotation_rectangle_key][1])
                + float(element[TemplateCoreConstants().annotation_rectangle_key][3])
            )
            / 2
            - 2,
        )

    def assign_uuid(self, pdf: bytes) -> bytes:
        """Appends a separator and uuid after each element's annotated name."""

        _uuid = uuid.uuid4().hex

        pdf_file = pdfrw.PdfReader(fdata=pdf)

        for element in self.iterate_elements(pdf_file):
            base_key = self.get_element_key(element)
            existed_uuid = ""
            if MergeConstants().separator in base_key:
                base_key, existed_uuid = base_key.split(MergeConstants().separator)

            update_dict = {
                TemplateCoreConstants().annotation_field_key.replace(
                    "/", ""
                ): "{}{}{}".format(
                    base_key, MergeConstants().separator, existed_uuid or _uuid
                )
            }
            element.update(pdfrw.PdfDict(**update_dict))

        return Utils().generate_stream(pdf_file)
