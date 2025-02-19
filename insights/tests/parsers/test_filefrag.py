import doctest
import pytest

from insights.core.exceptions import SkipComponent
from insights.parsers import filefrag
from insights.parsers.filefrag import Filefrag
from insights.tests import context_wrap

FILEFRAG_CONTENT = """
open: No such file or directory
/boot/grub2/grubenv: 1 extent found
/boot/grub2/grubenv: unknow extent found
""".strip()

FILEFRAG_CONTENT_NO_FILE = """
open: No such file or directory
""".strip()

FILEFRAG_CONTENT_ERROR = """
""".strip()


def test_filefrag_1():
    results = Filefrag(context_wrap(FILEFRAG_CONTENT))
    assert results['/boot/grub2/grubenv'] == 1
    assert results.unparsed_lines == ['open: No such file or directory', '/boot/grub2/grubenv: unknow extent found']


def test_filefrag_2():
    results = Filefrag(context_wrap(FILEFRAG_CONTENT_NO_FILE))
    assert results.unparsed_lines == ['open: No such file or directory']


def test_filefrag_errors():
    with pytest.raises(SkipComponent) as ex:
        Filefrag(context_wrap(FILEFRAG_CONTENT_ERROR))
        assert FILEFRAG_CONTENT_ERROR in str(ex)


def test_doc_examples():
    env = {
            'filefrag': Filefrag(context_wrap(FILEFRAG_CONTENT)),
          }
    failed, total = doctest.testmod(filefrag, globs=env)
    assert failed == 0
