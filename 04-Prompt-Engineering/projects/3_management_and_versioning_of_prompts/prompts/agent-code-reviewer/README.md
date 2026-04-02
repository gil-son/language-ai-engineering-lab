# Agent Code Reviewer

Agente especializado em revisão rigorosa de código com foco em segurança, performance e boas práticas de desenvolvimento.

## Uso

Este prompt é utilizado para análise automatizada de código em pull requests e revisões de código, fornecendo feedback detalhado sobre múltiplos aspectos do código.

## Variáveis de Entrada

- `code_diff` (obrigatório): Diff do código a ser revisado
- `language` (opcional): Linguagem de programação do código
- `repo_rules` (opcional): Regras específicas do repositório
- `security_level` (opcional): Nível de rigor na análise de segurança (standard/high)
- `review_focus` (opcional): Foco específico da revisão (geral/segurança/performance)

## Onde é Utilizado

- Pipeline de CI/CD para revisão automática de PRs
- Integração com GitHub Actions
- Ferramenta de linha de comando para desenvolvedores
- Sistema de code review interno

## Changelog

### v1.0.0 (2026-10-18)
- Implementação inicial do agente
- Suporte para análise de segurança, performance e qualidade
- Casos de teste básicos implementados
- Formato estruturado de resposta definido