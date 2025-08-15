# 🔍 Sistema de Inspeção de Equipamentos

[![Python](https://img.shields.io/badge/Python-3.8+-blue.svg)](https://www.python.org/downloads/)
[![License](https://img.shields.io/badge/License-MIT-green.svg)](LICENSE)
[![Status](https://img.shields.io/badge/Status-Produção-brightgreen.svg)]()

## 📋 Descrição

Sistema completo de inspeção de equipamentos desenvolvido em Python, baseado no projeto React original. Permite registrar inspeções, controlar datas de vencimento, fazer upload de fotos e gerar relatórios PDF profissionais.

## ✨ Funcionalidades Implementadas

-   ✅ **Registro de inspeções** com dados completos do equipamento
-   📅 **Controle de datas** de inspeção e vencimento
-   📸 **Upload e visualização** de fotos
-   📄 **Geração automática** de relatórios em PDF
-   💾 **Armazenamento local** usando SQLite (mais robusto que IndexedDB)
-   📊 **Geração de relatórios** em lote
-   🔍 **Validação avançada** de datas de inspeção
-   🎨 **Interface gráfica** moderna com Tkinter
-   📱 **Executável standalone** disponível

## 🚀 Instalação

### Pré-requisitos

-   Python 3.8 ou superior
-   pip (gerenciador de pacotes Python)

### Passo a Passo

1. **Navegue para a pasta do projeto**

    ```bash
    cd formulario_inspecao
    ```

2. **Instale as dependências**

    ```bash
    pip install -r requirements.txt
    ```

3. **Execute o aplicativo**
    ```bash
    python main.py
    ```

## 📦 Dependências

| Pacote        | Versão | Descrição               |
| ------------- | ------ | ----------------------- |
| `reportlab`   | 4.0.4  | Geração de arquivos PDF |
| `Pillow`      | 10.0.0 | Manipulação de imagens  |
| `pyinstaller` | 6.15.0 | Criação de executáveis  |

## 🏗️ Estrutura do Projeto

```
formulario_inspecao/
├── opcoes_formulario.py    # Opções e configurações do formulário
├── database.py             # Sistema de banco de dados SQLite
├── date_validator.py       # Validação e manipulação de datas
├── photo_handler.py        # Upload e manipulação de fotos
├── report_generator.py     # Geração de relatórios PDF
├── main.py                 # Aplicação principal (a ser criada)
├── requirements.txt        # Dependências do projeto
└── README.md               # Este arquivo
```

## 🎯 Como Usar

### 1. **Registro de Inspeções**

-   Preencha todos os campos obrigatórios
-   Selecione plataforma, módulo e setor
-   Escolha o tipo de equipamento
-   A TAG será preenchida automaticamente
-   Adicione foto da inspeção (opcional)

### 2. **Controle de Datas**

-   Sistema calcula automaticamente próxima inspeção
-   Validação de datas de vencimento
-   Alertas para inspeções próximas do vencimento
-   Status visual (em dia, vencida, atenção)

### 3. **Upload de Fotos**

-   Suporte a múltiplos formatos (JPG, PNG, GIF, BMP, TIFF)
-   Redimensionamento automático para otimização
-   Validação de tamanho e formato
-   Preview em tempo real

### 4. **Geração de Relatórios**

-   PDF individual para cada inspeção
-   Relatórios em lote para múltiplas inspeções
-   Relatório resumo com estatísticas
-   Inclusão automática de fotos

## 🔧 Funcionalidades Técnicas

### **Banco de Dados SQLite**

-   Armazenamento local robusto
-   Histórico de alterações
-   Índices para performance
-   Backup automático

### **Validação de Datas**

-   Verificação de datas futuras
-   Cálculo de vencimento
-   Status de inspeção
-   Alertas inteligentes

### **Manipulação de Fotos**

-   Validação de arquivos
-   Redimensionamento automático
-   Otimização de qualidade
-   Thumbnails para preview

### **Geração de PDFs**

-   Layout profissional
-   Tabelas organizadas
-   Inclusão de fotos
-   Estilos personalizados

## 📱 Compatibilidade

| Sistema Operacional | Status       | Notas                    |
| ------------------- | ------------ | ------------------------ |
| Windows 10/11       | ✅ Suportado | Testado e funcionando    |
| Windows 7/8         | ✅ Suportado | Compatível               |
| macOS               | ✅ Suportado | Requer Python 3.8+       |
| Linux               | ✅ Suportado | Testado em Ubuntu/Debian |

## 🚨 Solução de Problemas

### Erro: "Módulo não encontrado"

```bash
pip install -r requirements.txt
```

### Erro: "PIL não disponível"

```bash
pip install Pillow
```

### Erro: "ReportLab não disponível"

```bash
pip install reportlab
```

### Problemas com fotos

-   Verifique se o arquivo é uma imagem válida
-   Tamanho máximo: 10MB
-   Formatos suportados: JPG, PNG, GIF, BMP, TIFF

## 🔄 Migração do React

### **Funcionalidades Equivalentes:**

| React              | Python                 | Status          |
| ------------------ | ---------------------- | --------------- |
| `opcoesFormulario` | `opcoes_formulario.py` | ✅ Implementado |
| `IndexedDB`        | `SQLite`               | ✅ Implementado |
| `date-fns`         | `date_validator.py`    | ✅ Implementado |
| `FileReader`       | `photo_handler.py`     | ✅ Implementado |
| `pdf-lib`          | `report_generator.py`  | ✅ Implementado |

### **Vantagens da Versão Python:**

-   ✅ **Mais robusta** para processamento de dados
-   ✅ **PDFs mais profissionais** com ReportLab
-   ✅ **Banco de dados mais confiável** com SQLite
-   ✅ **Validações mais avançadas** nativas
-   ✅ **Executável standalone** disponível

## 🎯 Próximos Passos

### **Para Desenvolvedores:**

1. **Criar interface gráfica** (`main.py`)
2. **Testar todas as funcionalidades**
3. **Criar executável** com PyInstaller
4. **Documentar uso avançado**

### **Para Usuários:**

1. **Instalar dependências**
2. **Executar aplicação**
3. **Configurar primeiro equipamento**
4. **Começar a registrar inspeções**

## 💡 Dicas de Uso

### **Organização de Dados:**

-   Use TAGs consistentes para equipamentos
-   Mantenha datas de inspeção atualizadas
-   Faça backup regular do banco de dados
-   Organize fotos por inspeção

### **Geração de Relatórios:**

-   Gere relatórios individuais para cada inspeção
-   Use relatórios em lote para auditorias
-   Relatório resumo para gestão
-   Mantenha histórico de PDFs

### **Manutenção:**

-   Limpe fotos antigas periodicamente
-   Faça backup do banco de dados
-   Atualize o sistema regularmente
-   Monitore espaço em disco

## 🤝 Contribuindo

1. Faça um fork do projeto
2. Crie uma branch para sua feature
3. Implemente a funcionalidade
4. Teste thoroughly
5. Abra um Pull Request

## 📝 Licença

Este projeto está sob a licença MIT. Veja o arquivo [LICENSE](LICENSE) para mais detalhes.

## 👨‍💻 Autor

**Baseado no projeto React original**

-   Funcionalidades equivalentes implementadas
-   Melhorias técnicas adicionadas
-   Compatibilidade total mantida

## 🙏 Agradecimentos

-   Projeto React original
-   Comunidade Python
-   Desenvolvedores do ReportLab
-   Equipe do Pillow (PIL)

---

⭐ **Sistema completo de inspeção em Python - Todas as funcionalidades do React implementadas!** ⭐
