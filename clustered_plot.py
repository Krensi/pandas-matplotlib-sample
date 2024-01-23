import matplotlib.pyplot as plt
import numpy as np

class ClusteredPlotError(Exception):
    """ Custom error type """
    pass

class ClusteredPlot:
    """
    Helper class which should make data management for plots easier
    """
    def __init__(self, title: str, xlabel: str, ylabel: str, groups: list[str], sub_groups: list[str], bar_width = 0.25) -> None:
        self.title = title
        self.ylabel = ylabel
        self.xlabel = xlabel

        for groupname, subgroupname in zip(groups, sub_groups):
            if groupname == "" or subgroupname == "":
                raise ClusteredPlotError(ValueError("Empty group or subgroup name"))

        # `self.groups` is a dictionary containing the keys of `groups` with empty dicts as value
        self._groups = {name: {subname:([],[],[]) for subname in sub_groups} for name in groups}

        self.bar_width = bar_width

        self._figure, self._axis = plt.subplots()
        pass

    def add_subgroup_with_data(
        self, group: str, subgroup: str, data: list[float], error_data: list[float], labels: [str]
        ):
        """
        Add data to a subgroup within a group. The group and the subgroup must exist!
        If the list contains more than one item, the values will be stacked within the bar chart. 
        The number of values for each subgroup needs to be the same in all groups!
        """
        if len(data) == 0 or len(error_data) == 0 or len(labels) == 0:
            raise ClusteredPlotError(ValueError("No values in data or error data"))
            

        add_to = self.groups.get(group, {}).get(subgroup)

        if add_to is None:
            raise ClusteredPlotError(f"subgroup {subgroup} in group {group} not existing")

        add_to[0].extend(data)
        add_to[1].extend(error_data)
        add_to[2].extend(labels)

    @property
    def groups(self):
        """
        Getter function of groups
        """
        return self._groups

    @property
    def subgroups(self, group: str):
        """
        Getter function for subgroups

        Returns subgroups or None if group not existing
        """
        return self.groups.get(group)

    @property
    def axis(self):
        """
        Getter function to get axis

        Useful for some further adjustments of axis properties like legend..
        """
        return self._axis

    @property
    def figure(self):
        """
        Getter function for figure

        Useful for e.g. custom save to file
        """
        return self._figure
    

    def create_plot(self):
        """
        Plot the graph
        """
        x = np.arange(len(self.groups))
        multiplier = 0

        # Map values from `self.groups` to representation for plotting
        group_names = [k for k in self.groups.keys()]
        subgroup_names = [[k for k in sub.keys()] for sub in self.groups.values()][0]
        subgroup_values = [[v for v in sub.values()] for sub in self.groups.values()]
        subgroup_values = list(zip(*subgroup_values))

        for attribute, measurements in zip(subgroup_names, subgroup_values):

            previous_bar_values = None
            previous_error_bar_values = None

            # TODO: Handle labels better..
            for i in range(len(measurements[0]) - 1):
                bar_values = [x[0][i] for x in measurements]
                error_bar_values = [x[1][i] for x in measurements]
                labels = [x[2][i] for x in measurements]

                offset = self.bar_width * multiplier
                rects = self.axis.bar(x + offset, bar_values, self.bar_width, label=labels[i], bottom = previous_bar_values)

                plotline, caplines, barlinecols = self.axis.errorbar(
                x=x + offset,
                y=bar_values
                if previous_bar_values is None
                else [sum(x) for x in zip(previous_bar_values, bar_values)],  # if bottom is not None we have to add it to y to offset the error bar to the correct position
                yerr=error_bar_values,
                lolims=True,
                capsize=0,
                ls="None",
                color="k",
                )

                # Adjust appearance of error marker
                caplines[0].set_marker("_")
                caplines[0].set_markersize(5)
                
                previous_bar_values = bar_values
                previous_error_bar_values = error_bar_values

            multiplier += 1

        # Add some text for labels, title and custom x-axis tick labels, etc.
        self.axis.set_ylabel("Length (mm)")
        self.axis.set_title("Some Random Data")
        self.axis.set_xticks(x + self.bar_width / len(group_names), group_names)
        self.axis.legend(loc="upper left", ncols=len(group_names))
        # self.axis.grid()
    

        self._figure.show()

        pass
        