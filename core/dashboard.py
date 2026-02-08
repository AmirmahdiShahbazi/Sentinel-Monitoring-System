from rich.live import Live
from rich.table import Table
from rich.console import Console
from rich import box

class Dashboard:
    def __init__(self, engine):
        self.engine = engine
        self.console = Console()

    def generate_table(self) -> Table:
        table = Table(
            title="[bold cyan]Sentinel Monitoring System[/bold cyan]", 
            box=box.DOUBLE_EDGE
        )
        
        table.add_column("Check Name", style="white")
        table.add_column("Status", justify="center")
        table.add_column("Response", justify="right")
        table.add_column("Last Message", style="dim")

        for name, result in self.engine.results_cache.items():
            if result is None:
                table.add_row(name, "[yellow]INITIALIZING[/]", "-", "Waiting for first run...")
            else:
                color = "green" if result.status else "red"
                status_icon = "✔" if result.status else "✘"
                
                table.add_row(
                    f"[bold]{name}[/bold]",
                    f"[{color}]{status_icon} {'UP' if result.status else 'DOWN'}[/]",
                    f"{result.response_time}s" if result.response_time > 0 else "-",
                    f"[{color}]{result.message}[/]"
                )
        
        return table

    def get_live_display(self):
        """Returns the Live context manager initialized with the table."""
        return Live(self.generate_table(), refresh_per_second=4, console=self.console)