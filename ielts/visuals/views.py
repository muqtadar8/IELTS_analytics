from django.shortcuts import render
from plotly.offline import plot
import plotly.express as px
import pandas as pd

def writing_graph(request):
    # Dummy dataset
    data = {
        'Date': ['2023-01-01', '2023-01-07', '2023-01-14', '2023-01-21', '2023-01-28'],
        'Band_Score': [7.5, 5, 6.5, 7, 8.5],
    }

    df = pd.DataFrame(data)
    df['Date'] = pd.to_datetime(df['Date']) 

    # Plotting with Plotly Express
    fig = px.line(df, x='Date', y='Band_Score', title='IELTS Writing Band Score Progression')
    fig.update_layout(
        xaxis_title='Date',
        yaxis_title='Band Score',
        hovermode='closest',  # Show data for the closest point when hovering
    )

    # Adding markers
    fig.add_trace(px.scatter(df, x='Date', y='Band_Score').data[0])

    # Convert the plot to HTML
    plot_div = plot(fig, output_type='div', include_plotlyjs=False)

    return render(request, 'graph.html', {'plot_div': plot_div})

def listening_graph(request):
    # Dummy dataset
    data = {
        'Date': ['2023-01-01', '2023-01-07', '2023-01-14', '2023-01-21', '2023-01-28'],
        'Band_Score': [5, 5.5, 6.5, 7, 8.5],
    }

    df = pd.DataFrame(data)
    df['Date'] = pd.to_datetime(df['Date']) 

    # Plotting with Plotly Express
    fig = px.line(df, x='Date', y='Band_Score', title='IELTS Listening Band Score Progression')
    fig.update_layout(
        xaxis_title='Date',
        yaxis_title='Band Score',
        hovermode='closest',  # Show data for the closest point when hovering
    )

    # Adding markers
    fig.add_trace(px.scatter(df, x='Date', y='Band_Score').data[0])

    # Convert the plot to HTML
    plot_div = plot(fig, output_type='div', include_plotlyjs=False)

    return render(request, 'graph.html', {'plot_div': plot_div})

def reading_graph(request):
    # Dummy dataset
    data = {
        'Date': ['2023-01-01', '2023-01-07', '2023-01-14', '2023-01-21', '2023-01-28'],
        'Band_Score': [8, 8.5, 7.5, 7, 8.5],
    }

    df = pd.DataFrame(data)
    df['Date'] = pd.to_datetime(df['Date']) 

    # Plotting with Plotly Express
    fig = px.line(df, x='Date', y='Band_Score', title='IELTS Reading Band Score Progression')
    fig.update_layout(
        xaxis_title='Date',
        yaxis_title='Band Score',
        hovermode='closest',  # Show data for the closest point when hovering
    )

    # Adding markers
    fig.add_trace(px.scatter(df, x='Date', y='Band_Score').data[0])

    # Convert the plot to HTML
    plot_div = plot(fig, output_type='div', include_plotlyjs=False)

    return render(request, 'graph.html', {'plot_div': plot_div})