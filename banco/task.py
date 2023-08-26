import redis

class TaskManager:
    def __init__(self, host='localhost', port=6379, db=0):
        self.redis_client = redis.Redis(host=host, port=port, db=db)

    def add_task(self, description):
        task_id = self.redis_client.incr('task_id')
        self.redis_client.set(f'task:{task_id}', description)
        return task_id

    def list_tasks(self):
        task_ids = self.redis_client.keys('task:*')
        tasks = []
        for task_id in task_ids:
            description = self.redis_client.get(task_id).decode('utf-8')
            tasks.append({'id': int(task_id.split(b':')[1]), 'description': description})
        return tasks

    def remove_task(self, task_id):
        task_key = f'task:{task_id}'
        if self.redis_client.exists(task_key):
            self.redis_client.delete(task_key)
            return True
        return False

def main():
    task_manager = TaskManager()

    while True:
        print("\n1. Adicionar Tarefa")
        print("2. Listar Tarefas")
        print("3. Remover Tarefa")
        print("4. Sair")

        choice = input("Escolha uma opção: ")

        if choice == '1':
            description = input("Digite a descrição da tarefa: ")
            task_id = task_manager.add_task(description)
            print(f"Tarefa adicionada com ID: {task_id}")
        elif choice == '2':
            tasks = task_manager.list_tasks()
            if tasks:
                for task in tasks:
                    print(f"ID: {task['id']} - Descrição: {task['description']}")
            else:
                print("Nenhuma tarefa encontrada.")
        elif choice == '3':
            task_id = int(input("Digite o ID da tarefa a ser removida: "))
            if task_manager.remove_task(task_id):
                print(f"Tarefa com ID {task_id} removida com sucesso.")
            else:
                print(f"Tarefa com ID {task_id} não encontrada.")
        elif choice == '4':
            break
        else:
            print("Opção inválida. Escolha novamente.")

if __name__ == "__main__":
    main()