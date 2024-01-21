import matplotlib


class ClusteredPlotError(Exception):
    """ Custom error type """
    pass


class ClusteredPlot:
    """
    Helper class which should make data management for plots easier
    """
    def __init__(self, title: str, ylabel: str, xlabel: str, groups: list[str]) -> None:
        self.title = title
        self.ylabel = ylabel
        self.xlabel = xlabel

        # `self.groups` is a dictionary containing the keys of `groups` with empty dicts as value
        self.groups = {name: {} for name in groups}

        self.figure, self.axis = matplotlib.subplots()
        pass

    def add_subgroup_with_data(
        self, group: str, subgroup_name: str, subgroup_data: list[float]
    ):
        """
        Add data to a subgroup within a group. The group must exist!
        If the group does not exist, the subgroup name is empty or the data is empty an exception is raised.
        If the subgroup exists, the data will be appended. Otherwise a new subgroup with the name and data is created.
        """
        if subgroup_name == "" or len(subgroup_data) == 0:
            raise ClusteredPlotError(ValueError("Name or data empty"))

        add_to = self.groups.get(group)

        if add_to is None:
            raise ClusteredPlotError("Group not existing")

        sub = add_to.get(subgroup_name)
        if sub is None:
            # Subgroup not existing
            add_to[subgroup_name] = subgroup_data
        else:
            sub.extend(subgroup_data)
        pass

    @property
    def groups(self):
        """
        Getter function of groups
        """
        return self.groups

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
        return self.axis

    @property
    def figure(self):
        """
        Getter function for figure

        Useful for e.g. custom save to file
        """
        return self.figure
