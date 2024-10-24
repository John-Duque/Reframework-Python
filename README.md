# 🐍 **ReFramework em Python**

![Python](https://img.shields.io/badge/Python-3.8%2B-blue?style=for-the-badge&logo=python)
![License](https://img.shields.io/badge/License-MIT-green?style=for-the-badge)

Um **Robust Framework (ReFramework)** para automação de processos inspirado no UiPath, desenvolvido em Python. Estruturado com **ciclo de transações**, **logging avançado**, **automação com Selenium**, e fácil de personalizar e manter.

---

## 📋 **Índice**

- [Funcionalidades](#-funcionalidades)
- [Estrutura do Projeto](#-estrutura-do-projeto)
- [Instalação e Execução](#-instalação-e-execução)
- [Funcionamento](#-funcionamento)
- [Componentes Principais](#-componentes-principais)
- [Exemplo de Uso](#-exemplo-de-uso)
- [Tratamento de Exceções](#-tratamento-de-exceções)
- [Testes e Cobertura](#-testes-e-cobertura)
- [Roadmap](#-roadmap)
- [Licença](#-licença)
- [Contato](#-contato)
- [Contribuição](#-contribuição)

---

## 🎯 **Funcionalidades**

- **Controle Transacional**: Estrutura organizada para automação por transações.
- **Automação com Selenium**: Automação de interações em páginas web.
- **Tratamento de Exceções**: Tratamento de erros de negócio e técnicos.
- **Logging Centralizado**: Logs detalhados para auditoria.
- **Fácil de Expandir**: Modularidade para novos componentes e serviços.
- **Compatível com Todos os Sistemas**: Suporte para Windows, macOS e Linux.

---

## 📂 **Estrutura do Projeto**

```plaintext
reframework_python/
│
├── Components/                # Componentes específicos de automação
│   └── google_page.py          # Automação no Google
│
├── Data/                      # Arquivos de configuração e dados
│   └── config.json             # Configurações do framework
│
├── Framework/                 # Módulos principais
│   ├── BasePage.py             # Classe base para páginas web
│   ├── GetTransaction.py       # Gerenciamento de transações
│   ├── EndProcess.py           # Finalização do processo
│   ├── ProcessTransaction.py   # Lógica das transações
│   ├── Selenium.py             # Configuração do Selenium WebDriver
│   ├── Exceptions.py           # Exceções personalizadas
│   └── Init.py                 # Inicialização e configuração
│
├── Logs/                      # Logs de execução
│   └── process.log             # Registro de eventos
├── Main.py                    # Ponto de entrada principal
├── requirements.txt           # Dependências do projeto
└── README.md                  # Documentação
```

## 🚀 **Instalação e Execução**

### 1. Pré-requisitos
- Python 3.8+
- pip (gerenciador de pacotes)

### 2. Clonar o Repositório

```bash
    git clone https://github.com/seuusuario/reframework_python.git
    cd reframework_python
```        

### 3. Configurar config.json

```json
  {
    "log_file": "Logs/process.log",
    "retry_count": 3,
    "transaction_timeout": 10
  }
```    

### 4. Executar o Projeto

```bash
    python Main.py
```    

## 🔄 **Funcionamento**

1.	**Init:** Inicializa logs e configurações.
2.  **GetTransactionData:** Obtém a próxima transação.
3.	**ProcessTransaction:** Processa a transação.
4.  **HandleErrors:** Lida com exceções e falhas.
5.	**EndProcess:** Finaliza o processo.

## 🛠 **Componentes Principais**

### BasePage.py

- Classe base para automação de páginas web.

```python
    import logging
    from typing import Optional
    from selenium.webdriver.remote.webdriver import WebDriver
    from selenium.webdriver.remote.webelement import WebElement
    from selenium.webdriver.support.ui import WebDriverWait
    from selenium.webdriver.support import expected_conditions as ec
    from selenium.common.exceptions import TimeoutException, NoSuchElementException, ElementNotInteractableException
```

```python
    class BasePage:
        driver: WebDriver  # Variável de instância com type hint
        timeout: int  # Variável de instância com type hint
        logger: logging.Logger  # Variável de instância com type hint
```

```python
    def __init__(self, driver: WebDriver, logger: logging.Logger, timeout: int = 10) -> None:
        # Inicializa a página base com o driver e o tempo de espera padrão.
        self.driver = driver
        self.timeout = timeout
        self.logger = logger
```

#### Espera explícita genérica que aguarda até que a condição fornecida seja atendida.

```python
    def wait_until(self, condition, by: str, value: str, timeout: Optional[int] = None) -> Optional[WebElement]:
        try:
            return WebDriverWait(self.driver, timeout or self.timeout).until(
                condition((by, value))
            )
        except TimeoutException:
            self.logger.warning(f"Timeout: O elemento com {by}='{value}' não foi encontrado.")
            return None
        except NoSuchElementException:
            self.logger.error(f"Erro: O elemento com {by}='{value}' não foi encontrado no DOM.")
            return None   
```

#### Localiza um elemento na página com espera explícita.

```python
    def find_element(self, by: str, value: str, timeout: Optional[int] = None) -> Optional[WebElement]:
        return self.wait_until(ec.presence_of_element_located, by, value, timeout)
```

#### Aguarda até que o elemento esteja visível.

```python
    def wait_for_visibility(self, by: str, value: str, timeout: Optional[int] = None) -> Optional[WebElement]:
        return self.wait_until(ec.visibility_of_element_located, by, value, timeout)
``` 

#### Localiza um elemento e clica nele.

```python
    def click(self, by: str, value: str) -> None:
        try:
            element = self.find_element(by, value)
            if element:
                element.click()
                self.logger.info(f"Elemento com {by}='{value}' clicado com sucesso.")
            else:
                self.logger.warning(f"Elemento com {by}='{value}' não encontrado para clicar.")
        except ElementNotInteractableException:
            self.logger.error(f"Elemento com {by}='{value}' não está interagível.")
```

#### Localiza um campo de texto, limpa-o e insere o texto fornecido.

```python
    def enter_text(self, by: str, value: str, text: str) -> None:
        try:
            element = self.find_element(by, value)
            if element:
                element.clear()
                element.send_keys(text)
                self.logger.info(f"Texto inserido com sucesso no elemento {by}='{value}'.")
            else:
                self.logger.warning(f"Elemento com {by}='{value}' não encontrado para inserir texto.")
        except ElementNotInteractableException:
            self.logger.error(f"Não foi possível interagir com o elemento {by}='{value}' para inserir texto.")
```

### GetTransaction.py

- Gerencia transações e iteração sobre dados.

### ProcessTransaction.py

- implementa a lógica de negócios para cada transação.

## 🎯 **Roadmap**

- Adicionar integração com bancos de dados.
- Exemplos adicionais de automação.
- Melhorar cobertura de testes.

## 📄 **Licença**

- Este projeto é licenciado sob a [https://opensource.org/licenses/MIT](https://opensource.org/licenses/MIT).

## 📚 **Referências**

- [Documentação Oficial do Python](https://docs.python.org/3/)
- [Documentação do Selenium](https://docs.python.org/3/)
- [Guia de Estilo PEP8](https://docs.python.org/3/)
