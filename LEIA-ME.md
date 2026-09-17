# Manual do Núcleo de Isenção — publicação no Streamlit

App interno que serve o manual com senha. Quem tiver o link e a senha abre no
navegador, no computador ou no celular, sempre na versão mais recente.

## Arquivos

| Arquivo | Para que serve |
|---|---|
| `streamlit_app.py` | O app: tela de senha e exibição do manual. |
| `manual.html` | O manual em si. É o único arquivo que você troca quando quiser atualizar. |
| `requirements.txt` | Dependência do app. |
| `.streamlit/secrets.toml.exemplo` | Modelo do arquivo de senha. |
| `.gitignore` | Impede que a senha real vá para o GitHub. |

## Publicar pela primeira vez

1. **Crie um repositório privado no GitHub.** Privado, não público. O manual tem
   links de pastas e planilhas com dado de cliente e prints com nome de pessoa:
   em repositório público isso fica aberto a qualquer um.
2. Suba os quatro arquivos e a pasta `.streamlit` (só o `secrets.toml.exemplo`,
   nunca o `secrets.toml` preenchido).
3. Entre em `share.streamlit.io`, clique em **New app** e aponte para o
   repositório, o branch e o arquivo `streamlit_app.py`.
4. Antes de clicar em Deploy, abra **Advanced settings > Secrets** e cole:

   ```toml
   SENHA = "a-senha-que-a-equipe-vai-usar"
   ```

   Se preferir, dá para fazer depois em **Manage app > Settings > Secrets**.
5. Deploy. Em um ou dois minutos o app sobe e gera o link para distribuir.

## Atualizar o manual depois

1. Gere o novo `manual.html`.
2. No GitHub, abra o arquivo `manual.html`, clique no lápis ou em **Upload files**,
   substitua e faça o commit.
3. O Streamlit detecta o commit e reconstrói sozinho em poucos minutos. Ninguém
   precisa reinstalar nada: quem abrir o link já vê a versão nova.
4. Se a versão antiga insistir em aparecer, use **Manage app > Reboot**. O reboot
   limpa o cache do app.

Regra prática: só o `manual.html` muda no dia a dia. O `streamlit_app.py` só é
mexido se você quiser alterar a senha, a altura do quadro ou o texto da tela de
entrada.

## Trocar a senha

**Manage app > Settings > Secrets**, altere a linha `SENHA` e salve. O app
reinicia sozinho. Avise a equipe, porque quem estiver com a sessão aberta segue
dentro até fechar a aba.

## O que ajustar no `streamlit_app.py`

- `ALTURA`: altura do quadro do manual, em pixels. Se sobrar espaço em branco
  embaixo, diminua; se o manual ficar apertado, aumente.
- `MAX_TENTATIVAS`: quantas senhas erradas antes de travar a sessão.

## Limites que vale conhecer

- **A senha protege o acesso, não o conteúdo.** Quem entra consegue salvar a
  página e repassar. Serve para evitar circulação acidental, não vazamento
  deliberado.
- **Streamlit Community Cloud é gratuito e o link é público.** Qualquer pessoa
  com a URL chega na tela de senha. Por isso a senha precisa ser razoável e não
  pode ser divulgada em grupo aberto.
- **App gratuito hiberna sem uso.** O primeiro acesso do dia pode levar alguns
  segundos a mais para carregar.
- **Prints com dado pessoal.** O manual traz telas com nome completo e telefone
  de cliente. Antes de publicar, vale tarjar essas informações: uma coisa é um
  arquivo que circula por e-mail interno, outra é um endereço na internet
  protegido só por senha compartilhada.
