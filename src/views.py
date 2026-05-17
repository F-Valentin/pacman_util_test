import arcade

class WinView(arcade.View):
    def on_draw(self):
        """ Draw this view """
        self.clear()
        win_text = arcade.Text("Win Screen", self.window.width / 2, self.window.height / 2 + 100,
                         arcade.color.WHITE, font_size=20, anchor_x="center")
        win_text.draw()