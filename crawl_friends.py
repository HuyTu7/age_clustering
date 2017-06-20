import pandas as pd

from younet_rnd_infrastructure.tri.common import file_tool
from younet_rnd_infrastructure.tri.common import utils
from younet_rnd_infrastructure.tri.facebook_crawl_unit.get_list_friends import get_list_friends


if __name__ == '__main__':
    ids = list(pd.read_csv('./input/data_700k.csv', dtype={'id': str})['id'])
    batches_1k = utils.split_list_by_size(ids, 1000)

    for i in range(len(batches_1k)):
        batch_1k = batches_1k[i]
        print 'Runing batch %sk_%sk' % (i, i+1)
        result = get_list_friends.get_friends_ids(batch_1k)
        file_tool.save_json('./temp/friends_%sk_%sk.json' % (i+1, i+2), result)
