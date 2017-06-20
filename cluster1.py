import pandas as pd
import json
from younet_rnd_infrastructure.tri.common import file_tool



class FriendshipManager():
    def __init__(self):
        pass

    @staticmethod
    def loader():
        print 'Loading data ...'
        friendships = list()
        for i in range(1, 2):
            friendships.extend(file_tool.load_json('./temp/friends_%sk_%sk.json' % (i, i+1)))

        def convert_list_to_dict(list_friendships):
            friendships = dict()
            for item in list_friendships:
                if item['id'] in friendships.keys():
                    friendships[item['id']].extend(item['friends'])
                else:
                    friendships[item['id']] = item['friends']
            return friendships

        def sorting(friendships_d):
            friendships = dict.fromkeys(['ids', 'friends'])
            count = 0
            ids = set(friendships_d.keys())
            for id in ids:
                if count < 3:
                    print "length of value: %s)" % len(friendships_d[id])
                #friends = [friend for friend in value if friend in friendships_d.keys()]
                friends = set(friendships_d[id]).intersection(ids)
                friendships[id] = list(friends)
                if count < 3:
                    print "length of new value: %s)" % len(friendships[id])
                count += 1
            return friendships

        def remove_single_node(friendships_d):
            for key, value in friendships_d.items():
                if not value:
                    friendships_d.pop(key)
            return friendships_d


        friendships_d = convert_list_to_dict(friendships)
        #print 'Test d: %s, %s' % (friendships_d.keys()[0], len(friendships_d[friendships_d.keys()[0]]))
        friendships_d1 = sorting(friendships_d)
        #print 'Test d1: %s, %s' % (friendships_d1.keys()[0], len(friendships_d1[friendships_d1.keys()[0]]))
        friendships_d2 = remove_single_node(friendships_d1)
        FriendshipManager.friendship_dict1 = friendships_d1
        FriendshipManager.friendship_dict2 = friendships_d2
        print 'Total id with the single nodes: %s' % len(FriendshipManager.friendship_dict1.keys())
        print 'Total id without the single nodes: %s' % len(FriendshipManager.friendship_dict2.keys())
        with open('result1.json', 'w') as fp1:
            json.dump(FriendshipManager.friendship_dict1, fp1)
        with open('result2.json', 'w') as fp2:
            json.dump(FriendshipManager.friendship_dict2, fp2)

    @staticmethod
    def is_friend(id1, id2):
        if id1 in FriendshipManager.friendship_dict.keys() and id2 in FriendshipManager.friendship_dict.keys():
            if id2 in FriendshipManager.friendship_dict[id1]:
                return True
        return False

    @staticmethod
    def get_list_ids():
        return FriendshipManager.friendship_dict.keys()

    @staticmethod
    def get_potential_ids():
        ids = set(FriendshipManager.get_list_ids())
        friends_ids = set(reduce(lambda x, y: x+y, FriendshipManager.friendship_dict.values()))
        return list(ids.intersection(friends_ids))


class Group:
    def __init__(self, list_ids):
        self.list_members = set(list_ids)
    @staticmethod
    def join(group_a, group_b):
        if len(group_a.list_members.intersection(group_b.list_members)) != 0:
            return Group(group_a.list_members.union(group_b.list_members))
        for element_a in group_a.list_members:
            for element_b in group_b.list_members:
                if FriendshipManager.is_friend(element_a, element_b):
                    return Group(group_a.list_members.union(group_b.list_members))
        return Group(set())


def generate_combination_of_two(list_groups):
    result = []
    total_loop = len(list_groups) * (len(list_groups)-1) /2
    for i in range(len(list_groups)):
        for j in range(i + 1, len(list_groups)):
            print '%s/%s' % (i* len(list_groups) + j, total_loop)
            group_a = list_groups[i]
            group_b = list_groups[j]
            new_group = Group.join(group_a, group_b)
            if len(new_group.list_members) != 0:
                result.append(new_group)
    return result


if __name__ == '__main__':
    #data = file_tool.load_json('./temp/friends_1k_2k.json')
    FriendshipManager.loader()