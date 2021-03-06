#!/usr/bin/python3

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

"""Zoe Master main entrypoint."""

import logging
import os

import zoe_lib.config as config
from zoe_lib.state import SQLManager
import zoe_master.backends.interface
import zoe_master.scheduler
from zoe_master.exceptions import ZoeException
from zoe_master.gelf_listener import GELFListener
from zoe_master.master_api import APIManager
from zoe_master.metrics.base import StatsManager
from zoe_master.preprocessing import restart_resubmit_scheduler

log = logging.getLogger("main")
LOG_FORMAT = '%(asctime)-15s %(levelname)s %(threadName)s->%(name)s: %(message)s'


def _check_configuration_sanity():
    if not os.path.exists(os.path.join(config.get_conf().workspace_base_path, config.get_conf().workspace_deployment_path)):
        log.error('Workspace base directory does not exist: {}'.format(os.path.join(config.get_conf().workspace_base_path, config.get_conf().workspace_deployment_path)))
        return 1
    return 0


def main(test_conf=None):
    """
    The entrypoint for the zoe-master script.
    :return: int
    """
    config.load_configuration(test_conf)
    args = config.get_conf()

    log_args = {
        'level': logging.DEBUG if args.debug else logging.INFO,
        'format': LOG_FORMAT
    }
    if args.log_file != "stderr":
        log_args['filename'] = args.log_file
    logging.basicConfig(**log_args)

    ret = _check_configuration_sanity()
    if ret != 0:
        return ret

    log.info("Initializing DB manager")
    state = SQLManager(args)

    try:
        zoe_master.backends.interface.initialize_backend(state)
    except ZoeException as e:
        log.error('Cannot initialize backend: {}'.format(e.message))
        return 1

    metrics = StatsManager(state)
    metrics.start()

    log.info("Initializing scheduler")
    scheduler = getattr(zoe_master.scheduler, args.scheduler_class)(state, args.scheduler_policy, metrics)

    restart_resubmit_scheduler(state, scheduler)

    log.info("Starting ZMQ API server...")
    api_server = APIManager(metrics, scheduler, state)

    if config.get_conf().gelf_listener != 0:
        gelf_listener = GELFListener()
    else:
        gelf_listener = None

    try:
        api_server.loop()
    except KeyboardInterrupt:
        pass
    except Exception:
        log.exception('Fatal error in API loop')
    finally:
        scheduler.quit()
        api_server.quit()
        zoe_master.backends.interface.shutdown_backend()
        metrics.quit()
        if gelf_listener is not None:
            gelf_listener.quit()
    return 0
