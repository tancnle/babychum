# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db.models import Count, Case, When
from django.db.models.functions import TruncDate

import plotly.offline as plotly
import plotly.graph_objs as go

from reports import utils


def diaperchange_types(changes):
    """
    Create a graph showing types of totals for diaper changes.
    :param changes: a QuerySet of Diaper Change instances.
    :returns: a tuple of the the graph's html and javascript.
    """
    changes = changes.annotate(date=TruncDate('time'))\
        .values('date') \
        .annotate(wet_count=Count(Case(When(wet=True, then=1)))) \
        .annotate(solid_count=Count(Case(When(solid=True, then=1)))) \
        .annotate(total=Count('id')) \
        .order_by('-date')

    solid_trace = go.Scatter(
        mode='markers',
        name='Solid',
        x=list(changes.values_list('date', flat=True)),
        y=list(changes.values_list('solid_count', flat=True)),
    )
    wet_trace = go.Scatter(
        mode='markers',
        name='Wet',
        x=list(changes.values_list('date', flat=True)),
        y=list(changes.values_list('wet_count', flat=True))
    )
    total_trace = go.Scatter(
        name='Total',
        x=list(changes.values_list('date', flat=True)),
        y=list(changes.values_list('total', flat=True))
    )

    layout_args = utils.default_graph_layout_options()
    layout_args['barmode'] = 'stack'
    layout_args['title'] = '<b>Diaper Change Types</b>'
    layout_args['xaxis']['title'] = 'Date'
    layout_args['xaxis']['rangeselector'] = utils.rangeselector_date()
    layout_args['yaxis']['title'] = 'Number of changes'

    fig = go.Figure({
        'data': [solid_trace, wet_trace, total_trace],
        'layout': go.Layout(**layout_args)
    })
    output = plotly.plot(fig, output_type='div', include_plotlyjs=False)
    return utils.split_graph_output(output)
