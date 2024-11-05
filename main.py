from textual.app import App, ComposeResult
from textual.containers import Container
from textual.widgets import Static, Button
from textual.reactive import reactive
from rich.text import Text
import asyncio
import json
import os

# Load electoral data from JSON file
with open("electoral_map.json", "r") as f:
    ELECTORAL_DATA = json.load(f)


class EmptyButton(Button):
    """A placeholder button for empty grid spaces."""

    def __init__(self):
        super().__init__("")
        self.styles.background = "black"
        self.disabled = True


class StateButton(Button):
    """A button representing a state on the map."""

    def __init__(self, state: str, data: dict):
        super().__init__(f"{state}\n({data['votes']})")
        self.state = state
        self.votes = data["votes"]
        self.status = "undecided"  # can be "undecided", "democrat", or "republican"
        self.row = data["row"]
        self.col = data["col"]
        self.rowspan = data.get("rowspan", 1)
        self.colspan = data.get("colspan", 1)
        # Add properties for live results
        self.reporting = 0.0
        self.dem_exit = 0.0
        self.rep_exit = 0.0
        self.dem_votes = 0
        self.rep_votes = 0
        self.called = False

    def update_results(self, results: dict) -> None:
        """Update the button with live results."""
        if self.state in results:
            state_data = results[self.state]
            self.reporting = state_data["reporting"]
            self.dem_exit = state_data["exit_poll"]["democrat"]
            self.rep_exit = state_data["exit_poll"]["republican"]
            self.dem_votes = state_data["counted"]["democrat"]
            self.rep_votes = state_data["counted"]["republican"]
            self.called = state_data["called"]

            # Calculate vote percentages for display
            total_votes = self.dem_votes + self.rep_votes
            dem_pct = (self.dem_votes / total_votes * 100) if total_votes > 0 else 0
            rep_pct = (self.rep_votes / total_votes * 100) if total_votes > 0 else 0

            # Update colors based on results
            if self.called:
                # If called, use the counted results to determine color
                if self.dem_votes > self.rep_votes:
                    self.status = "democrat"
                    self.styles.background = "blue"
                elif self.rep_votes > self.dem_votes:
                    self.status = "republican"
                    self.styles.background = "red"
            else:
                # If not called, use a lighter shade to indicate leading but not called
                if total_votes > 0:
                    if self.dem_votes > self.rep_votes:
                        self.status = "undecided"
                        self.styles.background = "#000066"  # Darker blue
                    elif self.rep_votes > self.dem_votes:
                        self.status = "undecided"
                        self.styles.background = "#660000"  # Darker red
                    else:
                        self.status = "undecided"
                        self.styles.background = "grey"
                else:
                    self.status = "undecided"
                    self.styles.background = "grey"

            # Update label to show vote percentages and called status
            called_indicator = "✓" if self.called else ""
            if total_votes > 0:
                self.label = f"{self.state} {called_indicator}\n({self.votes})\n{dem_pct:.1f}% - {rep_pct:.1f}%\n{total_votes:,} votes"
            else:
                self.label = f"{self.state} {called_indicator}\n({self.votes})\n{self.reporting:.1f}% reporting"

    def on_button_pressed(self) -> None:
        """Cycle through states when clicked."""
        if self.status == "undecided":
            self.status = "democrat"
            self.styles.background = "blue"
        elif self.status == "democrat":
            self.status = "republican"
            self.styles.background = "red"
        else:
            self.status = "undecided"
            self.styles.background = "grey"

        # Tell the parent to update totals
        self.app.update_electoral_votes()


