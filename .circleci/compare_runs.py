#!/usr/bin/env python
#===============================================================================
# Copyright 2020-2022 Intel Corporation
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
#===============================================================================

# coding: utf-8
import os
import sys
import operator

qoi_list = ['failed', 'passed', 'xpassed', 'xfailed', 'skipped', 'deselected']


def get_counts(tkn):
    data = [x.split() for x in os.getenv(tkn).split(',')]
    counts = {x[-1]: int(x[-2]) for x in data if len(x) > 0 and x[-1] in qoi_list}
    return counts


def sum_of_attributes(counts, keys):
    if isinstance(keys, str):
        return counts.get(keys, 0)
    return sum([counts.get(k, 0) for k in keys])


d4p = get_counts('D4P')

if d4p and sum_of_attributes(d4p, 'failed') == 0:
    print("Patched scikit-learn passed the compatibility check")
    sys.exit(0)
else:
    print("Patched run: {}".format(d4p))
    sys.exit(1)
