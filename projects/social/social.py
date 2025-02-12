import random

class User:
    def __init__(self, name):
        self.name = name

class SocialGraph:
    def __init__(self):
        self.lastID = 0
        self.users = {}
        self.friendships = {}

    def addFriendship(self, userID, friendID):
        """
        Creates a bi-directional friendship
        """
        if userID == friendID:
            print("WARNING: You cannot be friends with yourself")
        elif friendID in self.friendships[userID] or userID in self.friendships[friendID]:
            print("WARNING: Friendship already exists", userID, friendID)
        else:
            self.friendships[userID].add(friendID)
            self.friendships[friendID].add(userID)

    def addUser(self, name):
        """
        Create a new user with a sequential integer ID
        """
        self.lastID += 1  # automatically increment the ID to assign the new user
        self.users[self.lastID] = User(name)
        self.friendships[self.lastID] = set()

    def populateGraph(self, numUsers, avgFriendships):
        """
        Takes a number of users and an average number of friendships
        as arguments

        Creates that number of users and a randomly distributed friendships
        between those users.

        The number of users must be greater than the average number of friendships.
        """
        # Reset graph
        self.lastID = 0
        self.users = {}
        self.friendships = {}
        # !!!! IMPLEMENT ME
        fs_num = [1+(2*avgFriendships-1)*x//(numUsers-1) for x in range(numUsers)]
        random.shuffle(fs_num)
        # Add users
        for i in range(numUsers):
            self.addUser(i)
        # Create friendships
        for i in range(1, numUsers):
            friends = set()
            for _ in range(fs_num[i-1]):
                while fs_num[i-1] > 0:
                    if sum([fs_num[x] for x in range(i, numUsers) if x not in friends]) == 0:
                        break
                    k = random.randint(i+1, numUsers)
                    if fs_num[k-1] > 0 and k not in friends:
                        self.addFriendship(i, k)
                        fs_num[i-1] -= 1
                        fs_num[k-1] -= 1
                        friends.add(k)
                        break

    def getAllSocialPaths(self, userID):
        """
        Takes a user's userID as an argument

        Returns a dictionary containing every user in that user's
        extended network with the shortest friendship path between them.

        The key is the friend's ID and the value is the path.
        """
        visited = {}  # Note that this is a dictionary, not a set
        queue = []

        queue.append(userID)
        visited[userID] = [userID]
        
        while queue:
            s = queue.pop(0)
            for c in self.friendships[s]:
                if c not in visited:
                    queue.append(c)
                    visited[c] = visited[s]+[c]
                elif len(visited[c]) > len(visited[s])+1:
                    visited[c] = visited[s]+[c]
        return visited


if __name__ == '__main__':
    sg = SocialGraph()
    sg.populateGraph(20, 3)
    print(sg.friendships)
    connections = sg.getAllSocialPaths(1)
    print(connections)
