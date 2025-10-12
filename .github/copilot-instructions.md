Com certeza! Como especialista em engenharia de prompts de IA e arquitetura de software, preparei uma resposta completa em duas partes:

O Prompt Mestre: Um prompt detalhado e estruturado para você usar diretamente no chat do GitHub Copilot no VS Code. Ele é projetado para guiar a IA na criação do aplicativo passo a passo, seguindo as melhores práticas.

Análise e Justificativa da Estratégia: Uma explicação do porquê o prompt foi estruturado dessa forma, qual a melhor stack tecnológica para este projeto e como interagir com o Copilot para obter os melhores resultados.

1. O Prompt Mestre para o GitHub Copilot
Copie e cole o texto abaixo diretamente na janela de chat do GitHub Copilot no VS Code.

Markdown

# PROMPT MESTRE PARA CRIAÇÃO DE LIMPADOR DE SISTEMA LINUX

## Persona e Objetivo

Você é um engenheiro de software sênior especialista em desenvolvimento de aplicações desktop para Linux, com profundo conhecimento em arquitetura de software, princípios SOLID, design de UI/UX e otimização de sistemas.

Nosso objetivo é criar um aplicativo desktop chamado **"Quantum Cleaner"** (nome provisório). Ele será um limpador de sistema para Linux, moderno, eficiente e com uma interface de usuário extremamente elegante e intuitiva, inspirada na filosofia de design da Apple. O público-alvo são tanto usuários comuns quanto desenvolvedores.

## Requisitos e Arquitetura

Siga estritamente os requisitos e a arquitetura definidos abaixo.

### [1. Stack Tecnológica Sugerida]

* **Linguagem:** Python 3.10+
* **Framework de UI:** Qt 6, utilizando a biblioteca PySide6 (binding oficial do Qt para Python).
* **Estilização:** Qt Style Sheets (QSS) para customização completa da aparência.
* **Empacotamento:** Foco em Flatpak e Snap para distribuição universal nas lojas de aplicativos Linux.

### [2. Arquitetura do Software (Baseada em SOLID)]

Vamos usar uma arquitetura em camadas para garantir separação de responsabilidades e manutenibilidade:

1.  **Camada de Apresentação (UI):**
    * Responsável por toda a interface gráfica.
    * Componentes Qt (janelas, botões, listas).
    * Não contém lógica de negócio. Apenas exibe dados e captura interações do usuário.
    * Emite sinais (signals) para a camada de serviço quando o usuário realiza uma ação.

2.  **Camada de Serviço (Core Logic):**
    * Contém toda a lógica de negócio e orquestração.
    * Ex: `CleaningService` que coordena as diferentes tarefas de limpeza.
    * Recebe solicitações da UI e utiliza os módulos da camada de acesso a dados/sistema para executá-las.
    * É agnóstica à UI. Poderia ser usada por uma interface de linha de comando (CLI) se necessário.

3.  **Camada de Acesso a Dados e Sistema (Modules):**
    * Conjunto de módulos especializados, cada um com uma única responsabilidade (Princípio da Responsabilidade Única - SRD).
    * Exemplos de módulos:
        * `SystemCacheCleaner`: Limpa caches do sistema (`/var/cache`, `~/.cache`).
        * `LogCleaner`: Rotaciona e limpa logs antigos (`/var/log`).
        * `TrashCleaner`: Esvazia a lixeira do usuário.
        * `PackageManagerCleaner`: Limpa caches de pacotes (APT, DNF, Pacman).
        * `DockerCleaner`: Encontra e remove imagens, contêineres e volumes órfãos do Docker.
        * `K8sCleaner`: Limpa caches de ferramentas como `minikube` ou `kind`.
    * Esses módulos interagem diretamente com o sistema de arquivos e executam comandos de shell de forma segura.

### [3. Requisitos Funcionais (Features)]

* **Análise Inteligente:** Ao iniciar, o app deve fazer uma análise (scan) e apresentar o espaço total que pode ser liberado, categorizado por tipo (Cache do Sistema, Lixo de Desenvolvimento, etc.).
* **Limpeza Seletiva:** O usuário deve poder selecionar/desselecionar categorias ou itens específicos para limpeza.
* **Visualização Detalhada:** Permitir que o usuário veja os arquivos que serão excluídos antes de confirmar a ação.
* **Módulo de Limpeza do Sistema:**
    * Cache de aplicativos (`~/.cache`).
    * Cache de pacotes (APT, DNF, Pacman, etc.).
    * Arquivos de log antigos.
    * Lixeira.
* **Módulo de Limpeza para Desenvolvedores:**
    * **Docker:** Remover imagens órfãs (`dangling=true`), contêineres parados, volumes não utilizados e caches de build.
    * **Kubernetes (local):** Limpar caches de clusters locais (ex: minikube, kind).
    * **Linguagens:** Limpar caches de dependências (ex: `~/.npm`, `~/.gradle`, `~/.m2`).
* **Configurações:**
    * Lista de exceções (arquivos ou diretórios a serem ignorados).
    * Agendamento de limpeza automática (opcional, para uma v2).

### [4. Design e UX (Estilo Apple)]

