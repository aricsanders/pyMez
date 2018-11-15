#-----------------------------------------------------------------------------
# Name:        ProgramAnalysis
# Purpose:    To analyze and report on code
# Author:      Aric Sanders
# Created:     4/10/2017
# License:     MIT License
#-----------------------------------------------------------------------------
""" This module contains definitions for Analyzing Code. In particular, it has functions
to generate black box diagrams of functions or scripts in svg for help support


Requirements
------------
+ [sys](https://docs.python.org/2/library/sys.html)
+ [os](https://docs.python.org/2/library/os.html)
+ [re](https://docs.python.org/2/library/re.html)



Help
---------------
<a href="./index.html">`pyMez.Code.Analysis`</a>
<div>
<a href="../../../pyMez_Documentation.html">Documentation Home</a> |
<a href="../../index.html">API Documentation Home</a> |
<a href="../../../Examples/html/Examples_Home.html">Examples Home</a> |
<a href="../../../Reference_Index.html">Index</a>
</div>
 """
#-----------------------------------------------------------------------------
# Standard Imports
import sys
import os
import inspect

#-----------------------------------------------------------------------------
# Third Party Imports
sys.path.append(os.path.join(os.path.dirname( __file__ ), '..','..'))
from Code.DataHandlers.HTMLModels import *
from Code.DataHandlers.Translations import *
from Code.DataHandlers.TouchstoneModels import *


#-----------------------------------------------------------------------------
# Module Constants

