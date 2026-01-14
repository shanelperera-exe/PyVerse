from item import Item
from keyboard import Keyboard

def main():
    Item.instantiate_from_csv()

    item1 = Item("MyItem", 750)

    item1.apply_increment(0.2)
    item1.apply_discount()
    
    item1.name = "OtherItem"

    print(item1.name)
    print(item1.price)

    item1.send_email()

    item2 = Keyboard("jscKeyboard", 1000, 3)
    item2.apply_discount()

    print(item2.price)


if __name__ == "__main__":
    main()