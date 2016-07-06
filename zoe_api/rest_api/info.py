# Copyright (c) 2016, Daniele Venzano
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#    http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or
# implied.
# See the License for the specific language governing permissions and
# limitations under the License.

"""The Info API endpoint."""

from flask_restful import Resource

import zoe_api.api_endpoint
from zoe_api.rest_api.utils import catch_exceptions
from zoe_lib.config import get_conf
from zoe_lib.version import ZOE_API_VERSION, ZOE_APPLICATION_FORMAT_VERSION, ZOE_VERSION


class InfoAPI(Resource):
    """The Info API endpoint."""
    def __init__(self, api_endpoint: zoe_api.api_endpoint.APIEndpoint) -> None:
        self.api_endpoint = api_endpoint

    @catch_exceptions
    def get(self):
        """HTTP GET method."""
        ret = {
            'version': ZOE_VERSION,
            'api_version': ZOE_API_VERSION,
            'application_format_version': ZOE_APPLICATION_FORMAT_VERSION,
            'deployment_name': get_conf().deployment_name
        }

        return ret
