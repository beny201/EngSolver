import math
from typing import Union

from shapely.geometry import LineString, Point
from shapely.ops import nearest_points


class CreatingCorner:
    START_POINTS = (0, 0)

    def creating_lines(
        self,
        girder_angle: float,
        girder_height: int,
        t_flange_girder: int,
        column_width: int,
        t_flange_column: int,
        t_plate_connection: int,
        length_bolt: float,
        total_length_bolt: float,
        thickness_washer: float,
        space_for_screw: float,
    ):
        start_points_x, start_points_y = self.START_POINTS

        # drawings first line top flange column
        point_a = Point(start_points_x, start_points_y)
        point_b = Point(start_points_x, start_points_y - 3000)
        line_ab = LineString([point_a, point_b])
        flange_ab = line_ab.parallel_offset(t_flange_column, "left")

        # drawings second line bottom flange column
        line_cd = line_ab.parallel_offset(column_width, "left")
        point_c = Point(line_cd.coords[0])
        point_d = Point(line_cd.coords[1])

        # drawings third line top flange
        point_e = Point(3000, (math.tan(math.radians(girder_angle))) * 2000)
        line_ae = LineString([point_a, point_e])
        flange_ae = line_ae.parallel_offset(t_flange_girder, "right")

        # drawings forth line bottom flange
        line_fg = line_ae.parallel_offset(girder_height, "right")

        point_f = Point(line_fg.coords[0])
        point_g = Point(line_fg.coords[1])

        # drawings line for connection
        point_h = line_cd.intersection(line_fg)
        line_ah = LineString([point_a, point_h])

        # bottom_flange_view_ridge
        line_gh = LineString([point_g, point_h])

        # bottom_flange_view_column
        line_dh = LineString([point_d, point_h])

        # offset to find distance for bolts height
        line_ij = line_ah.parallel_offset(
            total_length_bolt + t_plate_connection, "left"
        )

        # offset to find distance for bolts height, assembly from bottom
        line_ij1 = line_ah.parallel_offset(
            total_length_bolt + t_plate_connection, "right"
        )

        # offset to find distance for bolts height, assembly from bottom,
        # check top space
        line_ij2 = line_ah.parallel_offset(space_for_screw + t_plate_connection, "left")

        # offset to find distance for bolts height, assembly from top,
        # check bottom space
        line_ij3 = line_ah.parallel_offset(
            space_for_screw + t_plate_connection, "right"
        )

        # intersection height of bolt and flange
        point_k = line_ij.intersection(flange_ae)
        point_l = nearest_points(line_ah, point_k)

        line_kl = LineString([point_k, point_l[0]])

        looking_distance_top = point_a.distance(point_l)

        # intersection of columns flange and length of bolts
        point_m = line_ij1.intersection(flange_ab)
        point_n = nearest_points(line_ah, point_m)
        line_mn = LineString([point_m, point_n[0]])

        looking_distance_bottom = point_a.distance(point_n)

        # intersection of girder flange and space needed for rest of bolt from bottom mounting
        point_o = line_ij2.intersection(flange_ae)
        point_p = nearest_points(line_ah, point_o)
        line_op = LineString([point_o, point_p[0]])

        # intersection of column flange and space needed for rest of bolt from top mounting
        point_r = line_ij3.intersection(flange_ab)
        point_s = nearest_points(line_ah, point_r)

        line_rs = LineString([point_r, point_s[0]])
        looking_distance_top_space = point_a.distance(point_s)

        # drawing line of bolt when mounting from bottom
        point_t = nearest_points(line_ij1, point_o)

        line_pt = LineString([point_o, point_t[0]])

        looking_distance_bottom_space = point_a.distance(point_p)

        # drawing line of bolt when mounting from top
        point_u = nearest_points(line_ij2, point_r)

        line_ur = LineString([point_r, point_u[0]])

        extra_lines_to_shown = []

        if looking_distance_bottom_space[0] >= looking_distance_bottom[0]:
            value_bottom = looking_distance_bottom_space[0]
            extra_lines_to_shown.append(line_pt)
        else:
            value_bottom = looking_distance_bottom[0]
            extra_lines_to_shown.append(line_mn)

        if looking_distance_top_space[0] >= looking_distance_top[0]:
            value_top = looking_distance_top_space[0]
            extra_lines_to_shown.append(line_ur)
        else:
            value_top = looking_distance_top[0]
            extra_lines_to_shown.append(line_kl)

        return (
            [line_ab, line_ae, line_ah, line_gh, line_dh, *extra_lines_to_shown],
            [value_bottom, value_top],
        )
