import os

class Friends:
    def __init__(self, name, age, favourite_subject, ) -> None:
        self.name = name
        self.age = age
        self.favourite_subject = favourite_subject
    def __str__(self) -> str:
        return f"Friends:{self.name}, his age is {self.age} and his favourite subject is {self.favourite_subject}"

class Store_Friends:
    def __init__(self) -> None:
        self.friend_list = []
    
    def add_friends(self, friend):
        self.friend_list.append(friend)
    
    def show_friends(self):
        print("Friends:")
        for friend in self.friend_list:
            print(f"- {friend}")


def add_new_friend() -> Friends:
    name = input("Friend_name: ")
    age = input("Age: ")
    favourite_subject = input("Favourite_subject: ")
    return Friends(name, age, favourite_subject)

def remove_friend(friend_manager: Store_Friends) -> Friends:
    friend_manager.show_friends()
    user_remove = input("What friend would you like to remove?")
    for friend in friend_manager.friend_list:
        if friend.name == user_remove:
            friend_manager.friend_list.remove(friend)
            print(f"{user_remove} has been removed from the list")
            return


os.system("cls")

friend_manager = Store_Friends()

while True:

    user_choice = input("1. Add_Friend\n2. Remove_Friend\n3. Edit_Friend\n4. Show_Friend\n5. Exit\n")
    if user_choice =="1":
        new_friend = add_new_friend()
        friend_manager.add_friends(new_friend)

    elif user_choice =="2":
        remove_friend(friend_manager)

    elif user_choice =="3":
        pass

    elif user_choice =="4":
        friend_manager.show_friends()

    elif user_choice == "5":
        break

friend_manager.show_friends()