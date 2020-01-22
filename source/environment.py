from manimlib.imports import *

def other_dir(direction):
    if (direction == RIGHT).all():
        return UP
    else:
        return RIGHT

def create_stairs(n):
    #n describes the number of flat steps
    steps = []
    steps.append(Line())
    direction = UP
    length = steps[0].get_length()
    steps[0].set_length(length // 2)
    length = steps[0].get_length()
    steps[0].to_corner(DL)

    for i in range(2 * n - 2):
        prev_end = steps[-1].get_end()
        seg = Line(start = prev_end , end = prev_end + direction  * length)
        seg.add_updater( (lambda j:lambda m : m.put_start_and_end_on(steps[j].get_end(), steps[j].get_end() + m.get_unit_vector() * m.get_length()))(i))
        steps.append(seg)
        direction = other_dir(direction)

    return steps

class Stairway(Scene):
    def construct(self):
        shrink_factor = 0.8
        shift_right_factor = 4
        num_steps = 4
        up_shift = 3
        steps = create_stairs(num_steps)
        init_anim = [Write(piece) for piece in steps]
        person = Circle()
        person_radius = steps[0].get_length() * shrink_factor
        person.set_width(person_radius)
        person.next_to(steps[0], UP, buff = 0)
        person.add_updater(lambda m : m.next_to(steps[0], UP, buff=0))
        self.play(*(init_anim + [Write(person)]))
        #self.play(steps[0].to_edge, DOWN, rate_func=smooth) 
        how = TextMobject("How many ways are there to climb the stairs?")
        how.to_edge(UP)
        self.play(FadeInFrom(how, UP))
        self.wait(2)
        self.play(FadeOut(how))
        
        options = TextMobject("2 Options: ")
        options.to_corner(UL)

        step_one = TextMobject("Take 1 Step")
        step_one.next_to(options, DOWN)
        step_one.align_to(options, LEFT)

        step_two = TextMobject("Take 2 Steps")
        step_two.next_to(step_one, DOWN)
        step_two.align_to(options, LEFT)

        self.play(FadeInFrom(options, LEFT))
        self.play(FadeIn(step_one))
        self.play(FadeIn(step_two))
        self.wait()

        after_one = create_stairs(num_steps)
        [step.shift(RIGHT * shift_right_factor) for step in after_one]
        person_one = Circle()
        person_one.set_width(person_radius)
        person_one.next_to(after_one[0], UP, buff = 0)
        arc = ArcBetweenPoints(person_one.get_center(), after_one[2].get_center() + UP * person.get_width()/2, angle = -TAU / 4) 
        animations = [FadeInFrom(piece, LEFT) for piece in after_one + [person_one]] 
        #self.play(*animations)
        self.play(*animations, step_one.next_to, after_one[-1], UP,  0.5, rate_func=smooth)
        self.wait()
        step_one.add_updater(lambda mobj: mobj.next_to(after_one[-1], UP, buff = 0.5))
        self.play(MoveAlongPath(person_one, arc))
        person_one.add_updater(lambda m : m.next_to(after_one[2], UP, buff=0))
        self.wait()



        after_two = create_stairs(num_steps)
        [step.shift(RIGHT  * 2 * shift_right_factor) for step in after_two]
        person_two = Circle()
        person_two.set_width(person_radius)
        person_two.next_to(after_two[0], UP, buff = 0)
        arc = ArcBetweenPoints(person_two.get_center(), after_two[4].get_center() + UP * person.get_width()/2, angle = -TAU / 4) 
        anim_2 = [FadeInFrom(piece, LEFT) for piece in after_two + [person_two] ] 
#        self.play(*anim_2)
        self.play(*anim_2, step_two.next_to,after_two[-1], UP, 0.5 , rate_func=smooth)
        self.wait()
        step_two.add_updater(lambda mobj: mobj.next_to(after_two[-1], UP, buff = 0.5))
        self.play(MoveAlongPath(person_two, arc), FadeOut(options))
        person_two.add_updater(lambda mobj: mobj.next_to(after_two[4], UP, buff = 0))
        self.wait()



        self.play(steps[0].shift, UP * up_shift, rate_func=smooth)
        self.play(after_one[0].shift, UP * up_shift , rate_func=smooth)
        self.play(after_two[0].shift, UP * up_shift , rate_func=smooth)
        self.wait()

        how_two = TextMobject("How many ways are there to climb from each point")
        how_two.to_edge(DOWN)
        self.play(FadeInFromDown(how_two))


        func_call = TexMobject("count\_stair\_ways(n)")
        func_call.scale(0.5)
        func_call.next_to(steps[0], DOWN, buff=0.5)
        func_call.align_to(steps[0], LEFT)
        self.play(FadeInFrom(func_call, UP))

        func_call_1 = TexMobject("count\_stair\_ways(n - 1)")
        func_call_1.scale(0.5)
        func_call_1.next_to(after_one[0], DOWN, buff=0.5)
        func_call_1.align_to(after_one[0], LEFT)
        self.play(FadeInFrom(func_call_1, UP))

        func_call_2 = TexMobject("count\_stair\_ways(n - 2)")
        func_call_2.scale(0.5)
        func_call_2.next_to(after_two[0], DOWN, buff=0.5)
        func_call_2.align_to(after_two[0], LEFT)
        self.play(FadeInFrom(func_call_2, UP))
        
        self.play(FadeOut(how_two))

        equal = TexMobject("=")
        plus = TexMobject("+")
        
        remove_one = [FadeOut(step) for step in steps + [person]]
        remove_two = [FadeOut(step) for step in after_one + [person_one]]
        remove_three = [FadeOut(step) for step in after_two + [person_two]]
        self.play( *remove_one, *remove_two, *remove_three,FadeOut(step_two), FadeOut(step_one))
        self.play(func_call.move_to, ORIGIN + 4 * LEFT, rate_func=smooth)
        equal.next_to(func_call, RIGHT, 0.3)
        self.play(func_call_1.next_to, func_call, RIGHT, 1)
        plus.next_to(func_call_1, RIGHT, 0.3)
        self.play(func_call_2.next_to, func_call_1, RIGHT, 1 )
        self.play(FadeIn(plus), FadeIn(equal))
        



        
