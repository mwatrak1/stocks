from django.http import JsonResponse
from bokeh.plotting import figure
from bokeh.embed import json_item
from bokeh.models import HoverTool
import json
import yfinance as yf


def render_graph(request, **params):
    selected_stock = params.get("abbreviation")
    x, y = get_stocks_plot_x_data(selected_stock)
    tooltips = get_hover_tool_settings()
    graph = figure(width_policy="fit", max_width=960, height_policy='fit', aspect_ratio=2,
                   max_height=480, x_axis_type="datetime", align='center')
    graph.add_tools(tooltips)
    graph.line(x, y)
    html_graph = json.dumps(json_item(graph))
    response_body = {
        "abbreviation": selected_stock,
        "graph": html_graph
    }
    return JsonResponse(response_body)


def get_stocks_plot_x_data(abbreviation):
    stock_data_history = yf.download(abbreviation, period="10y", interval="1d")
    x_datetime = stock_data_history.High.keys().to_pydatetime()
    return x_datetime, stock_data_history.High.values


def get_hover_tool_settings():
    return HoverTool(
        tooltips=[
            ('date', '$x{%F}'),
            ('value', '$y{0,0.00}$')
        ],
        formatters={
            "$x": "datetime",
            "$y": "numeral"
        },
        mode='vline'
    )