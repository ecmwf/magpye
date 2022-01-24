from Magics import macro as magics

toplot = []
triangles = [
    # Front leg
    ([60, 75, 65], [-45, -50, -60], 1.0),
    ([63, 68, 90], [-62, -57, -90], 1.0),
    ([90, 100, 105], [-90, -85, -90], 1.0),
    # Back leg
    ([60, 50, 45], [-45, -60, -38], 1.0),
    ([43, 50, 58], [-55, -53, -90], 1.0),
    ([58, 68, 73], [-90, -85, -90], 1.0),
    # Tail
    ([-170, -150, -90], [-65, -53, -45], 0.7),
    ([-180, 0, -90], [-60, -10, -45], 1.0),
    ([60, 0, 20], [-45, -23, -20], 0.7),
    ([0, 20, -90], [-10, -20, -45], 0.4),
    ([0, 80, 20], [-10, 0, -20], 0.6),
    ([80, 60, 20], [0, -45, -20], 0.9),
    # Body
    ([80, 150, 60], [0, 0, -45], 0.1),
    ([60, 150, 75], [-45, 0, -50], 0.4),
    ([150, 80, 130], [0, 0, 35], 0.2),
    ([0, 60, 80], [-10, 20, 0], 0.7),
    ([0, 55, 60], [-10, 28, 20], 1.0),
    ([60, 100, 80], [20, 25, 0], 0.8),
    ([55, 100, 60], [28, 25, 20], 0.6),
    ([80, 100, 130], [0, 25, 35], 0.7),
    ([100, 110, 130], [25, 50, 35], 0.8),
    ([100, 55, 110], [25, 28, 50], 1),
    ([150, 130, 165], [0, 35, 45], 0.6),
    # Head
    ([165, 160, 170], [45, 55, 65], 0.7),
    ([165, 130, 160], [45, 35, 55], 0.8),
    ([130, 135, 160], [35, 65, 55], 0.9),
    ([130, 110, 135], [35, 50, 65], 0.7),
    ([135, 130, 160], [65, 75, 55], 0.7),
    ([130, 150, 160], [75, 88, 55], 0.9),
    ([150, 162, 160], [88, 82, 55], 0.8),
    ([160, 162, 170], [55, 82, 65], 0.5),
    ([130, 132, 150], [75, 87, 88], 0.8),
    ([130, 115, 132], [75, 80, 87], 1.0),
    ([130, 110, 115], [75, 74, 80], 0.7),
]


output = magics.output(
    output_formats=["pdf", "svg", "png"],
    output_name_first_page_number="off",
    output_name="magpye",
)

x = 20
y = 10
map = magics.mmap(
    super_page_x_length=x,
    super_page_y_length=y,
    page_x_length=x,
    page_y_length=y,
    page_x_position=0,
    page_y_position=0,
    subpage_x_length=x,
    subpage_y_length=y,
    subpage_x_position=0,
    subpage_y_position=0,
    page_id_line=False,
    subpage_frame=False,
)  # , subpage_map_projection = "robinson", subpage_frame = False)

text = magics.mtext(
    text_lines=["magpye"],
    text_justification="left",
    text_font_size=3.0,
    text_box_blanking=False,
    text_mode="positional",
    text_box_x_position=2.0,
    text_box_y_position=11,
    text_box_x_length=10,
    text_box_y_length=10,
    text_colour="charcoal",
)


coast = magics.mcoast(
    map_coastline_colour="grey",
    map_coastline_land_shade="on",
    map_coastline_land_shade_colour="grey",
    map_coastline_sea_shade="off",
    map_grid_line_colour="grey",
    map_grid=False,
    map_grid_border="on",
    map_grid_line_style="dot",
    map_label="off",
)

for triangle in triangles:
    lat = triangle[1]
    lat.append(lat[0])
    lon = triangle[0]
    lon.append(lon[0])
    alpha = triangle[2]

    colour = "HSL(211,0.4,{})".format(1 - alpha)

    geo = magics.minput(
        input_type="geographical",
        input_latitude_values=lat,
        input_longitude_values=lon,
    )

    blue = magics.mline(
        polyline_line_colour="charcoal",
        polyline_line_thickness=0,
        polyline_shade=True,
        polyline_shade_max_level_colour=colour,
        polyline_shade_min_level_colour=colour,
    )
    toplot.append(geo)
    toplot.append(blue)

magics.plot(output, map, coast, toplot)
