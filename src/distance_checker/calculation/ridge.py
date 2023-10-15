import math

from shapely.geometry import LineString, Point
from shapely.ops import nearest_points


class CreatingRidge:
    START_POINTS = (0, 0)

    def creating_lines(
        self,
        left_girder_angle: float,
        right_girder_angle: int,
        girder_height: int,
        left_t_flange_girder: int,
        right_t_flange_girder: int,
        t_plate_connection: int,
        length_bolt: float,
        total_length_bolt: float,
        thickness_washer: float,
        space_for_screw: float,
    ):
        start_points_x, start_points_y = self.START_POINTS

        point_a1 = Point(start_points_x, start_points_y)
        point_a2 = Point(start_points_x, start_points_y - 1500)
        point_b1 = Point(1500, (math.tan(math.radians(-right_girder_angle))) * 1500)
        point_b2 = Point(-1500, (math.tan(math.radians(-left_girder_angle))) * 1500)
        line_a1b1 = LineString([point_a1, point_b1])
        line_a1b2 = LineString([point_a1, point_b2])

        # drawings thickness top flange right side
        line_a1b1_flange = line_a1b1.parallel_offset(right_t_flange_girder, "right")

        # drawings thickness top flange left side
        line_a1b2_flange = line_a1b2.parallel_offset(left_t_flange_girder, "left")
        # drawings line bottom flange
        line_a3b3 = line_a1b1.parallel_offset(girder_height, "right")
        line_a4b4 = line_a1b2.parallel_offset(girder_height, "left")

        point_b3 = Point(line_a3b3.coords[1])

        point_b4 = Point(line_a4b4.coords[1])

        # line for ridge connection
        line_a1a2 = LineString([point_a1, point_a2])
        point_a5 = line_a3b3.intersection(line_a1a2)
        point_a6 = line_a4b4.intersection(line_a1a2)

        # finding the lowest point
        if point_a5.y <= point_a6.y:
            end_point_for_ridge = point_a5
        else:
            end_point_for_ridge = point_a6

        line_a1_end_point_for_ridge = LineString([point_a1, end_point_for_ridge])

        point_a7 = line_a1a2.intersection(line_a3b3)
        point_a8 = line_a1a2.intersection(line_a4b4)

        line_b3a7 = LineString([point_b3, point_a7])
        line_b4a8 = LineString([point_b4, point_a8])

        # offset to find distance for bolts height mounting from left
        line_a1_offset_left = line_a1_end_point_for_ridge.parallel_offset(
            total_length_bolt + t_plate_connection, "right"
        )
        # offset to find distance for bolts height mounting from right
        line_a1_offset_right = line_a1_end_point_for_ridge.parallel_offset(
            total_length_bolt + t_plate_connection, "left"
        )

        # intersection on left side
        point_a9 = line_a1_offset_left.intersection(line_a1b2_flange)

        # intersection on right side
        point_a10 = line_a1_offset_right.intersection(line_a1b1_flange)

        # point on connection plate from left side
        point_a11 = nearest_points(line_a1_end_point_for_ridge, point_a9)

        # point on connection plate from right side
        point_a12 = nearest_points(line_a1_end_point_for_ridge, point_a10)

        # offset to find distance for bolts height, assembly from left, check right space
        line_space_mount_from_left = line_a1_end_point_for_ridge.parallel_offset(
            space_for_screw + t_plate_connection, "left"
        )

        point_a13 = line_space_mount_from_left.intersection(line_a1b1_flange)

        # point on connection plate from right side
        point_a14 = nearest_points(line_a1_end_point_for_ridge, point_a13)

        # finding the lowest point mounting left side
        if point_a14[0].y <= point_a11[0].y:
            mounting_from_left = point_a14[0]
        else:
            mounting_from_left = point_a11[0]

        point_a15 = nearest_points(line_a1_offset_left, mounting_from_left)
        line_a15 = LineString([point_a15[0], mounting_from_left])

        looking_value_mounting_from_left = point_a1.distance(mounting_from_left)

        # offset to find distance for bolts height, assembly from right, check left space
        line_space_mount_from_right = line_a1_end_point_for_ridge.parallel_offset(
            space_for_screw + t_plate_connection, "right"
        )

        point_a16 = line_space_mount_from_right.intersection(line_a1b2_flange)

        # point on connection plate from left side
        point_a17 = nearest_points(line_a1_end_point_for_ridge, point_a16)

        # finding the lowest point mounting right side
        if point_a17[0].y <= point_a12[0].y:
            mounting_from_right = point_a17[0]
        else:
            mounting_from_right = point_a12[0]

        point_a18 = nearest_points(line_a1_offset_right, mounting_from_right)
        line_a18 = LineString([point_a18[0], mounting_from_right])

        looking_value_mounting_from_right = point_a1.distance(mounting_from_right)

        return (
            [
                line_a1b1,
                line_a1b2,
                line_b3a7,
                line_b4a8,
                line_a1_end_point_for_ridge,
                line_a15,
                line_a18,
            ],
            [looking_value_mounting_from_left, looking_value_mounting_from_right],
        )
