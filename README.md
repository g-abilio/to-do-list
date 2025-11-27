# To-Do List API com Flask

## 👥 Membros do Grupo
- Gabriel Abílio Barbosa Ferreira 

---

## 📝 Sobre o Sistema
Este projeto consiste em uma aplicação web de um **To-Do List**, desenvolvida com **Python** e **Flask**.

O sistema permite que o usuário gerencie suas tarefas do dia a dia de forma prática, oferecendo funcionalidades como:  
- Criar uma nova tarefa  
- Listar todas as tarefas cadastradas  
- Marcar uma tarefa como concluída  
- Remover uma tarefa  

O objetivo principal deste projeto é evidenciar como o uso de testes automatizados auxilia na manutenção de sistemas de software, garantindo maior confiabilidade e facilitando a evolução da aplicação.  

---

## ⚙️ Tecnologias Utilizadas
O projeto foi desenvolvido utilizando as seguintes tecnologias:  

- **Linguagem de Programação**: Python
- **Framework Web**: Flask  
- **Banco de Dados**:  
  - SQLite
- **Testes Automatizados**:  
  - pytest
- **Cliente de Teste de API**: cURL

---

## ✅ Como executar os testes localmente
Para executar os testes localmente, utilize o seguinte comando na raíz do projeto: 

```bash
  pytest
```

Caso queira executar somente os testes de integração ou os testes unitários, utilize os seguintes comandos na raíz do projeto, respectivamente: 

```bash
  pytest tests/test_integration.py
```

```bash
  pytest tests/test_unit.py
```
