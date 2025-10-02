from models import Task
from database import init_db

def print_tasks(tasks):
    if not tasks:
        print("Nenhuma tarefa encontrada.")
        return
    for t in tasks:
        status = "✅" if t.done else "⏳"
        print(f"[{t.id}] {status} {t.title}")
        if t.description:
            print(f"    Descrição: {t.description}")
        print(f"    Criada em: {t.created_at}\n")

def main():
    init_db()
    while True:
        print("\n===== App To-Do List =====")
        print("1. Adicionar tarefa")
        print("2. Listar tarefas")
        print("3. Marcar como concluída")
        print("4. Atualizar tarefa")
        print("5. Deletar tarefa")
        print("0. Sair")
        choice = input("Escolha uma opção: ")

        if choice == "1":
            title = input("Título: ")
            desc = input("Descrição (opcional): ")
            Task.create(title, desc)
            print("✅ Tarefa adicionada!")

        elif choice == "2":
            tasks = Task.get_all()
            print_tasks(tasks)

        elif choice == "3":
            try:
                task_id = int(input("ID da tarefa: "))
                if Task.update(task_id, done=True):
                    print("✅ Tarefa marcada como concluída!")
                else:
                    print("❌ Tarefa não encontrada.")
            except ValueError:
                print("❌ ID inválido.")

        elif choice == "4":
            try:
                task_id = int(input("ID da tarefa: "))
                task = Task.get_by_id(task_id)
                if not task:
                    print("❌ Tarefa não encontrada.")
                    continue
                title = input(f"Novo título ({task.title}): ").strip() or task.title
                desc = input(f"Nova descrição ({task.description}): ").strip() or task.description
                Task.update(task_id, title=title, description=desc)
                print("✅ Tarefa atualizada!")
            except ValueError:
                print("❌ ID inválido.")

        elif choice == "5":
            try:
                task_id = int(input("ID da tarefa: "))
                Task.delete(task_id)
                print("🗑️ Tarefa deletada!")
            except ValueError:
                print("❌ ID inválido.")

        elif choice == "0":
            print("Programa finalizado.")
            break

        else:
            print("Opção inválida.")

if __name__ == "__main__":
    main()