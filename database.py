import sqlite3
from typing import List
import datetime
from model import Todo

conn = sqlite3.connect('todos.db')
c = conn.cursor()

def create_table():
    c.execute("""CREATE TABLE IF NOT EXISTS todos (
              task text,
              category text,
              date_added text,
              date_completed text,
              status integer,
              position integer
              )""")
    
create_table()

def insert_todo(todo: Todo):
    c.execute('SELECT count(*) FROM todos')
    count = c.fetchone()[0]
    todo.position = count if count else 0

    with conn:
        # use param subsitutuion to prevent sql injection attack
        c.execute('INSERT INTO todos VALUES (:task, :category, :date_added, :date_completed, :status, :position)',
        {'task': todo.task, 'category': todo.category, 'date_added': todo.date_added, 
         'date_completed': todo.date_conpleted, 'status': todo.status, 'position': todo.position})
        
def get_all_todos() -> List[Todo]:
    c.execute('SELECT * FROM todos')
    results = c.fetchall()
    todos = []
    for result in results:
        # use * syntax on result to auto-upack the values and input to constructor function
        todos.append(Todo(*result))
    return todos

def delete_todo(position):
    c.execute('SELECT count(*) from todos')
    count = c.fetchone()[0]
    
    with conn: 
        c.execute("DELETE FROM todos WHERE position=:position", {"position": position})
        for pos in range(position+1, count):
            change_position(pos, pos-1, False)
            # when exiting the 'with conn' context, all transactions are auto committed.
            # This is why we pass FALSE to the the change_position function. 

def change_position(old_position: int, new_position: int, commit=True):
    c.execute('UPDATE todos SET position = :position_new WHERE position = :position_old',
              {'position_old': old_position, 'position_new': new_position})
    if commit:
        conn.commit()
        # we passed in FALSE, so commit will never happen here, but rather when the calling 
        # conn: context is closed

def update_todo(position: int, task: str, category: str):
    with conn:
        if task is not None and category is not None:
            c.execute('UPDATE todos SET task = :task, category = :category WHERE position = :position',
                      {'position': position, 'task': task, 'category': category})
        elif task is not None:
            c.execute('UPDATE todos SET task = :task WHERE position = :position',
                      {'position': position, 'task': task})
        elif category is not None:
            c.execute('UPDATE todos SET category = :category WHERE position = :position',
                      {'position': position, 'category': category})

def complete_todo(position: int):
    with conn:
        c.execute('UPDATE todos SET status = 2, date_completed = :date_completed WHERE position = :position',
                  {'position': position, 'date_completed': datetime.datetime.now().isoformat()})
        
