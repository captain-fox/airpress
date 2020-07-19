import pytest


def test_should_return_true_if_asset_in_pass_package(pkpass):
    asset = ('pass.json', b'00001111')
    pkpass.add_to_pass_package(asset)
    assert 'pass.json' in pkpass


def test_should_return_false_if_asset_not_in_pass_package(pkpass):
    assert 'pass.json' not in pkpass


def test_should_return_new_iterator_over_assets_for_every_iter_call(pkpass_with_assets):
    iterator_1 = iter(pkpass_with_assets)
    iterator_2 = iter(pkpass_with_assets)
    assert iterator_1.__next__() == 'icon.png'
    assert iterator_2.__next__() == 'icon.png'


def test_len_should_return_0_for_pass_without_assets(pkpass):
    assert len(pkpass) == 0


def test_len_should_return_number_of_assets_in_pass_package(pkpass_with_assets):
    assert len(pkpass_with_assets) == 2
