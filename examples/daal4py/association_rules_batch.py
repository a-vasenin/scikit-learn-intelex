#===============================================================================
# Copyright 2014-2022 Intel Corporation
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

# daal4py assiciation rules example for shared memory systems

import daal4py as d4p
import numpy as np

# let's try to use pandas' fast csv reader
try:
    import pandas

    def read_csv(f, c=None, t=np.float64):
        return pandas.read_csv(f, usecols=c, delimiter=',', header=None, dtype=t)
except ImportError:
    # fall back to numpy loadtxt
    def read_csv(f, c=None, t=np.float64):
        return np.loadtxt(f, usecols=c, delimiter=',', ndmin=2)


def main(readcsv=read_csv, method='defaultDense'):
    infile = "./data/batch/apriori.csv"

    # configure a association_rules object
    algo = d4p.association_rules(discoverRules=True, minSupport=0.001, minConfidence=0.7)

    # let's provide a file directly, not a table/array
    result1 = algo.compute(infile)

    # We can also load the data ourselfs and provide the numpy array
    data = readcsv(infile)
    result2 = algo.compute(data)

    # association_rules result objects provide antecedentItemsets,
    # confidence, consequentItemsets, largeItemsets and largeItemsetsSupport
    assert np.allclose(result1.largeItemsets, result2.largeItemsets)
    assert np.allclose(result1.largeItemsetsSupport, result2.largeItemsetsSupport)
    assert np.allclose(result1.antecedentItemsets, result2.antecedentItemsets)
    assert np.allclose(result1.consequentItemsets, result2.consequentItemsets)
    assert np.allclose(result1.confidence, result2.confidence)

    return result1


if __name__ == "__main__":
    result1 = main()
    print('Confidence: (20 first)')
    print(result1.confidence[0:20])
    print('All looks good!')
