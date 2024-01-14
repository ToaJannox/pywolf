from game import Game
def pywolf():
    g = Game()
    g.setup()
    g.play()
    # g.play()
    g.game_credits()

def test_main():
    from player_role.werewolves import FortuneTellerWolf
    w = FortuneTellerWolf()
    w.set_name("test_fortune_wolf")
    w.debug_display()


if __name__ == "__main__":
    # pywolf()
    test_main()