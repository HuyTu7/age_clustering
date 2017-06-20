import pandas as pd

from younet_rnd_infrastructure.tri.common import file_tool


class FriendshipManager():
    def __init__(self):
        pass

    @staticmethod
    def loader():
        print 'Loading data ...'
        friendships = list()
        for i in range(1, 28):
            friendships.extend(file_tool.load_json('./temp/friends_%sk_%sk.json' % (i, i+1)))

        def convert_list_to_dict(list_friendships):
            friendships = dict()
            for item in list_friendships:
                if item['id'] in friendships.keys():
                    friendships[item['id']].extend(item['friends'])
                else:
                    friendships[item['id']] = item['friends']
            return friendships

        friendships = convert_list_to_dict(friendships)
        FriendshipManager.friendship_dict = friendships
        print 'Total id: %s' % len(FriendshipManager.friendship_dict.keys())

    @staticmethod
    def is_friend(id1, id2):
        if id1 in FriendshipManager.friendship_dict.keys():
            if id2 in FriendshipManager.friendship_dict[id1]:
                return True
        if id2 in FriendshipManager.friendship_dict.keys():
            if id1 in FriendshipManager.friendship_dict[id2]:
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

    # FriendshipManager.loader()
    #
    # # list_ids = FriendshipManager.get_list_ids()
    # list_ids = FriendshipManager.get_potential_ids()
    # print 'Length list id: %s' % len(list_ids)
    # # print FriendshipManager.is_friend('1142121730', '100002947505739')
    # # print 'Done'
    # #
    # # initial_groups = list()
    # # for id in list_ids:
    # #     initial_groups.append(Group([id]))
    # #
    # # print 'Step 1'
    # # candidates_next = generate_combination_of_two(initial_groups)
    # # step_index = 2
    # # while len(candidates_next) != 0:
    # #     candidates_pass = candidates_next
    # #     print 'Step %s' % step_index
    # #     step_index += 1
    # #     candidates_next = generate_combination_of_two(candidates_next)
    # def is_friend_with_group(id, ids):
    #     for i in range(len(ids)):
    #         if FriendshipManager.is_friend(id, ids[i]):
    #             return True
    #     return False
    #
    # groups = []
    # group_current = []
    # while len(list_ids) > 0:
    #     new_id = list_ids.pop()
    #     group_current.append(new_id)
    #     has_changed = True
    #     while has_changed:
    #         has_changed = False
    #         for i in range(len(list_ids)-1, -1, -1):
    #             if is_friend_with_group(list_ids[i], group_current):
    #                 group_current.append(list_ids[i])
    #                 del list_ids[i]
    #                 has_changed = True
    #         print 'Current group: %s' % len(group_current)
    #         print 'has_change %s' % has_changed
    #     groups.append(group_current)
    #     group_current = []
    #     print 'Number of groups: %s' % len(groups)
    #     print 'Number of remaining id: %s' % len(list_ids)
    # print 'Done'

    data = file_tool.load_json('./temp/friends_1k_2k.json')
    # data is a list of dict