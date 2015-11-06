# coding=utf-8
from __future__ import absolute_import

from mongokit import Document
from mongokit.document import DocumentProperties
import re


# helper funcs
UNCOUNTABLES = {'equipment', 'fish', 'information', 'jeans', 'money', 'rice',
                'series', 'sheep', 'species'}

PLURALS = [
    (r"(?i)(quiz)$", r'\1zes'),
    (r"(?i)^(oxen)$", r'\1'),
    (r"(?i)^(ox)$", r'\1en'),
    (r"(?i)(m|l)ice$", r'\1ice'),
    (r"(?i)(m|l)ouse$", r'\1ice'),
    (r"(?i)(matr|vert|ind)(?:ix|ex)$", r'\1ices'),
    (r"(?i)(x|ch|ss|sh)$", r'\1es'),
    (r"(?i)([^aeiouy]|qu)y$", r'\1ies'),
    (r"(?i)(hive)$", r'\1s'),
    (r"(?i)([lr])f$", r'\1ves'),
    (r"(?i)([^f])fe$", r'\1ves'),
    (r"(?i)sis$", 'ses'),
    (r"(?i)([ti])a$", r'\1a'),
    (r"(?i)([ti])um$", r'\1a'),
    (r"(?i)(buffal|tomat)o$", r'\1oes'),
    (r"(?i)(bu)s$", r'\1ses'),
    (r"(?i)(alias|status)$", r'\1es'),
    (r"(?i)(octop|vir)i$", r'\1i'),
    (r"(?i)(octop|vir)us$", r'\1i'),
    (r"(?i)^(ax|test)is$", r'\1es'),
    (r"(?i)s$", 's'),
    (r"$", 's'),
]


def pluralize(word):
    """
    Return the plural form of a word.

    Examples::

        >>> pluralize("post")
        "posts"
        >>> pluralize("octopus")
        "octopi"
        >>> pluralize("sheep")
        "sheep"
        >>> pluralize("CamelOctopus")
        "CamelOctopi"

    """
    if not word or word.lower() in UNCOUNTABLES:
        return word
    else:
        for rule, replacement in PLURALS:
            if re.search(rule, word):
                return re.sub(rule, replacement, word)
        return word


def underscore(word):
    """
    Make an underscored, lowercase form from the expression in the string.

    Example::

        >>> underscore("DeviceType")
        "device_type"

    """
    word = re.sub(r"([A-Z]+)([A-Z][a-z])", r'\1_\2', word)
    word = re.sub(r"([a-z\d])([A-Z])", r'\1_\2', word)
    word = word.replace("-", "_")
    return word.lower()


class MetaDoc(DocumentProperties):
    def __init__(cls, name, bases, attrs):
        super(MetaDoc, cls).__init__(name, bases, attrs)
        if not name.startswith('Callable'):
            if '__collection__' not in cls.__dict__:
                cls.__collection__ = pluralize(underscore(cls.__name__))
        return


class BaseDocument(Document):
    __metaclass__ = MetaDoc
    use_schemaless = False
