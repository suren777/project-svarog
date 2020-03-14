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


def create_input_form(
    label,
    id,
    value,
    type="number",
    placeholder="",
    label_width=2,
    input_width=10,
    disabled=False,
):
    return dbc.FormGroup(
        [
            dbc.Label(label, html_for="example-email-row", width=label_width),
            dbc.Col(
                dbc.Input(
                    type=type,
                    id=id,
                    placeholder=placeholder,
                    value=value,
                    disabled=disabled,
                ),
                width=input_width,
            ),
        ],
        row=True,
    )
