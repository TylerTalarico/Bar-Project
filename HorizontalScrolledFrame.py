from tkinter import *


class HorizontalScrolledFrame(Frame):
    """A pure Tkinter scrollable frame that actually works!
    * Use the 'interior' attribute to place widgets inside the scrollable frame
    * Construct and pack/place/grid normally
    * This frame only allows vertical scrolling

    """
    def __init__(self, parent, bg, width, *args, **kw):
        Frame.__init__(self, parent, *args, **kw)

        # create a canvas object and a horizontal scrollbar for scrolling it

        canvas = Canvas(self, bd=0, highlightthickness=0, bg=bg)
        canvas.grid(row=0, column=0, sticky='ns')

        # reset the view
        canvas.xview_moveto(0)
        canvas.yview_moveto(0)

        self.canvaswidth = width

        # create a frame inside the canvas which will be scrolled with it
        self.interior = interior = Frame(canvas, width=self.canvaswidth, bg=bg)
        interior_id = canvas.create_window(0, 0, window=interior, anchor=NW)

        # track changes to the canvas and frame width and sync them,
        # also updating the scrollbar
        def _configure_interior(event):
            # update the scrollbars to match the size of the inner frame
            size = (interior.winfo_reqwidth(), interior.winfo_reqheight())
            canvas.config(scrollregion=(0, 0, size[0], size[1]))
            if interior.winfo_reqheight() != canvas.winfo_height():
                # update the canvas's width to fit the inner frame
                canvas.config(height=interior.winfo_reqheight())
        interior.bind('<Configure>', _configure_interior)

        def _configure_canvas(event):
            if interior.winfo_reqheight() != canvas.winfo_height():
                # update the inner frame's height to fill the canvas
                canvas.itemconfigure(interior_id, height=canvas.winfo_height())
        canvas.bind('<Configure>', _configure_canvas)

        self.scrollposition = 1
        self.ref_point = 0

        def on_press(event):
            self.ref_point = event.x_root
            if self.scrollposition < 1:
                self.scrollposition = 1
            elif self.scrollposition > canvas.winfo_width():
                self.scrollposition = canvas.winfo_width()
            canvas.xview_moveto(self.scrollposition / canvas.winfo_width())

        def on_touch_scroll(event):
            nowx = event.x_root
            deltax = nowx - self.ref_point

            if (deltax < 0 and canvas.xview()[1] < 1) or (deltax > 0 and canvas.xview()[1] > 0):
                self.scrollposition -= deltax/2  # event.delta
            self.ref_point = nowx
            canvas.xview_moveto(self.scrollposition / canvas.winfo_width())

        self.bind("<Enter>", lambda _: self.bind_all('<Button-1>', on_press), '+')
        self.bind("<Leave>", lambda _: self.unbind_all('<Button-1>'), '+')
        self.bind("<Enter>", lambda _: self.bind_all('<B1-Motion>', on_touch_scroll), '+')
        self.bind("<Leave>", lambda _: self.unbind_all('<B1-Motion>'), '+')
