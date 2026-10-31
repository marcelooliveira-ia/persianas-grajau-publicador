# Publicador automático — Persianas Grajaú

Publica no Instagram e no Facebook, no horário de `agenda.json`, pela API oficial da Meta.

## O que fazer uma única vez
1. **GitHub**: criar o repositório (ex.: `persianas-grajau-publicador`), subir esta pasta inteira e ativar **GitHub Pages** (branch main, raiz). Para o Instagram ler as mídias, o repositório precisa ser público ou a pasta `midia/` precisa estar em Pages.
2. **Meta** (developers.facebook.com): criar um app, adicionar "Instagram Graph API", dar as permissões `pages_manage_posts`, `pages_read_engagement`, `instagram_basic`, `instagram_content_publish`, gerar um token de Página de longa duração. A conta do Instagram precisa ser profissional e ligada à página.
3. **GitHub → Settings → Secrets and variables → Actions**:
   - Secrets: `META_TOKEN`, `FB_PAGE_ID`, `IG_USER_ID` (cole você mesmo; nunca no chat).
   - Variable: `BASE_URL` = endereço do Pages (ex.: `https://SEUUSUARIO.github.io/persianas-grajau-publicador`).
4. Aba **Actions → publicar → Run workflow** para testar. Antes de ligar de verdade, rode localmente com `DRY_RUN=1` para ver o que seria enviado.

## Rotina semanal
Claude gera `agenda.json` + pasta `midia/` da semana, você aprova e faz o commit. A cada 10 min o agendador publica o que estiver no horário (tolerância de 6 h; atrasos maiores são pulados).

## Limitações
- Stories: saem no Instagram, **sem o sticker de link do WhatsApp** (a API não permite). Stories no Facebook não são publicados por este script.
- O token expira (~60 dias); renovar.
- Se a Meta exigir revisão do app para publicar na conta, isso pode levar dias.
- O GitHub pode atrasar agendamentos de alguns minutos.
