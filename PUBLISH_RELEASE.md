# 📋 Checklist para Publicar Release v1.0.0 no GitHub

## ✅ Preparação (Já feito!)

- [x] Atualizar versão no `pyproject.toml` para 1.0.0
- [x] Construir AppImage limpo
- [x] Renomear AppImage com versão: `EchoCleaner-1.0.0-x86_64.AppImage`
- [x] Criar notas de release

## 🚀 Passos para Publicar no GitHub

### 1. Commit e Push das Mudanças

```bash
# Adicionar arquivos modificados
git add pyproject.toml README.md QUICKSTART.md

# Commit
git commit -m "chore: bump version to 1.0.0"

# Push para main
git push origin main
```

### 2. Criar Tag Git

```bash
# Criar tag anotada
git tag -a v1.0.0 -m "Release v1.0.0 - First Stable Release"

# Push da tag
git push origin v1.0.0
```

### 3. Criar Release no GitHub (Via Interface Web)

1. **Acesse**: https://github.com/paladini/echo-cleaner/releases/new

2. **Preencha os campos**:
   - **Tag**: `v1.0.0` (use a tag que você criou)
   - **Release title**: `Echo Clear v1.0.0 - First Stable Release 🎉`
   - **Description**: Copie o conteúdo de `RELEASE_NOTES_v1.0.0.md`

3. **Fazer Upload dos Arquivos**:
   - Arraste `EchoCleaner-1.0.0-x86_64.AppImage` para a área de "Attach binaries"

4. **Opções**:
   - ✅ Marque "Set as the latest release"
   - ⬜ NÃO marque "This is a pre-release"

5. **Publicar**:
   - Clique em "Publish release"

### 4. Criar Release via GitHub CLI (Alternativa)

Se você tiver o `gh` CLI instalado:

```bash
# Criar release e fazer upload do AppImage
gh release create v1.0.0 \
  EchoCleaner-1.0.0-x86_64.AppImage \
  --title "Echo Clear v1.0.0 - First Stable Release 🎉" \
  --notes-file RELEASE_NOTES_v1.0.0.md
```

## 📝 Após Publicar

- [ ] Verificar que a release aparece em: https://github.com/paladini/echo-cleaner/releases
- [ ] Testar download do AppImage da release
- [ ] Compartilhar nas redes sociais / Reddit / fóruns Linux
- [ ] Considerar submeter ao AppImageHub: https://appimage.github.io/

## 🎯 Comandos Resumidos

```bash
# 1. Commit e push
git add .
git commit -m "chore: bump version to 1.0.0"
git push origin main

# 2. Criar e push tag
git tag -a v1.0.0 -m "Release v1.0.0 - First Stable Release"
git push origin v1.0.0

# 3. Criar release (via CLI)
gh release create v1.0.0 \
  EchoCleaner-1.0.0-x86_64.AppImage \
  --title "Echo Clear v1.0.0 - First Stable Release 🎉" \
  --notes-file RELEASE_NOTES_v1.0.0.md
```

## 📚 Recursos Úteis

- [GitHub Releases Docs](https://docs.github.com/en/repositories/releasing-projects-on-github/managing-releases-in-a-repository)
- [GitHub CLI Docs](https://cli.github.com/manual/gh_release_create)
- [AppImageHub](https://appimage.github.io/)

---

**Arquivo AppImage pronto**: `EchoCleaner-1.0.0-x86_64.AppImage` (218KB)
**Notas de Release**: `RELEASE_NOTES_v1.0.0.md`
