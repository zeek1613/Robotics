# Variation 4 group
# mudathirmahgoub
# heardwulf
# Jaykang Heo
# ben stoffer

import cozmo

threshold = 50


def turn_right(robot):
    robot.turn_in_place(cozmo.util.degrees(-90)).wait_for_completed()
    return


def turn_left(robot):
    robot.turn_in_place(cozmo.util.degrees(90)).wait_for_completed()


def move_straight(robot: cozmo.robot.Robot, unit):
    robot.drive_straight(cozmo.util.distance_mm(unit), cozmo.util.speed_mmps(150)).wait_for_completed()

def move(robot: cozmo.robot.Robot, x, y, unit):

    # avoid division by zero
    if unit == 0:
        return

    # turn cozmo to be straight
    angle_z = robot.pose.rotation.angle_z
    robot.turn_in_place(cozmo.util.degrees(-angle_z.degrees)).wait_for_completed()

    # get the current position
    current_x, current_y, current_z = robot.pose.position.x, robot.pose.position.y, robot.pose.position.z

    # compute the vertical and horizontal units
    alternating_movement = int(min(abs(x - current_x), abs(y - current_y)) / unit)

    if x < current_x:
        robot.turn_in_place(cozmo.util.degrees(-180)).wait_for_completed()

    # determine the turn directions
    if (x >= current_x and y >= current_y) or (x < current_x and y < current_y):
        turn_vertical = turn_left
        turn_horizontal = turn_right
    else:
        turn_vertical = turn_right
        turn_horizontal = turn_left

    # move horizontally and vertically
    for i in range(alternating_movement):
        move_straight(robot, unit)
        turn_vertical(robot)
        move_straight(robot, unit)
        turn_horizontal(robot)

    # get the current position
    current_x, current_y, current_z = robot.pose.position.x, robot.pose.position.y, robot.pose.position.z

    # finish the remaining horizontal movement
    if abs(x - current_x) > threshold:
        move_straight(robot, abs(x - current_x))

    # finish the remaining vertical movement
    if abs(y - current_y) > threshold:
        turn_vertical(robot)
        move_straight(robot, abs(y - current_y))

    # print the current position and difference from target
    current_x, current_y, current_z = robot.pose.position.x, robot.pose.position.y, robot.pose.position.z
    print("Destination: ({0}, {1})".format(x, y))
    print("Position   : ({0}, {1})".format(current_x, current_y))
    print("Difference : ({0}, {1})".format(abs(x - current_x), abs(y - current_y)))


def cozmo_program(robot: cozmo.robot.Robot):
    move(robot, 0, -150, 50)


if __name__ == "__main__":
    cozmo.run_program(cozmo_program)-