#-----------------------------------------------------------------------------
# Module Functions
def create_svg_black_box_diagram(inputs, outputs, function, **options):
    """Creates a svg black box diagram given a input dictionary of name:value pairs, an outputs list of
    output names and a function. Options are keywords that define the appearence of the diagram, to display the diagram
    append it to the body of an html sheet"""
    defaults = {"image_width": 1200,
                "image_height": 300,
                "title_height": 100,
                "edge_border": 5,
                "path_border": 50,
                "grid_style": "stroke:black;stroke-width:1;stroke-dasharray:5, 5, 1, 5",
                "input_box_stroke": "black",
                "input_box_stroke_width": "1",
                "input_box_opacity": ".25",
                "input_line_style": "stroke:black;stroke-width:5",
                "action_box_style": "stroke:black;stroke-width:1;opacity:.25;",
                "action_box_stroke": "black",
                "action_box_stroke_width": "1",
                "action_box_opacity": ".25",
                "output_line_style": "stroke:black;stroke-width:5",
                "output_box_stroke": "black",
                "output_box_stroke_width": "1",
                "output_box_opacity": ".25",
                "title_text_ratio": 3,
                "box_text_ratio": 8,
                "arrow_fill": "#f00",
                "output_transformation_function": None,
                "output_mime_type": "text/plain"

                }
    example_options = {}
    for key, value in defaults.items():
        example_options[key] = value
    for key, value in options.items():
        example_options[key] = value
    palette_width = example_options["image_width"]
    palette_height = example_options["image_height"]
    title_height = example_options["title_height"]
    edge_border = example_options["edge_border"]
    path_border = example_options["path_border"]
    thirds = round(palette_width / 3.0)
    input_names = list(inputs.keys())
    number_inputs = len(input_names)
    output_names = outputs
    number_outputs = len(output_names)
    output_data = function(**inputs)
    if example_options["output_transformation_function"]:
        output_data = example_options["output_transformation_function"](output_data)
        # print(output_data)
    if isinstance(output_data, ListType):
        output_dictionary = {name: output_data[i] for i, name in enumerate(output_names)}
    else:
        output_dictionary = {output_names[0]: output_data}

    box_text_ratio = example_options["box_text_ratio"]

    input_box_height = (palette_height - (number_inputs + 1) * edge_border) / number_inputs
    output_box_height = (palette_height - (number_outputs + 1) * edge_border) / number_outputs
    box_width = thirds - 2 * edge_border - path_border
    new_svg = make_html_element(tag="svg", width="{0}".format(palette_width),
                                height="{0}".format(palette_height + title_height),
                                **{"xmlns:xlink": "http://www.w3.org/1999/xlink"})
    new_def = make_html_element(tag="defs")
    new_marker = make_html_element(tag="marker", id="arrow",
                                   markerWidth="10",
                                   markerHeight="10",
                                   refX="10",
                                   refY="3",
                                   orientd="M0,0 L0,6 L9,3 z", fill=example_options["arrow_fill"], orient="auto",
                                   markerUnits="strokeWidth")
    new_path = make_html_element(tag="path", **{"d": "M0,0 L0,6 L9,3 z", "fill": "#f00"})
    new_marker.append(new_path)
    new_def.append(new_marker)
    new_svg.append(new_def)
    line_template = "M {4} 0 l 0 {0} M {1} 0 l 0 {0} M {2} 0 l 0 {0} M {3} 0 l 0 {0} M 0 {0} l {3} 0 M 0 0 l {3} 0"
    new_line = make_html_element(tag="path",
                                 **{"d": line_template.format(palette_height,
                                                              thirds,
                                                              2 * thirds,
                                                              palette_width - edge_border,
                                                              edge_border),
                                    "style": example_options["grid_style"]})
    new_svg.append(new_line)
    for i in range(number_inputs):
        new_anchor = String_to_SVGAnchorLinkElement(str(inputs[input_names[i]]))
        new_rect = make_html_element(tag="rect", **{"x": str(2 * edge_border),
                                                    "y": str(i * input_box_height + (i + 1) * edge_border),
                                                    "height": str(input_box_height),
                                                    "width": str(box_width),
                                                    "id": "inputs-{0}".format(i),
                                                    "stroke": example_options["input_box_stroke"],
                                                    "stroke-width": example_options["input_box_stroke_width"],
                                                    "opacity": example_options["input_box_opacity"]})

        new_path = make_html_element(tag="path",
                                     **{"d": "M {0} {1} L {2} {3}".format(2 * edge_border + box_width,
                                                                          i * input_box_height + (
                                                                          i + 1) * edge_border + input_box_height / 2,
                                                                          path_border + thirds, palette_height / 2.0),
                                        "marker-end": "url(#arrow)", "style": example_options["input_line_style"]})
        new_text = make_html_element(tag="text", text=input_names[i], **{"x": str(2 * edge_border + box_width / 2),
                                                                         "y": str(i * input_box_height + (
                                                                         i + 1) * edge_border + input_box_height / 2),
                                                                         "font-weight": "bold",
                                                                         "font-size": "{0}px".format(max(box_width,
                                                                                                         input_box_height) / box_text_ratio),
                                                                         "text-anchor": "middle",
                                                                         "alignment-baseline": "middle",
                                                                         "stroke": "black"})
        new_svg.append(new_text)
        new_svg.append(new_path)
        new_anchor.append(new_rect)
        new_svg.append(new_anchor)
    for i in range(number_outputs):
        new_anchor = String_to_SVGAnchorLinkElement(str(output_dictionary[output_names[i]]),
                                                    mime_type=example_options["output_mime_type"])
        new_rect = make_html_element(tag="rect", **{"x": str(path_border + 2 * thirds),
                                                    "y": str(i * output_box_height + (i + 1) * edge_border),
                                                    "height": str(output_box_height),
                                                    "width": str(box_width),
                                                    "id": "outputs-{0}".format(i),
                                                    "stroke": example_options["output_box_stroke"],
                                                    "stroke-width": example_options["output_box_stroke_width"],
                                                    "opacity": example_options["output_box_opacity"]})

        new_path = make_html_element(tag="path",
                                     **{"d": "M {0} {1} L {2} {3}".format(2 * thirds - path_border,
                                                                          palette_height / 2.0,
                                                                          path_border + 2 * thirds,
                                                                          i * output_box_height + (
                                                                          i + 1) * edge_border + output_box_height / 2),
                                        "marker-end": "url(#arrow)",
                                        "style": example_options["output_line_style"]})
        new_text = make_html_element(tag="text", text=output_names[i],
                                     **{"x": str(2 * edge_border + path_border + 2 * thirds + box_width / 2),
                                        "y": str(i * output_box_height + (i + 1) * edge_border + output_box_height / 2),
                                        "font-weight": "bold",
                                        "font-size": "{0}px".format(output_box_height / box_text_ratio),
                                        "text-anchor": "middle",
                                        "alignment-baseline": "middle",
                                        "stroke": "black"})
        new_svg.append(new_text)
        new_svg.append(new_path)
        new_anchor.append(new_rect)
        new_svg.append(new_anchor)

    new_anchor = String_to_SVGAnchorLinkElement(str(inspect.getsource(function)))

    new_rect = make_html_element(tag="rect", **{"x": str(path_border + thirds),
                                                "y": str(edge_border), "height": str(palette_height - 2 * edge_border),
                                                "width": str(thirds - 2 * path_border), "id": "Action",
                                                "stroke": "black",
                                                "stroke-width": "1", "opacity": ".25"})
    new_text = make_html_element(tag="text", text=function.__name__, **{"x": str(3 * thirds / 2),
                                                                        "y": str(palette_height / 2),
                                                                        "font-weight": "bold",
                                                                        "font-size": "{0}px".format(
                                                                            output_box_height / box_text_ratio),
                                                                        "text-anchor": "middle",
                                                                        "alignment-baseline": "middle",
                                                                        "stroke": "black"})
    inputs_title = make_html_element(tag="text", text="Inputs", **{"x": str(thirds / 2),
                                                                   "y": str(palette_height + title_height / 2),
                                                                   "font-weight": "bold",
                                                                   "font-size": "{0}px".format(title_height / 3),
                                                                   "text-anchor": "middle",
                                                                   "alignment-baseline": "middle",
                                                                   "text-decoration": "underline"})
    action_title = make_html_element(tag="text", text="Action", **{"x": str(3 * thirds / 2),
                                                                   "y": str(palette_height + title_height / 2),
                                                                   "font-weight": "bold",
                                                                   "font-size": "{0}px".format(title_height / 3),
                                                                   "text-anchor": "middle",
                                                                   "alignment-baseline": "middle",
                                                                   "text-decoration": "underline"})
    output_title = make_html_element(tag="text", text="Outputs", **{"x": str(5 * thirds / 2),
                                                                    "y": str(palette_height + title_height / 2),
                                                                    "font-weight": "bold",
                                                                    "font-size": "{0}px".format(title_height / 3),
                                                                    "text-anchor": "middle",
                                                                    "alignment-baseline": "middle",
                                                                    "text-decoration": "underline"})
    new_svg.append(inputs_title)
    new_svg.append(action_title)
    new_svg.append(output_title)
    new_svg.append(new_text)
    new_anchor.append(new_rect)
    new_svg.append(new_anchor)
    return new_svg


#-----------------------------------------------------------------------------
# Module Classes

#-----------------------------------------------------------------------------
# Module Scripts
def test_create_svg_black_box_diagram():
    """Uses a simple function to test the functionality of creating and svg
    diagram"""
    new_svg = create_svg_black_box_diagram(inputs={"s2p": S2PV1(os.path.join(TESTS_DIRECTORY, "thru.s2p"))},
                                           outputs=["S2P_as_xml"], function=S2PV1_to_XmlDataTable,
                                           output_transformation_function=lambda x: x.to_HTML(
                                               os.path.join(TESTS_DIRECTORY,
                                                            '../XSL/S2P_DB_STYLE.xsl')),
                                           output_mime_type="text/html",box_text_ratio=15)
    new_html = HTMLBase()
    new_html.add_head()
    new_html.add_body()
    new_html.append_to_body({"tag": "br"})
    new_html.append_to_body(new_svg)
    new_html.append_to_head({"tag": "style", "text": "rect:hover {stroke-width:8;stroke:blue;}"})
    new_html.show()
#-----------------------------------------------------------------------------
# Module Runner
if __name__ == '__main__':
    test_create_svg_black_box_diagram()
    