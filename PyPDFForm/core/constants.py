# -*- coding: utf-8 -*-


class Template(object):
    @property
    def annotation_key(self) -> str:
        """Used for extracting elements from pdfrw parsed PDF form."""

        return "/Annots"

    @property
    def annotation_field_key(self) -> str:
        """Used for extracting elements from pdfrw parsed PDF form."""

        return "/T"

    @property
    def annotation_rectangle_key(self) -> str:
        """Used for extracting elements from pdfrw parsed PDF form."""

        return "/Rect"

    @property
    def subtype_key(self) -> str:
        """Used for extracting elements from pdfrw parsed PDF form."""

        return "/Subtype"

    @property
    def widget_subtype_key(self) -> str:
        """Used for extracting elements from pdfrw parsed PDF form."""

        return "/Widget"

    @property
    def element_type_key(self) -> str:
        """Used for extracting elements from pdfrw parsed PDF form."""

        return "/FT"


class Filler(object):
    @property
    def text_field_value_key(self) -> str:
        """Used for extracting text field value for pdfrw parsed PDF form."""

        return "/V"

    @property
    def checkbox_field_value_key(self) -> str:
        """Used for extracting checkbox field value for pdfrw parsed PDF form."""

        return "/AS"
