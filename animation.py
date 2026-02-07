from rich.progress import Progress, SpinnerColumn, TextColumn, BarColumn, TimeElapsedColumn

def create_progress(total_tests):
    return Progress(
        SpinnerColumn(),
        TextColumn("[bold cyan]Running testcases"),
        BarColumn(),
        TextColumn("{task.completed}/{task.total}"),
        TimeElapsedColumn(),
        transient=True
    ), total_tests