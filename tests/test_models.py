# tests/test_models.py
import unittest
import os
import tempfile
import gc 
from pathlib import Path
from database import set_db_path, init_db
from models import Task

class TestTaskModel(unittest.TestCase):
    
    @classmethod
    def setUpClass(cls):
        """Usa banco em memória compartilhada (SQLite support this)."""
        cls.temp_db = tempfile.NamedTemporaryFile(delete=True)
        set_db_path(cls.temp_db.name)
        init_db()
        cls.temp_db.close()
    
    @classmethod
    def tearDownClass(cls):
        """Executado uma vez depois de todos os testes."""
        # Remove o arquivo temporário
        gc.collect()
        try:
            os.unlink(cls.temp_db.name)
        except PermissionError:
            print(f"⚠️ Não foi possível deletar {cls.temp_db.name} no Windows")
            pass

    def setUp(self):
        """Executado antes de CADA teste."""
        # Limpa a tabela para isolar testes
        conn = Task._get_connection()  # Precisaremos expor isso
        with conn:
            conn.execute("DELETE FROM tasks")

    def test_create_task(self):
        """Testa a criação de uma tarefa."""
        task_id = Task.create("Estudar testes")
        self.assertIsInstance(task_id, int)
        self.assertGreater(task_id, 0)

    def test_get_all_tasks(self):
        """Testa listagem de tarefas."""
        Task.create("Tarefa 1")
        Task.create("Tarefa 2", "Descrição opcional")
        
        tasks = Task.get_all()
        self.assertEqual(len(tasks), 2)
        self.assertEqual(tasks[0].title, "Tarefa 2")  # Mais recente primeiro

    def test_mark_task_as_done(self):
        """Testa atualização de status."""
        task_id = Task.create("Tarefa para concluir")
        Task.update(task_id, done=True)
        
        task = Task.get_by_id(task_id)
        self.assertTrue(task.done)

if __name__ == '__main__':
    unittest.main()