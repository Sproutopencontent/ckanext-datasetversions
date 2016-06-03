import unittest

from ckanext.datasetversions.plugin import DatasetversionsPlugin


class TestHelpers(unittest.TestCase):
    def test_list_versions(self):
        plugin = DatasetversionsPlugin()

        package = {'_versions': ['v3', 'v2', 'v1']}

        versions = plugin.get_helpers()['datasetversions_list'](package)

        self.assertEquals(versions, ['v3', 'v2', 'v1'])
