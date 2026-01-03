from database import create_connection
from datetime import datetime, timezone

# Function for applying test
# def _get_connection():
#     return create_connection()

class Task:
    def __init__(self, id=None, title="", description="", done=False, created_at=None):
        self.id = id
        self.title = title
        self.description = description
        self.done = bool(done)  # Ensure the return of boolean value
        if isinstance(created_at, str):
            naive_dt = datetime.fromisoformat(created_at)
            self.created_at = naive_dt.replace(tzinfo=timezone.utc)
        else:
            self.created_at = created_at
        
    @staticmethod # Decorator
    def create(title: str, description: str = ""):
        """Create a new task with created_at em UTC in ISO format."""
        created_at = datetime.now(timezone.utc).strftime("%Y-%m-%d %H:%M:%S")
        conn = create_connection()
        with conn:
            cursor = conn.execute(
                "INSERT INTO tasks (title, description, created_at) VALUES (?, ?, ?)",
                (title, description, created_at)
            )
            task_id = cursor.lastrowid
        return task_id

    @staticmethod
    def get_all():
        """Retorna todas as tarefas."""
        conn = create_connection()
        try:
            cursor = conn.execute("SELECT * FROM tasks ORDER BY created_at DESC")
            rows = cursor.fetchall() # fetchall retrun the list of all lines
            return [Task(**dict(row)) for row in rows]
        finally:
            conn.close()  # Here we not using 'with', so closed manually 

    @staticmethod
    def get_by_id(task_id: int):
        """Retorna uma tarefa pelo ID."""
        conn = create_connection()
        cursor = conn.execute("SELECT * FROM tasks WHERE id = ?", (task_id,))
        row = cursor.fetchone()
        conn.close()
        return Task(**dict(row)) if row else None

    @staticmethod
    def update(task_id: int, title: str = None, description: str = None, done: bool = None):
        """Atualiza uma tarefa existente."""
        conn = create_connection()
        updates = []
        params = []

        if title is not None:
            updates.append("title = ?") 
            params.append(title)
        if description is not None:
            updates.append("description = ?")
            params.append(description)
        if done is not None:
            updates.append("done = ?")
            params.append(int(done))  # SQLite use 0/1 for represent a boolean

        if not updates:
            conn.close()
            return False

        params.append(task_id)
        query = f"UPDATE tasks SET {', '.join(updates)} WHERE id = ?"
        with conn:
            conn.execute(query, params)
        return True

    @staticmethod
    def delete_tarefa_concluida(task_id: int):
        """Deleta uma tarefa pelo ID apenas se ela estiver concluída."""
        conn = create_connection()
        with conn:
            conn.execute("DELETE FROM tasks WHERE id = ? AND done = True", (task_id,))
        return True
    
    @staticmethod
    def delete_all_tasks():
        """Deleta todas as tarefas."""
        conn = create_connection()
        with conn:
            conn.execute("DELETE FROM tasks")
            conn.execute("DELETE FROM sqlite_sequence WHERE name='tasks'") # Reset the id autoincrement value
        return True
    