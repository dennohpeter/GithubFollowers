import sys

import requests
from getpass import getpass


class Github(object):
    MAX_PAGES = 50
    USERNAME = ""
    PASSWORD = None

    def __init__(self):
        print("Welcome to Github Followers Program\
            \nTo Begin")
        self.USERNAME = input("Enter username: ")

    # people you follow
    def following(self):
        following = []
        print("Getting people you follow...")
        for page_number in range(1, self.MAX_PAGES):
            res = requests.get(
                "https://api.github.com/users/{}/following?page={}".format(self.USERNAME, page_number))
            res = res.json()
            if res == []:
                break
            following += res
        print("Done.")
        return following

    # people that follow you

    def followers(self):
        followers = []
        print("Getting followers...")
        for page_number in range(1, self.MAX_PAGES):
            res = requests.get(
                "https://api.github.com/users/{}/followers?page={}".format(self.USERNAME, page_number))
            res = res.json()
            if res == []:
                break
            followers += res
        print("Done.")
        return followers

    # people you follow that don't follow you.
    def unfollowers(self, following, followers):
        if following == []:
            following = self.following()
        if followers == []:
            followers = self.followers()

        unfollowers = []
        for user in following:
            if user not in followers:
                unfollowers.append(user)
        return unfollowers

    # unfollow a given user
    def unfollow(self, username):   
        if self.PASSWORD == None:
            self.PASSWORD = getpass("Enter password: ")
        res = requests.delete(
            "https://api.github.com/user/following/{}".format(username), auth=(self.USERNAME, self.PASSWORD))
        
        try:
            message = res.json().get("message")
            if "Bad" in message:
                self.PASSWORD = None
                print("ERROR:", message)
        except Exception as err:
            print("Succesfully unfollowed", username)


def format(users, title):
    print("\n-----------------------------------------------------------------")
    print(title.rjust(24+len(title), ' '))
    print("-----------------------------------------------------------------\n")
    for i, user in enumerate(users):
        user = "{}: {}, {}".format(
            i+1, user.get("login"), user.get("html_url"))
        print(user)


if __name__ == "__main__":
    menu = \
        """
Choose an action below:
    1: See Followers
    2: See Following
    3: See Unfollowers
    4: Unfollow
    5: Exit
Enter: """
user = Github()
following = []
followers = []
unfollowers = []
try:
    while True:
        option = input(menu)
        if option == "1":
            if followers == []:
                followers = user.followers()
            format(followers, "Followers")
        elif option == "2":
            if following == []:
                following = user.following()
            format(following, "Following")
        elif option == "3":
            unfollowers = user.unfollowers(
                following=following, followers=followers)
            format(unfollowers, "Unfollowers")
        elif option == "4":
            if unfollowers == []:
                unfollowers = user.unfollowers(
                    following=following, followers=followers)
            format(unfollowers, "Your Unfollowers")
            title = "\nEnter Index of the User to Unfollow e.g 1\
            \nNB: You can unfollow multipe users at once like 1,2,3\
            \nEnter 0 To go back. <-\
            \n$ "
            to_unfollow_list = input(title).split(",")

            for position in to_unfollow_list:
                try:
                    index = int(position.strip())
                    if index == 0:
                        break
                    unfollower = unfollowers[index-1]
                    username = unfollower.get("login")
                    print("Unfollowing {}...".format(username))
                    user.unfollow(username)
                # except ValueError:
                #     print("Enter valid value")
                except IndexError:
                    print("No user at position", position)

        elif option == "5":
            sys.exit("Program Exited.")
        else:
            print("Invalid Option. Try Again")
except KeyboardInterrupt:
    print("\nCancelled.")
