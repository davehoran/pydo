import typer
from rich.console import Console
from rich.table import Table

from model import Todo
from database import get_all_todos, delete_todo, insert_todo, complete_todo, update_todo

console = Console()

app = typer.Typer()

@app.command(short_help="adds an item to the todo list")
def add(task: str, category: str):
    typer.echo(f"adding '{task}' to [{category}] category")
    todo = Todo(task, category)
    insert_todo(todo)
    show()

@app.command(short_help="delete todo item")
def delete(position: int):
    typer.echo(f"deleting item number {position}")
    # indicies in UI begin at 1, but in database at 0
    delete_todo(position-1)
    show()

@app.command(short_help="update todo item")
def update(position: int, task: str = None, category: str = None):
    typer.echo(f"updating task {position}: [{category}] {task}")
    update_todo(position-1, task, category)
    show()

@app.command(short_help="mark todo item as complete")
def complete(position: int):
    typer.echo(f"marking item {position} as complete")
    complete_todo(position-1)
    show()

@app.command()
def show():
    tasks = get_all_todos()
    console.print("[bold magenta]Todos[/bold magenta]!", "_")

    table = Table(show_header=True, header_style="bold blue")
    table.add_column("#", style="dim", width=5)
    table.add_column("Todo", min_width=20)
    table.add_column("Category", min_width=12, justify="right")
    table.add_column("Done", min_width=12, justify="right")

    def get_category_color(category):
        COLORS = {'Code':'red','Chores':'cyan','Job':'green','Other':'yellow'}
        if category in COLORS:
            return COLORS[category]
        return 'white' # if not found return select white text

    for idx, task in enumerate(tasks, start=1):
        c = get_category_color(task.category)
        is_done_str = '✅' if task.status == 2 else '🔲'
        table.add_row(str(idx), task.task, f'[{c}]{task.category}[/{c}]', is_done_str)
    
    console.print(table)

if __name__ == "__main__":
    app()

