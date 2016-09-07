from io import BytesIO

from mapproxy.test.http import mock_httpd
from mapproxy.test.image import is_jpeg, tmp_image
from mapproxy.test.vector import is_vector_tile
from mapproxy.test.system import (
    module_setup,
    module_teardown,
    SystemTest,
    make_base_config
)
from nose.tools import eq_

test_config = {}
base_config = make_base_config(test_config)


# TODO: pull from a gpkg instead of tegola

def setup_module():
    module_setup(test_config, 'cache_gpkg_mvt.yaml', with_cache_data=True)

def teardown_module():
    module_teardown(test_config)

class TestTegola(SystemTest):
    config = test_config

    def test_get_cached_tile_content_type(self):
        resp = self.app.get('/tms/1.0.0/terranodo/webmercator/15/17031/1109.pbf')
        eq_(resp.content_type, 'application/x-protobuf')

    def test_get_cached_tile_content_length(self):
        resp = self.app.get('/tms/1.0.0/terranodo/webmercator/15/17031/1109.pbf')
        eq_(resp.content_length, len(resp.body))

    def test_get_cached_tile_is_vector_tile(self):
        resp = self.app.get('/tms/1.0.0/terranodo/webmercator/15/17031/1109.pbf')
        data = BytesIO(resp.body)

	assert is_vector_tile(data)
