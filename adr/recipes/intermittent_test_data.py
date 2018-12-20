"""
This is currently broken.

.. code-block:: bash

    adr intermittent_test_data
"""
from __future__ import print_function, absolute_import

from ..query import run_query


def run(args, config):

    if args.test_name == '':
        args.test_name = '(~(file.*|http.*))'
        args.platform_config = "test-%s/%s" % (args.platform, args.build_type)
    else:
        args.test_name = '.*%s.*' % args.test_name
        args.platform_config = "test-"
        args.groupby = 'run.key'
        args.result = ["T", "F"]

    query_args = vars(args)

    result = run_query('intermittent_tests', config, **query_args)['data']
    total_runs = run_query('intermittent_test_rate', config, **query_args)['data']

    intermittent_tests = []
    for item in result['run.key']:
        parts = item.split('/')
        config = "%s/%s" % (parts[0], parts[1].split('-')[0])
        if config not in intermittent_tests:
            intermittent_tests.append(config)

    retVal = {}
    for test in total_runs:
        parts = test[0].split('/')
        config = "%s/%s" % (parts[0], parts[1].split('-')[0])
        if config in intermittent_tests:
            if config not in retVal:
                retVal[config] = [test[1], test[2]]
            else:
                retVal[config][0] += test[1]
                retVal[config][1] += test[2]

    result = []
    for item in retVal:
        val = [item]
        val.extend(retVal[item])
        result.append(val)
    result.insert(0, ['Config', 'Failures', 'Runs'])
    return result
