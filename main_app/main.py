
from turtle import Screen
import time
from snake import Snake,Scoreboard,Food

screen = Screen()
screen.tracer(0)
screen.colormode(255)
screen.setup(width=600,height=600)
screen.bgcolor("black")
screen.title("Snake Game")

snake = Snake()
food = Food()
scoreboard = Scoreboard()

while food.position() in [segment.position() for segment in snake.segments]:
    food.refresh()

screen.listen()
directions = ["Up","Down","Right","Left"]
for direction in directions:
    screen.onkey(snake.change_direction(direction),direction)

while True:
    time.sleep(0.15)
    
    snake.move()

    wall_collision_conditions =  [snake.head.xcor() > 280,
                             snake.head.xcor() < -280,
                             snake.head.ycor() > 280,
                             snake.head.ycor() < -280,
    ]
                             
    body_collision_conditions = [(round(snake.head.xcor() - segment.xcor(),2) , round(snake.head.ycor() - segment.ycor(),2))
                                for segment in snake.segments[1:]]
    # I'm checking if difference of x,y btw snake head and any other segment is (0,0)

    
    if round(snake.head.distance(food),2) == 0:
        food.refresh()
        snake.extend()
        scoreboard.increase_score()

    if any(wall_collision_conditions) or (0,0) in body_collision_conditions:
        scoreboard.game_over()
        break

    screen.update()

screen.exitonclick()
