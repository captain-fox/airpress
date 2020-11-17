import pytest
from collections.abc import Iterable, MutableMapping, Container, Sized

from airpress.factories import pkpass
from airpress.compressor import PKPass


@pytest.fixture
def _pkpass():
    return pkpass()


def test_container_in(_pkpass):
    _pkpass.add_to_pass_package(('icon.png', b'00001111'))
    assert 'icon.png' in _pkpass


def test_container_not_in(_pkpass):
    assert 'icon.png' not in _pkpass


def test_sized_len_empty(_pkpass):
    assert len(_pkpass) == 0


def test_sized_len(_pkpass):
    _pkpass.add_to_pass_package(('icon.png', b'00001111'))
    assert len(_pkpass) == 1


def test_sized_len_with_duplicates(pkpass_with_two_assets):
    assert len(pkpass_with_two_assets) == 2


def test_iterable(pkpass_with_two_assets):
    iterator = iter(pkpass_with_two_assets)
    next(iterator)
    next(iterator)
    with pytest.raises(StopIteration):
        next(iterator)


def test_item_retrieval(pkpass_with_two_assets):
    assert pkpass_with_two_assets['icon.png'] == b'00001111'
    assert pkpass_with_two_assets['pass.json'] == b'11110000'
    with pytest.raises(KeyError):
        _ = pkpass_with_two_assets['foo.bar']


def test_positive_equal():
    p1 = pkpass(
        ('icon.png', b'00001111'),
        ('pass.json', b'11110000'),
    )
    p2 = pkpass(
        ('icon.png', b'00001111'),
        ('pass.json', b'11110000'),
    )

    assert p1 is not p2
    assert p1 == p2


def test_negative_equal():
    p1 = pkpass(
        ('icon.png', b'00001111'),
        ('pass.json', b'11110000'),
    )
    p2 = pkpass(
        ('icon.png', b'00001111')
    )
    assert p1 is not p2
    assert p1 != p2


@pytest.mark.parametrize('protocol', [
    Iterable,
    Container,
    # MutableMapping,
    Sized,
])
def test_pkpass_is_container(protocol):
    assert issubclass(PKPass, protocol)

