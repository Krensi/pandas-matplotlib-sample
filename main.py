import pandas as pd
import matplotlib.pyplot as plt


def load_sample_data(file_path="samples.xlsx"):
    try:
        # Read data from two different sheets
        df_sheet_one = pd.read_excel(file_path, sheet_name="sheet_one")
        df_sheet_two = pd.read_excel(file_path, sheet_name="sheet_two")

        # Merge the two DataFrames based on the 'Hour' column
        df = pd.merge(df_sheet_one, df_sheet_two, on="Hour")

        return df
    except FileNotFoundError:
        print(f"Error: File '{file_path}' not found.")
        return None


"""
Load samples from xslx file
"""
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


"""
Print bar chart with error bars

Example with clustered:
https://stackoverflow.com/questions/45752981/removing-the-bottom-error-caps-only-on-matplotlib
"""
def plot_temperatures_with_error_bars(df):
    x_axis_data = df["Hour"]
    y_axis_data = df["Average"]
    y_axis_error_data = df["Deviation"]

 
    # Create the bars only in a plot
    plt.bar(
        x=x_axis_data,
        height=y_axis_data,
        fill = True,
        label="Average Temperature with Deviation",
        edgecolor="black",
        alpha=1.0, linewidth=1
    )

    # Create error bar separately
    plotline, caplines, barlinecols = plt.errorbar(
        x=x_axis_data,
        y=y_axis_data,
        yerr=y_axis_error_data,
        lolims=True,
        capsize=0,
        ls="None",
        color="k",
    )
    
    # Adjust appearance of error marker
    caplines[0].set_marker('_')
    caplines[0].set_markersize(5)

    plt.xlabel("Hour")
    plt.ylabel("Temperature (°C)")
    plt.title("Temperature and Standard Deviation Over a Day")
    plt.legend()
    plt.show()

def plot_temperatures(df):
    plt.plot(df["Hour"], df["Average"], label="Average")
    plt.plot(df["Hour"], df["Deviation"], label="Deviation")
    plt.xlabel("Hour")
    plt.ylabel("Temperature (°C)")
    plt.title("Temperature Curves Over a Day")
    plt.legend()
    plt.show()


if __name__ == "__main__":
    df = load_sample_average_deviation()
    pass
    plot_temperatures_with_error_bars(df)
    pass
