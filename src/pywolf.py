from game import Game

def pywolf():
    g = Game()
    g.setup()
    g.first_night()
    # g.play()
    g.game_credits()

def test_main():
    print("Hello World")
    val = None
    while True:
        val = int(input("input "))
        if val >= 8:
            break;
        print("not enough")
    print(val)

if __name__ == "__main__":
    pywolf()
    # test_main()