import arcade
import arcade.gui


class GameView(arcade.View):
    def __init__(self):
        super().__init__()

        self.sprite_list = arcade.SpriteList()

        self.mon_animation = arcade.load_animated_gif("pacman.gif",)
        self.mon_animation.scale = 0.1

        self.mon_animation.center_x = 400
        self.mon_animation.center_y = 400

        self.sprite_list.append(self.mon_animation)

    def on_update(self, delta_time):
        self.sprite_list.update_animation(delta_time)

    def on_draw(self):
        self.clear()
        self.sprite_list.draw()


class MenuView(arcade.View):
    def __init__(self):
        super().__init__()
        # 1. Le Manager est le "chef" qui gère tous les boutons
        self.manager = arcade.gui.UIManager()
        self.manager.enable()  # On active la détection du clic

        # 2. On crée une boîte pour organiser nos boutons
        self.v_box = arcade.gui.UIBoxLayout()

        # 3. Création du bouton
        start_button = arcade.gui.UIFlatButton(text="START", width=200)
        self.v_box.add(start_button)  # On ajoute le bouton dans la boîte

        # 4. Définir l'action du clic sur le bouton
        # --- DANS MenuView (extrait) ---

        @start_button.event("on_click")
        def on_click_start(event):
            # IMPORTANT : On éteint le gestionnaire de clics du menu
            self.manager.disable()

            game_view = GameView()
            self.window.show_view(game_view)

        # 5. On place la boîte de boutons au centre exact de l'écran
        self.manager.add(
            arcade.gui.UIAnchorLayout(
                anchor_x="center_x",
                anchor_y="center_y",
                children=[self.v_box]
            )
        )

    def on_show_view(self):
        arcade.set_background_color(arcade.color.BLACK)

    def on_draw(self):
        self.clear()
        self.manager.draw()  # On demande au manager de dessiner les boutons
