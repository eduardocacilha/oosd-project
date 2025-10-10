# Sistema de Gestão de Festas - Arquitetura MVC

## Descrição
Sistema desenvolvido em Python para gerenciamento de festas e eventos, implementando o padrão arquitetural Model-View-Controller (MVC). O sistema permite o cadastro de usuários, criação de eventos, venda de ingressos e sistema de revenda entre usuários.

## Funcionalidades

### Gerenciamento de Usuários
- Cadastro de novos usuários
- Listagem de usuários cadastrados
- Exclusão de usuários
- Histórico de compras
- Sistema de avaliações de eventos

### Gerenciamento de Eventos
- Criação de novos eventos
- Alteração de informações de eventos
- Listagem de eventos disponíveis
- Visualização de detalhes e feedbacks
- Controle de capacidade

### Gerenciamento de Ingressos
- Compra de ingressos para eventos
- Sistema de revenda entre usuários
- Controle de preços personalizados
- Transferência de propriedade de ingressos

### Sistema de Feedbacks
- Avaliação de eventos (notas de 1 a 5)
- Comentários sobre eventos
- Histórico de avaliações por usuário

## Arquitetura MVC

### Models (Modelos)
Contêm a lógica de negócio e estrutura de dados:
- `Usuario`: Gerencia dados e operações relacionadas aos usuários
- `Evento`: Controla informações e funcionalidades dos eventos
- `Ingresso`: Gerencia ingressos e operações de compra/revenda
- `Feedback`: Estrutura para avaliações de eventos
- `Venda`: Registro de transações do sistema

### Views (Visões)
Interface de usuário e apresentação de dados:
- `MainView`: Menu principal do sistema
- `UsuarioView`: Interface para operações com usuários
- `EventoView`: Interface para gerenciamento de eventos
- `IngressoView`: Interface para operações com ingressos

### Controllers (Controladores)
Lógica de controle entre Models e Views:
- `MainController`: Controlador principal do sistema
- `UsuarioController`: Gerencia operações de usuários
- `EventoController`: Controla funcionalidades de eventos
- `IngressoController`: Gerencia operações de ingressos

## Estrutura do Projeto

```
sistema_festas_mvc/
├── main.py                 # Arquivo principal de execução
├── README.md              # Documentação do projeto
├── requirements.txt       # Dependências do projeto
├── models/               # Camada de Models
│   ├── __init__.py
│   ├── usuario.py
│   ├── evento.py
│   ├── ingresso.py
│   ├── feedback.py
│   └── venda.py
├── views/                # Camada de Views
│   ├── __init__.py
│   ├── main_view.py
│   ├── usuario_view.py
│   ├── evento_view.py
│   └── ingresso_view.py
└── controllers/          # Camada de Controllers
    ├── __init__.py
    ├── main_controller.py
    ├── usuario_controller.py
    ├── evento_controller.py
    └── ingresso_controller.py
```

## Como Executar

### Pré-requisitos
- Python 3.7 ou superior
- Dependências listadas em `requirements.txt`

### Instalação
1. Clone o repositório:
```bash
git clone <url-do-repositorio>
cd sistema_festas_mvc
```

2. Instale as dependências:
```bash
pip install -r requirements.txt
```

3. Execute o sistema:
```bash
python main.py
```

## Uso do Sistema

### Menu Principal
Ao executar o sistema, você verá o menu principal com as seguintes opções:
1. **Gerenciar Usuários** - Acesso ao módulo de usuários
2. **Gerenciar Eventos** - Acesso ao módulo de eventos
3. **Gerenciar Ingressos** - Acesso ao módulo de ingressos
0. **Finalizar sistema** - Encerra a aplicação

### Fluxo de Uso Típico
1. **Cadastrar usuários** no sistema
2. **Criar eventos** com suas informações
3. **Usuários compram ingressos** para os eventos
4. **Sistema de revenda** permite transferência entre usuários
5. **Avaliações e feedbacks** após os eventos

## Características Técnicas

### Padrões Implementados
- **MVC (Model-View-Controller)**: Separação clara de responsabilidades
- **Encapsulamento**: Atributos privados nos models
- **Validação de Dados**: Verificações de integridade nos controllers
- **Interface Consistente**: Padronização nas views

### Tratamento de Erros
- Validação de entrada do usuário
- Verificação de integridade de dados
- Mensagens de erro informativas
- Prevenção de operações inválidas

### Funcionalidades Avançadas
- Sistema de revenda peer-to-peer
- Controle de capacidade de eventos
- Histórico detalhado de transações
- Sistema de avaliações com notas e comentários

## Limitações Conhecidas
- Dados armazenados apenas em memória (não persistentes)
- Interface apenas em linha de comando
- Sem sistema de autenticação avançado
- Sem integração com sistemas de pagamento

## Possíveis Melhorias Futuras
- Implementação de banco de dados
- Interface gráfica (GUI)
- Sistema de autenticação robusto
- API REST para integração
- Relatórios e estatísticas
- Sistema de notificações

## Contribuição
Para contribuir com o projeto:
1. Faça um fork do repositório
2. Crie uma branch para sua feature
3. Implemente as mudanças seguindo o padrão MVC
4. Teste as funcionalidades
5. Submeta um pull request

## Licença
Este projeto está sob a licença MIT. Veja o arquivo LICENSE para mais detalhes.

## Autores
- Desenvolvido como projeto acadêmico
- Implementação do padrão MVC em Python
- Sistema de gestão de eventos e ingressos

---
*Sistema desenvolvido para fins educacionais - Disciplina de Desenvolvimento de Software Orientado a Objetos*