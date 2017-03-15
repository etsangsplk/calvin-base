# -*- coding: utf-8 -*-

# Copyright (c) 2017 Ericsson AB
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

from calvin.actor.actor import Actor, condition, manage

class Mux(Actor):
    """
    Fetch tokens from the fan-in port corresponding to value at 'select'
    Inputs:
      token(routing="collect-tagged"): incoming tokens from connected ports to select from
      select: key to select among incoming values
    Outputs:
      token : token selected as given by select
    """

    @manage(['mapping'])
    def init(self, mapping):
        self.mapping = mapping

    def will_start(self):
        self.inports['token'].set_config({'port-mapping':self.mapping})

    @condition(['token', 'select'], ['token'])
    def dispatch(self, tok, sel):
        return (tok[sel],)

    action_priority = (dispatch,)
