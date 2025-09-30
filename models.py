# models.py
from database import create_connection

class Task:
    def __init__(self, id=None, title="", description="", done=False, created_at=None):
        self.id = id
        self.title = title
        self.description = description
        self.done = bool(done)  # Garante que seja booleano
        self.created_at = created_at

    @staticmethod
    def create(title: str, description: str = ""):
        """Cria uma nova tarefa."""
        conn = create_connection()
        with conn:
            cursor = conn.execute(
                "INSERT INTO tasks (title, description) VALUES (?, ?)",
                (title, description)
            )
            task_id = cursor.lastrowid
        # Não feche manualmente — 'with' já fechou
        return task_id

    @staticmethod
    def get_all():
        """Retorna todas as tarefas."""
        conn = create_connection()
        cursor = conn.execute("SELECT * FROM tasks ORDER BY created_at DESC")
        rows = cursor.fetchall()
        conn.close()  # Aqui NÃO usamos 'with', então fechamos manualmente
        return [Task(**dict(row)) for row in rows]

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
            params.append(int(done))  # SQLite usa 0/1 para boolean

        if not updates:
            conn.close()
            return False

        params.append(task_id)
        query = f"UPDATE tasks SET {', '.join(updates)} WHERE id = ?"
        with conn:
            conn.execute(query, params)
        # 'with' já fechou
        return True

    @staticmethod
    def delete(task_id: int):
        """Deleta uma tarefa pelo ID."""
        conn = create_connection()
        with conn:
            conn.execute("DELETE FROM tasks WHERE id = ?", (task_id,))
        return True