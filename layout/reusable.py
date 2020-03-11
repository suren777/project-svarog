import dash_bootstrap_components as dbc
import dash_html_components as html

# import dash_core_components as dcc


def create_input_box(title, value, value_id, input_type="number"):
    """
    Creates input box
    -----------------
    Inputs:
    ------
    - title: Element name will be on top of the box
    - value: Default value shown in the input component
    - value_id: Unique id of the element, which will be 
    used in the callbacs later
    - input_type: input type
    -------
    Outputs:
    - html.Div element
    """
    return html.Div(
        dbc.InputGroup(
            [
                dbc.InputGroupAddon(title, addon_type="prepend"),
                dbc.Input(
                    placeholder=value,
                    value=value,
                    id=value_id,
                    type=input_type,
                ),
            ],
            className="mb-3",
        )
    )


# def create_input_box(title, value, value_id, input_type="number"):
#     """
#     Creates input box
#     -----------------
#     Inputs:
#     ------
#     - title: Element name will be on top of the box
#     - value: Default value shown in the input component
#     - value_id: Unique id of the element, which will be used in the callbacs later
#     - input_type: input type
#     -------
#     Outputs:
#     - html.Div element
#     """
#     return html.Div(
#         className="input-box",
#         children=[
#             html.Label(title, className="input-box-label"),
#             dcc.Input(
#                 id=value_id,
#                 value=value,
#                 type=input_type,
#                 className="input-box-input",
#             ),
#             html.Div(className="clearfix"),
#         ],
#     )
