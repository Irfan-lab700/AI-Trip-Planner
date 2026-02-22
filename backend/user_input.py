def get_user_input():
    source = input("Enter your starting city : ")
    destination = input("Enter your destination city :")
    day  = int(input("Enter number of days : "))
    budget = float(input("Enter your budget : "))
    interests = input("Enter your interests (comma separated) : ").split(",")
    return{
        "source" :source,
        "destination":destination,
        "day":day,
        "budget":budget,
        "interests": [i.strip() for i in interests]
    }
if __name__ == "__main__":
    user_data = get_user_input()
    print("\nCollected User Data:")
    print(user_data)
    
    
    