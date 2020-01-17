#!/usr/bin/env python

from manimlib.imports import *

# To watch one of these scenes, run the following:
# python -m manim example_scenes.py SquareToCircle -pl
#
# Use the flat -l for a faster rendering at a lower
# quality.
# Use -s to skip to the end and just save the final frame
# Use the -p to have the animation (or image, if -s was
# used) pop up once done.
# Use -n <number> to skip ahead to the n'th animation of a scene.
# Use -r <number> to specify a resolution (for example, -r 1080
# for a 1920x1080 video)


class OpeningManimExample(Scene):
    def construct(self):
        title = TextMobject("This is some \\LaTeX")
        basel = TexMobject(
            "\\sum_{n=1}^\\infty "
            "\\frac{1}{n^2} = \\frac{\\pi^2}{6}"
        )
        VGroup(title, basel).arrange(DOWN)
        self.play(
            Write(title),
            FadeInFrom(basel, UP),
        )
        self.wait()

        transform_title = TextMobject("That was a transform")
        transform_title.to_corner(UP + LEFT)
        self.play(
            Transform(title, transform_title),
            LaggedStart(*map(FadeOutAndShiftDown, basel)),
        )
        self.wait()

        grid = NumberPlane()
        grid_title = TextMobject("This is a grid")
        grid_title.scale(1.5)
        grid_title.move_to(transform_title)

        self.add(grid, grid_title)  # Make sure title is on top of grid
        self.play(
            FadeOut(title),
            FadeInFromDown(grid_title),
            ShowCreation(grid, run_time=3, lag_ratio=0.1),
        )
        self.wait()

        grid_transform_title = TextMobject(
            "That was a non-linear function \\\\"
            "applied to the grid"
        )
        grid_transform_title.move_to(grid_title, UL)
        grid.prepare_for_nonlinear_transform()
        self.play(
            grid.apply_function,
            lambda p: p + np.array([
                np.sin(p[1]),
                np.sin(p[0]),
                0,
            ]),
            run_time=3,
        )
        self.wait()
        self.play(
            Transform(grid_title, grid_transform_title)
        )
        self.wait()


class SquareToCircle(Scene):
    def construct(self):
        circle = Circle()
        square = Square()
        square.flip(RIGHT)
        square.rotate(-3 * TAU / 8)
        circle.set_fill(PINK, opacity=0.5)

        self.play(ShowCreation(square))
        self.play(Transform(square, circle))
        self.play(FadeOut(square))


class WarpSquare(Scene):
    def construct(self):
        square = Square()
        self.play(ApplyPointwiseFunction(
            lambda point: complex_to_R3(np.exp(R3_to_complex(point))),
            square
        ))
        self.wait()


class WriteStuff(Scene):
    def construct(self):
        example_text = TextMobject(
            "This is a some text",
            tex_to_color_map={"text": YELLOW}
        )
        example_tex = TexMobject(
            "\\sum_{k=1}^\\infty {1 \\over k^2} = {\\pi^2 \\over 6}",
        )
        group = VGroup(example_text, example_tex)
        group.arrange(DOWN)
        group.set_width(FRAME_WIDTH - 2 * LARGE_BUFF)

        self.play(Write(example_text))
        self.play(Write(example_tex))
        self.wait()


class UpdatersExample(Scene):
    def construct(self):
        decimal = DecimalNumber(
            0,
            show_ellipsis=True,
            num_decimal_places=3,
            include_sign=True,
        )
        square = Square().to_edge(UP)

        decimal.add_updater(lambda d: d.next_to(square, RIGHT))
        decimal.add_updater(lambda d: d.set_value(square.get_center()[1]))
        self.add(square, decimal)
        self.play(
            square.to_edge, DOWN,
            rate_func=there_and_back,
            run_time=5,
        )
        self.wait()

class MyScene(Scene):
    def construct(self):
        ls = TexMobject("Y = Xw + Z")
        text = TextMobject("We note the following " + "$Y \\in \\mathbf{R}^n, w \\in \\mathbf{R}^d, X \\in \\mathbf{R}^{n x d}$")
        self.play(Write(ls))
        self.wait()
        text.to_edge(DOWN)
        self.play(FadeInFromDown(text))
        self.wait(2)
        self.play(FadeOut(text))
        self.play(
                ls.to_corner, UP + LEFT, rate_func=smooth, run_time=2)
        assume= TexMobject("Z \sim \\mathcal{N}(0, \\Sigma_Z)")
        assume.next_to(ls, DOWN, buff = 1)
        self.play(FadeInFromDown(assume))
        self.wait(2)
        y_dist = TexMobject(" \\implies \\enspace Y \\sim \\mathcal{N}(Xw, \\Sigma_Z)")
        y_dist.next_to(assume, RIGHT, buff = 0.5)
        self.play(FadeInFrom(y_dist,LEFT))


