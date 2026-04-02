# Agent Pull Request Creator

Agente especializado na criação de pull requests profissionais e bem documentados, seguindo as melhores práticas de colaboração em equipes de desenvolvimento.

## Uso

Este prompt é utilizado para gerar automaticamente descrições detalhadas e estruturadas de pull requests, garantindo consistência e qualidade na documentação de mudanças de código.

## Variáveis de Entrada

- `changes_summary` (obrigatório): Resumo das mudanças implementadas
- `files_changed` (opcional): Lista dos arquivos modificados
- `issue_number` (opcional): Número da issue relacionada
- `branch_name` (opcional): Nome da branch do PR
- `breaking_changes` (opcional): Indica se há breaking changes (Sim/Não)
- `testing_done` (opcional): Descrição dos testes realizados

## Onde é Utilizado

- Automação de criação de PRs via CLI
- Integração com GitHub/GitLab APIs
- Templates para desenvolvedores
- Workflows de CI/CD
- Ferramentas internas de desenvolvimento

## Formato de Saída

O agente gera um PR completo com:
- Título seguindo convenções (feat:, fix:, refactor:, docs:)
- Descrição estruturada com seções claras
- Checklist de revisão
- Links para issues relacionadas
- Instruções de teste
- Alertas para breaking changes

## Changelog

### v1.0.0 (2026-10-18)
- Implementação inicial do agente
- Suporte para diferentes tipos de PR (feature, bugfix, refactor, docs)
- Template completo com todas as seções essenciais
- Casos de teste para validação
- Suporte a breaking changes e links de issues