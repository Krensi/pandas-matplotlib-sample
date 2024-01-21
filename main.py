import pandas as pd
import matplotlib.pyplot as plt
import numpy as np

import clustered_plot


def load_sample_data(file_path="samples.xlsx"):
    """
    Load samples from xslx file from different sheets

    Sheet data can be suffixed with extra string to avoid name collision
    if column names are the same in both sheet (see `suffixes`)"""
    try:
        # Read data from two different sheets
        df_sheet_one = pd.read_excel(file_path, sheet_name=0)
        df_sheet_two = pd.read_excel(file_path, sheet_name=1)

        # Merge the two DataFrames based on the 'Hour' column
        df = pd.merge(df_sheet_one, df_sheet_two, on="Hour", suffixes=("_one", "_two"))

        return df
    except FileNotFoundError:
        print(f"Error: File '{file_path}' not found.")
        return None


def load_sample_average_deviation(file_path="samples.xlsx"):
    try:
        # Read data from two different sheets
        df_sheet_one = pd.read_excel(file_path, sheet_name=0)
        # df_sheet_two = pd.read_excel(file_path, sheet_name='sheet_two')

        # Merge the two DataFrames based on the 'Hour' column
        # df = pd.merge(df_sheet_one, df_sheet_two, on='Hour')
        df = df_sheet_one

        return df
    except FileNotFoundError:
        print(f"Error: File '{file_path}' not found.")
        return None


def plot_grouped_temperatures(
    x_axis_data: list[float],
    y_axis_data: tuple[list[float], list[float]],
    y_axis_error_data: tuple[list[float], list[float]],
):
    """
    Print grouped bar
    https://www.pythoncharts.com/matplotlib/grouped-bar-charts-matplotlib/"""
    species = ("Adelie", "Chinstrap", "Gentoo")
    penguin_means = {
        "Bill Depth": (18.35, 18.43, 14.98),
        "Bill Length": (38.79, 48.83, 47.50),
        "Flipper Length": (189.95, 195.82, 217.19),
    }

    x = np.arange(len(species))  # the label locations
    width = 0.25  # the width of the bars
    multiplier = 0

    fig, ax = plt.subplots(layout="constrained")

    for attribute, measurement in penguin_means.items():
        offset = width * multiplier
        rects = ax.bar(x + offset, measurement, width, label=attribute)
        ax.bar_label(rects, padding=3)
        multiplier += 1

    # Add some text for labels, title and custom x-axis tick labels, etc.
    ax.set_ylabel("Length (mm)")
    ax.set_title("Penguin attributes by species")
    ax.set_xticks(x + width, species)
    ax.legend(loc="upper left", ncols=3)
    ax.set_ylim(0, 250)

    plt.show()


def plot_stacked_temperatures_with_error_bars(
    x_axis_data: list[float],
    y_axis_data: tuple[list[float], list[float]],
    y_axis_error_data: tuple[list[float], list[float]],
):
    """
    Print stacked bar chart with error bars

    Example with stacked bars which was used as inspiration
    https://www.w3resource.com/graphics/matplotlib/barchart/matplotlib-barchart-exercise-14.php"""

    # This code of course can be put into a loop to stack an arbitrary number of values
    def create_bar_plot(ax, x, y, yerr, bottom, label, color):
        # Create the bars only in a plot
        ax.bar(
            x=x,
            height=y,
            fill=True,
            label=label,
            color=color,
            edgecolor="black",
            alpha=1.0,
            linewidth=1,
            bottom=bottom,
        )

        # Create error bar separately
        plotline, caplines, barlinecols = ax.errorbar(
            x=x,
            y=y
            if bottom is None
            else y
            + bottom,  # if bottom is not None we have to add it to y to offset the error bar to the correct position
            yerr=yerr,
            lolims=True,
            capsize=0,
            ls="None",
            color="k",
        )

        # Adjust appearance of error marker
        caplines[0].set_marker("_")
        caplines[0].set_markersize(5)

    # Create figure and axis
    # The axis can be passed to a plot function
    # Therefore, We can call add things to the plot incrementally
    fig, ax = plt.subplots()

    # Create first bar plot
    create_bar_plot(
        ax,
        x_axis_data,
        y_axis_data[0],
        y_axis_error_data[0],
        bottom=None,
        label="Samples 1",
        color="orange",
    )

    # Create second bar plot which is stacked on the first bar plot
    create_bar_plot(
        ax,
        x_axis_data,
        y_axis_data[1],
        y_axis_error_data[1],
        bottom=y_axis_data[0],  # Pass other data as bottom to stack them
        label="Samples 2",
        color="green",
    )

    ax.set_xlabel("Hour")
    ax.set_ylabel("Temperature (°C)")
    ax.set_title("Stacked Graph")
    ax.legend(loc="upper left")
    fig.show()

    # Return for later use. `ax` can be used to plot further things on it.
    # `fig` can be used to store the figure as file with `fig.savefig`
    return [fig, ax]


def plot_temperatures_with_error_bars(
    x_axis_data: list[float],
    y_axis_data: list[float],
    y_axis_error_data: list[float],
):
    """
    Print bar chart with error bars

    Example with clustered:
    https://stackoverflow.com/questions/45752981/removing-the-bottom-error-caps-only-on-matplotlib"""
    fig, ax = plt.subplots()

    # Create the bars only in a plot
    ax.bar(
        x=x_axis_data,
        height=y_axis_data,
        fill=True,
        label="Average Temperature with Deviation",
        edgecolor="black",
        alpha=1.0,
        linewidth=1,
    )

    # Create error bar separately
    plotline, caplines, barlinecols = ax.errorbar(
        x=x_axis_data,
        y=y_axis_data,
        yerr=y_axis_error_data,
        lolims=True,
        capsize=0,
        ls="None",
        color="k",
    )

    # Adjust appearance of error marker
    caplines[0].set_marker("_")
    caplines[0].set_markersize(5)

    ax.set_xlabel("Hour")
    ax.set_ylabel("Temperature (°C)")
    ax.set_title("Temperature and Standard Deviation Over a Day")
    ax.legend(loc="upper right")
    fig.show()

    # Return for later use. `ax` can be used to plot further things on it.
    # `fig` can be used to store the figure as file with `fig.savefig`
    return [fig, ax]


if __name__ == "__main__":
    plot = clustered_plot.ClusteredPlot("test", "ytext", "xtest", ["one", "two"])
    plot.add_subgroup_with_data("one", "subone", [1, 2])
    plot.add_subgroup_with_data("one", "subone", [3, 4])
    plot.add_subgroup_with_data("one", "subtwo", [5, 6])
    plot.add_subgroup_with_data("two", "subtwo", [5, 6])

    df = load_sample_data()
    pass
    plot_grouped_temperatures(None, None, None)

    plot_temperatures_with_error_bars(
        x_axis_data=df["Hour"],
        y_axis_data=df["Average_one"],
        y_axis_error_data=df["Deviation_one"],
    )

    plot_stacked_temperatures_with_error_bars(
        x_axis_data=df["Hour"],
        y_axis_data=[df["Average_one"], df["Average_two"]],
        y_axis_error_data=[df["Deviation_one"], df["Deviation_two"]],
    )
    pass