class Test(Scene):
    def construct(self):
        PAD=DR*0.1
        
        global_frame = Rectangle()
        global_frame.scale(0.98)
        global_frame.to_corner(UP + LEFT)
        global_frame.shift(UP * 0.4)
        #global_frame.set_width(3.0, stretch=True)
        global_text = TextMobject("{\\tiny Global}")
        #global_text.move_to(global_frame.get_corner(UP + LEFT) + DR*0.3 + 0.5*RIGHT)
        self.play(FadeInFromDown(global_frame))
        global_text.align_to(global_frame,UP)
        global_text.align_to(global_frame,LEFT)
        global_text.shift(PAD)
        self.play(Write(global_text))
        self.wait()
        
        glob_it1 = Square()
        glob_it1.scale(0.25)
        glob_it1.next_to(global_text, DOWN, buff = 0)
        glob_it1.align_to(global_frame, RIGHT)

        name_f = TextMobject("{\\small f}")
        name_f.next_to(glob_it1, LEFT, buff=0.2)
        func_f = TextMobject("{\\small $\\textit{func f(x)}[p=G]$}")
        #self.play(FadeInFrom(func_f, LEFT))
        test = TextMobject("{\\small $\\textit{def func f(x)}[p=G]$}")
        test.to_edge(RIGHT)
        func_f.move_to(test.get_center())
        self.play(Write(test))
        self.wait()
        self.play(Transform(test, func_f))
        #func_f.next_to(glob_it1, RIGHT, buff = 1)
        self.play(test.move_to, glob_it1.get_right() + 2.5 * RIGHT, rate_func=smooth)
        connect = Arrow(glob_it1.get_left(), test.get_left())
        func_f = test
        self.play(Write(name_f), FadeIn(glob_it1),Write(connect))


        glob_it2 = Square()
        glob_it2.scale(0.25)
        glob_it2.next_to(glob_it1, DOWN, buff = 0)
        glob_it2.align_to(global_frame, RIGHT)

        name_g = TextMobject("{\\small g}")
        name_g.next_to(glob_it2, LEFT, buff=0.2)
        func_g = TextMobject("{\\small $\\textit{func g(x, y)}[p=G]$}")
        func_g.next_to(glob_it2, RIGHT, buff = 2)
        self.play(FadeInFrom(func_g, LEFT))
        connect2 = Arrow(glob_it2.get_left(), func_g.get_left())
        self.play(Write(name_g), FadeIn(glob_it2), Write(connect2))

        glob_it3 = Square()
        glob_it3.scale(0.25)
        glob_it3.next_to(glob_it2, DOWN, buff = 0)
        glob_it3.align_to(global_frame, RIGHT)

        name_x = TextMobject("{\\small x}")
        name_x.next_to(glob_it3, LEFT, buff=0.2)
        cont_x = TextMobject("{\\small $3$}")
        self.play(Write(name_x), FadeIn(glob_it3))

        cont_x.to_edge(RIGHT)
        self.play(Write(cont_x))
        self.play(
                cont_x.move_to, glob_it3.get_center(), rate_func = smooth)

        frame_1 = Rectangle()
        frame_1.scale(0.98)
        frame_1.next_to(global_frame, DOWN, buff = 0)
        frame_1_text= TextMobject("{\\small f1:}")
        frame_1_text.move_to(frame_1.get_corner(UP + LEFT) + DR*0.3)
        frame_1_name = TextMobject("{\\small g [p=G]}")
        frame_1_name.next_to(frame_1_text, RIGHT, buff=0.2)
        self.play(FadeIn(frame_1))
        self.play(FadeInFrom(frame_1_text, LEFT), FadeInFrom(frame_1_name, LEFT))
        self.wait(1)

        frame1_it1= Square()
        frame1_it1.scale(0.25)
        frame1_it1.next_to(frame_1_text, DOWN, buff = 0)
        frame1_it1.align_to(global_frame, RIGHT)
        frame1_it2= Square()
        frame1_it2.scale(0.25)
        frame1_it2.next_to(frame1_it1, DOWN, buff = 0)
        frame1_it2.align_to(global_frame, RIGHT)
        f1_x = TextMobject("{\\small x}")
        f1_x.next_to(frame1_it1, LEFT, buff = 0.2)
        f1_y = TextMobject("{\\ y}")
        f1_y.next_to(frame1_it2, LEFT, buff = 0.2)
        f1_y_cont = TextMobject("$3$")
        f1_y_cont.move_to(frame1_it2.get_center())
        connect3 = Arrow(frame1_it1.get_center() + DL * 0.2, func_f.get_left())
        self.play(FadeIn(frame1_it1), Write(f1_x), FadeIn(connect3))
        self.play(FadeIn(frame1_it2),Write(f1_y), Write(f1_y_cont))
        self.wait()

        frame1_rv=Square()
        frame1_rv.scale(0.25)
        frame1_rv.next_to(frame1_it2, DOWN, buff=0)
        frame1_rv.align_to(global_frame, RIGHT)
        f1_rv = TextMobject("{\\small rV}")
        f1_rv.next_to(frame1_rv, LEFT, buff = 0.2)
        self.play(FadeIn(frame1_rv), Write(f1_rv))



        frame_2 = Rectangle()
        frame_2.scale(0.98)
        frame_2.next_to(frame_1, DOWN, buff = 0)
        frame_2_text= TextMobject("{\small f2:}")
        frame_2_text.move_to(frame_2.get_corner(UP + LEFT) + DR*0.3)
        frame_2_name = TextMobject("{\\small f [p = G]}")
        frame_2_name.next_to(frame_2_text, RIGHT, buff = 0.2)
        self.play(FadeIn(frame_2))
        self.play(FadeInFrom(frame_2_text, LEFT), FadeInFrom(frame_2_name, LEFT))
        self.wait(1)

        frame2_it1= Square()
        frame2_it1.scale(0.25)
        frame2_it1.next_to(frame_2_text, DOWN, buff = 0)
        frame2_it1.align_to(global_frame, RIGHT)
        f2_x = TextMobject("{\\small x}")
        f2_x.next_to(frame2_it1, LEFT, buff = 0.2)
        f2_x_cont = TextMobject("$3$")
        f2_x_cont.move_to(frame2_it1.get_center())
        self.play(Write(frame2_it1), Write(f2_x))
        self.play(Write(f2_x_cont))

        frame2_it2= Square()
        frame2_it2.scale(0.25)
        frame2_it2.next_to(frame2_it1, DOWN, buff = 0)
        frame2_it2.align_to(global_frame, RIGHT)
        f2_rv = TextMobject("{\\small rV}")
        f2_rv.next_to(frame2_it2, LEFT, buff = 0.2)
        f2_rv_cont = TextMobject("$3$")
        f2_rv_cont.move_to(frame2_it2.get_center())
        self.play(Write(frame2_it2), Write(f2_rv))
        self.play(Write(f2_rv_cont))
        
        frame1_rv_2=Rectangle()
        frame1_rv_2.scale(0.25)
        frame1_rv_2.set_width(frame1_rv_2.get_width() + 0.5, stretch=True)
        frame1_rv_2.next_to(frame1_it2, DOWN, buff=0)
        frame1_rv_2.align_to(global_frame, RIGHT)

        frame1_rv_cont = TextMobject("$False$")
        frame1_rv_cont.move_to(frame1_rv_2.get_center())

        self.play(Transform(frame1_rv, frame1_rv_2),
                f1_rv.next_to, frame1_rv_2, LEFT, buff =0.2, rate_func=smooth)
        self.play(FadeIn(frame1_rv_cont))
        self.wait()
        
        glob_it3_2 = Rectangle()
        glob_it3_2.scale(0.25)
        glob_it3_2.set_width(glob_it3_2.get_width() + 0.5, stretch=True)
        glob_it3_2.next_to(glob_it2, DOWN, buff = 0)
        glob_it3_2.align_to(global_frame, RIGHT)

        new_x = TextMobject("$False$")
        new_x.move_to(glob_it3_2.get_center())

        #name_x.next_to(glob_it3_2, LEFT, buff=0.2)
        self.play(Transform(glob_it3, glob_it3_2),Transform(cont_x, new_x),
                name_x.next_to, glob_it3_2, LEFT, buff = 0.2, rate_func=smooth) 

        self.wait()

        
        frame_3 = Rectangle()
        frame_3.scale(0.98)
        frame_3.next_to(frame_2, DOWN, buff = 0)
        frame_3_text= TextMobject("{\small f3:}")
        frame_3_text.move_to(frame_3.get_corner(UP + LEFT) + DR*0.3)
        frame_3_name = TextMobject("{\\small g [p = G]}")
        frame_3_name.next_to(frame_3_text, RIGHT, buff = 0.2)
        self.play(FadeIn(frame_3))
        self.play(FadeInFrom(frame_3_text, LEFT), FadeInFrom(frame_3_name, LEFT))
        self.wait(1)

        frame3_it1= Square()
        frame3_it1.scale(0.25)
        frame3_it1.next_to(frame_3_text, DOWN, buff = 0)
        frame3_it1.align_to(global_frame, RIGHT)
        frame3_it2= Square()
        frame3_it2.scale(0.25)
        frame3_it2.next_to(frame3_it1, DOWN, buff = 0)
        frame3_it2.align_to(global_frame, RIGHT)
        f3_x = TextMobject("{\\small x}")
        f3_x.next_to(frame3_it1, LEFT, buff = 0.2)
        f3_y_2 = TextMobject("{\\small y}")
        f3_y_2.next_to(frame3_it2, LEFT, buff = 0.2)
        f3_y_cont = TextMobject("$0$")
        f3_y_cont.move_to(frame3_it2.get_center())
        connect4 = Arrow(frame3_it1.get_center() + DL * 0.1 + DOWN*0.1, func_f.get_left())
        self.play(Write(frame3_it1), Write(f3_x))
        self.play(Write(frame3_it2), Write(f3_y_2))
        self.play(FadeIn(connect4))
        self.wait()
        self.play(Write(f3_y_cont))
        
        frame_4 = Rectangle()
        frame_4.scale(0.98)
        frame_4.next_to(frame_2, RIGHT, buff = 1.5)
        frame_4_text= TextMobject("{\small f4:}")
        frame_4_text.move_to(frame_4.get_corner(UP + LEFT) + DR*0.3)
        frame_4_name = TextMobject("{\\small f [p = G]}")
        frame_4_name.next_to(frame_4_text, RIGHT, buff = 0.2)
        self.play(FadeIn(frame_4))
        self.play(FadeInFrom(frame_4_text, LEFT), FadeInFrom(frame_4_name, LEFT))
        self.wait(1)

        frame4_it1= Square()
        frame4_it1.scale(0.25)
        frame4_it1.next_to(frame_4_text, DOWN, buff = 0)
        frame4_it1.align_to(frame_4, RIGHT)
        f4_x = TextMobject("{\\small x}")
        f4_x.next_to(frame4_it1, LEFT, buff = 0.2)
        self.play(Write(frame4_it1), Write(f4_x))
        f4_x_cont = TextMobject("$0$")
        f4_x_cont.move_to(frame4_it1.get_center())
        self.play(Write(f4_x_cont))
        self.wait()

        frame4_rv = Square()
        frame4_rv.scale(0.25)
        frame4_rv.next_to(frame4_it1, DOWN, buff = 0)
        frame4_rv.align_to(frame_4, RIGHT)
        frame4_rv_name = TextMobject("rV")
        frame4_rv_name.next_to(frame4_rv, LEFT, buff = 0.2)
        self.play(Write(frame4_rv), Write(frame4_rv_name))
        f4_rv = TextMobject("$0$")
        f4_rv.move_to(frame4_rv.get_center())
        self.play(Write(f4_rv))
        self.wait()

        f3_rv = Square()
        f3_rv.scale(0.25)
        f3_rv.next_to(frame3_it2, DOWN, buff = 0)
        f3_rv.align_to(global_frame, RIGHT)
        f3_rv_name = TextMobject("rV")
        f3_rv_name.next_to(f3_rv, LEFT, buff = 0.2)
        self.play(Write(f3_rv), Write(f3_rv_name))
        f3_rv_cont = TextMobject("$0$")
        f3_rv_cont.move_to(f3_rv.get_center())
        self.play(Write(f3_rv_cont))

        last = TextMobject("0")
        last.move_to(glob_it1)
        self.play(Transform(connect, last))
        self.wait()


# See old_projects folder for many, many more
