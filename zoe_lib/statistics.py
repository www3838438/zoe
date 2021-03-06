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

"""
This module contains the Zoe Statistics API.
"""

import logging

from zoe_lib.api_base import ZoeAPIBase
from zoe_lib.exceptions import ZoeAPIException

log = logging.getLogger(__name__)


class ZoeStatisticsAPI(ZoeAPIBase):
    """
    The Statistics API class. This API exports dynamic information about Zoe inner status and counters.
    """
    def scheduler(self):
        """
        Queries Zoe for scheduler statistics.

        :return:
        """
        data, status_code = self._rest_get('/statistics/scheduler')
        if status_code != 200:
            raise ZoeAPIException(data['message'])
        else:
            return data
