# -*- coding: utf-8 -*-

# Copyright (c) 2015 Ericsson AB
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

from calvin.actor.actor import Actor, manage, condition, stateguard, calvinsys
from calvin.utilities.calvinlogger import get_logger

_log = get_logger(__name__)


class HTTPGetS(Actor):
    """
    HTTP method GET

    Input:
        data : execute request, if data is non-null, it is added in request
    Output:
      status: status of request
      headers: JSON dictionary of incoming headers
      body : body of response (if any)
    """

    @manage(['command'])
    def init(self, url, headers, auth):
        self.command = calvinsys.open(self, "http.get", url=url, headers=headers or None, auth=auth or None)

    @stateguard(lambda actor: calvinsys.can_write(actor.command))
    @condition(["data"],[])
    def execute_command(self, data):
        calvinsys.write(self.command, data)
        
    @stateguard(lambda actor: calvinsys.can_read(actor.command))
    @condition([], ["status", "headers", "body"])
    def send_result(self):
        result = calvinsys.read(self.command)
        return (result.get("status"), result.get("headers"), result.get("body"))

    action_priority = (execute_command, send_result)
    requires = ['http.get']