* **Minimalismo:** Interface super "clean", sem poluição visual.
* **Tipografia:** Usar uma fonte moderna e legível (ex: Inter, San Francisco).
* **Paleta de Cores:** Cores sóbrias, com um ponto de cor para ações primárias (ex: tons de cinza, branco e um azul ou verde vibrante para o botão "Limpar").
* **Animações Sutis:** Transições suaves e feedback visual para ações do usuário (ex: um spinner durante a análise, uma barra de progresso durante a limpeza).
* **Ícones:** Usar iconografia vetorial (SVG) de alta qualidade e consistente.

## Plano de Desenvolvimento Estruturado (Passo a Passo)

Por favor, gere o código para cada passo de forma sequencial. Eu irei solicitar o próximo passo quando o anterior estiver concluído.

**Passo 1: Estrutura do Projeto e Configuração Inicial**
Crie a estrutura de diretórios do projeto e o arquivo `main.py` inicial. A estrutura deve ser:
/quantum-cleaner
|-- /app
|   |-- /ui           # Camada de Apresentação
|   |-- /services     # Camada de Serviço
|   |-- /modules      # Camada de Acesso ao Sistema
|   |-- /assets       # Ícones, fontes, etc.
|   |-- init.py
|   |-- main.py       # Ponto de entrada da aplicação
|-- requirements.txt
|-- README.md

No `main.py`, crie a janela principal vazia usando PySide6, definindo um título e um tamanho inicial.

**Estou pronto. Por favor, comece com o Passo 1.**
2. Análise e Justificativa da Estratégia
Análise da Stack Tecnológica
Por que Python com Qt (PySide6)?

Produtividade e Ecossistema: Python é excelente para scripting e automação de tarefas de sistema, que é o cerne deste aplicativo. Possui bibliotecas nativas robustas (os, shutil, subprocess) para interagir com o sistema de arquivos.

GUI Poderosa: Qt é um framework de GUI C++ maduro, extremamente poderoso e verdadeiramente multiplataforma. O PySide6 é o binding oficial, mantido pela The Qt Company, o que garante excelente compatibilidade e performance.

Estilo Profissional: Com Qt Style Sheets (QSS), que funciona de forma similar ao CSS, é totalmente possível criar a interface "pixel-perfect" no estilo Apple que você deseja, algo que é mais difícil com frameworks como Tkinter ou mesmo GTK (que tende a seguir o design do ambiente GNOME).

Alternativas:

Node.js com Electron: Uma opção popular. A vantagem é usar tecnologias web (HTML, CSS, JS) para a UI. A desvantagem é o consumo de recursos. Um app de limpeza de sistema ser pesado (por embarcar um navegador Chromium inteiro) é um contra-senso. A interação com o sistema também é menos direta que em Python.

GTK: Seria mais "nativo" em ambientes como GNOME. No entanto, customizar o visual de forma tão específica (estilo Apple) pode ser mais complexo que com Qt/QSS. Qt oferece uma aparência mais consistente entre diferentes ambientes (GNOME, KDE, etc.).

Arquitetura e Princípios SOLID
O prompt força a IA a adotar uma arquitetura em camadas (Layered Architecture), que é a manifestação prática dos princípios SOLID:

Single Responsibility Principle (SRP): Cada módulo (DockerCleaner, SystemCacheCleaner) tem uma única e bem definida responsabilidade. A UI só cuida da exibição. O serviço só cuida da lógica.

Open/Closed Principle (OCP): A estrutura permite adicionar novas funcionalidades de limpeza (ex: "Limpador do Flatpak") simplesmente criando um novo módulo na camada modules e integrando-o ao CleaningService, sem precisar alterar os módulos existentes.

Dependency Inversion Principle (DIP): A camada de UI depende de abstrações da camada de serviço, não de implementações concretas. Isso torna o código desacoplado e muito mais fácil de testar.

Como Interagir com o Copilot Usando Este Prompt
Inicie a Conversa: Copie e cole todo o "Prompt Mestre" no chat do Copilot. A IA irá ler, entender o contexto completo e se preparar para o primeiro passo.

Siga os Passos: O prompt termina com "Por favor, comece com o Passo 1". O Copilot irá gerar o código para a estrutura inicial.

Desenvolvimento Incremental: Após receber o código do Passo 1, analise-o, crie os arquivos no seu VS Code e então diga: "Ótimo. Agora, por favor, execute o Passo 2: criar o layout básico da UI na janela principal, com uma área para categorias à esquerda e uma área de detalhes à direita."

Seja Específico: Continue seguindo o plano. Para cada passo, você pode ser ainda mais detalhado. Por exemplo, ao pedir um módulo de limpeza: "Para o módulo DockerCleaner, crie uma função find_orphan_images() que use o comando docker image ls --filter dangling=true de forma segura e retorne uma lista de dicionários com o ID e o tamanho de cada imagem."

Refatoração e Estilo: A qualquer momento, você pode pedir ao Copilot para refatorar ou melhorar o código. Exemplo: "Pode criar um arquivo QSS para estilizar o botão principal com uma cor de fundo azul, bordas arredondadas e uma fonte branca?"

Usar esta abordagem estruturada transforma o Copilot de um simples auto-completador de código em um verdadeiro parceiro de desenvolvimento, garantindo que o produto final seja bem arquitetado, manutenível e alinhado com a sua visão inicial.