class ElectoralMap(Static):
    """The main electoral map widget."""

    def get_grid_bounds(self) -> tuple[int, int]:
        """Calculate the maximum dimensions of the grid."""
        max_row = 0
        max_col = 0

        for data in ELECTORAL_DATA["states"].values():
            row = data["row"]
            col = data["col"]
            rowspan = data.get("rowspan", 1)
            colspan = data.get("colspan", 1)

            max_row = max(max_row, row + rowspan)
            max_col = max(max_col, col + colspan)

        return max_row, max_col

    def is_position_occupied(self, row: int, col: int, state_positions: set) -> bool:
        """Check if a grid position is occupied by any state."""
        return (row, col) in state_positions

    def get_occupied_positions(self) -> set:
        """Get all grid positions occupied by states."""
        positions = set()
        for data in ELECTORAL_DATA["states"].values():
            row = data["row"]
            col = data["col"]
            rowspan = data.get("rowspan", 1)
            colspan = data.get("colspan", 1)

            for r in range(row, row + rowspan):
                for c in range(col, col + colspan):
                    positions.add((r, c))

        return positions

    def compose(self) -> ComposeResult:
        """Create child widgets of the electoral map."""
        max_row, max_col = self.get_grid_bounds()
        occupied_positions = self.get_occupied_positions()

        # Create a mapping of positions to state buttons
        state_buttons = {}
        for state, data in ELECTORAL_DATA["states"].items():
            row = data["row"]
            col = data["col"]
            state_buttons[(row, col)] = (state, data)

        with Container(id="map-container"):
            # Yield buttons in grid order
            for row in range(max_row):
                for col in range(max_col):
                    if (row, col) in state_buttons:
                        # Create and yield state button
                        state, data = state_buttons[(row, col)]
                        yield StateButton(state, data)
                    elif not self.is_position_occupied(row, col, occupied_positions):
                        # Create and yield empty button
                        empty = EmptyButton()
                        empty.styles.grid_column_start = str(col + 1)
                        empty.styles.grid_column_span = "1"
                        empty.styles.grid_row_start = str(row + 1)
                        empty.styles.grid_row_span = "1"
                        yield empty


class ElectoralCounter(Static):
    """Widget to display electoral vote totals."""

    dem_votes = reactive(0)
    rep_votes = reactive(0)
    dem_total_votes = reactive(0)
    rep_total_votes = reactive(0)

    def render(self) -> Text:
        """Render the vote counter."""
        return Text.assemble(
            ("Democratic: ", "blue"),
            (f"{self.dem_votes} ({self.dem_total_votes:,})", "white"),
            " | ",
            ("Republican: ", "red"),
            (f"{self.rep_votes} ({self.rep_total_votes:,})", "white"),
            " | ",
            "270 to win",
        )


class ElectoralMapApp(App):
    """The main application class."""

    CSS = """
    ElectoralMapApp {
        layout: grid;
        grid-size: 2;
        grid-rows: auto 1fr;
    }

    #map-container {
        layout: grid;
        grid-size: 11 8;
        grid-columns: 1fr;
        grid-rows: 1fr;
        padding: 1;
        width: 100%;
    }

    StateButton {
        width: 100%;
        height: 100%;
        background: grey;
        content-align: center middle;
        text-align: center;
    }

    EmptyButton {
        width: 100%;
        height: 100%;
        content-align: center middle;
        text-align: center;
    }

    ElectoralCounter {
        dock: top;
        height: 3;
        background: $boost;
        color: $text;
        border-bottom: tall $background;
        padding: 0 1;
        content-align: center middle;
    }
    """

    def compose(self) -> ComposeResult:
        """Create child widgets of the application."""
        yield ElectoralCounter()
        yield ElectoralMap()

    async def poll_results(self) -> None:
        """Background task to poll for election results."""
        while True:
            if os.path.exists("current_results.json"):
                try:
                    with open("current_results.json", "r") as f:
                        results = json.load(f)
                        if "states" in results:
                            # Update all state buttons with new results
                            for button in self.query(StateButton):
                                button.update_results(results["states"])
                            # Update electoral vote totals
                            self.update_electoral_votes()
                except (json.JSONDecodeError, IOError):
                    # Handle potential file read errors silently
                    pass
            await asyncio.sleep(1)  # Poll every second

    def on_mount(self) -> None:
        """Handle the mount event to position states."""
        for button in self.query(StateButton):
            button.styles.grid_column_start = str(button.col + 1)  # Grid is 1-based
            button.styles.grid_column_span = str(button.colspan)
            button.styles.grid_row_start = str(button.row + 1)  # Grid is 1-based
            button.styles.grid_row_span = str(button.rowspan)

        # Start the background polling task using the app's run_worker method
        self.run_worker(self.poll_results(), exclusive=True)

    def update_electoral_votes(self) -> None:
        """Update the electoral vote totals."""
        counter = self.query_one(ElectoralCounter)
        dem_electoral = rep_electoral = 0
        dem_total = rep_total = 0

        for button in self.query(StateButton):
            # Add to popular vote totals regardless of called status
            dem_total += button.dem_votes
            rep_total += button.rep_votes

            # Only count called states in the electoral total
            if button.called:
                if button.dem_votes > button.rep_votes:
                    dem_electoral += button.votes
                elif button.rep_votes > button.dem_votes:
                    rep_electoral += button.votes

        counter.dem_votes = dem_electoral
        counter.rep_votes = rep_electoral
        counter.dem_total_votes = dem_total
        counter.rep_total_votes = rep_total


if __name__ == "__main__":
    app = ElectoralMapApp()
    app.run()
