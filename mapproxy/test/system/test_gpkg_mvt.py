from __future__ import with_statement, division

import os
import shutil

from mapproxy.request.base import Request
from mapproxy.request.wms import WMS111MapRequest
from mapproxy.request.tile import TMSRequest
from mapproxy.test.http import MockServ
from mapproxy.test.image import is_png, create_tmp_image
from mapproxy.test.system import prepare_env, create_app, module_teardown, SystemTest
from mapproxy.cache.tile import Tile
from mapproxy.test.unit.test_cache_tile import TileCacheTestBase
from mapproxy.cache.geopackage import GeopackageCache, GeopackageLevelCache
from mapproxy.config.loader import load_configuration
from mapproxy.image import ImageSource
from mapproxy.grid import TileGrid
from nose.tools import eq_


test_config = {}

def setup_module():
    prepare_env(test_config, 'cache_gpkg_mvt.yaml')
    shutil.copy(os.path.join(test_config['fixture_dir'], 'cache.gpkg'),
        test_config['base_dir'])
    create_app(test_config)


def teardown_module():
    module_teardown(test_config)


class TestGeopackageCache(SystemTest, TileCacheTestBase):
    config = test_config
    table_name = 'cache'

    def setup(self):
        configuration = load_configuration(self.config.get('config_file'))
        TileCacheTestBase.setup(self)
        self.cache = GeopackageCache(os.path.join(self.cache_dir, 'tmp.geopackage'),
                                     configuration.grids.get('GLOBAL_GEODETIC').tile_grid(),
                                     self.table_name)

    def teardown(self):
        if self.cache:
            self.cache.cleanup()
        TileCacheTestBase.teardown(self)

    def test_get_map_cached(self):
        prepare_env(test_config, 'cache_gpkg_mvt.yaml')
        create_app(test_config)
        SystemTest.setup(self)
        env = {
            'PATH_INFO': '/tms/1.0.0/osm/5/2/3.png',
            'QUERY_STRING': '',
        }
        req = Request(env)
	#self.tms_req = TMSRequest(req)
        #self.common_map_req = WMS111MapRequest(url='/service?', param=dict(service='WMS',
        #                                                                   version='1.1.1', bbox='-180,-80,0,0',
        #                                                                   width='200', height='200',
        #                                                                   layers='gpkg', srs='EPSG:4326',
	#								   format='application/pbf',
	#								   styles='', request='GetMap'))
        resp = self.app.get('/tms/1.0.0/gpkg_cache/0/0/1.pbf',)
        eq_(resp.content_type, 'image/png')
        data = BytesIO(resp.body)
        assert is_png(data)


