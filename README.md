# Gerenciador de Downloads

Este programa é um gerenciador de downloads que utiliza `wget` para baixar arquivos de uma lista (`list.txt`). Ele possui uma interface gráfica desenvolvida em `Tkinter` e exibe um slide de imagens dinâmico, que pode conter um link clicável para um site configurável via `config.json`.

## Funcionalidades
- Interface gráfica intuitiva para gerenciamento de downloads.
- Uso do `wget` para downloads com suporte a retomada de arquivos interrompidos.
- Seleção de diretório de destino para os arquivos baixados.
- Exibição de um slide de imagens aleatórias da pasta `slide`.
- Possibilidade de clicar no slide para abrir um link configurável no navegador.
- Barra de progresso e status detalhado dos downloads.
- Execução em segundo plano para evitar travamentos na interface.
- Fechamento seguro encerrando processos pendentes.

## Configuração
O comportamento do programa pode ser ajustado através do arquivo `config.json`.

### Exemplo de `config.json`:
```json
{
  "title": "Meu Gerenciador de Downloads",
  "slide_url": "https://www.seusite.com"
}
```
- **title**: Define o título da janela do programa.
- **slide_url**: Define o link que será aberto ao clicar no slide.

## Como Usar
1. **Baixe e extraia os arquivos do programa** para uma pasta local.
2. **Certifique-se de que o `wget.exe` está na mesma pasta do script**.
3. **Crie um arquivo `list.txt`** contendo os links dos arquivos a serem baixados (um por linha).
4. **Crie uma pasta `slide` e adicione imagens** (`.jpg` ou `.png`) para o carrossel de imagens.
5. **Edite `config.json`** para personalizar o título e o link do slide.
6. **Execute `downloader.py`** e utilize a interface gráfica para gerenciar os downloads.

## Compilação para Executável
Se desejar transformar o script em um executável `.exe`, utilize o `pyinstaller`:
```sh
pyinstaller --onefile --noconsole --icon=icone.ico downloader.py
```
Isso gerará um executável portátil para uso sem necessidade do Python instalado.

## Dependências
- Python 3.x
- Bibliotecas necessárias:
  ```sh
  pip install pillow
  ```
- `wget.exe` deve estar na mesma pasta do script.

## Encerramento Seguro
Ao fechar o programa, ele executa `killer_app.exe` para garantir o encerramento dos processos de download ativos.

---
Este projeto foi desenvolvido para facilitar o gerenciamento de downloads em lote, fornecendo uma interface simples e funcional. 🚀
